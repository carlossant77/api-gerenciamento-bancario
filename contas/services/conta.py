from fastapi import HTTPException
from database import database
from databases.interfaces import Record
from contas.models.conta import contas
from clientes.models.cliente import clientes
from sqlalchemy import select


class ContaService:
    async def __get_by_id(self, id) -> Record:
        query = contas.select().where(contas.c.id == id)
        conta = await database.fetch_one(query)
        if not conta:
            raise HTTPException(
                status_code=404,
                detail="Cliente não encontrado"
            )
        return conta

    async def get_client_by_id(self, id) -> Record:
        query = clientes.select().where(clientes.c.id == id)
        cliente = await database.fetch_one(query)
        if not cliente:
            raise HTTPException(
                status_code=404,
                detail="Cliente não encontrado"
            )
        return cliente

    async def count(self, id: int) -> None:
        query = "select count(id) as total from contas where id = :id"
        result = await database.fetch_one(query, {"id": id})
        return result.total

    async def show_accounts(self, limit: int, skip: int = 0):
        query = (
            select(
                contas.c.id.label("conta_id"),
                contas.c.saldo,
                contas.c.cliente_id,
                clientes.c.id.label("titular_id"),
                clientes.c.nome.label("titular_nome"),
            )
            .select_from(
                contas.join(clientes, clientes.c.id == contas.c.cliente_id)
            )
            .limit(limit)
            .offset(skip)
        )

        rows = await database.fetch_all(query)

        result = []
        for row in rows:
            data = dict(row)

            result.append({
                "id": data["conta_id"],
                "saldo": data["saldo"],
                "titular": {
                    "id": data["titular_id"],
                    "nome": data["titular_nome"],
                }
            })

        return result

    async def create(self, conta) -> int:
        command = clientes.select().where(clientes.c.id == conta.cliente_id)
        cliente = await database.fetch_one(command)
        if cliente:
            query = contas.insert().values(
                cliente_id=conta.cliente_id,
                saldo=0
            )
            return await database.execute(query)
        else:
            raise HTTPException(
                status_code=404
            )

    async def read_by_id(self, id: int) -> Record:
        return await self.__get_by_id(id)

    async def delete(self, id) -> None:
        total = await self.count(id)
        if not total:
            raise HTTPException(
                status_code=404
            )

        query = contas.delete().where(contas.c.id == id)
        return await database.execute(query)
