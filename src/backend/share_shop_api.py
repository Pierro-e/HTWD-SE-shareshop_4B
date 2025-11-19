import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Path, status, HTTPException, Response, Body, Query
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric, Date, DateTime, func, or_
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy.sql import case
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import re


load_dotenv()
DATABASE_URL = f"mysql+pymysql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}/{os.environ['DB_NAME']}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=True)
Base = declarative_base()

# --- Datenbankmodelle ---


class Nutzer(Base):
    __tablename__ = "Nutzer"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    passwort_hash = Column(String, nullable=False)
    theme = Column(Integer, default=0)
    color = Column(Integer, default=0)


class Einheit(Base):
    __tablename__ = "Einheiten"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, nullable=False)
    abkürzung = Column(String(10), unique=True, nullable=False)


class Produkt(Base):
    __tablename__ = "Produkt"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, unique=True)


class Liste(Base):
    __tablename__ = "Listen"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    ersteller = Column(Integer, ForeignKey('Nutzer.id', ondelete='SET NULL'), nullable=True)
    datum = Column(Date)


class ListeMitglieder(Base):
    __tablename__ = "ListeMitglieder"
    listen_id = Column(Integer, ForeignKey('Listen.id', ondelete='CASCADE'), primary_key=True)
    nutzer_id = Column(Integer, ForeignKey('Nutzer.id', ondelete='Cascade'), primary_key=True)
    beigetreten_am = Column(Date)


class ListeProdukte(Base):
    __tablename__ = "ListeProdukte"
    listen_id = Column(Integer, ForeignKey('Listen.id', ondelete='Cascade'), primary_key=True)
    produkt_id = Column(Integer, ForeignKey('Produkt.id'), primary_key=True)
    hinzugefügt_von = Column(Integer, ForeignKey('Nutzer.id', ondelete='SET NULL'), nullable=True)
    produkt_menge = Column(Numeric(10, 2), nullable=True)
    einheit_id = Column(Integer, nullable=True)
    beschreibung = Column(String, nullable=True)


class FavProdukte(Base):
    __tablename__ = "fav_Produkte"
    nutzer_id = Column(Integer, ForeignKey("Nutzer.id", ondelete="CASCADE"), primary_key=True)
    produkt_id = Column(Integer, ForeignKey("Produkt.id"), primary_key=True)
    menge = Column(Numeric(10, 2), nullable=True)
    einheit_id = Column(Integer, ForeignKey("Einheiten.id"), nullable=True)
    beschreibung = Column(String, nullable=True)


class Bedarfsvorhersage(Base):
    __tablename__ = "Bedarfsvorhersage"
    nutzer_id = Column(Integer, ForeignKey("Nutzer.id", ondelete="CASCADE"), primary_key=True )
    produkt_id = Column(Integer, ForeignKey("Produkt.id"), primary_key=True)
    counter = Column(Numeric(10, 2), default=0.00)
    last_update = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

class Einkaufsarchiv(Base):
    __tablename__ = "Einkaufsarchiv"
    einkauf_id = Column(Integer, primary_key=True, nullable=False)
    listen_id = Column(Integer, ForeignKey("Listen.id", ondelete="CASCADE"), nullable=False)
    eingekauft_von = Column(Integer, ForeignKey("Nutzer.id", ondelete="SET NULL"), nullable=True)
    eingekauft_am = Column(DateTime, server_default=func.now(), nullable=False)  
    gesamtpreis = Column(Numeric(10, 2), nullable=True)

class EingekaufteProdukte(Base):
    __tablename__ = "eingekaufte_Produkte"
    id = Column(Integer, primary_key=True, autoincrement=True)
    einkauf_id = Column(Integer, ForeignKey("Einkaufsarchiv.einkauf_id", ondelete="CASCADE"), nullable=False)
    produkt_id = Column(Integer, ForeignKey("Produkt.id"), nullable=False)
    produkt_menge = Column(Numeric(10, 2), nullable=True)
    einheit_id = Column(Integer, ForeignKey("Einheiten.id"), nullable=True)
    produkt_preis = Column(Numeric(10, 2), nullable=True)
    hinzugefuegt_von = Column(Integer, ForeignKey("Nutzer.id", ondelete="SET NULL"), nullable=True)
    beschreibung = Column(String, nullable=True)



# --- Pydantic-Modelle ---
class NameBasis(BaseModel):
    """Kapselt die Validierung und Bereinigung für den Namen (z.B. Nutzer, Produkte)."""
    
    # Der Feldname muss 'name' sein, damit der @field_validator in dieser Klasse funktioniert.
    name: str = Field(min_length=1)

    # Der Validator, der in der Basisklasse bleiben muss:
    @field_validator('name', mode='after') 
    @classmethod
    def validate_name_content(cls, value):
        # Ruft die externe Hilfsfunktion auf
        if not contains_at_least_one_letter(value):
            raise ValueError('Der Name muss mindestens einen Buchstaben enthalten (A-Z).')
        return value.strip()
    
class NutzerRead(BaseModel):
    id: int
    email: str
    name: str
    passwort_hash: str
    theme: int
    color: int

    class Config:
        from_attributes = True

class NutzerCreate(NameBasis):
    email: EmailStr
    passwort_hash: str
    pass


