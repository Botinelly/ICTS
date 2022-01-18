from fastapi import FastAPI
from .models.database import Database
from .models.databaselogs import DatabaseLogs

app = FastAPI()

print("STARTING APPLICATION")
Database.initialize(
    host="test-db",
    port=27017
)

Database.connect_to_db()
Database.set_db('operation')
Database.populate_database()

DatabaseLogs.initialize(
    host="test-logs-db",
    port=27020
)
DatabaseLogs.connect_to_db()
DatabaseLogs.set_db('logs')
DatabaseLogs.populate_database()

print("APPLICATION STARTED")