from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from app.core.config import settings


async def gerar_resposta(historico: list, prompt: str, temperatura: float, ia_provedor: str) -> str:
    if ia_provedor == "claude":
        return await usar_claude(historico, prompt, temperatura)
    return await usar_openai(historico, prompt, temperatura)


async def usar_openai(historico: list, prompt: str, temperatura: float) -> str:
    client = AsyncOpenAI(api_key=settings.OPENAI_KEY)
    messages = [{"role": "system", "content": prompt}] + historico

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=temperatura
    )
    return response.choices[0].message.content


async def usar_claude(historico: list, prompt: str, temperatura: float) -> str:
    client = AsyncAnthropic(api_key=settings.CLAUDE_KEY)

    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=prompt,
        messages=historico,
        temperature=temperatura
    )
    return response.content[0].text
