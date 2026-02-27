from app.db.connection import get_pool


async def buscar_numero_por_whatsapp(numero: str) -> dict | None:
    """Busca número e configurações do bot vinculado"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        resultado = await conn.fetchrow(
            """SELECT n.id as numero_id, n.numero, n.instancia,
                      b.id as bot_id, b.prompt, b.temperatura, b.ia_provedor, b.nome as bot_nome
               FROM numeros n
               JOIN bots b ON b.id = n.bot_id
               WHERE n.numero = $1 AND n.ativo = TRUE AND b.ativo = TRUE""",
            numero
        )
    return dict(resultado) if resultado else None

async def cadastrar_numero(numero: str, instancia: str, cliente_id: str = None):
    pool = await get_pool()
    async with pool.acquire() as conn:
        bot = await conn.fetchrow(
            "SELECT id, cliente_id FROM bots WHERE ativo = TRUE LIMIT 1"
        )
        if not bot:
            print("Nenhum bot ativo encontrado!")
            return
        await conn.execute(
            """INSERT INTO numeros (numero, instancia, bot_id, cliente_id, ativo)
               VALUES ($1, $2, $3, $4, TRUE)
               ON CONFLICT (numero) DO NOTHING""",
            numero, instancia, bot["id"], bot["cliente_id"]
        )
        print(f"Número {numero} cadastrado automaticamente!")