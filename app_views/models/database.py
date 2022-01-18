from typing import List
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import json
from bson import ObjectId
import re


class Database:
    '''Basic Database methods '''
    host: str = ""
    port: int = 0
    dbconn: MongoClient = None
    database: None = None


    @staticmethod
    def initialize(
            host: str = 'thanos-station-backend-db',
            port: int = 27017):

        Database.host = host
        Database.port = port
        Database.dbconn = None            

    @staticmethod
    def connect_to_db():
        try:
            Database.dbconn = MongoClient(
                host=Database.host,
                port=Database.port,
                serverSelectionTimeoutMS=3000
            )
            test_result = Database.check_connection()
            return test_result
        except Exception as err:
            print("connect to db error ", err)
            return False

    @staticmethod
    def check_connection():
        try:
            Database.dbconn.admin.command('ismaster')
        except ConnectionFailure as err:
            print("check connection error ",err)
            return False
        return True

    @staticmethod
    def disconnect_from_db():
        try:
            Database.dbconn.close()
        except Exception:
            return False
        return True

    @staticmethod
    def set_db(database):
        try:
            Database.database = Database.dbconn[database]
        except Exception as err:
            print("Set DB error", err)
            return False
        return True

    @staticmethod
    def insert_device(device):
        database = Database.get_db()
        if(Database.does_exists('device', {})):
            try:
                database['device'].insert_one(device).inserted_id
            except Exception as e:
                print("Error inserting device: {}".format(e))
                return False
            return True

    @staticmethod
    def update_device(device):
        return Database.update(
            "device", Database.make_a_query_text(device))
    
    @staticmethod
    def delete_device(device):
        query = {"_id": ObjectId(device)}
        return Database.remove(
            "device", query)

    @staticmethod
    def get_all_devices():
        devices = Database.get('device', {}, sortBy=[("_id", 1)])
        devices.pop(0)
        for device in devices:
            device["_id"] = str(device["_id"])
        return devices

    @staticmethod
    def get_db():
        try:
            return Database.database
        except Exception as err:
            print("GET DB ERROR", err)
            return False

    '''TODO implement this method'''
    @staticmethod
    def checks_if_the_db_exists(conn: dict, c: dict) -> bool:
        return True

    @staticmethod
    def populate_database() -> None:
        # station = {"macAddress": "00-1B-63-84-45-E6",
        #     "line": "02",
        #     "pc_name": "Test_machine_01"}

        Database.insert_collection("device")
        Database.insert_collection("sensor")
        # Database.insert_station(station)
 
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
        database = Database.get_db()
        if(not Database.does_exists(collection_name, {})):
            collection = [{"test": "test"}]
            for documents in collection:
                database[collection_name].insert_one(documents).inserted_id

    @staticmethod
    def get(collection, query, sortBy=''):
        data_dict = []
        try:
            database = Database.get_db()
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
            database = Database.get_db()
            response = database[collection].\
                update_one(data_dict["query"], data_dict["new_values"])
        except (Exception) as error:
            print('erro no update ', str(error))
        return response

    @staticmethod
    def remove(collection: str, query: dict):
        database = Database.get_db()
        return database[collection].delete_many(query)

    @staticmethod
    def does_exists(collection: str, query: dict):
        database = Database.get_db()
        print("DATABASE", database)
        print(database[collection].count_documents(query))
        return database[collection].count_documents(query) > 0
