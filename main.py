from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import database, metadata, engine
from clientes.controllers.cliente import ClienteRouter
from contas.controllers.conta import ContaRouter
from transacoes.controllers.transacao import TransacaoRouter
from controllers.auth import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    from clientes.models.cliente import clientes
    from contas.models.conta import contas
    from transacoes.models.transacao import transacoes
    
    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()

app = FastAPI(title="API Bancária", 
              description=
"""
API para realização de transações bancárias e gerenciamento de contas 

## Clientes
- Mostrar todos os clientes cadastrados
- Cadastrar novo cliente
- Buscar cliente por id
- Atualizar dados de um cliente específico
- Deletar cliente do sistema

## Contas
- Mostrar todas as contas cadastradas
- Criar uma nova conta vinculada um cliente: Um cliente pode ter apenas uma conta
- Buscar conta por id
- Deletar conta do sistema

## Transações
- Obter dados de todas as transações: pelo query paramenter "conta_id" é possível 
obter histórico de apenas uma conta específica
- Realizar transação: realiza uma transação de saque ou deposito, alterando automaticamente
o saldo da conta informada na transação
- Buscar transação por id
""",
              lifespan=lifespan,
              version="1.0.0")
app.include_router(ClienteRouter)
app.include_router(ContaRouter)
app.include_router(TransacaoRouter)
app.include_router(router)

