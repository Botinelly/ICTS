from typing import List
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import json
from bson import ObjectId
import re


class DatabaseLogs:
    '''Basic DatabaseLogs methods '''
    host: str = ""
    port: int = 0
    dbconn: MongoClient = None
    database: None = None


    @staticmethod
    def initialize(
            host: str = 'thanos-station-backend-db',
            port: int = 27017):

        DatabaseLogs.host = host
        DatabaseLogs.port = port
        DatabaseLogs.dbconn = None            

    @staticmethod
    def connect_to_db():
        try:
            print("IN CONNECT", DatabaseLogs.host, DatabaseLogs.port)
            DatabaseLogs.dbconn = MongoClient(
                host=DatabaseLogs.host + ":27017",
                port=DatabaseLogs.port,
                serverSelectionTimeoutMS=3000
            )
            test_result = DatabaseLogs.check_connection()
            return test_result
        except Exception as err:
            print("connect to db error ", err)
            return False

    @staticmethod
    def check_connection():
        try:
            DatabaseLogs.dbconn.admin.command('ismaster')
        except ConnectionFailure as err:
            print("check connection error ",err)
            return False
        return True

    @staticmethod
    def disconnect_from_db():
        try:
            DatabaseLogs.dbconn.close()
        except Exception:
            return False
        return True

    @staticmethod
    def set_db(database):
        try:
            DatabaseLogs.database = DatabaseLogs.dbconn[database]
        except Exception as err:
            print("Set DB error", err)
            return False
        return True

    @staticmethod
    def create_log(log):
        database = DatabaseLogs.get_db()
        if(DatabaseLogs.does_exists('logs', {})):
            try:
                database['logs'].insert_one(log).inserted_id
            except Exception as e:
                print("Error inserting log: {}".format(e))
                return False
            return True

    def get_all_logs():
        logs = DatabaseLogs.get('logs', {}, sortBy=[("_id", 1)])
        logs.pop(0)
        for log in logs:
            log["_id"] = str(log["_id"])
        return logs

    @staticmethod
    def get_db():
        try:
            return DatabaseLogs.database
        except Exception as err:
            print("GET DB ERROR", err)
            return False

    '''TODO implement this method'''
    @staticmethod
    def checks_if_the_db_exists(conn: dict, c: dict) -> bool:
        return True

    @staticmethod
    def populate_database() -> None:
        DatabaseLogs.insert_collection("logs")
 
    '''Generic methods'''

    @staticmethod
    def make_a_query_text(item):
        _id = item['_id']
        del item['_id']
        new_values: dict = {'$set': item}
        query = dict(_id=ObjectId(_id))
        return {"query": query, "new_values": new_values}

    @staticmethod
    def make_a_delete_query_text(item):
        _id = item['_id']
        query = dict(_id=ObjectId(_id))
        return {"query": query}

    @staticmethod
    def insert_collection(collection_name) -> None:
        database = DatabaseLogs.get_db()
        if(not DatabaseLogs.does_exists(collection_name, {})):
            collection = [
                {
                    "test": "test"
                }
            ]
            for documents in collection:
                database[collection_name].insert_one(documents).inserted_id

    @staticmethod
    def get(collection, query, sortBy=''):
        data_dict = []
        try:
            database = DatabaseLogs.get_db()
            if (len(sortBy) > 0):
                cursor = database[collection].find(query).sort(sortBy)
            else:
                cursor = database[collection].find(query)
            for register in cursor:
                data_dict.append(register)
        except Exception as e:
            print("\n\n\nError: {}".format(e))
        finally:
            return data_dict

    @staticmethod
    def update(collection: str, data_dict: dict):
        response = None
        try:
            database = DatabaseLogs.get_db()
            response = database[collection].\
                update_one(data_dict["query"], data_dict["new_values"])
        except (Exception) as error:
            print('erro', str(error))
        return response

    @staticmethod
    def remove(collection: str, query: dict):
        database = DatabaseLogs.get_db()
        return database[collection].delete_many(query)

    @staticmethod
    def does_exists(collection: str, query: dict):
        database = DatabaseLogs.get_db()
        return database[collection].count_documents(query) > 0
