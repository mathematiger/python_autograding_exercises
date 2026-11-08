# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_031_alarmauswertung.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_031_alarmauswertung

"""Aufgabe 2_031 – Alarmauswertung                               Stufe 2 ★★☆☆☆

Ein Monitoring-System überwacht die Server eines Unternehmens und
schreibt bei jedem Problem eine Alarmmeldung. Jede Meldung ist ein
Dictionary mit dem Namen des Servers (Host) und einem Fehlercode,
etwa {"host": "web01", "code": "DISK_FULL"}. Für die Frühbesprechung
des Betriebsteams sollen drei Fragen beantwortet werden. Schreiben Sie
drei Funktionen:

- `alarme_je_host(meldungen)` gibt ein Dictionary zurück, das jedem
  Host die Anzahl seiner Meldungen zuordnet. Hosts ohne Meldung
  kommen nicht vor.
- `neue_codes(gestern, heute)` gibt die Fehlercodes, die heute
  mindestens einmal vorkamen, gestern aber nie, als alphabetisch
  sortierte Liste ohne Doppelte zurück.
- `kritischster_host(meldungen, gewichte)` gibt den Host mit der
  höchsten Summe der Gewichte seiner Meldungen zurück. gewichte ordnet
  manchen Codes ein Gewicht zu; ein Code, der dort fehlt, zählt 1.
  Haben mehrere Hosts dieselbe höchste Summe, gewinnt der alphabetisch
  kleinste Name.

    gestern = [{"host": "web01", "code": "CPU_HIGH"}]
    heute = [
        {"host": "web01", "code": "CPU_HIGH"},
        {"host": "db01", "code": "DISK_FULL"},
        {"host": "web01", "code": "TIMEOUT"},
        {"host": "db01", "code": "TIMEOUT"},
    ]
    alarme_je_host(heute)                       →  {"web01": 2, "db01": 2}
    neue_codes(gestern, heute)                  →  ["DISK_FULL", "TIMEOUT"]
    kritischster_host(heute, {"DISK_FULL": 5})  →  "db01"   (5 + 1 gegen 1 + 1)

Grenzen: Jede Liste hat 0 bis 10 000 Meldungen, bei kritischster_host
mindestens eine. Host und Code sind nicht leere Texte aus
Großbuchstaben, Kleinbuchstaben, Ziffern und Unterstrichen. gewichte
hat 0 bis 100 Einträge, jedes Gewicht ist eine ganze Zahl von 1 bis
100. Die übergebenen Listen und Dictionaries bleiben unverändert.

Hintergrund: Diese Übung verbindet die letzten Aufgaben. Jede Meldung
ist ein Dictionary als Datensatz (Aufgabe 2_027), meldung["host"]
liefert den Host. Zum Zählen ordnet ein Dictionary jedem Schlüssel
seinen Zähler zu (Aufgabe 2_025); mit zaehler.get(host, 0) bekommt man
für einen neuen Schlüssel 0 statt eines KeyError (Aufgabe 2_026), genauso
liefert gewichte.get(code, 1) für einen fehlenden Code 1. Eine Menge
(Aufgabe 2_028) enthält jeden Code nur einmal; neben Schnitt & und
Vereinigung | gibt es die Differenz: a - b enthält die Elemente von a,
die nicht in b sind, also {"x", "y"} - {"y"} ergibt {"x"}. sorted(menge)
macht daraus eine sortierte Liste. Für den Vergleich bei gleicher Summe
hilft, dass man Texte mit < alphabetisch vergleichen kann:
"db01" < "web01" ist True.
"""


def alarme_je_host(meldungen):
    """Gibt zu jedem Host die Anzahl seiner Meldungen zurück."""
    anzahl = {}
    for meldung in meldungen:
        host = meldung["host"]
        anzahl[host] = anzahl.get(host, 0) + 1
    return anzahl


def neue_codes(gestern, heute):
    """Gibt die Codes, die heute vorkamen und gestern nicht, sortiert zurück."""
    alte = set()
    for meldung in gestern:
        alte.add(meldung["code"])
    aktuelle = set()
    for meldung in heute:
        aktuelle.add(meldung["code"])
    return sorted(aktuelle - alte)


def kritischster_host(meldungen, gewichte):
    """Gibt den Host mit der höchsten Summe der Gewichte zurück, bei Gleichstand den alphabetisch kleinsten."""
    summen = {}
    for meldung in meldungen:
        host = meldung["host"]
        summen[host] = summen.get(host, 0) + gewichte.get(meldung["code"], 1)
    bester = None
    for host, summe in summen.items():
        if bester is None or summe > summen[bester] or (summe == summen[bester] and host < bester):
            bester = host
    return bester


gestern = [{"host": "web01", "code": "CPU_HIGH"}]
heute = [
    {"host": "web01", "code": "CPU_HIGH"},
    {"host": "db01", "code": "DISK_FULL"},
    {"host": "web01", "code": "TIMEOUT"},
    {"host": "db01", "code": "TIMEOUT"},
]
print(alarme_je_host(heute))
print(neue_codes(gestern, heute))
print(kritischster_host(heute, {"DISK_FULL": 5}))


# Idee: alarme_je_host zählt mit einem Dictionary und get(host, 0) + 1. neue_codes sammelt die Codes beider
# Tage in zwei Mengen, die Differenz heute - gestern enthält genau die neuen, sorted macht daraus eine Liste.
# kritischster_host summiert wie beim Zählen, nur mit gewichte.get(code, 1) statt 1, und sucht dann in einer
# Schleife über summen.items() den besten Host; bei gleicher Summe gewinnt der kleinere Name.
#
# Anderer Weg: Für den besten Host alle Hosts zuerst mit sorted(summen) alphabetisch ordnen und dann den ersten
# mit der größten Summe nehmen (max(summen.values()) liefert sie). Die Mengen kann man auch mit
# set(liste) aus einer Liste der Codes bauen oder neue Codes mit not in prüfen.
#
# Typische Fehler: anzahl[host] += 1 ohne get (KeyError beim ersten Mal), gewichte[code] statt
# gewichte.get(code, 1) (KeyError bei fehlendem Code), die neuen Codes als Liste mit Doppelten oder unsortiert
# zurückgeben, gestern - heute statt heute - gestern, oder bei Gleichstand den zuerst gefundenen Host nehmen.
