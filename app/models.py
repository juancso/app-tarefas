from pydantic import BaseModel

class Tarefa(BaseModel):
    descricao: str

class TarefaInDB(Tarefa):
    id: str
