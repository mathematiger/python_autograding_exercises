# Automatisch erzeugt aus lehrkraft/muster/5_037_ansichten.py - nicht von Hand ändern.
# vorlage-hash: 65800f59f49f0b86
# text-hash: c4426a1c32304c7d
# thema: texte_zahlen
# inhalt: pickle mit __getstate__/__setstate__

import pickle
import sys

# pruefe.py führt Ihr Programm in einem eigenen Namensraum aus und nicht als Modul __main__. Damit
# pickle die Klasse wie sonst über ihr Modul und ihren Namen findet, wird sie dort eingetragen.
setattr(sys.modules[Ansicht.__module__], "Ansicht", Ansicht)


def beispiel():
    """Die Ansicht aus dem Aufgabentext mit einem lambda als Rückruf und einem Filter."""
    ansicht = Ansicht("Offene Aufträge", ["auftrag", "status", "standort"])
    ansicht.beobachten(lambda a: None)
    ansicht.filtern("status", "offen")
    return ansicht


def hin_und_zurueck(ansicht):
    """Speichert und lädt die Ansicht mit pickle; ein Fehler wird als Text zurückgegeben."""
    try:
        return pickle.loads(pickle.dumps(ansicht))
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def aus_zustand(zustand):
    """Legt eine leere Ansicht ohne __init__ an und ruft __setstate__ auf; Fehler als Text."""
    ansicht = Ansicht.__new__(Ansicht)
    try:
        ansicht.__setstate__(zustand)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"
    return ansicht


def beschreibung(ansicht):
    """Titel, Spalten, Filter und Rückrufe einer Ansicht als Tupel, oder der Text, wenn es keine ist."""
    if not isinstance(ansicht, Ansicht):
        return ansicht
    return (
        getattr(ansicht, "titel", "(fehlt)"),
        getattr(ansicht, "spalten", "(fehlt)"),
        getattr(ansicht, "filter", "(fehlt)"),
        getattr(ansicht, "beobachter", "(fehlt)"),
    )


# Eine Ansicht ohne Rückruf lässt sich speichern und laden
ansicht = Ansicht("Tickets", ["nummer", "betreff"])
kopie = hin_und_zurueck(ansicht)
assert beschreibung(kopie)[:3] == ("Tickets", ["nummer", "betreff"], {}), (
    f"Eine Ansicht ohne Rückruf ergibt nach dem Laden {beschreibung(kopie)[:3]!r},\n"
    "erwartet war ('Tickets', ['nummer', 'betreff'], {})."
)

# Eine Ansicht mit lambda-Rückruf lässt sich speichern
ansicht = beispiel()
kopie = hin_und_zurueck(ansicht)
assert isinstance(kopie, Ansicht), (
    f"pickle.dumps(ansicht) mit einem lambda als Rückruf ergibt {kopie}.\n"
    "Tipp: __getstate__ gibt ein Dictionary ohne beobachter zurück, dann speichert pickle das lambda nicht mit."
)

# Nach dem Laden stimmen Titel, Spalten und Filter
assert beschreibung(kopie)[:3] == ("Offene Aufträge", ["auftrag", "status", "standort"], {"status": "offen"}), (
    f"Nach dem Laden hat die Ansicht Titel, Spalten und Filter {beschreibung(kopie)[:3]!r},\n"
    "erwartet war ('Offene Aufträge', ['auftrag', 'status', 'standort'], {'status': 'offen'})."
)

# Nach dem Laden ist beobachter eine leere Liste
assert getattr(kopie, "beobachter", None) == [], (
    f"Nach dem Laden ist beobachter {getattr(kopie, 'beobachter', '(fehlt)')!r}, erwartet war [].\n"
    "Tipp: __init__ läuft beim Laden nicht; setzen Sie self.beobachter = [] in __setstate__."
)

# Die geladene Ansicht funktioniert: filtern und beobachten gehen
try:
    gemeldet = []
    kopie.beobachten(lambda a: gemeldet.append(a.filter.copy()))
    kopie.filtern("standort", "Köln")
except Exception as fehler:
    gemeldet = f"{type(fehler).__name__}: {fehler}"
assert gemeldet == [{"status": "offen", "standort": "Köln"}], (
    f"Nach dem Laden meldet ein neuer Rückruf beim Filtern {gemeldet!r}, erwartet war [{{'status': 'offen', 'standort': 'Köln'}}]."
)

# Das Speichern lässt die Rückrufe am Original stehen
ansicht = beispiel()
hin_und_zurueck(ansicht)
assert len(getattr(ansicht, "beobachter", [])) == 1 and hasattr(ansicht, "beobachter"), (
    f"Nach pickle.dumps(ansicht) hat das Original beobachter {getattr(ansicht, 'beobachter', '(fehlt)')!r},\n"
    "erwartet war weiter ein Rückruf.\nTipp: Löschen Sie nichts aus self.__dict__; geben Sie ein neues Dictionary zurück."
)

# __getstate__ liefert genau version, titel, spalten und filter
zustand = beispiel().__getstate__()
assert isinstance(zustand, dict) and sorted(zustand) == ["filter", "spalten", "titel", "version"], (
    f"__getstate__() ergibt {zustand!r}, erwartet war ein Dictionary mit den Schlüsseln version, titel, spalten, filter."
)

# __getstate__ trägt die Version 2 ein
assert zustand.get("version") == 2, f"__getstate__()['version'] ist {zustand.get('version')!r}, erwartet war 2."

