"""Aufgabe 2_024 – Fehlversuche                                  Stufe 2 ★★☆☆☆

Viele fehlgeschlagene Anmeldungen hintereinander können bedeuten, dass
jemand Passwörter durchprobiert. Die IT-Sicherheit eines Unternehmens
wertet deshalb regelmäßig (für eine Woche bis einen Monat) aus, wie oft
sich jemand vergeblich angemeldet hat. Das Anmeldesystem liefert eine
Liste der Benutzernamen und eine Liste von Listen: Zeile i gehört zum
Benutzer an Stelle i, Spalte j zum Tag j + 1 des Zeitraums.

    benutzer = ["mkoch", "aberg", "tlang"]
    versuche = [
        [0, 2, 0, 1, 0],
        [7, 0, 0, 12, 1],
        [0, 0, 3, 0, 0],
    ]

Schreiben Sie zwei Funktionen:

- `tagessummen(versuche)` gibt eine Liste mit der Summe der Fehlversuche
  aller Benutzer je Tag zurück, Tag 1 zuerst. Ohne Benutzer ist das
  Ergebnis die leere Liste.
- `auffaellig(benutzer, versuche, grenze)` gibt eine Liste von Tupeln
  (name, tag) zurück, eins für jeden Tag, an dem ein Benutzer mehr als
  grenze Fehlversuche hatte. tag ist die Nummer des Tages ab 1. Die
  Liste ist nach Namen sortiert, bei gleichem Namen nach Tag.

    tagessummen(versuche)               →  [7, 2, 3, 13, 1]
    auffaellig(benutzer, versuche, 2)   →  [("aberg", 1), ("aberg", 4), ("tlang", 3)]

Beide Funktionen lassen die übergebenen Listen unverändert.

Grenzen: benutzer hat 0 bis 1000 Einträge, nicht leere Texte aus
Kleinbuchstaben ohne Wiederholung. versuche hat genauso viele Zeilen
wie benutzer, alle Zeilen sind gleich lang mit 1 bis 31 Einträgen, ganze
Zahlen von 0 bis 1000. grenze ist eine ganze Zahl von 0 bis 1000.

Hintergrund: Diese Übung verbindet die letzten Aufgaben. versuche ist
eine Liste von Listen (Aufgabe 2_020): versuche[i][j] ist der Wert in
Zeile i und Spalte j, len(versuche[0]) die Anzahl der Spalten. Mit zip
(Aufgabe 2_022) läuft man durch benutzer und versuche zugleich und hat
so zu jedem Namen seine Zeile; mit enumerate (Aufgabe 2_021) bekommt
man beim Durchlaufen einer Zeile auch die Spaltennummer, mit
enumerate(zeile, start=1) gleich ab 1 gezählt. Tupel vergleicht
Python Element für Element, darum sortiert sorted (Aufgabe 2_023) eine
Liste von Tupeln (name, tag) erst nach dem Namen und bei gleichem Namen
nach dem Tag. Texte vergleicht Python dabei alphabetisch:

    ("aberg", 4) < ("mkoch", 1)    →  True     (erst der Name zählt)
    ("aberg", 1) < ("aberg", 4)    →  True     (gleicher Name, dann der Tag)

Eine Liste mit einer 0 je Tag bekommen Sie mit *: [0] * 3 ergibt
[0, 0, 0]; einen Eintrag darin ändern Sie mit summen[tag] = …
(Aufgabe 1_030). Dass die Funktionen die übergebenen Listen nicht
verändern dürfen, kennen Sie aus Aufgabe 2_019.
"""


def tagessummen(versuche):
    """Gibt die Summe der Fehlversuche je Tag zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def auffaellig(benutzer, versuche, grenze):
    """Gibt (name, tag) für jeden Tag mit mehr als grenze Fehlversuchen zurück, sortiert."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


benutzer = ["mkoch", "aberg", "tlang"]
versuche = [
    [0, 2, 0, 1, 0],
    [7, 0, 0, 12, 1],
    [0, 0, 3, 0, 0],
]
print(tagessummen(versuche))
print(auffaellig(benutzer, versuche, 2))
