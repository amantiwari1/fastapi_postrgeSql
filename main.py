from typing import List
import databases
import sqlalchemy
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import urllib
from dotenv import load_dotenv
load_dotenv()


host_server = os.environ.get('host_server')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port')))
database_name = os.environ.get('database_name')
db_username = urllib.parse.quote_plus(str(os.environ.get('db_username')))
db_password = urllib.parse.quote_plus(str(os.environ.get('db_password')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode')))
DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, pool_size=3, max_overflow=0
)
metadata.create_all(engine)

class NoteIn(BaseModel):
    text: str
    completed: bool

class Note(BaseModel):
    id: int
    text: str
    completed: bool


app = FastAPI(title="REST API using FastAPI PostgreSQL Async EndPoints")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()



@app.get("/")
async def read_main():
    return {"msg": "yes"}

@app.get("/note/", response_model=List[Note], status_code = status.HTTP_200_OK)
async def read_notes(skip: int = 0, take: int = 20):
    query = notes.select().offset(skip).limit(take)
    return await database.fetch_all(query)

@app.get("/note/{note_id}/", response_model=Note, status_code = status.HTTP_200_OK)
async def read_notes(note_id: int):
    query = notes.select().where(notes.c.id == note_id)
    return await database.fetch_one(query)

@app.post("/note/", response_model=Note, status_code = status.HTTP_201_CREATED)
async def create_note(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}

@app.put("/note/{note_id}/", response_model=Note, status_code = status.HTTP_200_OK)
async def update_note(note_id: int, payload: NoteIn):
    query = notes.update().where(notes.c.id == note_id).values(text=payload.text, completed=payload.completed)
    await database.execute(query)
    return {**payload.dict(), "id": note_id}

@app.delete("/note/{note_id}/", status_code = status.HTTP_200_OK)
async def delete_note(note_id: int):
    query = notes.delete().where(notes.c.id == note_id)
    await database.execute(query)
    return {"message": "Note with id: {} deleted successfully!".format(note_id)}

    


