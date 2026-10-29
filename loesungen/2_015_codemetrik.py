# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_015_codemetrik.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_015_codemetrik

"""Aufgabe 2_015 – Codemetrik                                    Stufe 2 ★★☆☆☆

Ein Entwicklungsteam will seinen Code aufräumen. Ein erster Hinweis auf
schwer lesbaren Code sind sehr lange Funktionen. Ein kleines Werkzeug
zählt deshalb für jedes Modul (jede Python-Datei) die Codezeilen und die
Funktionen und berechnet, wie viele Zeilen eine Funktion im Durchschnitt
hat. Das Ergebnis soll als ordentlich ausgerichtete Tabelle im Terminal
erscheinen:

    Modul            Zeilen Fkt.  Z/Fkt.
    login               120    8    15.0
    datenbank          2310   41    56.3
    konfiguration        95    0       -

Schreiben Sie die Funktion `zeile(modul, zeilen, funktionen)`, die eine
Zeile dieser Tabelle als Text zurückgibt, ohne sie auszugeben:

- der Modulname linksbündig in einer Spalte der Breite 16,
- die Zeilen rechtsbündig in einer Spalte der Breite 7,
- die Funktionen rechtsbündig in einer Spalte der Breite 5,
- die Zeilen pro Funktion rechtsbündig in einer Spalte der Breite 8 mit
  einer Nachkommastelle; hat das Modul keine Funktion, steht dort
  rechtsbündig ein "-".

    zeile("login", 120, 8)          →  "login               120    8    15.0"
    zeile("konfiguration", 95, 0)   →  "konfiguration        95    0       -"

Die Kopfzeile steht schon als KOPF im Code.

Grenzen: modul ist ein Text aus 1 bis 16 Zeichen (Buchstaben, Ziffern und
_). zeilen und funktionen sind ganze Zahlen mit 0 ≤ zeilen ≤ 99 999 und
0 ≤ funktionen ≤ 999.

Hintergrund: In einem f-String kann man hinter einem Doppelpunkt angeben,
wie breit ein Wert geschrieben werden soll. Ist der Wert kürzer, wird mit
Leerzeichen aufgefüllt; < richtet ihn dabei links aus, > rechts:

    f"[{'ab':<5}]"     →  "[ab   ]"
    f"[{42:>5}]"       →  "[   42]"
    f"[{3.14159:>7.2f}]"  →  "[   3.14]"

Die Breite kommt vor dem Punkt, die Nachkommastellen danach. Zahlen
richtet man in Tabellen rechtsbündig aus, damit Einer unter Einern
stehen; Texte linksbündig. Ohne < oder > werden Texte links und Zahlen
rechts ausgerichtet; schreiben Sie es trotzdem hin, dann sieht man es
beim Lesen sofort.
"""

KOPF = "Modul            Zeilen Fkt.  Z/Fkt."


def zeile(modul, zeilen, funktionen):
    """Gibt eine Tabellenzeile mit Modul, Zeilen, Funktionen und Zeilen pro Funktion zurück."""
    anfang = f"{modul:<16}{zeilen:>7}{funktionen:>5}"
    if funktionen == 0:
        return anfang + f"{'-':>8}"
    return anfang + f"{zeilen / funktionen:>8.1f}"


print(KOPF)
print(zeile("login", 120, 8))
print(zeile("datenbank", 2310, 41))
print(zeile("konfiguration", 95, 0))


# Idee: Ein f-String setzt die ersten drei Spalten mit {modul:<16}, {zeilen:>7} und {funktionen:>5}
# zusammen. Die letzte Spalte ist {zeilen / funktionen:>8.1f}; nur wenn funktionen 0 ist, kommt
# stattdessen {'-':>8} hin, weil man durch 0 nicht teilen kann.
#
# Anderer Weg: die Text-Methoden ljust und rjust, etwa modul.ljust(16) + str(zeilen).rjust(7) …,
# oder alle Spalten mit Leerzeichen von Hand auffüllen: " " * (7 - len(str(zeilen))) + str(zeilen).
# Das ist länger, zeigt aber, was die Breitenangabe im f-String erledigt.
#
# Typische Fehler: die Breiten vertauschen oder < und > verwechseln (Zahlen hängen dann links),
# :.1f ohne Breite (die Spalte rutscht), die Zeile mit print ausgeben statt zurückgeben oder bei
# 0 Funktionen teilen (ZeroDivisionError).
