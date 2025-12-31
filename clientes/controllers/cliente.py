from fastapi import APIRouter, status, HTTPException, Depends
from schemas import clienteOut
from clientes.schemas.cliente import clienteIn, clienteUpdateIn
from clientes.services.cliente import ClienteService
from security import login_required


ClienteRouter = APIRouter(prefix="/clientes", tags=["Clientes"], dependencies=[Depends(login_required)])

service = ClienteService()

@ClienteRouter.get("/", 
                   response_model=list[clienteOut], 
                   description="Obter dados de todos os clientes"
                   )
async def mostrar_clientes(limit: int = 100, skip: int = 0):
    try: 
        return await service.show_clients(limit=limit, skip=skip)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Erro ao buscar clientes"
        )
        
@ClienteRouter.post("/", 
                    status_code=status.HTTP_201_CREATED, 
                    response_model=clienteOut,
                    description="Adicionar novo cliente"
                    )
async def adicionar_cliente(cliente: clienteIn):
    return {**cliente.model_dump(), "id": await service.create(cliente)}

@ClienteRouter.get("/{id}", 
                   response_model=clienteOut,
                   description="Buscar cliente por id"
                   )
async def buscar_cliente_por_id(id: int):
    try:
        return await service.read_by_id(id)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum cliente foi encontrado no id {id}"
        )
        
@ClienteRouter.patch("/{id}",
                     response_model=clienteOut,
                     description="Atualizar dados de clientes por id")
async def atualizar_cliente_por_id(id: int, cliente: clienteUpdateIn):
    try:
        return await service.update(id, cliente)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum cliente foi encontrado no id {id}"
        )
        
@ClienteRouter.delete("/{id}", 
                      status_code=status.HTTP_204_NO_CONTENT,
                      response_model=None,
                      description="Deletar cliente por id"
                     )
async def deletar_cliente(id: int):
    try: 
        return await service.delete(id)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente não encontrado no id {id}"
        )

