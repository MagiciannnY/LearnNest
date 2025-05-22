from fastapi import APIRouter
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime, timezone

from app.models.history import HistoryRecord
from app.db import SessionLocal

router = APIRouter()

# 请求体模型
class StartSessionRequest(BaseModel):
    user_id: str
    title: str
    content: str

class SaveMessageRequest(BaseModel):
    session_id: str
    user_id: str
    content: str

# 会话重命名请求体
class RenameRequest(BaseModel):
    session_id: str
    new_title: str

# 创建新会话
@router.post("/start")
def start_chat_session(data: StartSessionRequest):
    session_id = str(uuid4())
    title = data.title.strip().replace("\n", " ")[:20]
    content = data.content
    db = SessionLocal()
    try:
        record = HistoryRecord(
            user_id=data.user_id,
            session_id=session_id,
            title=title,
            content=content
            # created_at=str(int(datetime.now(timezone.utc).timestamp()))
        )
        db.add(record)
        db.commit()
        return {"session_id": session_id, "title": title}
    finally:
        db.close()

# 保存后续消息
@router.post("/save")
def save_message(data: SaveMessageRequest):
    db = SessionLocal()
    try:
        record = HistoryRecord(
            user_id=data.user_id,
            session_id=data.session_id,
            title="",
            content=data.content.strip()
            # created_at=str(int(datetime.now(timezone.utc).timestamp()))
        )
        db.add(record)
        db.commit()
        return {"status": "ok"}
    finally:
        db.close()


# 获取指定用户所有历史会话（分组返回标题和时间）
@router.get("/list/{user_id}")
def get_user_history(user_id: str):
    db = SessionLocal()
    try:
        sessions = (
            db.query(HistoryRecord.session_id, HistoryRecord.title, HistoryRecord.created_at)
            .filter(HistoryRecord.user_id == user_id)
            .group_by(HistoryRecord.session_id, HistoryRecord.title, HistoryRecord.created_at)
            .order_by(HistoryRecord.created_at.desc())
            .all()
        )
        return {"history": [{"session_id": s[0], "title": s[1], "created_at": s[2]} for s in sessions]}
    finally:
        db.close()

# 删除某个会话的所有记录
@router.delete("/delete/{session_id}")
def delete_session(session_id: str):
    db = SessionLocal()
    try:
        db.query(HistoryRecord).filter(HistoryRecord.session_id == session_id).delete()
        db.commit()
        return {"status": "deleted"}
    finally:
        db.close()

# 重命名某个会话的标题
@router.post("/rename")
def rename_session(data: RenameRequest):
    db = SessionLocal()
    try:
        db.query(HistoryRecord).filter(HistoryRecord.session_id == data.session_id).update(
            {"title": data.new_title}
        )
        db.commit()
        return {"status": "renamed"}
    finally:
        db.close()

# 加载聊天记录（分页，默认获取最新20条）
@router.get("/load/{user_id}")
def load_chat_history(user_id: str, limit: int = 20):
    db = SessionLocal()
    try:
        records = (
            db.query(HistoryRecord.session_id, HistoryRecord.title, HistoryRecord.created_at)
            .filter(HistoryRecord.user_id == user_id)
            .order_by(HistoryRecord.created_at.desc())
            .limit(limit)
            .all()
        )
        return {"history": [{"session_id": r.session_id, "title": r.title, "created_at": r.created_at} for r in records]}
    finally:
        db.close()

# 获取指定 session 的完整聊天内容（按时间升序合并）
@router.get("/session/{session_id}")
def get_session_content(session_id: str):
    db = SessionLocal()
    try:
        records = (
            db.query(HistoryRecord.title, HistoryRecord.content)
            .filter(HistoryRecord.session_id == session_id)
            .order_by(HistoryRecord.created_at.asc())
            .all()
        )
        if not records:
            return {"session_id": session_id, "title": "", "content": ""}

        title = records[0].title
        merged_content = "\n".join([r.content for r in records if r.content])
        return {"session_id": session_id, "title": title, "content": merged_content}
    finally:
        db.close()
