import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://mongo:27017')
database = client['tarefas']
colecao_tarefas = database['tarefas']
