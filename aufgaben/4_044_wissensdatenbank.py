"""Aufgabe 4_044 – Wissensdatenbank                              Stufe 4 ★★★★☆

Der Service-Desk pflegt eine Wissensdatenbank: kurze Artikel, die
erklären, wie man häufige Probleme selbst löst, etwa „VPN-Verbindung
bricht ab“ oder „Drucker neu einrichten“. Jeder Artikel gehört zu
einer Kategorie und zählt mit, wie oft er aufgerufen wurde. Außerdem
protokolliert die Suche jeden Suchbegriff in der Reihenfolge, in der er
eingegeben wurde. Sucht jemand mehrmals direkt hintereinander dasselbe,
hat er offenbar nichts Passendes gefunden; dort fehlt ein Artikel.
Schreiben Sie mit itertools.groupby drei Funktionen:

- `kategorien(artikel)` bekommt eine Liste von Dictionaries mit den
  Schlüsseln "kategorie", "titel" und "aufrufe" in beliebiger
  Reihenfolge und gibt eine Liste von Tupeln (kategorie, anzahl der
  Artikel, summe der aufrufe) zurück, alphabetisch nach Kategorie.
- `meistgelesen(artikel)` gibt ein Dictionary zurück, das jeder
  Kategorie den Titel ihres am häufigsten aufgerufenen Artikels
  zuordnet; bei Gleichstand den alphabetisch ersten Titel.
- `wiederholte_suchen(protokoll)` bekommt die Liste der Suchbegriffe und
  gibt für jede Stelle, an der derselbe Begriff mindestens zweimal
  direkt hintereinander steht, ein Tupel (begriff, anzahl) zurück, in
  der Reihenfolge des Protokolls. Kommt ein Begriff später noch einmal
  so vor, steht er noch einmal da.

Die übergebenen Listen bleiben unverändert.

    artikel = [
        {"kategorie": "VPN", "titel": "Verbindung bricht ab", "aufrufe": 120},
        {"kategorie": "Drucker", "titel": "Treiber installieren", "aufrufe": 40},
        {"kategorie": "VPN", "titel": "Zertifikat erneuern", "aufrufe": 75},
    ]
    kategorien(artikel)    →  [("Drucker", 1, 40), ("VPN", 2, 195)]
    meistgelesen(artikel)  →  {"Drucker": "Treiber installieren",
                               "VPN": "Verbindung bricht ab"}
    wiederholte_suchen(["vpn", "vpn", "drucker", "vpn", "wlan", "wlan", "wlan"])
        →  [("vpn", 2), ("wlan", 3)]

Grenzen: artikel hat 0 bis 100 000 Einträge; kategorie und titel sind
nicht leere Texte, die Titel einer Kategorie sind verschieden, aufrufe
ist eine ganze Zahl von 0 bis 10**6. protokoll hat 0 bis 100 000
Einträge, nicht leere Texte; Groß- und Kleinschreibung zählt.

Hintergrund: itertools.groupby(iterable, key) fasst aufeinanderfolgende
Werte mit gleichem Schlüssel zusammen. Es liefert Paare (schluessel,
gruppe); gruppe ist ein Iterator über die Werte dieser Gruppe. Ohne key
ist der Wert selbst der Schlüssel:

    from itertools import groupby

    for zeichen, gruppe in groupby("aaabcc"):
        print(zeichen, len(list(gruppe)))      # a 3, b 1, c 2

Wichtig: groupby schaut nur auf direkte Nachbarn. Kommt derselbe
Schlüssel später noch einmal, beginnt eine neue Gruppe:
groupby("aabaa") hat die Gruppen "aa", "b" und "aa". Genau das will man
bei Läufen (wie bei der Lauflängenkodierung in Aufgabe 3_022). Will man
dagegen alle Werte mit gleichem Schlüssel in einer Gruppe, muss man
vorher nach demselben Schlüssel sortieren:

    zeilen = [("Ulm", 3), ("Kiel", 5), ("Ulm", 1)]
    nach_ort = lambda zeile: zeile[0]
    for ort, gruppe in groupby(sorted(zeilen, key=nach_ort), key=nach_ort):
        print(ort, sum(wert for _, wert in gruppe))    # Kiel 5, Ulm 4

Sortiert man nach mehr als dem Schlüssel, etwa mit key=lambda z: (z[0],
-z[1]), stehen die Gruppen trotzdem zusammen, und innerhalb jeder Gruppe
gilt die zweite Ordnung; next(gruppe) holt dann gleich das erste
Element. Eine Gruppe lässt sich nur einmal durchlaufen, und nur so
lange, bis groupby zur nächsten weitergeht. Braucht man sie später
noch, macht man sofort list(gruppe) daraus.
"""

from itertools import groupby


def kategorien(artikel):
    """Gibt (kategorie, anzahl, aufrufe) je Kategorie alphabetisch zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def meistgelesen(artikel):
    """Gibt je Kategorie den Titel des meistgelesenen Artikels zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def wiederholte_suchen(protokoll):
    """Gibt (begriff, anzahl) für jede direkte Wiederholung eines Suchbegriffs zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


artikel = [
    {"kategorie": "VPN", "titel": "Verbindung bricht ab", "aufrufe": 120},
    {"kategorie": "Drucker", "titel": "Treiber installieren", "aufrufe": 40},
    {"kategorie": "VPN", "titel": "Zertifikat erneuern", "aufrufe": 75},
]
print(kategorien(artikel))
print(meistgelesen(artikel))
print(wiederholte_suchen(["vpn", "vpn", "drucker", "vpn", "wlan", "wlan", "wlan"]))
