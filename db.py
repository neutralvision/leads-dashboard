from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base


engine = create_engine("sqlite:///./leads.db")
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
