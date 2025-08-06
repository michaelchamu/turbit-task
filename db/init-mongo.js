//create user_data table and indexes for collations
db = db.getSiblingDB('users_data');

// Create text indexes for partial text searches with case-insensitive collation
db.createCollection('users');
//this will make it easier to search partially by username
db.users.createIndex({ "username": "text" });

db.createCollection('posts');
//these are set to false because there are identical values in some documents from the api
db.createCollection('comments');

//create time_series_data following the timeseries schema
db = db.getSiblingDB('time_series_data');

db.createCollection("turbine_readings", {
    timeseries: {
        timeField: "timestamp",
        metaField: "metadata",
        granularity: "minutes"
    }
});