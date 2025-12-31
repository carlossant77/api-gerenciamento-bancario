from fastapi import HTTPException
from database import database
from databases.interfaces import Record
from clientes.models.cliente import clientes


class ClienteService:
    async def __get_by_id(self, id) -> Record:
        query = clientes.select().where(clientes.c.id == id)
        cliente =  await database.fetch_one(query)    
        if not cliente: 
            raise HTTPException(
                status_code=404,
            )
        return cliente
    
    async def count(self, id: int) -> None:
        query = "select count(id) as total from clientes where id = :id"
        result = await database.fetch_one(query, {"id": id})
        return result.total
    
    async def show_clients(self, limit: int, skip: int = 0) -> list[Record]:
        try: 
            query = clientes.select().limit(limit).offset(skip)
            return await database.fetch_all(query)
        except Exception as e:
            print(f"ocorreu um erro ao realizar a busca: {e}")
            return []
                 
    async def create(self, cliente) -> int:
        try: 
            query = clientes.insert().values(
                nome = cliente.nome,
                cpf = cliente.cpf,
                endereco = cliente.endereco,
                data_nascimento = cliente.data_nascimento
            )     
            return await database.execute(query)
        except Exception as e:
            print(f"ocorreu um erro ao inserir dados: {e}") 
            
    async def read_by_id(self, id: int) -> Record:
        return await self.__get_by_id(id)
    
    async def update(self, id: int, cliente):
        total = await self.count(id)
        if not total:
            raise HTTPException(
                status_code=404
            )
        
        data = cliente.model_dump(exclude_unset=True)
        query = clientes.update().where(clientes.c.id == id).values(**data)
        await database.execute(query)
        
        return await self.__get_by_id(id)
    
    async def delete(self, id) -> None:
        total = await self.count(id)
        if not total:
            raise HTTPException(
                status_code=404
            )
            
        query = clientes.delete().where(clientes.c.id == id)
        return await database.execute(query)
