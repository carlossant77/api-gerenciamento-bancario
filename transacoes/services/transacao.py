from fastapi import HTTPException
from database import database
from databases.interfaces import Record
from transacoes.models.transacao import transacoes
from contas.models.conta import contas
from sqlalchemy import select, update
from decimal import Decimal


class TransacaoService:
    async def __get_by_id(self, id) -> Record:
        query = transacoes.select().where(transacoes.c.id == id)
        transacao = await database.fetch_one(query)
        if not transacao:
            raise HTTPException(
                status_code=404,
                detail="Transação não encontrada"
            )
        return transacao

    async def show_transations(self, limit: int, skip: int = 0, id: int = None) -> list[Record]:
        if id:
            query = transacoes.select().limit(limit).offset(skip).filter(transacoes.c.conta == id)
        else:
            query = transacoes.select().limit(limit).offset(skip)
        return await database.fetch_all(query)
    
    async def create(self, transacao):
        command = contas.select().where(contas.c.id == transacao.conta)
        conta = await database.fetch_one(command)
        if conta:
            
            valor = transacao.valor
            
            if valor <= Decimal("0.0"):
                    raise ValueError(
                        "O valor da transação não pode ser menor ou igual a 0."
                    )
                    
            if transacao.tipo.value == 'deposito':
                updade_query = contas.update().where(contas.c.id == transacao.conta).values(saldo=contas.c.saldo + valor)
                await database.execute(updade_query)
            
            if transacao.tipo.value == 'saque':
                query = contas.update().where(
                    (contas.c.id == transacao.conta) & (contas.c.saldo >= valor)
                ).values(saldo=contas.c.saldo - valor)
                
                rows = await database.execute(query)
                if rows == 0:
                    raise HTTPException(400, "Saldo insuficiente ou conta inexistente.")
                                            
            query = transacoes.insert().values(
                tipo=transacao.tipo,
                valor=transacao.valor,
                conta=transacao.conta
            )
            result = await database.execute(query)
            id_query = transacoes.select().where(transacoes.c.id == result)
            response = await database.fetch_one(id_query)
            return dict(response)
        else:
            raise HTTPException(
                status_code=404
            )

    async def read_by_id(self, id: int) -> Record:
        return await self.__get_by_id(id)