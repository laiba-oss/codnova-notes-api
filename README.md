# CodNova Notes API

## Project Overview
CodNova Notes API is a RESTful API developed using Python, FastAPI, and SQLite. It allows users to create, view, update, and delete notes.

## Technologies Used
- Python
- FastAPI
- Uvicorn
- SQLite
- Pydantic
- Swagger UI

## Features
- Create a new note
- Retrieve all notes
- Retrieve a note by ID
- Update an existing note
- Delete a note
- Validate note title and content
- Handle missing notes with HTTP 404 errors

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API status |
| POST | `/notes` | Create a note |
| GET | `/notes` | Retrieve all notes |
| GET | `/notes/{note_id}` | Retrieve a note by ID |
| PUT | `/notes/{note_id}` | Update a note |
| DELETE | `/notes/{note_id}` | Delete a note |

## Run the Project

1. Create and activate a Python virtual environment.
2. Install dependencies:

   `python -m pip install fastapi "uvicorn[standard]"`

3. Start the server:

   `python -m uvicorn main:app --reload`

4. Open the API documentation:

   `http://127.0.0.1:8000/docs`

## Database
The project uses SQLite to store notes. The database and notes table are initialized automatically when the application starts.

## Validation
- Title: 1–100 characters
- Content: 1–5000 characters
- Invalid request data returns HTTP 422.
- A note that does not exist returns HTTP 404.