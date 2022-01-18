from os import path
import subprocess
from datetime import datetime
import pytz

import platform
import subprocess

from fastapi import FastAPI, Depends

from ..models.models import Aparelho, UpdateAparelho
from ..models.database import Database
from ..models.databaselogs import DatabaseLogs

from ..main import app


def start_station():
    try:
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

    except (Exception) as error:
        print('erro', str(error))

def create_log(msg):
    IST = pytz.timezone('America/Manaus')
    date = datetime.now(IST).strftime('%Y-%m-%dT%H-%M-%S')
    DatabaseLogs.create_log({
        "msg": msg,
        "date": date
        })

#Rota de teste
@app.get('/')
def home():
    print("STARTING APPLICATION")
    start_station()
    print("APPLICATION STARTED")
    return {"API Online": 200}


"""------------------APARELHOS------------------"""
#rota que cria um novo Aparelho
@app.post('/cria_aparelho')
def cria_aparelho(value: Aparelho):
    #instancia um novo objeto da classe Aparelho
    print(value)
    Database.insert_device(value.__dict__)
    create_log("device " + value.nome + " created!")
    return {"Novo aparelho inserido com sucesso!": 200}
    
#Rota que atualiza dados de um aparelho existente
@app.post('/atualiza_aparelho')
def atualiza_aparelho(value: UpdateAparelho):
    #Atribui os dados do novo ao antigo aparelho

    new_dev = value.__dict__
    new_dev["_id"] = value.id
    del new_dev["id"]
    result = Database.update_device(new_dev)
    print(new_dev, value)
    create_log("device " + value.nome + " updated!")
    return {"Atualizado com sucesso": 200}

#Rota que remove um aparelho já existente
@app.get('/remove_aparelho/{id}')
def remove_aparelho(id: str):
    Database.delete_device(id)
    create_log("device id " + id + " removed!")
    return {"Removido com sucesso": 200}

#Rota que lista o aparelho por Nome e ID
@app.get('/lista_aparelho')
def lista_aparelho():
    devices = Database.get_all_devices()
    return {"devices": devices}

@app.get('/get_all_logs')
def get_all_logs():
    logs = DatabaseLogs.get_all_logs()
    return {"devices": logs}
