from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel
from typing import List
from fastapi import Path
from datetime import date
from typing import Optional
from fastapi import status
from fastapi import HTTPException
from fastapi import Response



DATABASE_URL = "mysql+pymysql://userAdmin:xdb_Admin890!@141.56.137.83/share_shop"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class Nutzer(Base):                                                     # nutzer ----------------------
    __tablename__ = "Nutzer"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    passwort_hash = Column(String, nullable=False)

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

class Einheit(Base):                                            # einheiten ------------------------------------------
    __tablename__ = "Einheiten"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, nullable=False)
    abkürzung = Column(String(10))

class EinheitRead(BaseModel):
    id: int
    name: str
    abkürzung: str

    class Config:
        from_attributes = True

class Produkt(Base):                                                # produkte
    __tablename__ = "Produkt"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, unique=True)
    standard_einheit = Column(Integer, nullable=False)
    

class ProduktRead(BaseModel):
    id: int
    name: str
    standard_einheit: int

    class Config:
        from_attributes = True

class ProduktCreate(BaseModel):
    name: str
    standard_einheit: int



class Liste(Base):                                               # listen ------------------------------------------
    __tablename__ = "Listen"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    ersteller = Column(Integer)  
    datum = Column(String)    

class ListeRead(BaseModel):
    id: int
    name: str
    ersteller: int | None = None
    datum: date | None = None

    class Config:
        from_attributes = True 

class ListeCreate(BaseModel):
    name: str
    ersteller: Optional[int] = None
    datum: Optional[date] = None



class ListeMitglieder(Base):                                            # listeMitglieder --------------------------
    __tablename__ = "ListeMitglieder"
    listen_id = Column(Integer, primary_key=True)
    nutzer_id = Column(Integer, primary_key=True)
    beigetreten_am = Column(String)  

class MitgliedRead(BaseModel):
    nutzer_id: int
    beigetreten_am: date  

class MitgliedCreate(BaseModel):
    listen_id: int
    nutzer_id: int
    beigetreten_am: Optional[str] = None  



class ListeProdukte(Base):                                             # listeProdukte -----------------------
    __tablename__ = "ListeProdukte"
    listen_id = Column(Integer, primary_key=True)
    produkt_id = Column(Integer, primary_key=True)
    hinzugefügt_von = Column(Integer, primary_key=True)
    produkt_menge = Column(String)  
    einheit_id = Column(Integer)
    beschreibung = Column(String)
    
class ProduktInListeRead(BaseModel):
    produkt_id: int
    produkt_menge: float
    einheit_id: int
    hinzugefügt_von: int
    beschreibung: str | None = None

class ProduktInListeCreate(BaseModel):
    produkt_id: int
    produkt_menge: float
    einheit_id: int
    hinzugefügt_von: int
    beschreibung: Optional[str] = None


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/nutzer/by-id", response_model=NutzerRead)                              # Nur ein Nutzer wird zurückgegeben
def get_nutzer_by_id(id: int, db: Session = Depends(get_db)):             #anhand id
    nutzer = db.query(Nutzer).filter(Nutzer.id == id).first()
    if not nutzer:
        raise HTTPException(status_code=404, detail="Nutzer nicht gefunden")
    return nutzer

@app.get("/nutzer/by-email", response_model=NutzerRead)                              # Nur ein Nutzer wird zurückgegeben
def get_nutzer_by_email(email: str, db: Session = Depends(get_db)):         #anhand email
    nutzer = db.query(Nutzer).filter(Nutzer.email == email).first()
    if not nutzer:
        raise HTTPException(status_code=404, detail="Nutzer nicht gefunden")
    return nutzer

@app.post("/nutzer")                                                                # nutzer hinzufügen
def create_nutzer(nutzer: NutzerCreate, db: Session = Depends(get_db)):
    db_nutzer = Nutzer(
        name=nutzer.name,
        email=nutzer.email,
        passwort_hash=nutzer.passwort
    )
    db.add(db_nutzer)
    db.commit()
    db.refresh(db_nutzer)
    return db_nutzer

