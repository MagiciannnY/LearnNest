# app/services/llm_qa.py

import httpx
import asyncio
from app.config import LLM_API_KEY, LLM_API_BASE, LLM_MODEL

async def stream_deepseek_response(prompt: str):
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }

    url = f"{LLM_API_BASE}/v1/chat/completions"

    payload = {
        "model": LLM_MODEL,
        "stream": True,
        "messages": [
            {"role": "system", "content": "你是一名数据库学习助手，请结合提供的参考资料，简洁、准确地回答用户的问题。"},
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", url, headers=headers, json=payload) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    content = line[len("data: "):]
                    yield f"data: {content}\n\n"
                await asyncio.sleep(0.01)
