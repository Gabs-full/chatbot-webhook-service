from fastapi import APIRouter, BackgroundTasks, Request
from app.services import numero_service, historico_service, ia_service, whatsapp_service
from app.db.connection import get_pool
import json
import uuid

router = APIRouter(prefix="/webhook", tags=["Webhook"])


@router.post("/")
async def receber_webhook(request: Request, background: BackgroundTasks):
    data = await request.json()
    await salvar_webhook_log(data)
    background.add_task(processar_mensagem, data)
    return {"ok": True}


async def salvar_webhook_log(data: dict):
    try:
        pool = await get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """INSERT INTO webhook_logs (id, payload, tipo)
                   VALUES ($1, $2::jsonb, $3)""",
                uuid.uuid4(), json.dumps(data), data.get("type")
            )
            print("Webhook salvo no banco!")
    except Exception as e:
        print(f"Erro ao salvar webhook log: {e}")


def extrair_texto(data: dict) -> str | None:
    return data.get("text", {}).get("message")


def eh_mensagem_valida(data: dict) -> bool:
    try:
        if data.get("fromMe"):
            return False
        return extrair_texto(data) is not None
    except Exception:
        return False


async def processar_mensagem(data: dict):
    try:
        if not eh_mensagem_valida(data):
            return

        contato = data["phone"]
        texto = extrair_texto(data)
        numero_limpo = contato

        config = await numero_service.buscar_numero_por_whatsapp(numero_limpo)
        if not config:
            await numero_service.cadastrar_numero(numero_limpo, data["instanceId"])
            config = await numero_service.buscar_numero_por_whatsapp(numero_limpo)
            if not config:
                print(f"Não foi possível cadastrar {numero_limpo}")
                return

        numero_id = str(config["numero_id"])
        instancia = config["instancia"]

        await historico_service.salvar_mensagem(numero_id, contato, "user", texto)

        historico = await historico_service.buscar_historico(numero_id, contato)

        resposta = await ia_service.gerar_resposta(
            historico=historico,
            prompt=config["prompt"],
            temperatura=config["temperatura"],
            ia_provedor=config["ia_provedor"]
        )

        await historico_service.salvar_mensagem(numero_id, contato, "assistant", resposta)
        await whatsapp_service.enviar_mensagem(instancia, contato, resposta)

    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")