// Create first database (db1) with a collection
db = db.getSiblingDB('users-demo')
db.createCollection('users_data')

// Create second database (db2) with a collection
db = db.getSiblingDB('time-series-demo')
db.createCollection('time_series_data')

print("Initialized databases: users_data and times_series_data")