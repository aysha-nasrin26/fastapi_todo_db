from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()
DATABASE_URL = os.getenv("mysql+pymysql://root:aysha_262006@localhost/fastapi")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()