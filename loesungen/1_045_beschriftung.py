# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_045_beschriftung.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_045_beschriftung

"""Aufgabe 1_045 – Beschriftung                                  Stufe 1 ★☆☆☆☆

Eine Firma bietet ihre Bestell-App in mehreren Sprachen an. Der Knopf,
mit dem man eine Bestellung abschickt, soll in der Sprache beschriftet
sein, die jemand eingestellt hat. Die Sprache steht als kurzer Code
fest, etwa "de" für Deutsch oder "fr" für Französisch. Die Übersetzungen
stehen schon im Dictionary beschriftungen, das Programm fragt nach dem
Sprachcode. Ergänzen Sie den Code so, dass text die Beschriftung zur
eingegebenen Sprache enthält. Gibt es für einen Code keine Übersetzung,
nimmt die App die deutsche Beschriftung. Bei Eingabe en:

    Knopf: Send

Grenzen: Der Sprachcode besteht aus zwei Kleinbuchstaben, zum Beispiel
de, en oder it.

Hintergrund: Ein Dictionary ordnet Schlüsseln Werte zu, wie ein
Wörterbuch einem Wort seine Übersetzung. Man schreibt es in geschweifte
Klammern, je Eintrag Schlüssel: Wert, getrennt durch Kommas. Den Wert zu
einem Schlüssel holt man mit eckigen Klammern, so wie bei einer Liste
(Aufgabe 1_027), nur steht darin der Schlüssel statt einer Stelle:

    farben = {"rot": "#ff0000", "blau": "#0000ff"}
    farben["blau"]          →  "#0000ff"
    "grün" in farben        →  False

Fragt man nach einem Schlüssel, den es nicht gibt (farben["grün"]),
bricht das Programm mit einem KeyError ab. Mit in prüft man vorher, ob
der Schlüssel vorkommt; das kennen Sie von Listen aus Aufgabe 1_030.
"""

beschriftungen = {
    "de": "Absenden",
    "en": "Send",
    "fr": "Envoyer",
    "es": "Enviar",
    "it": "Invia",
    "nl": "Verzenden",
    "pl": "Wyślij",
    "tr": "Gönder",
}

sprache = input("Sprachcode: ")

if sprache in beschriftungen:
    text = beschriftungen[sprache]
else:
    text = beschriftungen["de"]

print("Knopf:", text)


# Idee: Erst mit sprache in beschriftungen prüfen, ob es zum Code eine Übersetzung gibt. Wenn ja, holt
# beschriftungen[sprache] sie heraus, sonst nimmt man beschriftungen["de"].
# Anderer Weg: text = beschriftungen.get(sprache, beschriftungen["de"]) erledigt beides in einer
# Zeile; get liefert den Standardwert, wenn der Schlüssel fehlt (kommt in Aufgabe 2_026). Eine Kette
# aus if sprache == "en": ... elif ... funktioniert auch, wiederholt aber jede Übersetzung im Code
# und muss bei jeder neuen Sprache ergänzt werden.
# Typische Fehler: beschriftungen[sprache] ohne Prüfung (KeyError bei "da"), beschriftungen["sprache"]
# mit Anführungszeichen (sucht den Schlüssel "sprache" statt des eingegebenen Codes) oder im else-Zweig
# den Text "de" statt der Beschriftung beschriftungen["de"] nehmen.
