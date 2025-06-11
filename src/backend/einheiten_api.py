from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel
from typing import List

DATABASE_URL = "mysql+pymysql://userAdmin:xdb_Admin890!@141.56.137.83/share_shop"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class Einheit(Base):
    __tablename__ = "Einheiten"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, nullable=False)
    abkürzung = Column(String(10))

class EinheitRead(BaseModel):
    name: str
    abkürzung: str

    class Config:
        from_attributes = True

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/einheiten", response_model=List[EinheitRead])
def get_einheiten(db: Session = Depends(get_db)):
    einheiten = db.query(Einheit).all()
    return einheiten
