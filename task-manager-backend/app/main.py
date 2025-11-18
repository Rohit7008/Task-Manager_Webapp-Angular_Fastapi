from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models, auth, tasks, database

app = FastAPI(title="Task Manager API")

# Allow CORS from our Angular dev server and production origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "https://your-frontend-domain.example"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(tasks.router, prefix="/tasks")

# create tables on startup (for dev)
@app.on_event("startup")
def on_startup():
    database.init_db()

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Task Manager API running!"}
