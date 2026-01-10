from unittest.mock import MagicMock #  Mocking-Werkzeuge
from contextlib import closing # closing, um den Generator zu handhaben
from share_shop_api import get_db # die zu testende Funktion


def test_get_db_yields_session_and_closes_it_fixture(mock_db_session: MagicMock):
    """
    Beschreibung:
        Verifiziert den vollständigen Lebenszyklus des Datenbank-Generators (Dependency Injection).
        Der Test stellt sicher, dass eine Session korrekt bereitgestellt und nach der Nutzung garantiert geschlossen wird.

    Parameter:
        mock_db_session (MagicMock): Die durch die Fixture bereitgestellte Mock-Session.

    Validierungen (Asserts):
        - Identität: Prüft, ob das vom Generator gelieferte Objekt exakt unser Mock-Objekt ist.
        - Zustand während der Nutzung: Stellt sicher, dass .close() nicht zu früh aufgerufen wird.
        - Ressourcen-Management: Verifiziert, dass .close() nach Verlassen des Kontext-Blocks genau einmal aufgerufen wurde (Schutz vor Speicherlecks).

    Relevante zusätzliche Hinweise:
        Verwendet 'contextlib.closing', um den Generator-Stream sicher zu steuern und das 
        Verhalten der FastAPI-Middleware zu simulieren.
    """
    with closing(get_db()) as db:
        # 1.Identität
        assert next(db) is mock_db_session
        
        # 2Zustand
        mock_db_session.close.assert_not_called()
    
    # 3. ressourcen-management
    mock_db_session.close.assert_called_once()