# Automatisch erzeugt aus lehrkraft/muster/5_022_backlog.py - nicht von Hand ändern.
# vorlage-hash: d7fcfb89fa5b24df
# text-hash: ae17bbcedfc897cb
# thema: datenstrukturen
# inhalt: Eigenes Dictionary

def normal(kennung):
    """Normalisiert eine Kennung wie verlangt."""
    return kennung.strip().upper()


def ausnahme_bei(aktion):
    """Führt aktion() aus und liefert den Namen der Ausnahme oder "keine"."""
    try:
        aktion()
    except Exception as fehler:
        return type(fehler).__name__
    return "keine"


def lesen(backlog, kennung):
    """Liefert backlog[kennung] oder den Namen der ausgelösten Ausnahme."""
    try:
        return backlog[kennung]
    except Exception as fehler:
        return type(fehler).__name__


def inhalt(backlog):
    """Die Einträge als Liste von Paaren über __iter__ und __getitem__, ohne geerbte Methoden."""
    return [(kennung, backlog[kennung]) for kennung in backlog]


# Speichern und Lesen mit derselben Kennung
backlog = Backlog()
backlog["PROJ-1"] = 5
assert backlog["PROJ-1"] == 5 and len(backlog) == 1, (
    f"Nach backlog['PROJ-1'] = 5 erwartet backlog['PROJ-1'] == 5 und len 1, gefunden {backlog['PROJ-1']!r} und {len(backlog)}."
)

# Lesen mit anders geschriebener Kennung
backlog = Backlog()
backlog["PROJ-1"] = 5
gefunden = [lesen(backlog, kennung) for kennung in ["proj-1", " Proj-1  ", "\tPROJ-1\n"]]
assert gefunden == [5, 5, 5], (
    f"Nach backlog['PROJ-1'] = 5 ergeben backlog['proj-1'], backlog[' Proj-1  '], backlog['\\tPROJ-1\\n'] {gefunden!r}, erwartet war [5, 5, 5].\n"
    "Tipp: Normalisieren Sie die Kennung auch in __getitem__ mit strip() und upper()."
)

# Überschreiben mit anders geschriebener Kennung ergibt keinen zweiten Eintrag
backlog = Backlog()
backlog["proj-1"] = 5
backlog[" PROJ-1 "] = 8
assert inhalt(backlog) == [("PROJ-1", 8)], (
    f"Nach backlog['proj-1'] = 5 und backlog[' PROJ-1 '] = 8 erwartet genau einen Eintrag ('PROJ-1', 8), gefunden {inhalt(backlog)!r}."
)

# Iteration liefert normalisierte Kennungen in der Reihenfolge des ersten Eintrags
backlog = Backlog()
for kennung, punkte in [("web-3", 2), ("App-1", 5), (" WEB-3", 1), ("db-7 ", 13)]:
    backlog[kennung] = punkte
assert inhalt(backlog) == [("WEB-3", 1), ("APP-1", 5), ("DB-7", 13)], (
    "Nach Einträgen für 'web-3', 'App-1', ' WEB-3', 'db-7 ' erwartet [('WEB-3', 1), ('APP-1', 5), ('DB-7', 13)], "
    f"gefunden {inhalt(backlog)!r}."
)

# Löschen mit anders geschriebener Kennung
backlog = Backlog()
backlog["PROJ-1"] = 5
backlog["PROJ-2"] = 3
grund = ausnahme_bei(lambda: backlog.__delitem__(" proj-1"))
assert grund == "keine" and inhalt(backlog) == [("PROJ-2", 3)], (
    f"del backlog[' proj-1'] löst {grund} aus, danach ist der Inhalt {inhalt(backlog)!r}; erwartet war [('PROJ-2', 3)]."
)

# Fehlende Kennungen lösen KeyError aus, beim Lesen und beim Löschen
backlog = Backlog()
backlog["PROJ-1"] = 5
gefunden = (lesen(backlog, "PROJ-2"), ausnahme_bei(lambda: backlog.__delitem__("proj-2")))
assert gefunden == ("KeyError", "KeyError"), (
    f"backlog['PROJ-2'] und del backlog['proj-2'] (fehlt) lösen {gefunden!r} aus, erwartet war jeweils KeyError."
)

