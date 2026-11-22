"""Aufgabe 4_052 – Wartungsfenster                               Stufe 4 ★★★★☆

Der IT-Service einer Firma betreibt eine Statusseite, auf der alle
Beschäftigten sehen, ob ein Dienst (E-Mail, VPN, Drucker …) läuft. Sie
ist ein Dictionary: Dienst → Status, etwa "in Betrieb" oder "Störung".
Während einer Wartung soll dort "Wartung" stehen, damit niemand ein
Ticket wegen einer geplanten Unterbrechung aufmacht. Außerdem darf ein
Ticket immer nur von einer Person zugleich bearbeitet werden. Schreiben
Sie mit contextlib.contextmanager zwei Kontextmanager als
Generatorfunktionen:

- `wartung(statusseite, dienst, protokoll)`: Beim Betreten setzt er den
  Status des Diensts auf "Wartung" und hängt ("beginn", dienst) an die
  Liste protokoll an; der with-Block bekommt nichts (as liefert None).
  Beim Verlassen steht wieder der alte Status da (fehlte der Dienst
  vorher, wird er entfernt), und im protokoll steht ("ende", dienst),
  nach einer Ausnahme stattdessen ("abbruch", dienst, str(fehler)). Die
  Ausnahme fliegt danach weiter.
- `bearbeitung(ticket, person)`: ticket ist ein Dictionary mit den
  Schlüsseln "nummer", "bearbeiter" (None, wenn niemand es gerade
  bearbeitet) und "notizen" (eine Liste von Texten). Ist das Ticket schon
  in Bearbeitung, löst bearbeitung beim Betreten einen RuntimeError aus,
  dessen Meldung den Namen der bearbeitenden Person nennt, und ändert
  nichts. Sonst trägt es person als Bearbeiter ein und gibt dem
  with-Block das Ticket. Beim Verlassen ist "bearbeiter" wieder None;
  nach einer Ausnahme hängt es vorher den Text "Abbruch: " mit der
  Fehlermeldung an die Notizen an und lässt die Ausnahme weiterfliegen.

    statusseite = {"VPN": "in Betrieb"}
    protokoll = []
    with wartung(statusseite, "VPN", protokoll):
        statusseite["VPN"]       →  "Wartung"
    statusseite                  →  {"VPN": "in Betrieb"}
    protokoll                    →  [("beginn", "VPN"), ("ende", "VPN")]

    ticket = {"nummer": 4711, "bearbeiter": None, "notizen": []}
    with bearbeitung(ticket, "Kim") as t:
        t["bearbeiter"]          →  "Kim"
        t["notizen"].append("Drucker neu gestartet")
    ticket["bearbeiter"]         →  None

Grenzen: statusseite hat 0 bis 1000 Einträge, dienst ist ein nicht
leerer Text. person ist ein nicht leerer Text. Wartungen und
Bearbeitungen dürfen verschachtelt werden (zwei Dienste zugleich, ein
Ticket bearbeiten während einer Wartung).

Hintergrund: In Aufgabe 4_051 haben Sie Kontextmanager als Klassen mit
__enter__ und __exit__ geschrieben. Oft geht es kürzer mit dem
Dekorator contextlib.contextmanager über einer Generatorfunktion
(Generatoren kennen Sie aus Aufgabe 3_022):

    from contextlib import contextmanager

    @contextmanager
    def eingerueckt(zeilen):
        zeilen.append("Anfang")            # wie __enter__
        try:
            yield len(zeilen)              # das bekommt as
        except Exception as fehler:
            zeilen.append(f"Abbruch: {fehler}")
            raise                          # weiterfliegen lassen
        else:
            zeilen.append("Ende")          # nur ohne Fehler
        finally:
            zeilen.append("aufgeräumt")    # immer

Alles vor dem yield läuft beim Betreten, der Wert hinter yield landet
hinter as (ein yield ohne Wert liefert None), dann läuft der with-Block.
Danach geht es hinter dem yield weiter. Löst der Block eine Ausnahme
aus, wirft Python sie genau an der Stelle des yield in den Generator
hinein. Darum steht das yield in einem try: In except reagiert man auf
den Fehler, in finally räumt man in jedem Fall auf. Ohne try würde der
Code hinter dem yield bei einem Fehler gar nicht laufen. Fängt man die
Ausnahme mit except und löst sie nicht mit raise neu aus, gilt sie als
verschluckt. Der Generator muss genau einmal yield erreichen. Löst er
vor dem yield eine Ausnahme aus, beginnt der with-Block gar nicht.
"""

from contextlib import contextmanager


@contextmanager
def wartung(statusseite, dienst, protokoll):
    """Zeigt für die Dauer des with-Blocks "Wartung" an und protokolliert Beginn und Ende."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


@contextmanager
def bearbeitung(ticket, person):
    """Sperrt das Ticket für die Dauer des with-Blocks für eine Person."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


statusseite = {"VPN": "in Betrieb"}
protokoll = []
with wartung(statusseite, "VPN", protokoll):
    print(statusseite["VPN"])
print(statusseite)
print(protokoll)

ticket = {"nummer": 4711, "bearbeiter": None, "notizen": []}
with bearbeitung(ticket, "Kim") as t:
    print(t["bearbeiter"])
    t["notizen"].append("Drucker neu gestartet")
print(ticket)
