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
from models.timeseries import TimeSeriesModel
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv() 

collection_name = "time-series-data"
data_directory = os.getenv("CSV_DIRECTORY")

#iterate through a selected CSV file and create a TimeSeriesModel document for each row
def parse_csv_row(row: Dict[str, str], turbine_id: str) -> Dict:
    timestamp = datetime.strptime(row['Dat/Zeit'], '%Y-%m-%d %H:%M:%S')
    #to handle the case where Leistung or Wind might be empty and also 
    #to convert the comma to a dot for float conversion for consistent values
    #clean up the row data
    power = float(row['Leistung'].replace(',', '.')) if row['Leistung'] else 0.0
    wind_speed = float(row['Wind'].replace(',', '.')) if row['Wind'] else None

    return TimeSeriesModel(
        timestamp=timestamp,
        power=power,
        wind_speed=wind_speed,
        turbine_id=turbine_id
        ).model_dump()  

#actual service to read CSVs then call parse_csv_row for each row and insert into MongoDB
async def populate_time_series(db: AsyncIOMotorClient):
    try:
        #retrieve collections from named database
        existing_collections = await db.list_collection_names()

        #check if the time-series collection exists and is not empty
        if collection_name not in existing_collections or await db[collection_name].count_documents({}) == 0:
            print(f"Collection {collection_name} does not exist or is empty. Populating it from CSV files.")
            #check if the CSV directory exists
            if not os.path.exists(data_directory):
                raise FileNotFoundError(f"CSV directory {data_directory} does not exist.")
            
            #now check if there are any CSV files in the directory
            csv_files = [f for f in os.listdir(data_directory) if f.endswith('.csv')]
            if not csv_files:
                raise FileNotFoundError("No CSV files found in the directory.")
            
            #since csv_files is not empty, iterate through each file
            for csv_file in csv_files:
                file_path = os.path.join(data_directory, csv_file)
                turbine_id = Path(csv_file).stem  # extract filename and remove extension to use as turbine_id
                print(f"Processing file: {csv_file} with turbine_id: {turbine_id}")

            #Files have more than 10k lines, so to be safe with memory issues, perfomance
            #and mongo batch insert, read the data in chunks
            batch: List[Dict] = []
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=';')
                for row in reader:
                    try:
                        document = parse_csv_row(row, turbine_id)
                        batch.append(document)

                        #once batch reaches 1000 documents, insert into MongoDB and clear it
                        if len(batch) >= 1000:
                            await db[collection_name].insert_many(batch)
                            print(f"Inserted {len(batch)} documents into {collection_name}.")
                            batch.clear()
                    except Exception as e:
                        print(f"Error processing row {row}: {e}")
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