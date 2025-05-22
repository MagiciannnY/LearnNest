# app/main.py

from fastapi import FastAPI
from app.api import upload, ask, wiki, history
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="数据库学习助手",
    description="支持文件上传、语义检索与大模型问答",
    version="0.1.0"
)

# 允许所有跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/upload", tags=["上传"])
app.include_router(ask.router, prefix="/ask", tags=["问答"])
app.include_router(wiki.router, prefix="/wiki", tags=["知识库"])
app.include_router(history.router, prefix='/history', tags=["聊天记录"])