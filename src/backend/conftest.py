import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_db_session():
    """
    Beschreibung:
        Erstellt ein Mock-Objekt für eine SQLAlchemy-Datenbanksitzung und patcht 
        die globale 'SessionLocal' in der API. Dies verhindert echte Datenbankzugriffe während des Tests.

    Parameter:
        Keine (Pytest Fixture).

    Rückgabe:
        MagicMock: Ein Mock-Objekt, das sich wie eine SQLAlchemy-Session verhält.

    Details zum Ablauf:
        1. Ein MagicMock-Objekt wird als Stellvertreter für die Session erstellt.
        2. Mittels 'patch' wird der Aufruf von 'share_shop_api.SessionLocal' abgefangen.
        3. Jedes Mal, wenn die App eine neue Session anfordert, wird stattdessen dieses Mock-Objekt zurückgegeben.
        4. Nach Abschluss des Tests wird der Patch automatisch aufgehoben.
    """

    mock_session = MagicMock()


    with patch('share_shop_api.SessionLocal') as MockSessionLocal:
        MockSessionLocal.return_value = mock_session
        
        yield mock_session
        