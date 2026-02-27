import httpx
from app.core.config import settings


async def enviar_mensagem(instancia: str, numero: str, texto: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.z-api.io/instances/{instancia}/token/{settings.ZAPI_TOKEN}/send-text",
            headers={"Client-Token": settings.ZAPI_SECURITY_TOKEN},
            json={"phone": numero, "message": texto},
            timeout=15
        )
        print(f"Z-API response: {response.status_code} - {response.text}")