import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bloggingApi.db")
engine = create_engine(DATABASE_URL)

Session = sessionmaker(engine)

Base.metadata.create_all(engine)


def get_db():
    db = Session()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
