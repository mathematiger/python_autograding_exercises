# Automatisch erzeugt aus lehrkraft/muster/1_045_beschriftung.py - nicht von Hand ändern.
# vorlage-hash: 0ee3ada5c9880094
# text-hash: 28bdec3c135680c9
# thema: datenstrukturen
# inhalt: Wert zu einem Schlüssel

EINGABEN = ["en"]

UEBERSETZUNGEN = {
    "de": "Absenden",
    "en": "Send",
    "fr": "Envoyer",
    "es": "Enviar",
    "it": "Invia",
    "nl": "Verzenden",
    "pl": "Wyślij",
    "tr": "Gönder",
}


def ausgabe_bei(code):
    """Startet das Programm mit dem Sprachcode; ein Abbruch wird als Text zurückgegeben."""
    try:
        return starte(code)
    except Exception as fehler:
        return f"(Abbruch: {fehler})"


def meldung(code, erwartet, ausgabe):
    """Fehlermeldung mit Eingabe, erwarteter und tatsächlicher Ausgabe."""
    text = f'Bei Eingabe {code} erwartet: "Knopf: {erwartet}" – Ihr Programm: "{ausgabe}"'
    if "KeyError" in ausgabe:
        text += "\nTipp: Diesen Code gibt es im Dictionary nicht; prüfen Sie vorher mit in, ob er vorkommt."
    if vergleichbar(ausgabe) == vergleichbar("Knopf: de"):
        text += '\nTipp: beschriftungen["de"] holt die deutsche Beschriftung, "de" ist nur der Code.'
    return text


# Bei Eingabe en heißt der Knopf Send
assert vergleichbar(AUSGABE) == vergleichbar("Knopf: Send"), meldung("en", "Send", AUSGABE)

# Bei Eingabe fr heißt der Knopf Envoyer (nicht fest Send hinschreiben!)
ausgabe = ausgabe_bei("fr")
assert vergleichbar(ausgabe) == vergleichbar("Knopf: Envoyer"), (
    meldung("fr", "Envoyer", ausgabe) + "\nTipp: beschriftungen[sprache] holt den Wert zum eingegebenen Code."
)

# Bei Eingabe de heißt der Knopf Absenden
ausgabe = ausgabe_bei("de")
assert vergleichbar(ausgabe) == vergleichbar("Knopf: Absenden"), meldung("de", "Absenden", ausgabe)

# Alle Sprachen aus dem Dictionary
for code, erwartet in UEBERSETZUNGEN.items():
    ausgabe = ausgabe_bei(code)
    assert vergleichbar(ausgabe) == vergleichbar(f"Knopf: {erwartet}"), meldung(code, erwartet, ausgabe)

# Unbekannter Code: die deutsche Beschriftung
ausgabe = ausgabe_bei("da")
assert vergleichbar(ausgabe) == vergleichbar("Knopf: Absenden"), (
    meldung("da", "Absenden", ausgabe) + "\nFür einen Code ohne Übersetzung soll die deutsche Beschriftung erscheinen."
)

# Ein zweiter unbekannter Code: ebenfalls die deutsche Beschriftung
ausgabe = ausgabe_bei("zz")
assert vergleichbar(ausgabe) == vergleichbar("Knopf: Absenden"), meldung("zz", "Absenden", ausgabe)

# Viele zufällige Sprachcodes aus zwei Kleinbuchstaben
zufall = Zufall(1045)
buchstaben = "abcdefghijklmnopqrstuvwxyz"
for _ in range(40):
    code = zufall.choice(buchstaben) + zufall.choice(buchstaben)
    if zufall.random() < 0.3:
        code = zufall.choice(list(UEBERSETZUNGEN))
    erwartet = UEBERSETZUNGEN.get(code, "Absenden")
    ausgabe = ausgabe_bei(code)
    assert vergleichbar(ausgabe) == vergleichbar(f"Knopf: {erwartet}"), meldung(code, erwartet, ausgabe)