class EinheitRead(BaseModel):
    id: int
    name: str
    abkürzung: Optional[str] = None

    class Config:
        from_attributes = True

class ProduktRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class ProduktCreate(NameBasis):
    pass

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
    listen_id: int
    nutzer_id: int
    beigetreten_am: date

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str
    passwort: str


class ProduktInListeRead(BaseModel):
    produkt_id: int
    produkt_name: Optional[str] = None
    produkt_menge: Optional[Decimal] = None
    einheit_id: Optional[int] = None
    einheit_abk: Optional[str] = None
    hinzugefügt_von: int
    beschreibung: Optional[str] = None

    class Config:
        from_attributes = True


class ProduktInListeCreate(BaseModel):
    listen_id: int
    produkt_id: int
    hinzugefügt_von: int


class ProduktInListeUpdate(BaseModel):
    produkt_menge: Decimal
    einheit_id: int
    beschreibung: Optional[str] = None


class ListeDatumUpdate(BaseModel):
    datum: date


class ProduktDeleteRequest(BaseModel):
    hinzugefügt_von: int


class FavProdukteRead(BaseModel):
    nutzer_id: int
    produkt_id: int
    produkt_name: Optional[str] = None
    menge: Optional[Decimal] = None
    einheit_id: Optional[int] = None
    einheit_abk: Optional[str] = None
    beschreibung: Optional[str] = None
    class Config:
        from_attributes = True


class FavProdukteCreate(BaseModel):
    produkt_id: int
    menge: Optional[Decimal] = None
    einheit_id: Optional[int] = None
    beschreibung: Optional[str] = None

class FavProdukteUpdate(BaseModel):
    menge: Optional[Decimal] = None
    einheit_id: Optional[int] = None
    beschreibung: Optional[str] = None  

class BedarfsvorhersageRead(BaseModel):
    nutzer_id: int
    produkt_id: int
    produkt_name: Optional[str] = None
    counter: Decimal
    last_update: Optional[datetime] = None
    class Config:
        from_attributes = True

class BedarfvorhersageCreate(BaseModel):
    produkt_id: int
    counter: Decimal

class PasswortÄndern(BaseModel):
    neues_passwort: str

class NameAendern(NameBasis):

    # Die Klasse erbt das Feld 'name' und dessen Validierung. gilt für 'NutzerCreate' und 'ProduktCreate'.
    # Wir überschreiben das Feld nur, wenn es einen anderen Feldnamen braucht,
    # aber hier verwenden wir das geerbte 'name'-Feld direkt.
    pass

class EmailAendern(BaseModel):
    neue_email: str

class EinkaufsarchivRead(BaseModel):
    einkauf_id: int
    listen_id: int
    listen_name: Optional[str] = None
    eingekauft_von: Optional[int] = None
    einkaeufer_name: Optional[str] = None
    eingekauft_am: Optional[date] = None  
    gesamtpreis: Optional[Decimal] = None

    class Config:
        from_attributes = True

class EinkaufsarchivCreate(BaseModel):
    eingekauft_von: Optional[int] = None
    gesamtpreis: Optional[Decimal] = None

class eingekaufteProdukteRead(BaseModel):
    einkauf_id: int
    produkt_id: int
    produkt_name: Optional[str] = None
    produkt_menge: Optional[Decimal] = None
    einheit_id: Optional[int] = None
    einheit_abk: Optional[str] = None
    produkt_preis: Optional[Decimal] = None
    hinzugefuegt_von: Optional[int] = None
    hinzufueger_name: Optional[str] = None
    beschreibung: Optional[str] = None

    class Config:
        from_attributes = True

class eingekaufteProdukteCreate(BaseModel):
    produkt_id: int
    produkt_menge: Optional[Decimal] = None
    einheit_id: Optional[int] = None
    produkt_preis: Optional[Decimal] = None
    hinzugefuegt_von: Optional[int] = None
    beschreibung: Optional[str] = None




# --- Hilfsfunktion zur Buchstabenprüfung ---
def contains_at_least_one_letter(s: str) -> bool:
    """
    Prüft, ob der übergebene String mindestens einen Buchstaben enthält (A-Z, äöü).

    Anwendung: Wird im @field_validator des Pydantic-Modells 'NutzerCreate' 
                für das Feld 'name' verwendet, um reine Zahlen oder Symbole 
                (z.B. '123' oder '!!!') abzufangen.

    Rückgabe: True, wenn ein Buchstabe gefunden wird, sonst False.
    """
    return any(c.isalpha() or c in 'äöüÄÖÜß' for c in s)
# --- FastAPI-App ---

app = FastAPI()

# CORS Middleware hinzufügen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def start():
    return {"message": "API für share_shop DB"}

# --- Nutzer ---


@app.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    # Nutzer mit E-Mail suchen
    nutzer = db.query(Nutzer).filter(func.lower(Nutzer.email)
                                     == func.lower(login_data.email)).first()
    if not nutzer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Falsche Zugangsdaten")

    # Passwort prüfen - hier Beispiel: einfacher Vergleich
    # TODO: In Produktion: Passwort mit bcrypt oder ähnlichem prüfen
    if nutzer.passwort_hash != login_data.passwort:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Falsche Zugangsdaten")

    # Falls alles stimmt: Nutzerdaten zurückgeben (ohne passwort_hash)
    return {
        "id": nutzer.id,
        "email": nutzer.email,
        "name": nutzer.name,
        "theme": nutzer.theme,
        "color": nutzer.color
    }


