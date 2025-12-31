from fastapi import APIRouter, status, HTTPException, Depends
from schemas import contaOut
from contas.schemas.conta import contaIn
from contas.services.conta import ContaService
from security import login_required

ContaRouter = APIRouter(prefix="/contas", tags=["Contas"], dependencies=[Depends(login_required)])

service = ContaService()

@ContaRouter.get("/", 
                   response_model=list[contaOut], 
                   description="Obter dados de todas as contas"
                   )
async def mostrar_contas(limit: int = 100, skip: int = 0):
    try: 
        return await service.show_accounts(limit=limit, skip=skip)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Erro ao buscar contas"
        )
        
@ContaRouter.post("/", 
                    status_code=status.HTTP_201_CREATED, 
                    response_model=contaOut,
                    description="Adicionar nova conta"
                    )
async def adicionar_conta(conta: contaIn):
    try:
        return {**conta.model_dump(), 
                "id": await service.create(conta), 
                "saldo": 0, 
                "titular": await service.get_client_by_id(conta.cliente_id)}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Não foi possível cadastrar nova conta. Erro: {e}"
        )

@ContaRouter.get("/{id}", 
                   response_model=contaOut,
                   description="Buscar conta por id"
                   )
async def buscar_conta_por_id(id: int):
    try:
        data = dict(await service.read_by_id(id))
        print(data)
        return {
            "id": data["id"],
            "saldo": data["saldo"],
            "titular": await service.get_client_by_id(data["cliente_id"])
        }
    except Exception:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhuma conta foi encontrado no id {id}"
        )
        

        
@ContaRouter.delete("/{id}", 
                      status_code=status.HTTP_204_NO_CONTENT,
                      response_model=None,
                      description="Deletar conta por id"
                     )
async def deletar_conta(id: int):
    try: 
        return await service.delete(id)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail=f"Conta não encontrado no id {id}"
        )