# __getstate__ gibt neue Listen und Dictionaries zurück, nicht die des Objekts
ansicht = beispiel()
zustand = ansicht.__getstate__()
zustand["spalten"].append("extra")
zustand["filter"]["extra"] = "x"
assert ansicht.spalten == ["auftrag", "status", "standort"] and ansicht.filter == {"status": "offen"}, (
    f"Wer den Zustand aus __getstate__ ändert, ändert die Ansicht mit: spalten {ansicht.spalten}, filter {ansicht.filter}.\n"
    "Tipp: list(self.spalten) und dict(self.filter) legen Kopien an."
)

# Ein Zustand der Version 2 wird wiederhergestellt
ansicht = aus_zustand({"version": 2, "titel": "Rechnungen", "spalten": ["nummer", "summe"], "filter": {"jahr": "2026"}})
assert beschreibung(ansicht)[:3] == ("Rechnungen", ["nummer", "summe"], {"jahr": "2026"}), (
    f"__setstate__ mit einem Zustand der Version 2 ergibt {beschreibung(ansicht)[:3]!r},\n"
    "erwartet war ('Rechnungen', ['nummer', 'summe'], {'jahr': '2026'})."
)

# Ein Zustand der Version 1: spalten als Text mit Kommas
ansicht = aus_zustand({"titel": "Lager", "spalten": "artikel,menge", "filter": {}})
assert beschreibung(ansicht)[:3] == ("Lager", ["artikel", "menge"], {}), (
    f"__setstate__ mit dem alten Zustand {{'titel': 'Lager', 'spalten': 'artikel,menge', 'filter': {{}}}} ergibt "
    f"{beschreibung(ansicht)[:3]!r},\nerwartet war ('Lager', ['artikel', 'menge'], {{}}).\n"
    "Tipp: Fehlt der Schlüssel version, zerlegen Sie spalten mit split(\",\")."
)

# Version 1 mit einer einzigen Spalte
ansicht = aus_zustand({"titel": "Kurz", "spalten": "nummer", "filter": {"a": "b"}})
assert beschreibung(ansicht)[:3] == ("Kurz", ["nummer"], {"a": "b"}), f"Version 1 mit spalten 'nummer' ergibt {beschreibung(ansicht)[:3]!r}."

# Randfall Version 1: der leere Text heißt keine Spalte
ansicht = aus_zustand({"titel": "Leer", "spalten": "", "filter": {}})
assert beschreibung(ansicht)[:3] == ("Leer", [], {}), (
    f"Version 1 mit spalten '' ergibt {beschreibung(ansicht)[:3]!r}, erwartet war ('Leer', [], {{}}).\n"
    "Tipp: ''.split(',') ist [''], eine Liste mit einem leeren Text."
)

# Randfall Version 2: keine Spalten und keine Filter, über pickle
kopie = hin_und_zurueck(Ansicht("", []))
assert beschreibung(kopie)[:3] == ("", [], {}), f"Ansicht('', []) ergibt nach dem Laden {beschreibung(kopie)[:3]!r}."

# Spalten mit Leerzeichen bleiben, wie sie sind
kopie = hin_und_zurueck(Ansicht("x", [" a ", "b c"]))
assert beschreibung(kopie)[1] == [" a ", "b c"], f"Die Spalten [' a ', 'b c'] werden nach dem Laden zu {beschreibung(kopie)[1]!r}."

# Die Ausgabe des Programms
erwartet = "neu zeichnen: Offene Aufträge\n2 ['auftrag', 'status', 'standort'] {'status': 'offen'} [] 1\n['artikel', 'menge']"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Ansichten
zufall = Zufall(5037)
woerter = ["auftrag", "status", "standort", "kunde", "summe", "Köln", "offen", "a b", ""]
for _ in range(200):
    spalten = [zufall.choice(woerter[:-1]) for _ in range(zufall.randint(0, 6))]
    ansicht = Ansicht(zufall.choice(woerter), spalten)
    for _ in range(zufall.randint(0, 3)):
        ansicht.beobachten(lambda a: None)
    for _ in range(zufall.randint(0, 4)):
        ansicht.filtern(zufall.choice(woerter), zufall.choice(woerter))
    kopie = hin_und_zurueck(ansicht)
    erwartet = (ansicht.titel, ansicht.spalten, ansicht.filter, [])
    assert beschreibung(kopie) == erwartet, f"Nach dem Laden ergibt die Ansicht {beschreibung(kopie)!r}, erwartet war {erwartet!r}."
    nicht_leer = [spalte for spalte in spalten if spalte != ""]
    alt = aus_zustand({"titel": "alt", "spalten": ",".join(nicht_leer), "filter": dict(ansicht.filter)})
    assert beschreibung(alt) == ("alt", nicht_leer, ansicht.filter, []), (
        f"Version 1 mit spalten {','.join(nicht_leer)!r} ergibt {beschreibung(alt)!r}."
    )

# Obere Grenze: 1000 Spalten und 10 000 Filter
ansicht = Ansicht("groß", [f"spalte{n}" for n in range(1000)])
for n in range(10000):
    ansicht.filter[f"feld{n}"] = str(n)
ansicht.beobachten(lambda a: None)
kopie = hin_und_zurueck(ansicht)
assert beschreibung(kopie)[:3] == ("groß", ansicht.spalten, ansicht.filter), "Bei 1000 Spalten und 10 000 Filtern stimmt die geladene Ansicht nicht."
