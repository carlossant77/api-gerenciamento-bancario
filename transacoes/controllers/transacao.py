from fastapi import APIRouter, Depends, status, HTTPException
from schemas import transacaoOut
from security import login_required
from transacoes.schemas.transacao import transacaoIn
from transacoes.services.transacao import TransacaoService

TransacaoRouter = APIRouter(prefix="/transacoes", tags=["Transacoes"], dependencies=[Depends(login_required)])

service = TransacaoService()

@TransacaoRouter.get("/", 
                   response_model=list[transacaoOut], 
                   description="Obter dados de todas as transações (ou buscar historico de conta por id)"
                   )
async def mostrar_transacoes(limit: int = 100, skip: int = 0, conta_id: int = None):
    try: 
        return await service.show_transations(limit=limit, skip=skip, id=conta_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar transacoes: {e}"
        )
        
@TransacaoRouter.post("/", 
                    status_code=status.HTTP_201_CREATED, 
                    response_model=transacaoOut,
                    description="Realizar Transação"
                    )
async def realizar_transacao(transacao: transacaoIn):
    try:
        return await service.create(transacao)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Não foi possível realizar a transação. Erro: {e}"
        )

@TransacaoRouter.get("/{id}", 
                   response_model=transacaoOut,
                   description="Buscar transacao por id"
                   )
async def buscar_transacao_por_id(id: int):
    try:
        return await service.read_by_id(id)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhuma transacao foi encontrada no id {id}"
        )