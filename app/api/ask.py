# app/api/ask.py

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from app.services.embedder import get_embeddings
from app.services.llm_qa import stream_deepseek_response
from app.db import SessionLocal
from sqlalchemy.sql import text
from app.config import LLM_MODEL
from sqlalchemy import bindparam
from pgvector.sqlalchemy import Vector
# from sklearn.decomposition import PCA
# import numpy as np

# def reduce_embeddings_dim(embeddings: list[list[float]], dim: int = 1024) -> list[list[float]]:
#     X = np.array(embeddings)
#     n_samples, n_features = X.shape
#     dim = min(dim, n_samples, n_features)
#     pca = PCA(n_components=dim)
#     reduced = pca.fit_transform(X)
#     return reduced.tolist()

router = APIRouter()

@router.post("/")
async def ask_question(request: Request):
    body = await request.json()
    question = body.get("question")
    if not question:
        return {"error": "问题不能为空"}

    # 生成问题向量
    embedding = (await get_embeddings([question]))[0]
    # embedding = reduce_embeddings_dim([embedding])[0]
    # print(embedding)
    # 从数据库中查询 Top-K 相似文本
    db = SessionLocal()
    try:
        query = text("""
            SELECT file_name, chunk_text 
            FROM knowledge_chunks
            ORDER BY embedding <-> :embedding
            LIMIT 7
        """).bindparams(bindparam("embedding", type_=Vector(4096)))
        result = db.execute(query, {"embedding": embedding}).fetchall()
        context_chunks = [f"所属文件: 【{row[0]}】\n ---\n {row[1]}"  for row in result]
        # print(context_chunks)
    finally:
        db.close()

    # 构造 prompt（上下文拼接）
    context = "\n\n".join([f"[参考内容{i+1}]: {chunk}" for i, chunk in enumerate(context_chunks)])
    full_prompt = f"""
请参考以下资料回答用户提出的问题，若有使用请在最后添加引用注释，包含资料所属文件（注意显示时不要重复）；
资料：
```
{context}
```
用户问题：
```
{question}
```
---
注意：
1. 尽量输出富文本形式的内容，便于我前端markdown渲染;
2. 代码块需要在其前后添加```，从而能够单独渲染代码
3. 回答与参考内容之间一定要添加分割线
4. 参考内容使用markdown的注释语法和无序列表
形如：
```
回答部分

--------

> 参考内容：
> - 所属文件1
> - 所属文件2
...
```
"""
    # print(context)
    # 调用 deepseek-chat 并返回流式响应
    return StreamingResponse(
        stream_deepseek_response(full_prompt),
        media_type="text/event-stream"
    )
