import sys
import asyncio
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import init_db
from routers import auth, users, conversations, groups, websocket


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Signal Clone API", version="1.0.0", lifespan=lifespan)

# Allow configured origins (comma-separated in env) or default to localhost + production frontend URL
allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(conversations.router)
app.include_router(groups.router)
app.include_router(websocket.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
