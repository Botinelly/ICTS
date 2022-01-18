from os import path
from pydantic import BaseModel


class Aparelho(BaseModel):
    nome: str
    comodo: str
    ip: str
    consumo: str

class UpdateAparelho(BaseModel):
    id: str
    nome: str
    comodo: str
    ip: str
    consumo: str
