import logging

from fastapi import FastAPI, Request, Response
from telegram import Update

from bot import build_application

logger = logging.getLogger(__name__)

tg_app = build_application()
app = FastAPI()


@app.get("/")
async def root():
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        async with tg_app:
            update = Update.de_json(data, tg_app.bot)
            await tg_app.process_update(update)
    except Exception:
        logger.exception("webhook xatosi")
    return Response(status_code=200)
