from fastapi import FastAPI, Depends, Path, status, HTTPException, Response
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

DATABASE_URL = "mysql+pymysql://userAdmin:xdb_Admin890!@141.56.137.83/share_shop"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# --- Datenbankmodelle ---

class Nutzer(Base):                                                    
    __tablename__ = "Nutzer"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    passwort_hash = Column(String, nullable=False)

class Einheit(Base):                                            
    __tablename__ = "Einheiten"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, nullable=False)
    abkürzung = Column(String(10))

class Produkt(Base):                                                
    __tablename__ = "Produkt"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, unique=True)
    standard_einheit = Column(Integer, ForeignKey('Einheiten.id'), nullable=False)

class Liste(Base):                                               
    __tablename__ = "Listen"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    ersteller = Column(Integer, ForeignKey('Nutzer.id', ondelete='SET NULL'), nullable=True)
    datum = Column(String)    

class ListeMitglieder(Base):                                            
    __tablename__ = "ListeMitglieder"
    listen_id = Column(Integer, primary_key=True)
    nutzer_id = Column(Integer, primary_key=True)
    beigetreten_am = Column(String)  

from sqlalchemy import ForeignKey

class ListeProdukte(Base):
    __tablename__ = "ListeProdukte"
    listen_id = Column(Integer, ForeignKey('Listen.id'), primary_key=True)
    produkt_id = Column(Integer, ForeignKey('Produkt.id'), primary_key=True)
    hinzugefügt_von = Column(Integer, ForeignKey('Nutzer.id', ondelete='SET NULL'), nullable=True)
    produkt_menge = Column(String)
    einheit_id = Column(Integer)
    beschreibung = Column(String)





# --- Pydantic-Modelle ---

