# init_db.py

from app.db import engine, Base
from app.models import chunk, history

if __name__ == "__main__":
    print("Creating tables in PostgreSQL...")
    Base.metadata.create_all(bind=engine)
    print("Done.")