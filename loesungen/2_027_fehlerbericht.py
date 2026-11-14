# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_027_fehlerbericht.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_027_fehlerbericht

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
    return {"titel": titel, "modul": modul, "schwere": schwere, "status": "offen"}


def schliessen(bericht, version):
    """Setzt den Status des Berichts auf "behoben" und trägt die Version unter "behoben_in" ein."""
    bericht["status"] = "behoben"
    bericht["behoben_in"] = version


def kurzinfo(bericht):
    """Gibt die Übersichtszeile des Berichts zurück, etwa "[S2] login: Login hängt (offen)"."""
    if bericht["status"] == "offen":
        zustand = "offen"
    else:
        zustand = f"behoben in {bericht['behoben_in']}"
    return f"[S{bericht['schwere']}] {bericht['modul']}: {bericht['titel']} ({zustand})"


bericht = neuer_bericht("Login hängt", "login", 2)
print(kurzinfo(bericht))
schliessen(bericht, "1.4")
print(kurzinfo(bericht))


# Idee: neuer_bericht schreibt ein Dictionary mit den vier Feldern in geschweiften Klammern und gibt es
# zurück. schliessen weist zwei Schlüsseln Werte zu: "status" gibt es schon und wird ersetzt,
# "behoben_in" wird neu angelegt. Weil das Dictionary veränderlich ist, sieht der Aufrufer die Änderung,
# ein return ist nicht nötig. kurzinfo liest die Felder und baut daraus mit einem f-String die Zeile;
# nur bei behobenen Berichten darf es bericht["behoben_in"] lesen.
#
# Anderer Weg: In neuer_bericht erst bericht = {} anlegen und die Felder einzeln mit bericht["titel"] = titel
# usw. eintragen. In kurzinfo kann man statt des Status auch mit "behoben_in" in bericht prüfen, ob der
# Bericht geschlossen ist.
#
# Typische Fehler: Schlüssel anders schreiben ("Status", "behoben in"), in schliessen ein neues Dictionary
# bauen und zurückgeben (der Bericht des Aufrufers bleibt dann offen), bericht["behoben_in"] auch bei
# offenen Berichten lesen (KeyError) oder ein Dictionary außerhalb der Funktion anlegen und in jedem Aufruf
# von neuer_bericht dasselbe ändern (dann sind alle Berichte ein und derselbe).
