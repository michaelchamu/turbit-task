#service runs on every application startup
#after connection to database is established, service checks if time-series collection is present
#and if it is not empty
#if it is empty, it checks the CSV directory for CSV files
#if CSV files are present, it reads them and populates the time-series collection
#it only takes data from the Dat/Zeit, Wind, and Leistung columns
#it also uses the filename as the turbine_id

import os
import csv
from typing import List, Dict
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pathlib import Path
from ..models.timeseries import TimeSeriesModel, TurbineMetadata

csv_data_path = Path(__file__).resolve().parents[3].joinpath("data/csv/")

collection_name = "time-series-data"

#iterate through a selected CSV file and create a TimeSeriesModel document for each row
def parse_csv_row(row: Dict[str, str], turbine_id: str) -> Dict:
    #here, the timestamp is in the format 'dd.mm.yyyy, HH:MM' without seconds, so
    #we need to parse it correctly inclucing the comma
    timestamp = datetime.strptime(row['Dat/Zeit'].strip(), '%d.%m.%Y, %H:%M')
    #to handle the case where Leistung or Wind might be empty and also 
    #to convert the comma to a dot for float conversion for consistent values
    #clean up the row data
    power = float(row['Leistung'].replace(',', '.')) if row['Leistung'] else 0.0
    wind_speed = float(row['Wind'].replace(',', '.')) if row['Wind'] else None
    azimuth = float(row['Azimut'].replace(',', '.')) if row['Azimut'] else 0.0
    external_temperature = float(row['Außen'].replace(',', '.')) if row['Außen'] else 0.0
    internal_temperature = float(row['Lager'].replace(',', '.')) if row['Lager'] else 0.0
    rpm = float(row['Rotor'].replace(',', '.')) if row['Rotor'] else 0.0
    #csv files do not have longitude and latitude, so this is handled here
    #this is a scalability adjustment to allow it to work with a CSV file that has location data

    latitude = row.get('Latitude')
    longitude = row.get('Longitude')
    altitude = row.get('Altitude')

    return TimeSeriesModel(
        timestamp=timestamp,
        power=power,
        wind_speed=wind_speed,
        metadata=TurbineMetadata(
            turbine_id=turbine_id,
            latitude=float(latitude.replace(',', '.')) if latitude else None,
            longitude=float(longitude.replace(',', '.')) if longitude else None,
            altitude=float(altitude.replace(',', '.')) if longitude else None,
            azimuth=azimuth,
            external_temperature=external_temperature,
            internal_temperature=internal_temperature,
            rpm=rpm
        )
        ).model_dump()  

#method to create the time-series collection if it does not exist
async def create_time_series_collection(db: AsyncIOMotorClient):
    try:
        existing_collections = await db.list_collection_names()

        if collection_name not in existing_collections:
            #create the time-series collection with the specified options
            await db.create_collection(
                collection_name,
                timeseries={
                    'timeField': 'timestamp',
                    'metaField': 'metadata',
                    'granularity': 'minutes'
                }
            )
            print(f"Time-series collection '{collection_name}' created successfully.")
        else:
            print(f"Time-series collection '{collection_name}' already exists.")
    except Exception as e:
        print(f"An error occurred while creating the time-series collection: {e}")
        raise e
    

#actual service to read CSVs then call parse_csv_row for each row and insert into MongoDB
async def populate_time_series(db: AsyncIOMotorClient):
    try:
        #ensure that the timeseries colection exists by calling the createtimeseries_collection method
        await create_time_series_collection(db)

        #now check if the timeseries collection exists is empty
        document_count = await db[collection_name].count_documents({})

        if document_count == 0:
            print(f"Collection {collection_name} is empty. Populating it from CSV files.")
            #check if the CSV data directory exists
            if not os.path.exists(csv_data_path):
                raise FileNotFoundError(f"CSV directory {csv_data_path} does not exist.")
            
            #now check if there are any CSV files in the directory
            csv_files = [f for f in os.listdir(csv_data_path) if f.endswith('.csv')]
            if not csv_files:
                raise FileNotFoundError("No CSV files found in the directory.")
            
            #since csv_files is not empty, iterate through each file
            for csv_file in csv_files:
                file_path = os.path.join(csv_data_path, csv_file)
                turbine_id = Path(csv_file).stem  # extract filename and remove extension to use as turbine_id
                print(f"Processing file: {csv_file} with turbine_id: {turbine_id}")

                #Files have more than 10k lines, so to be safe with memory issues, perfomance
                #and mongo batch insert, read the data in chunks
                batch: List[Dict] = []
                with open(file_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter=';')

                    #fieldnames in 1st row contain spaces, so we need to strip them
                    reader.fieldnames = [field.strip() for field in reader.fieldnames]
                    #2nd data row is also part of header so skip it
                    next(reader)

                    for row in reader:
                        try:
                            document = parse_csv_row(row, turbine_id)
                            batch.append(document)

                            #once batch reaches 1000 documents, insert into MongoDB and clear it
                            if len(batch) >= 1000:
                                await db[collection_name].insert_many(batch)
                                #print(f"Inserted {len(batch)} documents into {collection_name}.")
                                batch.clear()
                        except Exception as e:
                            print(f"Skipping row due to error: {e}")
                            continue
                    #we are chuncking in multiples of 1000
                    #some documents may remain, so insert them here
                    if batch:
                        await db[collection_name].insert_many(batch)
                        print(f"Inserted remaining {len(batch)} documents into {collection_name}.")

                print(f"Populated {collection_name} collection with data from {len(csv_files)} CSV files.")
            else:
                print(f"{collection_name} collection already exists and is not empty. No action taken.")
    except Exception as e:
        print(f"An error occurred while populating the time-series data: {e}")