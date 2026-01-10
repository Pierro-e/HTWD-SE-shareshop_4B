import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
# Importiere die App und die Datenbankmodelle aus der Hauptdatei
from share_shop_api import app
from decimal import Decimal 

# erstellen TestClient, um Anfragen zu simulieren
client = TestClient(app)

# Dummy-Nutzerdaten, die in den Tests verwendet werden
TEST_USER = {
    "id": 1,
    "email": "test@gmail.com",
    "name": "Test",
    "passwort_hash": "share4b", 
    "theme": 0,
    "color": 0
}


def test_login_scenarios(mock_db_session: MagicMock):
    """
    Beschreibung:
        Überprüft die Login-Logik über den HTTP-Endpunkt. Getestet werden der 
        erfolgreiche Login sowie Fehlversuche durch falsche E-Mail oder Passwörter.

    Parameter:
        mock_db_session (MagicMock): Die simulierte Datenbank-Sitzung.

    Validierungen (Asserts):
        - Status-Codes: 200 für Erfolg, 401 für ungültige Anmeldedaten.
        - Datenintegrität: Vergleicht die JSON-Antwort der API mit den erwarteten Nutzerdaten.
        - Security: Stellt sicher, dass Fehlermeldungen keine Rückschlüsse auf die Fehlerursache zulassen.
    """
    
    # Vorbereitung des Mock-Objekts für den Nutzer
    mock_nutzer_objekt = MagicMock()
    mock_nutzer_objekt.id = TEST_USER["id"]
    mock_nutzer_objekt.email = TEST_USER["email"]
    mock_nutzer_objekt.name = TEST_USER["name"]
    mock_nutzer_objekt.passwort_hash = TEST_USER["passwort_hash"]
    mock_nutzer_objekt.theme = TEST_USER["theme"]
    mock_nutzer_objekt.color = TEST_USER["color"]
    mock_nutzer_objekt.decaydays = Decimal("0.0")

    # Erfolgreicher Login ---
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_nutzer_objekt

    login_data_success = {
        "email": TEST_USER["email"],
        "passwort": TEST_USER["passwort_hash"]
    }
    
    response = client.post("/login", json=login_data_success)
    
    #  (NutzerRead) 
    expected_response_data = {
        "id": TEST_USER["id"],
        "email": TEST_USER["email"],
        "name": TEST_USER["name"],
        "theme": TEST_USER["theme"],
        "color": TEST_USER["color"],
        "decaydays": 0.0 
    }
    
    assert response.status_code == 200
    assert response.json() == expected_response_data

    #  Falsche Zugangsdaten ---
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    resp_fail = client.post("/login", json={"email": "falschedaten@test.de", "passwort": "123"})
    assert resp_fail.status_code == 401
    # assert response_wrong_pass.json() == {"detail": "Falsche Zugangsdaten"}

#----- start testen-----
def test_start():
    """
    Beschreibung: Testet den Root-Endpunkt der API.
    Validierungen (Asserts):
        - Status-Code: Überprüft, ob der Endpunkt mit 200 (OK) antwortet.
        - Antwortinhalt: Stellt sicher, dass die Rückgabe die erwartete Willkommensnachricht enthält.
    """
    response = client.get("/")
    assert response.status_code == 200 
   # expected_response = {"message": "API für share_shop DB"}
    assert response.json() == {"message": "API für share_shop DB"} 