import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker


load_dotenv()
database_url = os.getenv("DATABASE_URL", "sqlite:///url_shortener.db")
engine = create_engine(database_url)


Session = sessionmaker(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
