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
import ssl
from datetime import datetime
import time

ctx = ssl.create_default_context(cafile='')
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

host_server = os.environ.get('host_server')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port')))
database_name = os.environ.get('database_name')
db_username = urllib.parse.quote_plus(str(os.environ.get('db_username')))
db_password = urllib.parse.quote_plus(str(os.environ.get('db_password')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode')))
# DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)
DATABASE_URL = 'postgres://hquasadanjovxm:74cbc8adaa3db997056839dea9ba9cf88f1ea76b946c1ff2e45bffc39f182946@ec2-18-211-171-122.compute-1.amazonaws.com:5432/de96010mpiergn?sslmode=disable'

database = databases.Database(DATABASE_URL, ssl=ctx)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "postdemo",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("uuid", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column('username', sqlalchemy.String(16), nullable=False),
    sqlalchemy.Column('imageurl', sqlalchemy.String()),
    sqlalchemy.Column("nlike", sqlalchemy.Integer),
    sqlalchemy.Column("ncomment", sqlalchemy.Integer),
    sqlalchemy.Column("commentid", sqlalchemy.String),
    sqlalchemy.Column("datetimenow", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(
    'postgres://hquasadanjovxm:74cbc8adaa3db997056839dea9ba9cf88f1ea76b946c1ff2e45bffc39f182946@ec2-18-211-171-122.compute-1.amazonaws.com:5432/de96010mpiergn', pool_size=3, max_overflow=0,
)
metadata.create_all(engine)



class Post(BaseModel):
    id: int
    uuid: str
    description: str
    username: str
    imageurl: str
    nlike: int
    ncomment: int
    commentid: str
    datetimenow: str


class PostIn(BaseModel):
    uuid: str
    description: str
    username: str
    imageurl: str
    nlike: int
    ncomment: int
    commentid: str


    


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

@app.get("/posts/", response_model=List[Post], status_code = status.HTTP_200_OK)
async def read_notes(page_no: int = 0):
    query = notes.select().offset(page_no*10).limit(10)
    return await database.fetch_all(query)


@app.post("/posts/", response_model=PostIn, status_code = status.HTTP_201_CREATED)
async def create_note(note: PostIn):
    query = notes.insert().values(
        uuid=note.uuid,
        description=note.description,
        username=note.username,
        imageurl=note.imageurl,
        nlike=note.nlike,
        ncomment=note.ncomment,
        commentid=note.commentid,
        datetimenow=str(time.time()),
    )
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}


# @app.get("/notes/{note_id}/", response_model=Note, status_code = status.HTTP_200_OK)
# async def read_notes(note_id: int):
#     query = notes.select().where(notes.c.id == note_id)
#     return await database.fetch_one(query)


# @app.put("/notes/{note_id}/", response_model=Note, status_code = status.HTTP_200_OK)
# async def update_note(note_id: int, payload: NoteIn):
#     query = notes.update().where(notes.c.id == note_id).values(text=payload.text, completed=payload.completed)
#     await database.execute(query)
#     return {**payload.dict(), "id": note_id}

# @app.delete("/notes/{note_id}/", status_code = status.HTTP_200_OK)
# async def delete_note(note_id: int):
#     query = notes.delete().where(notes.c.id == note_id)
#     await database.execute(query)
#     return {"message": "Note with id: {} deleted successfully!".format(note_id)}

    