# Der Konstruktor nimmt ein Dictionary oder Paare und normalisiert
erstes = Backlog({"proj-1": 5, "PROJ-2": 3, " proj-1": 8})
zweites = Backlog([("a-1", 1), ("A-1 ", 2), ("b-2", 0)])
leer = Backlog()
gefunden = (inhalt(erstes), inhalt(zweites), inhalt(leer))
assert gefunden == ([("PROJ-1", 8), ("PROJ-2", 3)], [("A-1", 2), ("B-2", 0)], []), (
    "Backlog({'proj-1': 5, 'PROJ-2': 3, ' proj-1': 8}), Backlog([('a-1', 1), ('A-1 ', 2), ('b-2', 0)]) und Backlog() "
    f"ergeben {gefunden!r}, erwartet war ([('PROJ-1', 8), ('PROJ-2', 3)], [('A-1', 2), ('B-2', 0)], []).\n"
    "Tipp: Legen Sie in __init__ zuerst self._daten = {} an und rufen Sie dann self.update(eintraege) auf."
)

# Zwei Backlogs teilen sich keinen Speicher
a = Backlog()
b = Backlog()
a["X-1"] = 1
assert len(b) == 0, (
    f"Nach a['X-1'] = 1 hat ein anderes Backlog b {len(b)} Einträge, erwartet 0.\n"
    "Tipp: Legen Sie das Dictionary in __init__ auf self an, nicht als Klassenattribut oder Standardwert."
)

# Ungültige Story Points lösen ValueError aus, der Inhalt bleibt
backlog = Backlog({"PROJ-1": 5})
gefunden = [ausnahme_bei(lambda: backlog.__setitem__("PROJ-1", punkte)) for punkte in [-1, 2.5, "3", True, None]]
assert gefunden == ["ValueError"] * 5 and inhalt(backlog) == [("PROJ-1", 5)], (
    f"backlog['PROJ-1'] = -1, 2.5, '3', True, None lösen {gefunden!r} aus, danach ist der Inhalt {inhalt(backlog)!r}; "
    "erwartet war jeweils ValueError und [('PROJ-1', 5)].\n"
    "Tipp: Prüfen Sie zuerst isinstance(punkte, bool), denn True ist in Python auch ein int."
)

# 0 Story Points sind erlaubt
backlog = Backlog()
grund = ausnahme_bei(lambda: backlog.__setitem__("PROJ-0", 0))
assert grund == "keine" and inhalt(backlog) == [("PROJ-0", 0)], (
    f"backlog['PROJ-0'] = 0 löst {grund} aus, danach ist der Inhalt {inhalt(backlog)!r}; erwartet war [('PROJ-0', 0)]."
)

# Eine Kennung, die kein Text ist: TypeError beim Speichern, KeyError beim Lesen und Löschen
backlog = Backlog({"PROJ-1": 5})
gefunden = (
    ausnahme_bei(lambda: backlog.__setitem__(17, 3)),
    lesen(backlog, 17),
    ausnahme_bei(lambda: backlog.__delitem__(None)),
)
assert gefunden == ("TypeError", "KeyError", "KeyError") and inhalt(backlog) == [("PROJ-1", 5)], (
    f"backlog[17] = 3, backlog[17] und del backlog[None] lösen {gefunden!r} aus, erwartet war "
    "('TypeError', 'KeyError', 'KeyError'), und der Inhalt soll unverändert bleiben.\n"
    "Tipp: Ein AttributeError von 17.strip() kommt nicht in Frage; prüfen Sie vorher mit isinstance(kennung, str)."
)

