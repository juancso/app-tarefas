from fastapi import APIRouter, HTTPException
from app.models import Tarefa, TarefaInDB
from app.database import colecao_tarefas
from bson import ObjectId

router = APIRouter()

@router.post("/tarefas/", response_model=TarefaInDB)
async def criar_tarefa(tarefa: Tarefa):
    tarefa_doc = tarefa.dict()
    resultado = await colecao_tarefas.insert_one(tarefa_doc)
    tarefa_in_db = TarefaInDB(id=str(resultado.inserted_id), **tarefa_doc)
    return tarefa_in_db

@router.get("/tarefas/", response_model=list[TarefaInDB])
async def listar_tarefas():
    tarefas = await colecao_tarefas.find().to_list(1000)
    return [TarefaInDB(id=str(tarefa["_id"]), descricao=tarefa["descricao"]) for tarefa in tarefas]

@router.get("/tarefas/{id}", response_model=TarefaInDB)
async def obter_tarefa(id: str):
    tarefa = await colecao_tarefas.find_one({"_id": ObjectId(id)})
    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return TarefaInDB(id=str(tarefa["_id"]), descricao=tarefa["descricao"])

@router.put("/tarefas/{id}", response_model=TarefaInDB)
async def atualizar_tarefa(id: str, tarefa: Tarefa):
    resultado = await colecao_tarefas.update_one({"_id": ObjectId(id)}, {"$set": tarefa.dict()})
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return TarefaInDB(id=id, **tarefa.dict())

@router.delete("/tarefas/{id}")
async def deletar_tarefa(id: str):
    resultado = await colecao_tarefas.delete_one({"_id": ObjectId(id)})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"mensagem": "Tarefa deletada com sucesso"}
