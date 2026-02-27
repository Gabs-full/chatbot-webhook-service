from fastapi import FastAPI
from app.routers.webhook import router as webhook_router
from app.db.connection import get_pool, close_pool

app = FastAPI(
    title="Chatbot Webhook Service",
    description="Microserviço que recebe mensagens do WhatsApp e responde com IA",
    version="1.0.0"
)

app.include_router(webhook_router)


@app.on_event("startup")
async def startup():
    await get_pool()


@app.on_event("shutdown")
async def shutdown():
    await close_pool()


@app.get("/health")
async def health():
    return {"status": "ok", "service": "chatbot-webhook-service"}