class NutzerRead(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class NutzerCreate(BaseModel):
    name: str
    email: str
    passwort: str

class EinheitRead(BaseModel):
    id: int
    name: str
    abkürzung: Optional[str] = None

    class Config:
        from_attributes = True

class ProduktRead(BaseModel):
    id: int
    name: str
    standard_einheit: int

    class Config:
        from_attributes = True

class ProduktCreate(BaseModel):
    name: str
    standard_einheit: int

class ListeRead(BaseModel):
    id: int
    name: str
    ersteller: Optional[int] = None
    datum: Optional[date] = None

    class Config:
        from_attributes = True 

class ListeCreate(BaseModel):
    name: str
    ersteller: Optional[int] = None
    datum: Optional[date] = None

class MitgliedRead(BaseModel):
    nutzer_id: int
    beigetreten_am: date  

    class Config:
        from_attributes = True

class MitgliedCreate(BaseModel):
    nutzer_id: int
    beigetreten_am: Optional[str] = None

class ProduktInListeRead(BaseModel):
    produkt_id: int
    produkt_menge: float
    einheit_id: int
    hinzugefügt_von: int
    beschreibung: Optional[str] = None

    class Config:
        from_attributes = True

class ProduktInListeCreate(BaseModel):
    produkt_id: int
    produkt_menge: float
    einheit_id: int
    hinzugefügt_von: int
    beschreibung: Optional[str] = None


# --- FastAPI-App ---

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Nutzer ---

@app.get("/nutzer/by-id", response_model=NutzerRead)
def get_nutzer_by_id(id: int, db: Session = Depends(get_db)):
    nutzer = db.query(Nutzer).filter(Nutzer.id == id).first()
    if not nutzer:
        raise HTTPException(status_code=404, detail="Nutzer nicht gefunden")
    return nutzer

@app.get("/nutzer/by-email", response_model=NutzerRead)
def get_nutzer_by_email(email: str, db: Session = Depends(get_db)):
    nutzer = db.query(Nutzer).filter(Nutzer.email == email).first()
    if not nutzer:
        raise HTTPException(status_code=404, detail="Nutzer nicht gefunden")
    return nutzer

@app.post("/nutzer", response_model=NutzerRead, status_code=status.HTTP_201_CREATED)
def create_nutzer(nutzer: NutzerCreate, db: Session = Depends(get_db)):
    db_nutzer = Nutzer(
        name=nutzer.name,
        email=nutzer.email,
        passwort_hash=nutzer.passwort  # ACHTUNG: Passwort sollte gehashed werden
    )
    db.add(db_nutzer)
    db.commit()
    db.refresh(db_nutzer)
    return db_nutzer

@app.delete("/nutzer/{nutzer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_nutzer(nutzer_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    nutzer = db.query(Nutzer).filter(Nutzer.id == nutzer_id).first()
    if not nutzer:
        raise HTTPException(status_code=404, detail="Nutzer nicht gefunden")

    db.delete(nutzer)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# --- Einheiten ---

@app.get("/einheiten", response_model=List[EinheitRead])
def get_einheiten(db: Session = Depends(get_db)):
    einheiten = db.query(Einheit).all()
    return einheiten

@app.get("/einheiten/{einheit_id}", response_model=EinheitRead)
def get_einheit(einheit_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    einheit = db.query(Einheit).filter(Einheit.id == einheit_id).first()
    if einheit is None:
        raise HTTPException(status_code=404, detail="Einheit nicht gefunden")
    return einheit


# --- Produkte ---

@app.get("/produkte/{produkt_id}", response_model=ProduktRead)
def get_produkt(produkt_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    produkt = db.query(Produkt).filter(Produkt.id == produkt_id).first()
    if not produkt:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden")
    return produkt

@app.post("/produkte", response_model=ProduktRead, status_code=status.HTTP_201_CREATED)
def create_produkt(produkt: ProduktCreate, db: Session = Depends(get_db)):
    existing = db.query(Produkt).filter(Produkt.name == produkt.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Produkt mit diesem Namen existiert bereits")

    db_produkt = Produkt(
        name=produkt.name,
        standard_einheit=produkt.standard_einheit
    )
    db.add(db_produkt)
    db.commit()
    db.refresh(db_produkt)
    return db_produkt

@app.delete("/produkte/{produkt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_produkt(produkt_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    produkt = db.query(Produkt).filter(Produkt.id == produkt_id).first()
    if not produkt:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden")
    db.delete(produkt)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --- Listen ---

@app.get("/listen", response_model=List[ListeRead])
def get_listen(db: Session = Depends(get_db)):
    listen = db.query(Liste).all()
    return listen

@app.post("/listen", response_model=ListeRead, status_code=status.HTTP_201_CREATED)
def create_liste(liste: ListeCreate, db: Session = Depends(get_db)):
   
    # Prüfen, ob Nutzer mit hinzugefügt_von existiert
    existierender_nutzer = db.query(Nutzer).filter_by(id=liste.ersteller).first()
    if not existierender_nutzer:
        raise HTTPException(status_code=400, detail="Der Nutzer zum Hinzufügen wurde nicht gefunden")
   
    db_liste = Liste(
        name=liste.name,
        ersteller=liste.ersteller,
        datum=liste.datum.isoformat() if liste.datum else None
    )
    db.add(db_liste)
    db.commit()
    db.refresh(db_liste)
   
   
    # Ersteller automatisch als Mitglied hinzufügen
    neues_mitglied = ListeMitglieder(
        listen_id=db_liste.id,
        nutzer_id=liste.ersteller,
        beigetreten_am=date.today() # oder liste.datum, je nach gewünschter Logik
    )
    db.add(neues_mitglied)
    db.commit()

    return db_liste
 

@app.delete("/listen/{listen_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_liste(listen_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    liste = db.query(Liste).filter(Liste.id == listen_id).first()
    if not liste:
        raise HTTPException(status_code=404, detail="Liste nicht gefunden")
    db.delete(liste)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --- Mitglieder in Listen ---

@app.get("/listen/{listen_id}/mitglieder", response_model=List[MitgliedRead])
def get_mitglieder(listen_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    mitglieder = db.query(ListeMitglieder).filter(ListeMitglieder.listen_id == listen_id).all()
    return mitglieder

@app.post("/listen/{listen_id}/mitglieder", response_model=MitgliedRead, status_code=status.HTTP_201_CREATED)
def add_mitglied(listen_id: int = Path(..., gt=0), mitglied: MitgliedCreate = None, db: Session = Depends(get_db)):
    if mitglied is None:
        raise HTTPException(status_code=400, detail="Mitgliedsdaten fehlen")

    neues_mitglied = ListeMitglieder(
        listen_id=listen_id,
        nutzer_id=mitglied.nutzer_id,
        beigetreten_am=mitglied.beigetreten_am
    )
    db.add(neues_mitglied)
    db.commit()
    db.refresh(neues_mitglied)
    return neues_mitglied

@app.delete("/listen/{listen_id}/mitglieder/{nutzer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mitglied(listen_id: int = Path(..., gt=0), nutzer_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    eintrag = db.query(ListeMitglieder).filter(
        ListeMitglieder.listen_id == listen_id,
        ListeMitglieder.nutzer_id == nutzer_id
    ).first()
    if not eintrag:
        raise HTTPException(status_code=404, detail="Mitglied nicht gefunden")
    db.delete(eintrag)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --- Produkte in Listen ---

@app.get("/listen/{listen_id}/produkte", response_model=List[ProduktInListeRead])
def get_produkte_in_liste(listen_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    produkte = db.query(ListeProdukte).filter(ListeProdukte.listen_id == listen_id).all()
    return produkte

@app.post("/listen/{listen_id}/produkte", response_model=ProduktInListeRead, status_code=status.HTTP_201_CREATED)
def add_produkt_in_liste(listen_id: int = Path(..., gt=0), produkt: ProduktInListeCreate = None, db: Session = Depends(get_db)):
    if produkt is None:
        raise HTTPException(status_code=400, detail="Produktdaten fehlen")

    # Prüfen, ob Produkt mit produkt.produkt_id in DB existiert
    existierendes_produkt = db.query(Produkt).filter_by(id=produkt.produkt_id).first()
    if not existierendes_produkt:
        raise HTTPException(status_code=400, detail="Das Produkt muss erst in der DB hinzugefügt werden")

    # Prüfen, ob Nutzer mit hinzugefügt_von existiert
    existierender_nutzer = db.query(Nutzer).filter_by(id=produkt.hinzugefügt_von).first()
    if not existierender_nutzer:
        raise HTTPException(status_code=400, detail="Der Nutzer zum Hinzufügen wurde nicht gefunden")

    vorhandenes_produkt = db.query(ListeProdukte).filter_by(listen_id=listen_id, produkt_id=produkt.produkt_id).first()

    if vorhandenes_produkt:
        # Prüfen, ob die Mengeneinheit übereinstimmt
        if vorhandenes_produkt.einheit_id != produkt.einheit_id:
            raise HTTPException(
                status_code=400,
                detail=f"Mengeneinheit stimmt nicht überein (vorhanden: {vorhandenes_produkt.einheit_id}, übergeben: {produkt.einheit_id})"
            )

        try:
            aktuelle_menge = float(vorhandenes_produkt.produkt_menge)
            neue_menge = float(produkt.produkt_menge)
        except ValueError:
            raise HTTPException(status_code=400, detail="Ungültiges Mengenformat")

        summe = aktuelle_menge + neue_menge
        vorhandenes_produkt.produkt_menge = str(summe)

        db.commit()
        db.refresh(vorhandenes_produkt)
        return vorhandenes_produkt

    else:
        neues_produkt = ListeProdukte(
            listen_id=listen_id,
            produkt_id=produkt.produkt_id,
            produkt_menge=str(produkt.produkt_menge),
            einheit_id=produkt.einheit_id,
            hinzugefügt_von=produkt.hinzugefügt_von,
            beschreibung=produkt.beschreibung
        )
        db.add(neues_produkt)
        db.commit()
        db.refresh(neues_produkt)
        return neues_produkt
    
@app.delete("/listen/{listen_id}/produkte/{produkt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_produkt_in_liste(listen_id: int = Path(..., gt=0), produkt_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    eintrag = db.query(ListeProdukte).filter(
        ListeProdukte.listen_id == listen_id,
        ListeProdukte.produkt_id == produkt_id
    ).first()
    if not eintrag:
        raise HTTPException(status_code=404, detail="Produkt in Liste nicht gefunden")
    db.delete(eintrag)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