@app.delete("/nutzer/{nutzer_id}", status_code=status.HTTP_204_NO_CONTENT)                  # nutzer löschen
def delete_nutzer(nutzer_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    nutzer = db.query(Nutzer).filter(Nutzer.id == nutzer_id).first()
    if not nutzer:
        raise HTTPException(status_code=404, detail="Nutzer nicht gefunden")

    db.delete(nutzer)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.get("/einheiten", response_model=List[EinheitRead])  # einheiten ------------------------------------------
def get_einheiten(db: Session = Depends(get_db)):           # get_einheiten liefert die verschiedenen Mengeneinheiten
    einheiten = db.query(Einheit).all()                     # liefert id, name, abkürzung
    return einheiten

@app.get("/einheiten/{einheit_id}")
def get_einheit(einheit_id: int, db: Session = Depends(get_db)):            # get einheit anhand id
    einheit = db.query(Einheit).filter(Einheit.id == einheit_id).first()
    if einheit is None:
        raise HTTPException(status_code=404, detail="Einheit nicht gefunden")
    return einheit

@app.get("/produkte/{produkt_id}", response_model=ProduktRead)
def get_produkt(produkt_id: int = Path(..., gt=0), db: Session = Depends(get_db)):          # produkt liefern anhand produkt_id
    produkt = db.query(Produkt).filter(Produkt.id == produkt_id).first()
    if not produkt:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden")
    return produkt


@app.post("/produkte", response_model=ProduktRead, status_code=status.HTTP_201_CREATED)             #produkt hinzufügen (in db nicht in Liste)
def create_produkt(produkt: ProduktCreate, db: Session = Depends(get_db)):
    # Prüfen, ob Produktname schon existiert
    existing = db.query(Produkt).filter(Produkt.name == produkt.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Produkt mit diesem Namen existiert bereits")

    db_produkt = Produkt(
        name=produkt.name,
        standard_einheit = produkt.standard_einheit
    )
    db.add(db_produkt)
    db.commit()
    db.refresh(db_produkt)
    return db_produkt


@app.delete("/produkte/{produkt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_produkt(produkt_id: int = Path(..., gt=0), db: Session = Depends(get_db)):           # produkt löschen (eigentlich unnötig)
    produkt = db.query(Produkt).filter(Produkt.id == produkt_id).first()
    if not produkt:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden")

    db.delete(produkt)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.get("/listen", response_model=List[ListeRead])       # listen ------------------------------------------
def get_listen(db: Session = Depends(get_db)):              # get_listen liefert alle listen die es gibt
    listen = db.query(Liste).all()                          # liefert listen_id, name, ersteller, date
    return listen

@app.post("/listen", response_model=ListeRead, status_code=status.HTTP_201_CREATED)
def create_liste(liste: ListeCreate, db: Session = Depends(get_db)):            # mit create_liste könnt ihr eine Liste erstellen
    db_liste = Liste(                                                           # einzugeben sind Name, Ersteller, Datum
        name=liste.name,
        ersteller=liste.ersteller,
        datum=liste.datum.isoformat() if liste.datum else None
    )
    db.add(db_liste)
    db.commit()
    db.refresh(db_liste)  
    return db_liste

@app.delete("/listen/{listen_id}", status_code=status.HTTP_204_NO_CONTENT)             # delete_liste löscht eine Liste anhand ihrer listen_id
def delete_liste(listen_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    liste = db.query(Liste).filter(Liste.id == listen_id).first()
    if not liste:
        raise HTTPException(status_code=404, detail="Liste nicht gefunden")

    db.delete(liste)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/listen/{listen_id}/mitglieder", response_model=List[MitgliedRead])                       # listenMitglieder
def get_listen_mitglieder(listen_id: int = Path(..., gt=0), db: Session = Depends(get_db)):         # liefert die Mitglieder der Liste anhand der listen_id
    mitglieder = db.query(ListeMitglieder).filter(ListeMitglieder.listen_id == listen_id).all()
    return mitglieder

@app.post("/listen/{listen_id}/mitglieder", status_code=status.HTTP_201_CREATED)            
def add_mitglied(listen_id: int = Path(..., gt=0), mitglied: MitgliedCreate = Depends(), db: Session = Depends(get_db)):
    liste = db.query(Liste).filter(Liste.id == listen_id).first()
    if not liste:
        raise HTTPException(status_code=404, detail="Liste nicht gefunden")                 # hier kann man einen nutzer zur Liste hinzufügen
                                                                                            # anhand der listen_id, nutzer_id, beigetretem am
    vorhanden = db.query(ListeMitglieder).filter(
        ListeMitglieder.listen_id == listen_id,
        ListeMitglieder.nutzer_id == mitglied.nutzer_id
    ).first()
    if vorhanden:
        raise HTTPException(status_code=400, detail="Mitglied ist bereits in der Liste")

    neues_mitglied = ListeMitglieder(
        listen_id=listen_id,
        nutzer_id=mitglied.nutzer_id,
        beigetreten_am=mitglied.beigetreten_am or date.today().isoformat()
    )
    db.add(neues_mitglied)
    db.commit()
    return {"message": "Mitglied hinzugefügt"}

@app.delete("/listen/{listen_id}/mitglieder/{nutzer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mitglied(
    listen_id: int = Path(..., gt=0),
    nutzer_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)                                               # hier kann ein Mitglied aus der Liste gelöscht werden
):                                                                              # anhand der listen_id, nutzer_id
    eintrag = db.query(ListeMitglieder).filter(
        ListeMitglieder.listen_id == listen_id,
        ListeMitglieder.nutzer_id == nutzer_id
    ).first()

    if not eintrag:
        raise HTTPException(status_code=404, detail="Mitglied nicht in der Liste gefunden")

    db.delete(eintrag)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.get("/listen/{listen_id}/produkte", response_model=List[ProduktInListeRead])                   # listenProdukte
def get_listen_produkte(listen_id: int = Path(..., gt=0), db: Session = Depends(get_db)):           # liefert die Produkte einer Liste anhand der listen_id
    produkte = db.query(ListeProdukte).filter(ListeProdukte.listen_id == listen_id).all()
    return produkte

@app.post("/listen/{listen_id}/produkte", status_code=status.HTTP_201_CREATED)
def add_listen_produkt(
    listen_id: int = Path(..., gt=0),
    produkt: ProduktInListeCreate = Depends(),
    db: Session = Depends(get_db)
):
    liste = db.query(Liste).filter(Liste.id == listen_id).first()
    if not liste:
        raise HTTPException(status_code=404, detail="Liste nicht gefunden")

    einheit = db.query(Einheit).filter(Einheit.id == produkt.einheit_id).first()
    if not einheit:
        raise HTTPException(status_code=400, detail="Ungültige Einheit (einheit_id)")

    vorhanden = db.query(ListeProdukte).filter(
        ListeProdukte.listen_id == listen_id,
        ListeProdukte.produkt_id == produkt.produkt_id,
        ListeProdukte.hinzugefügt_von == produkt.hinzugefügt_von
    ).first()

    if vorhanden:
        vorhandene_menge = float(vorhanden.produkt_menge)
        neue_menge = vorhandene_menge + float(produkt.produkt_menge)
        vorhanden.produkt_menge = str(neue_menge)
        db.commit()
        return {"message": "Produktmenge aktualisiert"}

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

    return {"message": "Produkt erfolgreich hinzugefügt"}


@app.delete("/listen/{listen_id}/produkte/{produkt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_produkt_aus_liste(
    listen_id: int = Path(..., gt=0),
    produkt_id: int = Path(..., gt=0),
    hinzugefügt_von: int = None,                                                                # hier wird ein produkt aus der liste gelöscht
    db: Session = Depends(get_db)
):
    if hinzugefügt_von is None:
        raise HTTPException(status_code=400, detail="Parameter 'hinzugefügt_von' ist erforderlich")

    eintrag = db.query(ListeProdukte).filter(
        ListeProdukte.listen_id == listen_id,
        ListeProdukte.produkt_id == produkt_id,
        ListeProdukte.hinzugefügt_von == hinzugefügt_von
    ).first()

    if not eintrag:
        raise HTTPException(status_code=404, detail="Produkt in Liste nicht gefunden")

    db.delete(eintrag)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



