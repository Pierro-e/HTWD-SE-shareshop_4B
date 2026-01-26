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
    from share_shop_api import delete_nutzer, get_eingekaufte_produkte, get_kostenaufteilung_empfaenger, delete_liste, create_liste
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

# Hilfsfunktion zum Erstellen von Dummy-FavProdukte-Objekten
def create_mock_fav_produkt(nutzer_id, produkt_id, produkt_name, menge=None, einheit_id=None, einheit_abk=None, beschreibung=None):
    mock = MagicMock()
    mock.nutzer_id = nutzer_id
    mock.produkt_id = produkt_id
    mock.produkt_name = produkt_name
    mock.menge = menge
    mock.einheit_id = einheit_id
    mock.einheit_abk = einheit_abk
    mock.beschreibung = beschreibung
    return mock

# Hilfsfunktion zum Erstellen von Dummy-EingekaufteProdukte-Objekten
def create_mock_eingekauftes_produkt(einkauf_id, produkt_id, hinzugefuegt_von, menge, preis):
    mock = MagicMock()
    mock.einkauf_id = einkauf_id
    mock.produkt_id = produkt_id
    mock.hinzugefuegt_von = hinzugefuegt_von
    mock.menge = menge
    mock.preis = preis
    return mock

# Hilfsunktion zum Erstellen von Dummy-Kostenaufteilung-Objekten
def create_mock_kostenaufteilung(empfaenger_id, schuldner_id, betrag):
    mock = MagicMock()
    mock.empfaenger_id = empfaenger_id
    mock.schuldner_id = schuldner_id
    mock.betrag = betrag
    return mock
# Hilfsfunktion zum Erstellen von Dummy-Liste-Objekten
def create_mock_liste(id, name, ersteller_id):
    mock = MagicMock()
    mock.id = id
    mock.name = name
    mock.ersteller_id = ersteller_id
    return mock
######################################## Tests für Nutzer-Endpunkte############################################################
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


@patch('share_shop_api.SessionLocal')
def test_create_nutzer_success(mock_session_local):
    """ Testet das erfolgreiche Erstellen eines neuen Nutzers. """
    # Arrange
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_db.query.return_value.filter.return_value.first.return_value = None  # Kein vorhandener Nutzer
    mock_nutzer = create_mock_nutzer(1, 'newuser@example.com', 'New User')
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = lambda obj: setattr(obj, 'id', 1)

    nutzer_data = NutzerCreate(email="newuser@example.com", name="New User", passwort_hash="hashedpassword")

    # Act
    result = create_nutzer(nutzer_data, db=mock_db)

    # Assert
    assert result.id == 1
    assert result.email == 'newuser@example.com' 

@patch('share_shop_api.SessionLocal')
def test_create_nutzer_already_exists(mock_session_local):
    """ Testet das Verhalten beim Erstellen eines Nutzers mit bereits existierender Email. """
    # Arrange
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_existing = create_mock_nutzer(1, 'existing@example.com', 'Existing')
    mock_db.query.return_value.filter.return_value.first.return_value = mock_existing

    nutzer_data = NutzerCreate(email="existing@example.com", name="New User", passwort_hash="hashedpassword")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        create_nutzer(nutzer_data, db=mock_db)
    assert "Nutzeremail existiert bereits" in str(exc_info.value)

     


########################### Tests für Produkte-Endpunkte###############################

@patch('share_shop_api.SessionLocal')
def test_get_produkte_all_success(mock_session_local):
    """ Testet das erfolgreiche Abrufen aller Produkte. """
    # Arrange
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_produkt1 = create_mock_produkt(1, 'Apfel')
    mock_produkt2 = create_mock_produkt(2, 'Banane')
    mock_db.query.return_value.all.return_value = [mock_produkt1, mock_produkt2]

    # Act
    result = get_produkte_all(db=mock_db)

    # Assert
    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].name == 'Apfel'

@patch('share_shop_api.SessionLocal')
def test_get_produkt_by_id_success(mock_session_local):
    """ Testet das erfolgreiche Abrufen eines Produkts nach ID. """
    # Arrange
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_produkt = create_mock_produkt(1, 'Apfel')
    mock_db.query.return_value.filter.return_value.first.return_value = mock_produkt

    # Act
    result = get_produkt_by_id(1, db=mock_db)

    # Assert
    assert result.id == 1
    assert result.name == 'Apfel'

