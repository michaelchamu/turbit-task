// Create users data database for 1st task with no collection
db = db.getSiblingDB('users-data')

// Create time series database for 2nd task with no collection
db = db.getSiblingDB('time-series-data')

print("Initialized databases: users_data and times_series_data")