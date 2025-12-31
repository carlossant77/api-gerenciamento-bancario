from pydantic import BaseModel
from typing import Optional

class clienteIn(BaseModel):
    nome: str
    cpf: str
    data_nascimento: str
    endereco: str
    
class clienteUpdateIn(BaseModel):
    nome: str | None = None
    cpf: str | None = None
    data_nascimento: str | None = None
    endereco: str | None = None
    
class clienteOut(BaseModel):
    id: int
    nome: str
    data_nascimento: str
    
class reformedClientOut(BaseModel):
    id: int
    nome: str
    