@app.get("/nutzer", response_model=List[NutzerRead])
def get_nutzer_all(db: Session = Depends(get_db)):
    nutzer = db.query(Nutzer).all()
    return nutzer


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


@app.post("/nutzer_create", response_model=NutzerRead, status_code=status.HTTP_201_CREATED)
def create_nutzer(nutzer: NutzerCreate, db: Session = Depends(get_db)):

    vorhanden = db.query(Nutzer).filter(Nutzer.email == nutzer.email).first()

    if vorhanden:
        raise HTTPException(
            status_code=400, detail="Nutzeremail existiert bereits")
    else:
        db_nutzer = Nutzer(
            email=nutzer.email,
            name=nutzer.name,
            passwort_hash=nutzer.passwort_hash
        )
        db.add(db_nutzer)
        db.commit()
        db.refresh(db_nutzer)
        return db_nutzer


@app.delete("/nutzer_delete/{nutzer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_nutzer(nutzer_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    nutzer = db.query(Nutzer).filter(Nutzer.id == nutzer_id).first()
    if not nutzer:
        raise HTTPException(status_code=404, detail="Nutzer nicht gefunden")

    db.delete(nutzer)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/nutzer_change/{nutzer_id}/passwort", status_code=status.HTTP_200_OK)
def change_passwort(nutzer_id: int, passwort: PasswortÄndern, db: Session = Depends(get_db)):
    nutzer = db.query(Nutzer).filter(Nutzer.id == nutzer_id).first()

    if not nutzer:
        raise HTTPException(status_code=404, detail="Nutzer nicht gefunden")

    nutzer.passwort_hash = passwort.neues_passwort
    db.commit()
    db.refresh(nutzer)

    return nutzer


@app.put("/nutzer_change/{nutzer_id}/name", status_code=status.HTTP_200_OK)
def change_name(nutzer_id: int, name_data: NameAendern, db: Session = Depends(get_db)):
    nutzer = db.query(Nutzer).filter(Nutzer.id == nutzer_id).first()

    if not nutzer:
        raise HTTPException(status_code=404, detail="Nutzer nicht gefunden")
    # Name validiert durch Pydantic im NameAendern Modell
    nutzer.name = name_data.name
    db.commit()
    db.refresh(nutzer)

    return nutzer

@app.put("/nutzer_change/{nutzer_id}/email", status_code=status.HTTP_200_OK)
def change_email(nutzer_id: int, email: EmailAendern, db: Session = Depends(get_db)):
    nutzer = db.query(Nutzer).filter(Nutzer.id == nutzer_id).first()

    if not nutzer:
        raise HTTPException(status_code=404, detail="Nutzer nicht gefunden")

    vorhandener_nutzer = db.query(Nutzer).filter(Nutzer.email == email.neue_email).first()
    if vorhandener_nutzer:
        raise HTTPException(status_code=400, detail="E-Mail ist bereits vergeben")

    nutzer.email = email.neue_email
    db.commit()
    db.refresh(nutzer)

    return nutzer   


@app.get("/nutzer/{nutzer_id}/listen", response_model=List[ListeRead])
def get_listen_by_nutzer(nutzer_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    listen = (
        db.query(Liste)
        .join(ListeMitglieder)
        .filter(ListeMitglieder.nutzer_id == nutzer_id)
        .all()
    )
    if not listen:
        raise HTTPException(
            status_code=404, detail="Keine Listen für diesen Nutzer gefunden")
    return listen




# -- Funktion, in der die Ansichtseinstellungen des Nutzer geändert werden können ---
@app.put("/nutzer_change/{nutzer_id}/theme_color", status_code=status.HTTP_200_OK)
def change_theme_color(
    nutzer_id: int = Path(..., gt=0),                   # muss >0 sein
    theme: int = Body(..., ge=0, le=2),                 # theme 0–2  ge = greater equal, le = less equal
    color: int = Body(..., ge=0, le=4),                 # color 0–4
    db: Session = Depends(get_db)
):
    # Prüfen, ob der Nutzer existiert
    nutzer = db.query(Nutzer).filter(Nutzer.id == nutzer_id).first()
    if not nutzer:
        raise HTTPException(status_code=404, detail="Nutzer nicht gefunden")

    # Werte aktualisieren
    nutzer.theme = theme
    nutzer.color = color
    db.commit()
    db.refresh(nutzer)

    return nutzer


# --- Einheiten ---

@app.get("/einheiten", response_model=List[EinheitRead])
def get_einheiten_all(db: Session = Depends(get_db)):
    einheiten = db.query(Einheit).all()
    return einheiten


@app.get("/einheiten/{einheit_id}", response_model=EinheitRead)
def get_einheit_by_id(einheit_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    einheit = db.query(Einheit).filter(Einheit.id == einheit_id).first()
    if einheit is None:
        raise HTTPException(status_code=404, detail="Einheit nicht gefunden")
    return einheit


# --- Produkte ---
@app.get("/produkte/", response_model=List[ProduktRead])
def get_produkte_all(db: Session = Depends(get_db)):
    produkte = db.query(Produkt).all()

    return produkte


@app.get("/produkte/by-id/{produkt_id}", response_model=ProduktRead)
def get_produkt_by_id(produkt_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    produkt = db.query(Produkt).filter(Produkt.id == produkt_id).first()
    if not produkt:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden")
    return produkt


@app.get("/produkte/by-name/{produkt_name}", response_model=ProduktRead)
def get_produkt_by_name(produkt_name: str = Path(...), db: Session = Depends(get_db)):
    produkt = db.query(Produkt).filter(func.lower(
        Produkt.name) == produkt_name.lower()).first()
    if not produkt:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden")
    return produkt


@app.post("/produkte_create", response_model=ProduktRead, status_code=status.HTTP_201_CREATED)
def create_produkt(produkt: ProduktCreate, db: Session = Depends(get_db)):

    # product.name ist bereits validiert und formatiert

    # Prüfen, ob Produkt mit dem formatierten Namen schon existiert
    existing = db.query(Produkt).filter(func.lower(
        Produkt.name) == produkt.name.lower()).first()
    if existing:
        raise HTTPException(
            status_code=400, detail="Produkt mit diesem Namen existiert bereits")

    # Produkt speichern
    db_produkt = Produkt(
        name=produkt.name,
    )
    db.add(db_produkt)
    db.commit()
    db.refresh(db_produkt)
    return db_produkt


# -- Funktion, um Produkte zu suchen anahnd des Namen aber mit 'LIKE' (fur die Suchvorschläge) ---
@app.get("/produkte/suche", response_model=List[ProduktRead])
def search_products(
    query: str = Query(..., min_length=1, description="Suchstring für Produktnamen"),
    db: Session = Depends(get_db)
):
    if not query.strip():  # leerer String oder nur Leerzeichen
        raise HTTPException(status_code=400, detail="Der Suchstring darf nicht leer sein.")

    produkte = (
        db.query(Produkt)
        .filter(func.lower(Produkt.name).like(f"{query.lower()}%"))  # nur Anfangsstring
        .limit(10)
        .all()
    )

    if not produkte:  # keine Treffer gefunden
        raise HTTPException(status_code=404, detail="Keine Produkte gefunden")

    return produkte



# --- FavProdukte ---

@app.get("/fav_produkte/nutzer/{nutzer_id}", response_model=List[FavProdukteRead])
def get_fav_produkte_by_nutzer(nutzer_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    
    user = db.query(Nutzer).filter(Nutzer.id == nutzer_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Nutzer nicht gefunden")

     # JOIN zwischen FavProdukte und Produkt, um die Produktnamen direkt zu holen
    
    fav_produkte = (
        db.query(
            FavProdukte.nutzer_id,
            FavProdukte.produkt_id,
            Produkt.name.label("produkt_name"),
            FavProdukte.menge,
            FavProdukte.einheit_id,
            case((Einheit.id != None, Einheit.abkürzung), else_=None).label("einheit_abk"),
            FavProdukte.beschreibung
        )
        .join(Produkt, FavProdukte.produkt_id == Produkt.id)
        .outerjoin(Einheit, Einheit.id == FavProdukte.einheit_id)
        .filter(FavProdukte.nutzer_id == nutzer_id)
        .all()
    )
    return fav_produkte

@app.post("/fav_produkte_create/nutzer/{nutzer_id}", response_model=FavProdukteRead, status_code=status.HTTP_201_CREATED)
def create_fav_produkt(nutzer_id: int = Path(..., gt=0), fav_produkt: FavProdukteCreate = Body(...), db: Session = Depends(get_db)):

    anzahl_favoriten = db.query(FavProdukte).filter(
        FavProdukte.nutzer_id == nutzer_id).count() 
    
    if anzahl_favoriten >= 10:
        raise HTTPException(
            status_code=400, detail="Maximale Anzahl von 10 Favoriten erreicht")

    vorhandenes_fav_produkt = db.query(FavProdukte).filter(
        FavProdukte.nutzer_id == nutzer_id,
        FavProdukte.produkt_id == fav_produkt.produkt_id
    ).first()

    if vorhandenes_fav_produkt:
        raise HTTPException(
            status_code=400, detail="Das Produkt ist bereits in den Favoriten vorhanden")

    neues_fav_produkt = FavProdukte(
        nutzer_id=nutzer_id,
        produkt_id=fav_produkt.produkt_id,
        menge=fav_produkt.menge,
        einheit_id=fav_produkt.einheit_id,
        beschreibung=fav_produkt.beschreibung
    )

    db.add(neues_fav_produkt)
    db.commit()
    db.refresh(neues_fav_produkt)
    return neues_fav_produkt


@app.delete("/fav_produkte_delete/nutzer/{nutzer_id}/produkt/{produkt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fav_produkt(nutzer_id: int = Path(..., gt=0), produkt_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    fav_produkt = db.query(FavProdukte).filter(
        FavProdukte.nutzer_id == nutzer_id,
        FavProdukte.produkt_id == produkt_id
    ).first()
    if not fav_produkt:
        raise HTTPException(status_code=404, detail="Favorisiertes Produkt nicht gefunden")
    db.delete(fav_produkt)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/fav_produkte_update/nutzer/{nutzer_id}/produkt/{produkt_id}", response_model=FavProdukteRead)
def update_fav_produkt(nutzer_id: int = Path(..., gt=0), produkt_id: int = Path(..., gt=0), fav_produkt_update: FavProdukteUpdate = Body(...), db: Session = Depends(get_db)):
    fav_produkt = db.query(FavProdukte).filter(
        FavProdukte.nutzer_id == nutzer_id,
        FavProdukte.produkt_id == produkt_id
    ).first()
    if not fav_produkt:
        raise HTTPException(status_code=404, detail="Favorisiertes Produkt nicht gefunden")

    fav_produkt.menge = fav_produkt_update.menge
    fav_produkt.einheit_id = fav_produkt_update.einheit_id
    fav_produkt.beschreibung = fav_produkt_update.beschreibung

    db.commit()
    db.refresh(fav_produkt)
    return fav_produkt

# --- Bedarfsvorhersage ---
# Hilfsfunktion, um die Bedarfsvorhersage zu aktualisieren
def calc_bedarfsvorhersage_by_nutzer(nutzer_id: int, db: Session):
    # Alle Bedarfsvorhersage-Objekte des Nutzers holen
    eintraege =db.query(Bedarfsvorhersage).filter(
            Bedarfsvorhersage.nutzer_id == nutzer_id
        ).all()

    now = datetime.utcnow()
    decay_rate = 0.05  # Zerfallsrate pro Tag

    for eintrag in eintraege:
        # Tage seit last_update
        delta_days = (now - eintrag.last_update).days if eintrag.last_update else 0
        # if delta_days <= 0: --------------------------------------------------------------------------muss dann wieder hinzugeügt werden-------------------------------------------------
        #   continue

        new_counter = float(eintrag.counter) * max(0, (1 - decay_rate * delta_days)) # neuen Counter berechnen
        eintrag.counter = Decimal(round(new_counter, 2))
        eintrag.last_update = now

    db.commit()
    aktualisierte_einträge = []
    for eintrag in eintraege:
        produkt = db.query(Produkt).filter(Produkt.id == eintrag.produkt_id).first()
        aktualisierte_einträge.append(
            BedarfsvorhersageRead(
                nutzer_id=eintrag.nutzer_id,
                produkt_id=eintrag.produkt_id,
                produkt_name=produkt.name if produkt else None,
                counter=eintrag.counter,
                last_update=eintrag.last_update
            )
        )

    return aktualisierte_einträge


# Abrufen der Bedarfsvorhersage für einen Nutzer
@app.get("/bedarfsvorhersage/{nutzer_id}", response_model=List[BedarfsvorhersageRead])
def get_bedarfsvorhersage_by_nutzer(nutzer_id: int = Path(..., gt=0), db: Session = Depends(get_db)):

    user = db.query(Nutzer).filter(Nutzer.id == nutzer_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Nutzer nicht gefunden")

     # Bedarfsvorhersage-Einträge aktualisieren
    aktualisierte_einträge = calc_bedarfsvorhersage_by_nutzer(nutzer_id, db)

    return aktualisierte_einträge


# zum Löschen eines Bedarfvorhersage-Produkt
@app.delete("/bedarfsvorhersage_per_user_and_product/nutzer/{nutzer_id}/produkt/{produkt_id}", response_model=BedarfsvorhersageRead)
def delete_bedarfsvorhersage_eintrag(nutzer_id: int = Path(..., gt=0), produkt_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    eintrag = db.query(Bedarfsvorhersage).filter(
        Bedarfsvorhersage.nutzer_id == nutzer_id,
        Bedarfsvorhersage.produkt_id == produkt_id
    ).first()

    if not eintrag:
        raise HTTPException(status_code=404, detail="Eintrag nicht gefunden")
    
    db.delete(eintrag)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# erstellt einen Eintrag für die Bedarfsvorhersage oder aktualisiert den Counter, wenn der Eintrag bereits existiert
# der Counter wird erstmal im Body mit übergeben
@app.post("/bedarfsvorhersage_create/nutzer/{nutzer_id}", response_model=BedarfsvorhersageRead, status_code=status.HTTP_201_CREATED)
def create_bedarfsvorhersage_eintrag(nutzer_id: int = Path(..., gt=0), eintrag_data: BedarfvorhersageCreate = Body(...), db: Session = Depends(get_db)):

     # Prüfen, ob Eintrag existiert
    eintrag = db.query(Bedarfsvorhersage).filter(
        Bedarfsvorhersage.nutzer_id == nutzer_id,
        Bedarfsvorhersage.produkt_id == eintrag_data.produkt_id
    ).first()

    if eintrag:
        eintrag.counter = (Decimal(eintrag.counter) if eintrag.counter else Decimal(0)) + Decimal(eintrag_data.counter)
        eintrag.last_update = func.current_timestamp()
    else:
        eintrag = Bedarfsvorhersage(
            nutzer_id=nutzer_id,
            produkt_id=eintrag_data.produkt_id,
            counter=Decimal(eintrag_data.counter),
            last_update=func.current_timestamp()
        )
        db.add(eintrag)

    db.commit()
    db.refresh(eintrag)

    # Top-10 Einträge nach counter
    alle_eintraege = db.query(Bedarfsvorhersage)\
        .filter(Bedarfsvorhersage.nutzer_id == nutzer_id)\
        .order_by(Bedarfsvorhersage.counter.desc())\
        .all()

    if len(alle_eintraege) > 10:
        for e in alle_eintraege[10:]:
            db.delete(e)
        db.commit()

    return eintrag


# --- Listen ---

@app.get("/listen", response_model=List[ListeRead])
def get_listen_all(db: Session = Depends(get_db)):
    listen = db.query(Liste).all()
    return listen


@app.get("/listen/by-id/{list_id}", response_model=ListeRead)
def get_liste_by_id(list_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    liste = db.query(Liste).filter(Liste.id == list_id).first()
    if not liste:
        raise HTTPException(status_code=404, detail="Liste nicht gefunden")
    return liste


@app.post("/listen", response_model=ListeRead, status_code=status.HTTP_201_CREATED)
def create_liste(liste: ListeCreate, db: Session = Depends(get_db)):

    if liste is None:
        raise HTTPException(status_code=400, detail="Listendaten fehlen")

    # Prüfen, ob Nutzer mit hinzugefügt_von existiert
    existierender_nutzer = db.query(
        Nutzer).filter_by(id=liste.ersteller).first()
    if not existierender_nutzer:
        raise HTTPException(
            status_code=400, detail="Der Nutzer zum Hinzufügen wurde nicht gefunden")

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
        beigetreten_am=date.today()
    )
    db.add(neues_mitglied)
    db.commit()

    return db_liste


@app.put("/listen/{listen_id}/datum", response_model=ListeRead)
def update_liste_datum(listen_id: int, datum_update: ListeDatumUpdate = Body(...), db: Session = Depends(get_db)):
    liste = db.query(Liste).filter(Liste.id == listen_id).first()
    if not liste:
        raise HTTPException(status_code=404, detail="Liste nicht gefunden")

    # Datum als ISO-String speichern, da in DB als String definiert
    liste.datum = datum_update.datum

    db.commit()
    db.refresh(liste)
    return liste


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
def get_mitglieder_for_list(listen_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    mitglieder = db.query(ListeMitglieder).filter(
        ListeMitglieder.listen_id == listen_id).all()
    if not mitglieder:
        raise HTTPException(
            status_code=404, detail="Keine Mitglieder für diese Liste gefunden")
    return mitglieder


@app.post("/listen/{listen_id}/mitglieder/{nutzer_id}", response_model=MitgliedRead, status_code=status.HTTP_201_CREATED)
def add_mitglied(listen_id: int = Path(..., gt=0), nutzer_id: int = Path(..., gt=0), db: Session = Depends(get_db)):

    vorhanden = db.query(Nutzer).filter(Nutzer.id == nutzer_id).first()

    if not vorhanden:
        raise HTTPException(status_code=404, detail="Nutzer nicht gefunden")

    neues_mitglied = ListeMitglieder(
        listen_id=listen_id,
        nutzer_id=nutzer_id,
        beigetreten_am=date.today()
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
    # Prüfen, ob die Liste existiert
    liste = db.query(Liste).filter(Liste.id == listen_id).first()
    if not liste:
        raise HTTPException(status_code=404, detail="Liste nicht gefunden")

    # JOIN zwischen ListeProdukte, Produkt und Einheit, um die Produktnamen und Einheitenabkürzungen direkt zu holen
    produkte = (
        db.query(
            ListeProdukte.produkt_id,
            Produkt.name.label("produkt_name"),
            ListeProdukte.produkt_menge,
            ListeProdukte.einheit_id,
            case((Einheit.id != None, Einheit.abkürzung), else_=None).label("einheit_abk"),  # gucken ob einheit_id NULL ist
            ListeProdukte.hinzugefügt_von,
            ListeProdukte.beschreibung
        )
        .join(Produkt, Produkt.id == ListeProdukte.produkt_id)
        .outerjoin(Einheit, Einheit.id == ListeProdukte.einheit_id)
        .filter(ListeProdukte.listen_id == listen_id)
        .all()
    )
    return produkte


@app.post("/listen/{listen_id}/produkte/{produkt_id}/nutzer/{nutzer_id}", response_model=ProduktInListeRead, status_code=status.HTTP_201_CREATED)
def add_produkt_in_liste(listen_id: int = Path(..., gt=0), produkt_id: int = Path(..., gt=0), nutzer_id: int = Path(..., gt=0), db: Session = Depends(get_db)):

    existing_list = db.query(Liste).filter_by(id=listen_id).first()
    if not existing_list:
        raise HTTPException(status_code=404, detail="Liste nicht gefunden")

    existierendes_produkt = db.query(Produkt).filter_by(id=produkt_id).first()
    if not existierendes_produkt:
        raise HTTPException(
            status_code=400, detail="Das Produkt muss erst in der DB_Tabelle Produkt hinzugefügt werden")

    existierender_nutzer = db.query(Nutzer).filter_by(id=nutzer_id).first()
    if not existierender_nutzer:
        raise HTTPException(
            status_code=400, detail="Der Nutzer zum Hinzufügen wurde nicht gefunden")

    vorhandenes_produkt = db.query(ListeProdukte).filter(
        ListeProdukte.listen_id == listen_id,
        ListeProdukte.produkt_id == produkt_id,
        or_(
            ListeProdukte.hinzugefügt_von == nutzer_id,
            ListeProdukte.hinzugefügt_von == None  # prüft auf NULL
        )
    ).first()

    if vorhandenes_produkt:
        raise HTTPException(
            status_code=400,
            detail=f"Das Produkt ist bereits vorhanden. Du kannst es über den Button bearbeiten."
        )
    else:
        neues_Produkt = ListeProdukte(
            listen_id=listen_id,
            produkt_id=produkt_id,
            hinzugefügt_von=nutzer_id,
            produkt_menge=None,
            einheit_id=None,
            beschreibung=''
        )

    db.add(neues_Produkt)
    db.commit()
    db.refresh(neues_Produkt)
    return neues_Produkt


@app.put("/listen/{listen_id}/produkte/{produkt_id}/nutzer/{nutzer_id}", response_model=ProduktInListeRead, status_code=status.HTTP_201_CREATED)
def update_produkt_in_liste(listen_id: int = Path(..., gt=0), produkt_id: int = Path(..., gt=0), nutzer_id: int = Path(..., gt=0), produkt: ProduktInListeUpdate = Body(...), db: Session = Depends(get_db)):

    existing_list = db.query(Liste).filter_by(id=listen_id).first()
    if not existing_list:
        raise HTTPException(status_code=404, detail="Liste nicht gefunden")

    existierendes_produkt = db.query(Produkt).filter_by(id=produkt_id).first()
    if not existierendes_produkt:
        raise HTTPException(
            status_code=400, detail="Das Produkt muss erst in der DB_Tabelle Produkt hinzugefügt werden")

    existierender_nutzer = db.query(Nutzer).filter_by(id=nutzer_id).first()
    if not existierender_nutzer:
        raise HTTPException(
            status_code=400, detail="Der Nutzer zum Hinzufügen wurde nicht gefunden")

    vorhandenes_produkt = db.query(ListeProdukte).filter(
        ListeProdukte.listen_id == listen_id,
        ListeProdukte.produkt_id == produkt_id,
        ListeProdukte.hinzugefügt_von == nutzer_id
    ).first()

    if not vorhandenes_produkt:
        raise HTTPException(
            status_code=404, detail="Produkt in Liste nicht gefunden")
    else:
        if produkt.produkt_menge == 0:
            vorhandenes_produkt.produkt_menge = None
            vorhandenes_produkt.einheit_id = None
        else:
            vorhandenes_produkt.produkt_menge = produkt.produkt_menge
            vorhandenes_produkt.einheit_id = produkt.einheit_id

        vorhandenes_produkt.beschreibung = produkt.beschreibung

        db.commit()
        db.refresh(vorhandenes_produkt)
        return vorhandenes_produkt
    
    
@app.delete("/listen/{listen_id}/produkte/{produkt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_produkt_in_liste(listen_id: int = Path(..., gt=0), produkt_id: int = Path(..., gt=0), deleteRequest: ProduktDeleteRequest = Body(...), db: Session = Depends(get_db)):
    eintrag = db.query(ListeProdukte).filter(
        ListeProdukte.listen_id == listen_id,
        ListeProdukte.produkt_id == produkt_id,
        ListeProdukte.hinzugefügt_von == deleteRequest.hinzugefügt_von
    ).first()
    if not eintrag:
        raise HTTPException(
            status_code=404, detail="Produkt in Liste nicht gefunden")
    db.delete(eintrag)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Einkaufsarchiv ------------------------------------

@app.get("/einkaufsarchiv/list/{listen_id}", response_model=List[EinkaufsarchivRead])
def get_einkaufsarchiv(listen_id: int = Path(..., gt=0), db: Session = Depends(get_db)):

    # Prüfen, ob die Liste existiert
    liste = db.query(Liste).filter(Liste.id == listen_id).first()
    if not liste:
        raise HTTPException(status_code=404, detail="Liste nicht gefunden")
    
    einkaeufe = (
        db.query(
            Einkaufsarchiv.einkauf_id,
            Einkaufsarchiv.listen_id,
            Liste.name.label("listen_name"),
            Einkaufsarchiv.eingekauft_von,
            Nutzer.name.label("einkaeufer_name"),
            func.date(Einkaufsarchiv.eingekauft_am).label("eingekauft_am"),
            Einkaufsarchiv.gesamtpreis
        )
        .join(Liste, Liste.id == Einkaufsarchiv.listen_id)
        .outerjoin(Nutzer, Nutzer.id == Einkaufsarchiv.eingekauft_von)
        .filter(Einkaufsarchiv.listen_id == listen_id)
        .all()
    )


    return einkaeufe

@app.post("/create/einkaufsarchiv/list/{listen_id}", response_model=EinkaufsarchivRead, status_code=status.HTTP_201_CREATED)
def create_einkaufsarchiv(listen_id: int = Path(..., gt=0), einkauf: EinkaufsarchivCreate = Body(...), db: Session = Depends(get_db)):

    liste = db.query(Liste).filter(Liste.id == listen_id).first()
    if not liste:
        raise HTTPException(status_code=404, detail="Liste nicht gefunden")
    
    if einkauf.eingekauft_von is not None:
        nutzer = db.query(Nutzer).filter(Nutzer.id == einkauf.eingekauft_von).first()
        if not nutzer:
            raise HTTPException(status_code=400, detail="Eingekäufer nicht gefunden")
    
    neuer_einkauf = Einkaufsarchiv(
        listen_id = listen_id,
        eingekauft_von = einkauf.eingekauft_von,
        eingekauft_am=datetime.utcnow(),         # aktuelles Datum/Uhrzeit in UTC
        gesamtpreis = einkauf.gesamtpreis
    )

    db.add(neuer_einkauf)
    db.commit()
    db.refresh(neuer_einkauf)
    return neuer_einkauf

@app.delete("/delete/einkaufsarchiv/list/{listen_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_einkaufsarchiv(listen_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    einkaeufe = db.query(Einkaufsarchiv).filter(
        Einkaufsarchiv.listen_id == listen_id
    ).all()
    if not einkaeufe:
        raise HTTPException(status_code=404, detail="Keine Einkäufe für diese Liste gefunden")
    
    for einkauf in einkaeufe:
        db.delete(einkauf)   # die eingekauften Produkte werden in der DB gelöscht da ein ON DELETE CASCADE auf den Fremdschlüssel einkauf_id gesetzt ist

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# eingekaufte Produkte ------------------------------------

@app.get("/eingekaufte_produkte/einkauf/{einkauf_id}", response_model=List[eingekaufteProdukteRead])
def get_eingekaufte_produkte(einkauf_id: int = Path(..., gt=0), db: Session = Depends(get_db)):

    einkauf = db.query(Einkaufsarchiv).filter(Einkaufsarchiv.einkauf_id == einkauf_id).first()

    if not einkauf:
        raise HTTPException(status_code=404, detail="Einkauf nicht gefunden")

    eingekaufte_produkte = (
        db.query(
            EingekaufteProdukte.einkauf_id,
            EingekaufteProdukte.produkt_id,
            Produkt.name.label("produkt_name"),
            EingekaufteProdukte.produkt_menge,
            EingekaufteProdukte.einheit_id,
            Einheit.abkürzung.label("einheit_abk"),
            EingekaufteProdukte.produkt_preis,
            EingekaufteProdukte.hinzugefuegt_von,
            Nutzer.name.label("hinzufueger_name"),
            EingekaufteProdukte.beschreibung
        )
        .join(Produkt, Produkt.id == EingekaufteProdukte.produkt_id)
        .outerjoin(Einheit, Einheit.id == EingekaufteProdukte.einheit_id)
        .outerjoin(Nutzer, Nutzer.id == EingekaufteProdukte.hinzugefuegt_von)
        .filter(EingekaufteProdukte.einkauf_id == einkauf_id)
        .all()
    )

    return eingekaufte_produkte

@app.get("/eingekaufte_produkte/einkauf/{einkauf_id}/produkt/{produkt_id}/hinzugefuegt_von/{hinzugefuegt_von}", response_model=eingekaufteProdukteRead)
def get_eingekauftes_produkt(einkauf_id: int = Path(..., gt=0), produkt_id: int = Path(..., gt=0), hinzugefuegt_von: int = Path(..., gt=0), db: Session = Depends(get_db)):
    eingekauftes_produkt = db.query(EingekaufteProdukte).filter(
        EingekaufteProdukte.einkauf_id == einkauf_id,
        EingekaufteProdukte.produkt_id == produkt_id,
        EingekaufteProdukte.hinzugefuegt_von == hinzugefuegt_von
    ).first()

    if not eingekauftes_produkt:
        raise HTTPException(status_code=404, detail="Eingekauftes Produkt nicht gefunden")

    return eingekauftes_produkt

@app.post("/create/eingekaufte_produkte/einkauf/{einkauf_id}", response_model=eingekaufteProdukteRead, status_code=status.HTTP_201_CREATED)
def create_eingekaufte_produkte(einkauf_id: int = Path(..., gt=0), eingekauftes_produkt: eingekaufteProdukteCreate = Body(...), db: Session = Depends(get_db)):
    
    einkauf = db.query(Einkaufsarchiv).filter(Einkaufsarchiv.einkauf_id == einkauf_id).first()

    if not einkauf:
        raise HTTPException(status_code=404, detail="Einkauf nicht gefunden")
    
    neues_eingekauftes_produkt = EingekaufteProdukte(
        einkauf_id = einkauf_id,
        produkt_id = eingekauftes_produkt.produkt_id,
        produkt_menge = eingekauftes_produkt.produkt_menge,
        einheit_id = eingekauftes_produkt.einheit_id,
        produkt_preis = eingekauftes_produkt.produkt_preis,
        hinzugefuegt_von = eingekauftes_produkt.hinzugefuegt_von,
        beschreibung = eingekauftes_produkt.beschreibung
    )

    db.add(neues_eingekauftes_produkt)
    db.commit() 

    return neues_eingekauftes_produkt

# delete EingekaufteProdukte fällt weg, da es in der Datenbank durch die Fremdschlüsselbeziehung mit ON DELETE CASCADE automatisch gelöscht wird, wenn der zugehörige Einkauf gelöscht wird