# Geerbte Methoden normalisieren mit: in, get, update, pop, setdefault
backlog = Backlog({"PROJ-1": 5})
backlog.update({" proj-1": 8, "proj-2": 3})
gefunden = (
    "proj-2" in backlog,
    17 in backlog,
    backlog.get(" Proj-2 "),
    backlog.get("PROJ-9", "fehlt"),
    backlog.setdefault("proj-3", 1),
    backlog.pop("proj-1"),
    backlog.pop("PROJ-1", "weg"),
    inhalt(backlog),
)
assert gefunden == (True, False, 3, "fehlt", 1, 8, "weg", [("PROJ-2", 3), ("PROJ-3", 1)]), (
    f"Mit den geerbten Methoden erwartet (True, False, 3, 'fehlt', 1, 8, 'weg', [('PROJ-2', 3), ('PROJ-3', 1)]), gefunden {gefunden!r}.\n"
    "Tipp: Erben Sie von MutableMapping und lösen Sie bei fehlenden Kennungen genau einen KeyError aus."
)

# Vergleich mit einem Dictionary über das geerbte ==
backlog = Backlog({"a-1": 2, "b-2": 3})
assert backlog == {"A-1": 2, "B-2": 3} and backlog != {"a-1": 2, "b-2": 3}, (
    f"Backlog({{'a-1': 2, 'b-2': 3}}) soll gleich {{'A-1': 2, 'B-2': 3}} sein (Inhalt {inhalt(backlog)!r})."
)

# Viele zufällige Änderungen im Vergleich mit einem normalen Dictionary
zufall = Zufall(5022)
backlog = Backlog()
soll = {}
fehlerfall = None
schritte_text = []
for schritt in range(3000):
    nummer = zufall.randint(1, 15)
    kennung = zufall.choice(["", " ", "  "]) + zufall.choice(["proj", "PROJ", "Proj"]) + f"-{nummer}" + zufall.choice(["", " ", "\t"])
    aktion = zufall.choice(["setzen", "setzen", "lesen", "loeschen"])
    punkte = zufall.choice([0, 1, 2, 3, 5, 8, 13, -1])
    if aktion == "setzen":
        schritte_text = (schritte_text + [f"backlog[{kennung!r}] = {punkte}"])[-4:]
        bekommen = ausnahme_bei(lambda: backlog.__setitem__(kennung, punkte))
        if punkte >= 0:
            soll[normal(kennung)] = punkte
            erwartet = "keine"
        else:
            erwartet = "ValueError"
    elif aktion == "lesen":
        schritte_text = (schritte_text + [f"backlog[{kennung!r}]"])[-4:]
        bekommen = lesen(backlog, kennung)
        erwartet = soll.get(normal(kennung), "KeyError")
    else:
        schritte_text = (schritte_text + [f"del backlog[{kennung!r}]"])[-4:]
        bekommen = ausnahme_bei(lambda: backlog.__delitem__(kennung))
        erwartet = "keine" if normal(kennung) in soll else "KeyError"
        soll.pop(normal(kennung), None)
    if bekommen != erwartet or inhalt(backlog) != list(soll.items()):
        fehlerfall = (schritte_text, bekommen, erwartet, inhalt(backlog), list(soll.items()))
        break
assert fehlerfall is None, (
    f"Nach {'; '.join(fehlerfall[0])}:\n  letzter Schritt ergibt {fehlerfall[1]!r}, erwartet {fehlerfall[2]!r}\n"
    f"  Inhalt {fehlerfall[3]!r}\n  erwartet {fehlerfall[4]!r}"
)

# Obere Grenze: 100 000 Einträge, Zugriff in O(1) Schritten
backlog = Backlog((f"proj-{nummer}", nummer % 21) for nummer in range(100000))
wert, schritte_lesen = zaehle_schritte(backlog.__getitem__, " PROJ-99999 ")
_, schritte_setzen = zaehle_schritte(backlog.__setitem__, "proj-50000", 13)
assert len(backlog) == 100000 and wert == 99999 % 21 and backlog["PROJ-50000"] == 13 and schritte_lesen <= 20 and schritte_setzen <= 20, (
    f"Backlog mit 100 000 Einträgen: len {len(backlog)}, backlog[' PROJ-99999 '] = {wert!r} in {schritte_lesen} Schritten, "
    f"Setzen in {schritte_setzen} Schritten; erwartet len 100000, Wert {99999 % 21}, je höchstens 20 Schritte.\n"
    "Tipp: Speichern Sie in einem Dictionary self._daten, nicht in einer Liste von Paaren."
)