@patch('share_shop_api.SessionLocal')
def test_get_produkt_by_id_not_found(mock_session_local):
    """ Testet das Verhalten beim Abrufen eines nicht existierenden Produkts nach ID. """
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        get_produkt_by_id(999, db=mock_db)
    assert "Produkt nicht gefunden" in str(exc_info.value)

@patch('share_shop_api.SessionLocal')
def test_create_produkt_success(mock_session_local):
    """ Testet das erfolgreiche Erstellen eines neuen Produkts. """
    # Arrange
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_db.query.return_value.filter.return_value.first.return_value = None  # Kein vorhandenes Produkt
    mock_produkt = create_mock_produkt(1, 'Neues Produkt')
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = lambda obj: setattr(obj, 'id', 1)

    produkt_data = ProduktCreate(name="Neues Produkt")

    # Act
    result = create_produkt(produkt_data, db=mock_db)

    # Assert
    assert result.id == 1
    assert result.name == 'Neues Produkt'

@patch('share_shop_api.SessionLocal')
def test_create_produkt_already_exists(mock_session_local):
    """ Testet das Verhalten beim Erstellen eines Produkts mit bereits existierendem Namen. """
    # Arrange
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_existing = create_mock_produkt(1, 'Apfel')
    mock_db.query.return_value.filter.return_value.first.return_value = mock_existing

    produkt_data = ProduktCreate(name="Apfel")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        create_produkt(produkt_data, db=mock_db)
    assert "Produkt mit diesem Namen existiert bereits" in str(exc_info.value)

# ###############Tests für Favoriten-Endpunkte#############################

@patch('share_shop_api.SessionLocal')
def test_get_fav_produkte_by_nutzer_success(mock_session_local):
    """ Testet das erfolgreiche Abrufen der Favoriten-Produkte eines Nutzers. """
    # Arrange
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_user = create_mock_nutzer(1, 'user@example.com', 'User')
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    mock_fav1 = create_mock_fav_produkt(1, 1, 'Apfel', 2.0, 1, 'kg', 'Frisch')
    mock_fav2 = create_mock_fav_produkt(1, 2, 'Banane', 1.0, 2, 'Stück', None)
    # Mock the complex query chain
    mock_query = mock_db.query.return_value
    mock_query.join.return_value.outerjoin.return_value.filter.return_value.all.return_value = [mock_fav1, mock_fav2]

    # Act
    result = get_fav_produkte_by_nutzer(1, db=mock_db)

    # Assert
    assert len(result) == 2
    assert result[0].nutzer_id == 1
    assert result[0].produkt_name == 'Apfel'

@patch('share_shop_api.SessionLocal')
def test_get_fav_produkte_by_nutzer_not_found(mock_session_local):
    """ Testet das Verhalten beim Abrufen der Favoriten-Produkte eines nicht existierenden Nutzers. """
    # Arrange
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_db.query.return_value.filter.return_value.first.return_value = None  # Nutzer nicht gefunden

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        get_fav_produkte_by_nutzer(999, db=mock_db)
    assert "Nutzer nicht gefunden" in str(exc_info.value)

# Tests für DELETE-Endpunkte für Nutzer#############################

@patch('share_shop_api.SessionLocal')
def test_delete_nutzer_success(mock_session_local):
    # Arrange
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_nutzer = create_mock_nutzer(1, 'user@example.com', 'User')
    mock_db.query.return_value.filter.return_value.first.return_value = mock_nutzer

    # Act
    result = delete_nutzer(1, db=mock_db)

    # Assert
    assert result.status_code == 204
    mock_db.delete.assert_called_once_with(mock_nutzer)
    mock_db.commit.assert_called_once()

@patch('share_shop_api.SessionLocal')
def test_delete_nutzer_not_found(mock_session_local):
    # Arrange
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        delete_nutzer(999, db=mock_db)
    assert "Nutzer nicht gefunden" in str(exc_info.value)
################ liste tests #############################
@patch('share_shop_api.SessionLocal')
def test_create_liste_success(mock_session_local):
    # Arrange
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_nutzer = create_mock_nutzer(1, 'creator@example.com', 'Creator')
    mock_db.query.return_value.filter_by.return_value.first.return_value = mock_nutzer  # Nutzer gefunden
    mock_liste = create_mock_liste(1, 'Neue Liste', 1)
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = lambda obj: setattr(obj, 'id', 1)

    liste_data = ListeCreate(name="Neue Liste", ersteller=1)

    # Act
    result = create_liste(liste_data, db=mock_db)

    # Assert
    assert result.id == 1
    assert result.name == 'Neue Liste'

