import asyncio

from fastapi import FastAPI, Request, Response
from telegram import Update

from bot import build_application

tg_app = build_application()
_lock = asyncio.Lock()
_ready = False


async def ensure_ready():
    global _ready
    if not _ready:
        async with _lock:
            if not _ready:
                await tg_app.initialize()
                _ready = True


app = FastAPI()


@app.get("/")
async def root():
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(request: Request):
    await ensure_ready()
    data = await request.json()
    update = Update.de_json(data, tg_app.bot)
    await tg_app.process_update(update)
    return Response(status_code=200)
