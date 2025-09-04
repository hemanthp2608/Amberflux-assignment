from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.session import engine
from .models.base import Base
from .models import models as models_module
from .routers import auth, assignments, submissions

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Amberflux Assignment API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(assignments.router, prefix="/api")
app.include_router(submissions.router, prefix="/api")

@app.get("/")
def root():
    return {"status": "ok", "service": "amberflux-assignment"}
