from fastapi import Body
from fastapi import FastAPI, Depends, Path, status, HTTPException, Response
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric, Date, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from decimal import Decimal
from sqlalchemy import or_
from fastapi.middleware.cors import CORSMiddleware


DATABASE_URL = "mysql+pymysql://userAdmin:xdb_Admin890!@141.56.137.83/share_shop"

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
    ersteller = Column(Integer, ForeignKey(
        'Nutzer.id', ondelete='SET NULL'), nullable=True)
    datum = Column(Date)


class ListeMitglieder(Base):
    __tablename__ = "ListeMitglieder"
    listen_id = Column(Integer, ForeignKey(
        'Listen.id', ondelete='CASCADE'), primary_key=True)
    nutzer_id = Column(Integer, ForeignKey(
        'Nutzer.id', ondelete='Cascade'), primary_key=True)
    beigetreten_am = Column(Date)


class ListeProdukte(Base):
    __tablename__ = "ListeProdukte"
    listen_id = Column(Integer, ForeignKey(
        'Listen.id', ondelete='Cascade'), primary_key=True)
    produkt_id = Column(Integer, ForeignKey('Produkt.id'), primary_key=True)
    hinzugefügt_von = Column(Integer, ForeignKey(
        'Nutzer.id', ondelete='SET NULL'), nullable=True)
    produkt_menge = Column(Numeric(10, 2), nullable=True)
    einheit_id = Column(Integer, nullable=True)
    beschreibung = Column(String, nullable=True)

# --- Pydantic-Modelle ---


class NutzerRead(BaseModel):
    id: int
    email: str
    name: str
    passwort_hash: str

    class Config:
        from_attributes = True


class NutzerCreate(BaseModel):
    email: str
    name: str
    passwort_hash: str


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


class ProduktCreate(BaseModel):
    name: str


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
    produkt_menge: Optional[Decimal] = None
    einheit_id: Optional[int] = None
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


class PasswortÄndern(BaseModel):
    neues_passwort: str


class NameAendern(BaseModel):
    neuer_name: str


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
def change_name(nutzer_id: int, name: NameAendern, db: Session = Depends(get_db)):
    nutzer = db.query(Nutzer).filter(Nutzer.id == nutzer_id).first()

    if not nutzer:
        raise HTTPException(status_code=404, detail="Nutzer nicht gefunden")

    nutzer.name = name.neuer_name
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
    # Formatierter Produktname
    formatted_name = ' '.join([word.capitalize()
                              for word in produkt.name.split()])

    # Prüfen, ob Produkt mit dem formatierten Namen schon existiert
    existing = db.query(Produkt).filter(func.lower(
        Produkt.name) == formatted_name.lower()).first()
    if existing:
        raise HTTPException(
            status_code=400, detail="Produkt mit diesem Namen existiert bereits")

    # Produkt speichern
    db_produkt = Produkt(
        name=formatted_name,
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
    else:
        db.delete(produkt)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)


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

    produkte = db.query(ListeProdukte).filter(
        ListeProdukte.listen_id == listen_id).all()
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
