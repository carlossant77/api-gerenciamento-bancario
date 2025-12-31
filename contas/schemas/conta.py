from pydantic import BaseModel
from decimal import Decimal

class contaIn(BaseModel):
    cliente_id: int

class contaOut(BaseModel):
    id: int
    saldo: Decimal
    titular: "reformedClientOut"
    
    