"""Aufgabe 5_037 – Ansichten                                     Stufe 5 ★★★★★

Eine Verwaltungsoberfläche zeigt Tabellen, etwa alle offenen Aufträge.
Jede Nutzerin kann sich Ansichten zusammenstellen: welche Spalten in
welcher Reihenfolge erscheinen und welche Filter gelten (status = offen,
standort = Köln). Andere Teile der Oberfläche melden sich mit
beobachten(rueckruf) bei einer Ansicht an; ändert sich ein Filter, ruft
die Ansicht jeden Rückruf mit sich selbst auf, und die Tabelle, der
Zähler im Menü und die Exportschaltfläche zeichnen sich neu.

Beim Abmelden soll die Oberfläche alle Ansichten mit pickle speichern
und beim nächsten Anmelden wieder laden. Das geht so noch nicht: Die
Rückrufe sind oft lambda-Ausdrücke, und die kann pickle nicht speichern.
Sie gehören auch nicht in die Datei, denn nach dem Laden melden sich die
Teile der Oberfläche neu an. Außerdem liegen noch Dateien der alten
Version 1 herum, in der die Spalten als ein Text mit Kommas gespeichert
waren ("auftrag,status") und es noch keine Versionsnummer gab.
Ergänzen Sie in der Klasse `Ansicht`:

- `__getstate__(self)` gibt ein neues Dictionary mit den Schlüsseln
  version (immer 2), titel, spalten und filter zurück, ohne beobachter.
  Das Objekt selbst bleibt dabei unverändert, auch seine Rückrufe.
- `__setstate__(self, zustand)` stellt die Ansicht aus einem solchen
  Dictionary wieder her, mit einer leeren Liste beobachter. Fehlt der
  Schlüssel version, stammt der Zustand aus Version 1: spalten ist dann
  ein Text mit Kommas, den Sie in eine Liste zerlegen; der leere Text
  heißt keine Spalte.

    ansicht = Ansicht("Offene Aufträge", ["auftrag", "status", "standort"])
    ansicht.beobachten(lambda a: print("neu zeichnen:", a.titel))
    ansicht.filtern("status", "offen")         # gibt aus: neu zeichnen: Offene Aufträge
    daten = pickle.dumps(ansicht)               # ohne __getstate__: PicklingError
    kopie = pickle.loads(daten)
    kopie.spalten, kopie.filter, kopie.beobachter
    →  (['auftrag', 'status', 'standort'], {'status': 'offen'}, [])
    len(ansicht.beobachter)                     →  1

    alt = Ansicht.__new__(Ansicht)
    alt.__setstate__({"titel": "Lager", "spalten": "artikel,menge", "filter": {}})
    alt.spalten                                 →  ['artikel', 'menge']

Grenzen: titel ist ein Text, spalten eine Liste von 0 bis 1000 Texten
ohne Komma, filter ein Dictionary mit 0 bis 10 000 Paaren aus Texten.
Ein Zustand der Version 1 hat genau die Schlüssel titel, spalten und
filter, einer der Version 2 genau die vier Schlüssel aus __getstate__.

Hintergrund: pickle speichert fast jedes Python-Objekt als Folge von
Bytes und baut es später wieder auf, auch Listen von Objekten eigener
Klassen mit allen Verweisen dazwischen:

    import pickle

    daten = pickle.dumps({"liste": [1, 2], "menge": {3}})   # bytes
    pickle.loads(daten)                                     # {'liste': [1, 2], 'menge': {3}}
    with open("stand.pkl", "wb") as datei:                  # Bytes: Modus "wb", kein encoding
        pickle.dump(objekt, datei)

Bei einem Objekt einer eigenen Klasse speichert pickle nur den Namen der
Klasse und den Zustand, normalerweise self.__dict__. Beim Laden legt es
das Objekt mit cls.__new__(cls) an, ohne __init__ aufzurufen, und
schreibt den Zustand wieder hinein. Funktionen speichert pickle nur als
Verweis über ihren Namen im Modul; ein lambda oder eine Funktion, die
in einer anderen Funktion steht, hat keinen solchen Namen und führt zu
einem PicklingError (oder AttributeError). Ebenso wenig lassen sich
offene Dateien, Locks oder Verbindungen speichern.

Was gespeichert wird, bestimmt die Klasse selbst. pickle ruft
__getstate__() auf und speichert dessen Rückgabe; beim Laden ruft es
__setstate__(zustand) auf dem neuen, leeren Objekt auf:

    class Verbindung:
        def __init__(self, host):
            self.host = host
            self.socket = oeffne(host)          # nicht speicherbar

        def __getstate__(self):
            zustand = self.__dict__.copy()      # eine Kopie, nicht __dict__ selbst
            del zustand["socket"]
            return zustand

        def __setstate__(self, zustand):
            self.__dict__.update(zustand)
            self.socket = oeffne(self.host)     # beim Laden neu aufbauen

Wer in __getstate__ direkt aus self.__dict__ löscht, zerstört das
Objekt, das gerade gespeichert wird. Weil gespeicherte Daten älter sein
können als der Code, legt man eine Versionsnummer in den Zustand;
__setstate__ erkennt daran alte Zustände und rechnet sie um. Seit
Python 3.11 hat jedes Objekt ein __getstate__, das ohne eigene Fassung
das __dict__ liefert. copy.copy und copy.deepcopy benutzen dieselben
beiden Methoden. Und eine Warnung: pickle.loads kann beim Laden
beliebigen Code ausführen. Laden Sie nie Pickle-Daten aus einer Quelle,
der Sie nicht trauen; für den Austausch mit anderen ist json der
sichere Weg.
"""


class Ansicht:
    """Eine gespeicherte Tabellenansicht mit Spalten, Filtern und angemeldeten Rückrufen."""

    def __init__(self, titel, spalten):
        """Legt die Ansicht ohne Filter und ohne Rückrufe an."""
        self.titel = titel
        self.spalten = list(spalten)
        self.filter = {}
        self.beobachter = []

    def beobachten(self, rueckruf):
        """Meldet einen Rückruf an, der bei jeder Änderung mit der Ansicht aufgerufen wird."""
        self.beobachter.append(rueckruf)

    def filtern(self, spalte, wert):
        """Setzt einen Filter und benachrichtigt alle Rückrufe."""
        self.filter[spalte] = wert
        for rueckruf in self.beobachter:
            rueckruf(self)

    def __getstate__(self):
        """Gibt den speicherbaren Zustand mit Versionsnummer zurück, ohne die Rückrufe."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __setstate__(self, zustand):
        """Stellt die Ansicht aus einem Zustand der Version 1 oder 2 wieder her, ohne Rückrufe."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


ansicht = Ansicht("Offene Aufträge", ["auftrag", "status", "standort"])
ansicht.beobachten(lambda a: print("neu zeichnen:", a.titel))
ansicht.filtern("status", "offen")
# pickle.dumps(ansicht) speichert genau das, was __getstate__ liefert, und pickle.loads legt mit
# Ansicht.__new__ ein leeres Objekt an und ruft __setstate__ auf. Hier ohne Datei von Hand:
zustand = ansicht.__getstate__()
kopie = Ansicht.__new__(Ansicht)
kopie.__setstate__(zustand)
print(zustand["version"], kopie.spalten, kopie.filter, kopie.beobachter, len(ansicht.beobachter))
alt = Ansicht.__new__(Ansicht)
alt.__setstate__({"titel": "Lager", "spalten": "artikel,menge", "filter": {}})
print(alt.spalten)
