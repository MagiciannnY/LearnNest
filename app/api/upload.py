# app/api/upload.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.embedder import get_embeddings
from app.models.chunk import KnowledgeChunk
from app.db import SessionLocal
import uuid
from tempfile import NamedTemporaryFile
from pathlib import Path
from app.services.file_parser import extract_text_from_file
import spacy
from typing import List
# from sklearn.decomposition import PCA
# import numpy as np

nlp = spacy.load("zh_core_web_sm")

router = APIRouter()

# 每个文本块最大字符数
CHUNK_SIZE = 500
# 每批嵌入的最大文本块数
BATCH_SIZE = 32

def smart_chunk_by_sentence(text: str, max_chars: int = CHUNK_SIZE) -> list[str]:
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chars:
            current_chunk += sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# def reduce_embeddings_dim(embeddings: list[list[float]], dim: int = 1024) -> list[list[float]]:
#     X = np.array(embeddings)
#     n_samples, n_features = X.shape
#     dim = min(dim, n_samples, n_features)  # 限制降维维度
#     pca = PCA(n_components=dim)
#     reduced = pca.fit_transform(X)
#     return reduced.tolist()

def insert_chunks_with_add_all(file, chunks, embeddings):
    db = SessionLocal()
    try:
        db_chunks = []
        for i, (chunk_text, embedding_data) in enumerate(zip(chunks, embeddings)):
            db_chunks.append(
                KnowledgeChunk(
                    file_name=file.filename,
                    chunk_index=i,
                    chunk_text=chunk_text,
                    embedding=embedding_data,
                )
            )
        db.add_all(db_chunks)
        db.commit()
        print(f"Successfully inserted {len(chunks)} chunks using add_all.")
    except Exception as e:
        db.rollback()
        print(f"Error during add_all chunk insertion: {e}")
    finally:
        db.close()


@router.post("/")
async def upload_files(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        ext = Path(file.filename).suffix.lower()
        allowed_exts = {".txt", ".md", ".pdf", ".doc", ".docx", ".pptx", ".ppt"}
        if ext not in allowed_exts:
            results.append({"file": file.filename, "status": "❌ 不支持的文件类型"})
            continue
        # 临时保存上传文件
        with NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(await file.read())
            tmp_path = Path(tmp.name)
        
        try:
            file_text = extract_text_from_file(tmp_path, ext[1:])
        finally:
            tmp_path.unlink()
        
        chunks = smart_chunk_by_sentence(file_text, CHUNK_SIZE)
        # 去除空或空白文本块
        chunks = [c.strip() for c in chunks if c.strip()]
        if not chunks:
            results.append({"file": file.filename, "status": "[Logging]文件内容为空或无有效段落，已跳过"})
            continue

        embeddings = []
        for i in range(0, len(chunks), BATCH_SIZE):
            batch = chunks[i:i + BATCH_SIZE]
            batch_embeddings = await get_embeddings(batch)
            embeddings.extend(batch_embeddings)
        # embeddings = reduce_embeddings_dim(embeddings)  # 如启用降维，解注释
        insert_chunks_with_add_all(file, chunks, embeddings)

        results.append({"file": file.filename, "status": f"✅ 成功处理 {len(chunks)} 个文本块"})

    return {"message": results}
