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