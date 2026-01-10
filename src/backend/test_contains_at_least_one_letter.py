import pytest
from share_shop_api import contains_at_least_one_letter

# Definition der Testdaten mit IDs für bessere Lesbarkeit im Testbericht
test_cases = [
    # Positive Fälle
    pytest.param("Hallo Welt", True, id="Standard-Satz"),
    pytest.param("Brot 123", True, id="Buchstaben-Zahlen-Mix"),
    pytest.param("Müller", True, id="Umlaute"), 
    pytest.param("Äpfel & Birnen", True, id="Sonderzeichen-Mix"),
    pytest.param("a", True, id="Einzelner-Buchstabe"),
    pytest.param("123a", True, id="Zahlen-gefolgt-von-Buchstabe"),
    pytest.param("TEST!", True, id="Großbuchstaben-Ausrufezeichen"),
    
    # Negative Fälle
    pytest.param("", False, id="Leerer-String"),
    pytest.param("12345", False, id="Reine-Zahlenfolge"),
    pytest.param("!!!", False, id="Reine-Sonderzeichen"),
    pytest.param("123 * !@#", False, id="Zahlen-Symbole-Leerzeichen-Kombination"),
]

@pytest.mark.parametrize("input_string, expected_output", test_cases)
def test_contains_at_least_one_letter(input_string, expected_output):
    """
    Beschreibung:
        Validiert die Hilfsfunktion 'contains_at_least_one_letter', die sicherstellt, 
        dass ein Eingabestring nicht nur aus Zahlen oder Symbolen besteht, 
        sondern mindestens einen alphabetischen Charakter enthält.

    Parameter:
        input_string (str): Der zu prüfende Text (Eingabe).
        expected_output (bool): Das erwartete Ergebnis der Prüfung.

    Validierungen (Asserts):
        - Logik-Check: Entspricht der Rückgabewert der Funktion der Erwartung?
        - Typprüfung: Die Funktion muss korrekt auf Strings, Leerstrings und Sonderzeichen reagieren.

    Relevante zusätzliche Hinweise:
        Diese Funktion ist essenziell für die Namensvalidierung bei der Nutzerregistrierung, 
        um "Fake-Namen" wie "12345" oder "!!!" zu unterbinden.
    """
    # Act: Aufruf der zu testenden Funktion
    actual_output = contains_at_least_one_letter(input_string)
    
    # Assert: Abgleich mit dem erwarteten Ergebnis
    assert actual_output == expected_output