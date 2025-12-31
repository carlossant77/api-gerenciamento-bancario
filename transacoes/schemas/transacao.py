from pydantic import BaseModel
from decimal import Decimal
from enum import Enum
from datetime import datetime


class TipoTransacao(str, Enum):
    DEPOSITO = "deposito"
    SAQUE = "saque"

class transacaoIn(BaseModel):
    tipo: TipoTransacao
    valor: Decimal
    conta: int
    
class transacaoOut(BaseModel):
    id: int
    tipo: str
    valor: Decimal
    conta: int
    hora: datetime
    