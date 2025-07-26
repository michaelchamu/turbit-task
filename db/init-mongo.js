// Create first database (db1) with a collection
db = db.getSiblingDB('users-data')

// Create second database (db2) with a collection
db = db.getSiblingDB('time-series-data')

print("Initialized databases: users_data and times_series_data")