# app/services/embedder.py

import httpx
from app.config import EMBEDDING_API_KEY, EMBEDDING_API_BASE, EMBEDDING_MODEL

async def get_embeddings(texts: list[str]) -> list[list[float]]:
    headers = {
        "Authorization": f"Bearer {EMBEDDING_API_KEY}",
        "Content-Type": "application/json"
    }

    url = f"{EMBEDDING_API_BASE}/embeddings"

    payload = {
        "model": EMBEDDING_MODEL,
        "input": texts
    }

    # print("🔍 Embedding Request Payload Preview:")
    # print(payload)

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            print("❌ Embedding API returned error:", response.status_code)
            print("Response text:", response.text)
            raise
        data = response.json()

    return [item["embedding"] for item in data["data"]]