@patch('share_shop_api.SessionLocal')
def test_delete_liste_success(mock_session_local):
    """ Testet das erfolgreiche Löschen einer Liste. """
    # Arrange
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_liste = create_mock_liste(1, 'Test Liste', 1)
    mock_db.query.return_value.filter.return_value.first.return_value = mock_liste

    # Act
    result = delete_liste(1, db=mock_db)

    # Assert
    assert result.status_code == 204
    mock_db.delete.assert_called_once_with(mock_liste)
    mock_db.commit.assert_called_once()

@patch('share_shop_api.SessionLocal')
def test_delete_liste_not_found(mock_session_local):
    """ Testet das Verhalten beim Löschen einer nicht existierenden Liste. """
    # Arrange
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        delete_liste(999, db=mock_db)
    assert "Liste nicht gefunden" in str(exc_info.value)


################Tests für Eingekaufte Produkte############################

@patch('share_shop_api.SessionLocal')
def test_get_eingekaufte_produkte_success(mock_session_local):
    """ Testet das erfolgreiche Abrufen der eingekauften Produkte eines Einkaufs. """
    # Arrange
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_einkauf = MagicMock()
    mock_einkauf.einkauf_id = 1

    mock_produkt1 = create_mock_eingekauftes_produkt(1, 1, 1, 2.0, 5.50)
    mock_produkt2 = create_mock_eingekauftes_produkt(1, 2, 2, 1.0, 3.20)

    # Mock query mit side_effect für zwei Aufrufe
    mock_query1 = MagicMock()
    mock_query1.filter.return_value.first.return_value = mock_einkauf

    mock_query2 = MagicMock()
    mock_query2.join.return_value.outerjoin.return_value.outerjoin.return_value.filter.return_value.all.return_value = [mock_produkt1, mock_produkt2]

    mock_db.query.side_effect = [mock_query1, mock_query2]

    # Act
    result = get_eingekaufte_produkte(1, db=mock_db)

    # Assert
    assert len(result) == 2
    assert result[0].einkauf_id == 1
    assert result[0].produkt_id == 1

@patch('share_shop_api.SessionLocal')
def test_get_eingekaufte_produkte_empty(mock_session_local):
    """ Testt das Abrufen der eingekauften Produkte eines Einkaufs, wenn keine Produkte vorhanden sind. """
    # Arrange
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_einkauf = MagicMock()
    mock_einkauf.einkauf_id = 1

    # Mock query mit side_effect für zwei Aufrufe
    mock_query1 = MagicMock()
    mock_query1.filter.return_value.first.return_value = mock_einkauf

    mock_query2 = MagicMock()
    mock_query2.join.return_value.outerjoin.return_value.outerjoin.return_value.filter.return_value.all.return_value = []

    mock_db.query.side_effect = [mock_query1, mock_query2]

    # Act
    result = get_eingekaufte_produkte(1, db=mock_db)

    # Assert
    assert result == []

############## Tests für Kostenaufteilung################################
@patch('share_shop_api.SessionLocal')
def test_get_kostenaufteilung_empfaenger_success(mock_session_local):
    """ Testet das erfolgreiche Abrufen der Kostenaufteilung für einen Empfänger. """
    # Arrange
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_kosten1 = create_mock_kostenaufteilung(1, 2, 10.50)
    mock_kosten2 = create_mock_kostenaufteilung(1, 3, 5.25)
    mock_db.query.return_value.join.return_value.join.return_value.filter.return_value.all.return_value = [mock_kosten1, mock_kosten2]

    # Act
    result = get_kostenaufteilung_empfaenger(1, db=mock_db)

    # Assert
    assert len(result) == 2
    assert result[0].empfaenger_id == 1
    assert result[0].betrag == 10.50

    @patch('share_shop_api.SessionLocal')
    def test_get_kostenaufteilung_empfaenger_empty(mock_session_local):
        # Arrange
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db

        mock_db.query.return_value.join.return_value.join.return_value.filter.return_value.all.return_value = []

        # Act
        result = get_kostenaufteilung_empfaenger(1, db=mock_db)

        # Assert
        assert result == []