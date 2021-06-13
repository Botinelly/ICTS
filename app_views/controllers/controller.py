from os import path
import subprocess

import platform
import subprocess

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from ..models.models import Aparelho, Sensor
from ..models.model import db, SessionLocal

from ..main import app

#Instancia a sessão para acesso ao banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Função pra dar um ping pelo terminal para saber se o dispositivo está online
def ping(host):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]

    #Subprocess chama o terminal e executa o comando ping com os parâmetros da variável command
    return subprocess.call(command) == 0

#Rota de teste
@app.get('/')
def home():
    return {"API Online": 200}


"""------------------APARELHOS------------------"""
#rota que cria um novo Aparelho
@app.get('/cria_aparelho/{nome}/{comodo}/{ip}/{consumo}')
def cria_aparelho(nome: str=None, comodo: str=None, ip: str=None, consumo: str=None, db: Session = Depends(get_db)):
    
    #Verifica se há dados faltando
    if nome == None or comodo == None or ip == None or consumo == None:
        return {"Dados faltando, favor reenviar": 200}
    else:    
        #instancia um novo objeto da classe Aparelho
        novo = Aparelho(nome=nome, comodo=comodo, ip=ip, consumo=consumo)
        db.add(novo)
        db.commit()
        #Zera o objeto
        novo = None
        return {"Novo aparelho inserido com sucesso!": 200}
    
#Rota que atualiza dados de um aparelho existente
@app.get('/atualiza_aparelho/{id}/{nome}/{comodo}/{ip}/{consumo}')
def atualiza_aparelho(id: str=None, nome: str=None, comodo: str=None, ip: str=None, consumo: str=None, db: Session = Depends(get_db)):
    
    #Verifica se há dados faltando
    if nome == None or comodo == None or ip == None or consumo == None:
        return {"Dados faltando, favor reenviar": 200}
    else:
        #Atribui os dados do novo ao antigo aparelho
        old = db.query(Aparelho).filter(Aparelho.id==id).first()
        print(old)
        old.nome = nome
        old.comodo = comodo
        old.ip = ip
        old.consumo = consumo
        
        #comandos para enviar os dados ao banco de dados SQLite3 através do SQLAlchemy
        db.add(old)
        db.commit()
        return {"Atualizado com sucesso": 200}

#Rota que remove um aparelho já existente
@app.get('/remove_aparelho/{id}')
def remove_aparelho(id: str, db: Session = Depends(get_db)):
      
    #verifica se faltam dados
    if id == None:
        return {"Dados faltando, favor reenviar": 200}
        
    else:
        old = db.query(Aparelho).filter(Aparelho.id==id).first()
        
        #comandos para deletar os dados do banco de dados SQLite3 através do SQLAlchemy
        db.delete(old)
        db.commit()
        return {"Removido com sucesso": 200}

#Rota que lista o aparelho por Nome e ID
@app.get('/lista_nome_aparelho')
def lista_nome_aparelho(db: Session = Depends(get_db)):
    
    full_list = db.query(Aparelho).all()
    
    #Dicionário para criação do arquivo JSON de retorno
    json = {"Items":[]}
    
    #Percorre todo o objeto da classe Aparelho e adiciona os respectivos ID's e Nomes ao dicionário
    for i in full_list:
        json["Items"].append([i.id, i.nome])
    
    #Converte para JSON e retorna o mesmo.    
    return json

#Rota que lista um aparelho específico por ID
@app.get('/lista_aparelho/{id}')
def lista_aparelho(id: str,db: Session = Depends(get_db)):
        
    ligado = True
    if id == None:
        return {"Dados faltando, favor reenviar": 200}
    else:
        obj = db.query(Aparelho).filter(Aparelho.id==id).first()
        
        #comando ping para saber se o objeto está ligado ou não
        ligado = "Ligado: " + str(ping(obj.ip))
        
        json = {"Items":[]}
        json["Items"].append([obj.id, obj.nome, obj.comodo, obj.ip, ligado, obj.consumo])

        return json

""" ---------------SENSORES DE TEMPERATURA---------------- """

#Rota para criação de sensores 
@app.get('/cria_sensor/{comodo}/{temp}')
def cria_sensor(comodo: str, temp:float, db: Session = Depends(get_db)):
   
    #verifica se faltam dados
    if comodo == None or temp == None:
        return {"Dados faltando, favor reenviar": 200}
    else:
        novo = Sensor(comodo=comodo, temp=temp)
        
        #comandos para enviar os dados ao banco de dados SQLite3 através do SQLAlchemy
        db.add(novo)
        db.commit()
        novo = None
        return {"Novo sensor de temperatura inserido com sucesso!": 200}
    
#Rota para listar todos os sensores existentes
@app.get('/lista_sensor')
def lista_sensor(db: Session = Depends(get_db)):
    full_list = db.query(Sensor).all()
    return full_list

#rota para atualizar a temperatura de um sensor já existente
@app.get('/atualiza_temperatura/{id}/{temp}')
def atualiza_temperatura(id:int, temp:float ,db: Session = Depends(get_db)):
    #verifica se faltam dados
    if temp == None:
        return {"Dados faltando, favor reenviar": 200}
    else:
        old = db.query(Sensor).filter(Sensor.id == id).first()
        old.temp = temp
        
        #comandos para enviar os dados ao banco de dados SQLite3 através do SQLAlchemy
        db.add(old)
        db.commit()
        return {"Temperatura atualizada com sucesso!": 200}

#Rota para verificação das maiores e menores temperaturas dos sensores
@app.get('/verifica_temp')
def verifica_temp(db: Session = Depends(get_db)):
    
    full_list = db.query(Sensor).all()
    
    maior = Sensor()
    menor = Sensor()
    
    #Percorre comparando a temperatura de todos os sensores cadastrados e armazena o maior e o menor
    for i in full_list:  
        if i.temp >= full_list[0].temp:
            maior = i
        if i.temp <= full_list[0].temp:
            menor = i
                    
    #Monta um json com a maior e menor temperatura, junto com seus respectivos cômodos
    json = {"Maior":[maior.comodo, maior.temp], "Menor":[menor.comodo, menor.temp]}
    return json
    
    
#Rota para remoção de um sensor já existente
@app.get('/remover_sensor/{id}')
def remover_sensor(id:int, db: Session = Depends(get_db)):
       
    #verifica se faltam dados
    if id == None:
        return {"Dados faltando, favor reenviar": 200}
        
    else:
        old = db.query(Sensor).filter(Sensor.id == id).first()
        
        #comandos para deletar os dados do banco de dados SQLite3 através do SQLAlchemy
        db.delete(old)
        db.commit()
        return {"Removido com sucesso": 200}
