import pytest
from unittest.mock import MagicMock
from share_shop_api import create_nutzer, NutzerCreate

NEUER_NUTZER_DATEN = NutzerCreate(
    email="neu@test.de", 
    name="Neuer Nutzer", 
    passwort_hash="sicherespasswort" 
)

def test_create_nutzer_success(mock_db_session: MagicMock):
    """
    Beschreibung:
        Testet die erfolgreiche Erstellung eines neuen Nutzers in der Datenbank.
        Dabei wird sichergestellt, dass bei einer noch nicht vergebenen E-Mail-Adresse
        der Nutzer korrekt verarbeitet und die Datenbank-Transaktion abgeschlossen wird.

    Parameter:
        mock_db_session (MagicMock): Die durch die Fixture bereitgestellte Mock-Session.

    Validierungen (Asserts):
        - Datenbank-Interaktion: Prüft, ob .add(), .commit() und .refresh() aufgerufen wurden.
        - Daten-Integrität: Verifiziert, dass das zurückgegebene Objekt die korrekte E-Mail enthält.

    Relevante zusätzliche Hinweise:
        Der Test simuliert eine leere Datenbank-Antwort (None) für die E-Mail-Suche,
        um den Pfad für eine erfolgreiche Neuanlage zu erzwingen.
    """
    db = mock_db_sessionS
    db.query.return_value.filter.return_value.first.return_value = None
    result_nutzer = create_nutzer(db=db, nutzer=NEUER_NUTZER_DATEN)

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()

    assert result_nutzer.email == NEUER_NUTZER_DATEN.email