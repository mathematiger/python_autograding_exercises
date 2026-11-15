# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_040_lizenzmodule.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_040_lizenzmodule

"""Aufgabe 2_040 – Lizenzmodule                                  Stufe 2 ★★☆☆☆

Ein Softwarehaus verkauft seine Warenwirtschaft in Modulen: Lager, Einkauf,
Buchhaltung und so weiter. Jedes gebuchte Modul kostet eine Lizenzgebühr. Welche
Module eine Kundin gebucht hat, steht in der Lizenzdatei als eine einzige ganze
Zahl: In ihrer Binärdarstellung (der Darstellung mit den Ziffern 0 und 1) steht
jede 1 für ein gebuchtes Modul. Für die Rechnung braucht die Buchhaltung die
Binärdarstellung und die Anzahl der gebuchten Module. Schreiben Sie zwei
Funktionen:

- `binaer(zahl)` gibt die Binärdarstellung von zahl als Text zurück, ohne
  führende Nullen (nur die Zahl 0 selbst wird zu "0").
- `anzahl_module(zahl)` gibt zurück, wie viele Einsen in der
  Binärdarstellung stehen.

    binaer(13)         →  "1101"
    anzahl_module(13)  →  3
    binaer(0)          →  "0"
    anzahl_module(0)   →  0

Rechnen Sie mit // und %, ohne die fertigen Werkzeuge bin(...), format(...)
oder f"{zahl:b}".

Grenzen: zahl ist eine ganze Zahl mit 0 ≤ zahl ≤ 2**64.

Hintergrund: Im Zehnersystem ist jede Stelle zehnmal so viel wert wie die
rechts daneben, im Binärsystem (Zweiersystem) nur doppelt so viel: Die Stellen
von rechts sind 1, 2, 4, 8, … wert. "1101" bedeutet also 8 + 4 + 0 + 1 = 13.
Die Binärdarstellung einer Zahl findet man wie ihre Ziffern im Zehnersystem
(Aufgabe 2_039), nur mit 2 statt 10: zahl % 2 ist die letzte Binärziffer (0
oder 1), zahl // 2 schneidet sie ab. Das wiederholt man, bis die Zahl 0 ist:

    13 % 2 → 1,   13 // 2 → 6
     6 % 2 → 0,    6 // 2 → 3
     3 % 2 → 1,    3 // 2 → 1
     1 % 2 → 1,    1 // 2 → 0

Die Reste von unten nach oben gelesen ergeben "1101". Eine neue Ziffer setzt
man deshalb vorn an den Text: text = str(rest) + text.
"""


def binaer(zahl):
    """Gibt die Binärdarstellung von zahl als Text ohne führende Nullen zurück."""
    if zahl == 0:
        return "0"
    text = ""
    while zahl > 0:
        text = str(zahl % 2) + text
        zahl = zahl // 2
    return text


def anzahl_module(zahl):
    """Gibt die Anzahl der Einsen in der Binärdarstellung von zahl zurück."""
    return binaer(zahl).count("1")


print(binaer(13))
print(anzahl_module(13))


# Idee: Wie bei den Dezimalziffern in 2_039: zahl % 2 ist die letzte Binärziffer, zahl // 2 schneidet sie
# ab. In einer while-Schleife wird jede Ziffer vorn an den Text gesetzt, bis zahl 0 ist; die 0 selbst wird
# vorher gesondert behandelt. anzahl_module zählt die Einsen im Text mit count("1").
#
# Anderer Weg: Die Stellenwerte von oben nach unten durchgehen: die größte Zweierpotenz suchen, die nicht
# größer als zahl ist, und dann für jede Potenz eine 1 schreiben und sie abziehen, wenn sie hineinpasst,
# sonst eine 0. anzahl_module geht auch ohne Text: in einer Schleife zahl % 2 aufsummieren.
#
# Typische Fehler: text = text + str(rest) (Ziffern verkehrt herum), die 0 vergessen (leerer Text),
# eine Zahl wie 1101 statt eines Textes zurückgeben oder zahl / 2 statt zahl // 2.
