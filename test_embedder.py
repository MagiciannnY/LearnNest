# test_embedder.py

import asyncio
from app.services.embedder import get_embeddings

async def main():
    test_texts = [
        "什么是数据库的主键？",
        "外键和主键之间的区别是什么？",
        "什么是范式？"
    ]

    try:
        embeddings = await get_embeddings(test_texts)
        for i, emb in enumerate(embeddings):
            print(f"🔹 文本{i+1} 向量维度: {len(emb)}，前5维: {emb[:5]}")
    except Exception as e:
        print("❌ 调用出错:", e)

if __name__ == "__main__":
    asyncio.run(main())
    