from os import path
from sqlalchemy import Column, Integer, String, Float
from .model import db

class Aparelho(db):
    #Classe Aparelho para criação do banco de dados sqlite3
    
    __tablename__ = "aparelhos"
    id = Column(Integer, primary_key=True)
    nome = Column(String(80), unique=False, nullable=False)
    comodo = Column(String(120), unique=False, nullable=False)
    ip = Column(String(120), unique=False, nullable=False)
    consumo = Column(Integer, unique=False, nullable=False)
    
    def __repr__(self):
        return '<Aparelho %r>' % self.nome

class Sensor(db):
    #Classe sensor para criação do banco de dados sqlite3
    __tablename__ = "sensores"
    id = Column(Integer, primary_key=True)
    comodo = Column(String(120), unique=False, nullable=False)
    temp = Column(Float, unique=False, nullable=False)
     
    def __repr__(self):
        return '<Sensor %r>' % self.nome
