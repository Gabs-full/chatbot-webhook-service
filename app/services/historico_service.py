from app.db.connection import get_pool


async def salvar_mensagem(numero_id: str, contato: str, role: str, conteudo: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """INSERT INTO mensagens (numero_id, contato, role, conteudo)
               VALUES ($1, $2, $3, $4)""",
            numero_id, contato, role, conteudo
        )


async def buscar_historico(numero_id: str, contato: str, limite: int = 20) -> list:
    pool = await get_pool()
    async with pool.acquire() as conn:
        mensagens = await conn.fetch(
            """SELECT role, conteudo FROM mensagens
               WHERE numero_id = $1 AND contato = $2
               ORDER BY criado_em DESC
               LIMIT $3""",
            numero_id, contato, limite
        )
    return [{"role": m["role"], "content": m["conteudo"]} for m in reversed(mensagens)]
