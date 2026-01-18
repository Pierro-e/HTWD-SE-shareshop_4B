import pytest
from unittest.mock import MagicMock, patch
from decimal import Decimal
import os

# Mock environment variables before importing
with patch.dict(os.environ, {
    'DB_USER': 'test',
    'DB_PASSWORD': 'test',
    'DB_HOST': 'localhost',
    'DB_NAME': 'test'
}):
    from share_shop_api import get_nutzer_all, get_nutzer_by_id, create_nutzer, get_produkte_all, get_produkt_by_id, create_produkt, get_fav_produkte_by_nutzer
    from share_shop_api import NutzerCreate, ProduktCreate

# Hilfsfunktion zum Erstellen von Dummy-Nutzer-Objekten (als MagicMock mit Attributen)
def create_mock_nutzer(id, email, name, passwort_hash="hashed", theme=0, color=0, decaydays=Decimal('7.0')):
    mock = MagicMock()
    mock.id = id
    mock.email = email
    mock.name = name
    mock.passwort_hash = passwort_hash
    mock.theme = theme
    mock.color = color
    mock.decaydays = decaydays
    return mock

# Hilfsfunktion zum Erstellen von Dummy-Produkt-Objekten
def create_mock_produkt(id, name):
    mock = MagicMock()
    mock.id = id
    mock.name = name
    return mock

# Hilfsfunktion zum Erstellen von Dummy-Produkt-Objekten
def create_mock_produkt(id, name):
    mock = MagicMock()
    mock.id = id
    mock.name = name
    return mock

# Tests für Nutzer-Endpunkte
@patch('share_shop_api.SessionLocal')
def test_get_nutzer_all_success(mock_session_local):
    # Arrange
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_nutzer1 = create_mock_nutzer(1, 'user1@example.com', 'User1')
    mock_nutzer2 = create_mock_nutzer(2, 'user2@example.com', 'User2')
    mock_db.query.return_value.all.return_value = [mock_nutzer1, mock_nutzer2]

    # Act
    result = get_nutzer_all(db=mock_db)

    # Assert
    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].email == 'user1@example.com'
    assert result[1].id == 2


@patch('share_shop_api.SessionLocal')
def test_get_nutzer_by_id_success(mock_session_local):
    """ Testet das erfolgreiche Abrufen eines Nutzers nach ID. """
    # Arrange
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_nutzer = create_mock_nutzer(1, 'user1@example.com', 'User1')
    mock_db.query.return_value.filter.return_value.first.return_value = mock_nutzer

    # Act
    result = get_nutzer_by_id(1, db=mock_db)

    # Assert
    assert result.id == 1
    assert result.email == 'user1@example.com'

@patch('share_shop_api.SessionLocal')
def test_get_nutzer_by_id_not_found(mock_session_local):
    """ Testet das Verhalten beim Abrufen eines nicht existierenden Nutzers nach ID. """
    # Arrange
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        get_nutzer_by_id(999, db=mock_db)
    assert "Nutzer nicht gefunden" in str(exc_info.value)