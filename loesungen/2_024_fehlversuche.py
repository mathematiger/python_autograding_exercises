# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_024_fehlversuche.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_024_fehlversuche

"""Aufgabe 2_024 – Fehlversuche                                  Stufe 2 ★★☆☆☆

Viele fehlgeschlagene Anmeldungen hintereinander können bedeuten, dass
jemand Passwörter durchprobiert. Die IT-Sicherheit eines Unternehmens
wertet deshalb jede Woche aus, wie oft sich jemand vergeblich angemeldet
hat. Das Anmeldesystem liefert eine Liste der Benutzernamen und eine
Liste von Listen: Zeile i gehört zum Benutzer an Stelle i, Spalte j
zum Tag j + 1 der Woche.

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

Grenzen: benutzer hat 0 bis 1000 Einträge, nicht leere Texte aus
Kleinbuchstaben ohne Wiederholung. versuche hat genauso viele Zeilen
wie benutzer, alle Zeilen sind gleich lang mit 1 bis 31 Einträgen, ganze
Zahlen von 0 bis 1000. grenze ist eine ganze Zahl von 0 bis 1000. Die
Listen bleiben unverändert.

Hintergrund: Diese Übung verbindet die letzten Aufgaben. versuche ist
eine Liste von Listen (Aufgabe 2_020): versuche[i][j] ist der Wert in
Zeile i und Spalte j, len(versuche[0]) die Anzahl der Spalten. Mit zip
(Aufgabe 2_022) läuft man durch benutzer und versuche zugleich und hat
so zu jedem Namen seine Zeile; mit enumerate (Aufgabe 2_021) bekommt
man beim Durchlaufen einer Zeile auch die Spaltennummer, mit
enumerate(zeile, start=1) gleich ab 1 gezählt. Tupel vergleicht
Python Element für Element, darum sortiert sorted (Aufgabe 2_023) eine
Liste von Tupeln (name, tag) erst nach dem Namen und bei gleichem Namen
nach dem Tag.
"""


def tagessummen(versuche):
    """Gibt die Summe der Fehlversuche je Tag zurück."""
    if not versuche:
        return []
    summen = [0] * len(versuche[0])
    for zeile in versuche:
        for tag, anzahl in enumerate(zeile):
            summen[tag] = summen[tag] + anzahl
    return summen


def auffaellig(benutzer, versuche, grenze):
    """Gibt (name, tag) für jeden Tag mit mehr als grenze Fehlversuchen zurück, sortiert."""
    treffer = []
    for name, zeile in zip(benutzer, versuche):
        for tag, anzahl in enumerate(zeile, start=1):
            if anzahl > grenze:
                treffer.append((name, tag))
    return sorted(treffer)


benutzer = ["mkoch", "aberg", "tlang"]
versuche = [
    [0, 2, 0, 1, 0],
    [7, 0, 0, 12, 1],
    [0, 0, 3, 0, 0],
]
print(tagessummen(versuche))
print(auffaellig(benutzer, versuche, 2))


# Idee: tagessummen legt eine Liste mit einer 0 je Tag an (so viele, wie die erste Zeile Einträge hat)
# und addiert jede Zeile Spalte für Spalte dazu; enumerate(zeile) liefert dabei den Index des Tages.
# auffaellig läuft mit zip(benutzer, versuche) durch Namen und Zeilen zugleich, mit
# enumerate(zeile, start=1) durch die Tage und sammelt (name, tag), wenn anzahl > grenze ist. sorted
# ordnet die Tupel zum Schluss nach Namen und dann nach Tag.
#
# Anderer Weg: tagessummen über die Spalten: für jeden Index j die Summe von zeile[j] über alle Zeilen,
# oder kurz [sum(spalte) for spalte in zip(*versuche)], was erst später erklärt wird. In auffaellig geht
# auch for i in range(len(benutzer)) mit benutzer[i] und versuche[i].
#
# Typische Fehler: Zeilen- statt Spaltensummen bilden, bei leerer Liste versuche[0] lesen (IndexError),
# die Tage ab 0 zählen, >= statt > oder das Sortieren vergessen. versuche.sort() in der Funktion würde
# außerdem die Liste des Aufrufers durcheinanderbringen.
