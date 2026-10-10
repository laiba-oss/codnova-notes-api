

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from pydantic import BaseModel, Field

from database import create_table, get_connection



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    yield


app = FastAPI(
    title="CodNova Notes API",
    description="A REST API to manage notes",
    version="1.0.0",
    lifespan=lifespan
)



class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1, max_length=5000)



@app.get("/")
def home():
    return {"message": "CodNova Notes API is running!"}


@app.post("/notes", status_code=201)
def create_note(note: NoteCreate):
    connection = get_connection()

    cursor = connection.execute(
        "INSERT INTO notes (title, content) VALUES (?, ?)",
        (note.title, note.content)
    )

    connection.commit()
    note_id = cursor.lastrowid
    connection.close()

    return {
        "id": note_id,
        "title": note.title,
        "content": note.content
    }


@app.get("/notes")
def get_notes():
    connection = get_connection()
    rows = connection.execute(
        "SELECT id, title, content FROM notes ORDER BY id"
    ).fetchall()
    connection.close()

    return [dict(row) for row in rows]


@app.get("/notes/{note_id}")
def get_note(note_id: int):
    connection = get_connection()
    row = connection.execute(
        "SELECT id, title, content FROM notes WHERE id = ?",
        (note_id,)
    ).fetchone()
    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return dict(row)


@app.put("/notes/{note_id}")
def update_note(note_id: int, note: NoteCreate):
    connection = get_connection()

    cursor = connection.execute(
        "UPDATE notes SET title = ?, content = ? WHERE id = ?",
        (note.title, note.content, note_id)
    )

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    row = connection.execute(
        "SELECT id, title, content FROM notes WHERE id = ?",
        (note_id,)
    ).fetchone()

    connection.close()

    return dict(row)


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    connection = get_connection()

    cursor = connection.execute(
        "DELETE FROM notes WHERE id = ?",
        (note_id,)
    )

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    connection.close()

    return {"message": "Note deleted successfully"}
