"""Aufgabe 2_027 – Fehlerberichte                               Stufe 2 ★★☆☆☆

Ein Entwicklungsteam sammelt die Programmfehler (Bugs), die beim Testen
gefunden werden, in einem kleinen Bugtracker. Jeder Fehlerbericht ist
ein Dictionary mit festen Schlüsseln: dem Titel, dem Modul (der
Python-Datei), in dem der Fehler steckt, der Schwere von 1 (kritisch)
bis 4 (nur ein Schönheitsfehler) und dem Status. Ein neuer Bericht hat
den Status "offen". Ist der Fehler behoben, bekommt der Bericht den
Status "behoben" und einen neuen Schlüssel "behoben_in" mit der Version,
in der die Korrektur ausgeliefert wird. Schreiben Sie drei Funktionen:

- `neuer_bericht(titel, modul, schwere)` gibt einen neuen Bericht mit
  den Schlüsseln "titel", "modul", "schwere" und "status" zurück.
- `schliessen(bericht, version)` ändert den übergebenen Bericht: Der
  Status wird "behoben", und "behoben_in" bekommt die Version. Die
  Funktion gibt nichts zurück.
- `kurzinfo(bericht)` gibt eine Zeile für die Übersicht zurück, ohne
  den Bericht zu ändern: in eckigen Klammern S und die Schwere, dann
  Modul, Doppelpunkt und Titel, dahinter in runden Klammern "offen"
  oder "behoben in" und die Version.

    bericht = neuer_bericht("Login hängt", "login", 2)
    bericht        →  {"titel": "Login hängt", "modul": "login", "schwere": 2, "status": "offen"}
    kurzinfo(bericht)              →  "[S2] login: Login hängt (offen)"
    schliessen(bericht, "1.4")
    bericht["status"]              →  "behoben"
    bericht["behoben_in"]          →  "1.4"
    kurzinfo(bericht)              →  "[S2] login: Login hängt (behoben in 1.4)"

Grenzen: titel, modul und version sind nicht leere Texte mit höchstens
200 Zeichen, schwere ist eine ganze Zahl von 1 bis 4. kurzinfo bekommt
nur Berichte, die neuer_bericht angelegt und vielleicht schliessen
geändert hat. schliessen bekommt nur offene Berichte.

Hintergrund: In Aufgabe 2_025 waren die Schlüssel eines Dictionaries
Daten (die DNS-Namen), und es kamen beliebig viele dazu. Ein Dictionary
kann aber auch einen einzelnen Datensatz beschreiben, wie eine Zeile
einer Tabelle: Die Schlüssel sind feste Feldnamen, die Werte dürfen
verschiedene Typen haben.

    person = {"name": "Ada", "alter": 36}
    print(person["name"], person["alter"])     # Ada 36
    person["alter"] = person["alter"] + 1      # Feld ändern
    person["ort"] = "London"                   # neues Feld anlegen

Anders als bei einer Liste ["Ada", 36] muss man sich nicht merken, an
welcher Stelle welches Feld steht; person["alter"] sagt, was gemeint
ist. Jedes Ausführen von {...} legt ein neues Dictionary an. Ein
Dictionary ist veränderlich: Ändert eine Funktion den Datensatz, den sie
bekommen hat, sieht der Aufrufer die Änderung (Aufgabe 2_019).

In einem f-String (Aufgabe 1_010) brauchen Sie innen andere
Anführungszeichen als außen: f"{person['name']} ist {person['alter']}".
Mit gleichen Anführungszeichen gibt es unter Python 3.11 einen
SyntaxError.
"""


def neuer_bericht(titel, modul, schwere):
    """Gibt einen neuen, offenen Fehlerbericht als Dictionary zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def schliessen(bericht, version):
    """Setzt den Status des Berichts auf "behoben" und trägt die Version unter "behoben_in" ein."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def kurzinfo(bericht):
    """Gibt die Übersichtszeile des Berichts zurück, etwa "[S2] login: Login hängt (offen)"."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


bericht = neuer_bericht("Login hängt", "login", 2)
print(kurzinfo(bericht))
schliessen(bericht, "1.4")
print(kurzinfo(bericht))
