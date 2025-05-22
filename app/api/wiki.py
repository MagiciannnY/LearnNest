# app/api/wiki.py

from fastapi import APIRouter
from sqlalchemy import func
from fastapi.responses import JSONResponse
from app.db import SessionLocal
from app.models.chunk import KnowledgeChunk

router = APIRouter()

@router.get("/files")
def get_uploaded_files():
    db = SessionLocal()
    try:
        # 验证模型字段存在性
        if not hasattr(KnowledgeChunk, 'file_name'):
            raise AttributeError("KnowledgeChunk模型缺少file_name字段")
            
        # 使用GROUP BY替代DISTINCT并获取最新上传时间
        subquery = (
            db.query(
                KnowledgeChunk.file_name,
                func.max(KnowledgeChunk.upload_time).label('latest_upload')
            )
            .group_by(KnowledgeChunk.file_name)
            .subquery()
        )

        query = (
            db.query(subquery.c.file_name)
            .order_by(subquery.c.latest_upload.desc())
        )
        
        file_names = query.all()
        # print(file_names)
        # for file in file_names:
        #     print(file)
        
        # 严格类型过滤
        clean_files = [str(f[0]) for f in file_names if f and f[0]]
        # print(f"清洗后文件列表: {clean_files}")
        
        return JSONResponse(
            content={"files": clean_files},
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        
    except Exception as e:
        print(f"API错误: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "文件获取失败"},
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        
    finally:
        db.close()
