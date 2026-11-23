# Automatisch erzeugt aus lehrkraft/muster/5_044_planungspoker.py - nicht von Hand ändern.
# vorlage-hash: bf21c4e72122dd33
# text-hash: 45898586d06043db
# thema: nebenlaeufigkeit
# inhalt: threading: start, join, Ergebnisse

VIER = ["Aylin", "Ben", "Chiara", "Dario"]
BEISPIEL = {"Aylin": 5, "Ben": 8, "Chiara": 3, "Dario": 8}
WERTE = [0, 1, 2, 3, 5, 8, 13, 20, 40, 100]


def stelle_ein(karten, antwortzeit=0.1):
    """Setzt KARTEN und ANTWORTZEIT neu und leert PROTOKOLL und FRAGENDE."""
    KARTEN.clear()
    KARTEN.update(karten)
    ANTWORTZEIT.clear()
    for person in karten:
        ANTWORTZEIT[person] = antwortzeit
    PROTOKOLL.clear()
    FRAGENDE.clear()


def wert_von(aufruf):
    """Führt den Aufruf aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def gleichzeitig():
    """True, wenn im PROTOKOLL alle Personen gefragt wurden, bevor die erste geantwortet hat."""
    gefragt = [stelle for stelle, eintrag in enumerate(PROTOKOLL) if eintrag.startswith("gefragt")]
    geantwortet = [stelle for stelle, eintrag in enumerate(PROTOKOLL) if eintrag.startswith("geantwortet")]
    return not gefragt or not geantwortet or max(gefragt) < min(geantwortet)


def vergleich_aussprache(karten):
    """Vergleichslösung: sucht niedrigste und höchste Karte mit einer Schleife."""
    niedrigste = None
    hoechste = None
    for person, karte in karten.items():
        if niedrigste is None or karte < karten[niedrigste]:
            niedrigste = person
        if hoechste is None or karte > karten[hoechste]:
            hoechste = person
    if niedrigste is None or karten[niedrigste] == karten[hoechste]:
        return None
    return niedrigste, hoechste


# Abfrage ist eine Unterklasse von threading.Thread
assert isinstance(Abfrage, type) and issubclass(Abfrage, threading.Thread), (
    "Abfrage ist keine Unterklasse von threading.Thread. Schreiben Sie class Abfrage(threading.Thread):"
)

# Abfrage merkt sich person und story
stelle_ein(BEISPIEL)
abfrage = wert_von(lambda: Abfrage("Ben", "Export"))
werte = (getattr(abfrage, "person", None), getattr(abfrage, "story", None)) if not isinstance(abfrage, str) else abfrage
assert werte == ("Ben", "Export"), (
    f"Abfrage('Ben', 'Export') hat person und story {werte!r}, erwartet war ('Ben', 'Export').\n"
    "Tipp: super().__init__() aufrufen und dann self.person und self.story setzen."
)

# Abfrage: nach start() und join() steht die Karte im Attribut karte
fehler = wert_von(lambda: (abfrage.start(), abfrage.join()))
karte = getattr(abfrage, "karte", "(kein Attribut karte)") if not isinstance(abfrage, str) else abfrage
assert karte == 8, (
    f"Nach start() und join() hat Abfrage('Ben', 'Export').karte den Wert {karte!r}, erwartet war 8.\n"
    "Tipp: In run() self.karte = frage(self.person, self.story)."
)

# Abfrage fragt in einem eigenen Thread
fragende = list(FRAGENDE)
assert len(fragende) == 1 and fragende[0] is abfrage and fragende[0] is not threading.main_thread(), (
    f"frage wurde {len(fragende)}-mal aufgerufen, aus dem Thread {fragende}; erwartet war einmal, aus der Abfrage "
    "selbst.\nTipp: Die Arbeit gehört in run(), nicht in __init__."
)

# runde: das Beispiel
stelle_ein(BEISPIEL)
ergebnis = wert_von(lambda: runde(VIER, "Login per Fingerabdruck"))
assert ergebnis == BEISPIEL, (
    f"runde({VIER}, 'Login per Fingerabdruck') ergibt {ergebnis!r}, erwartet war {BEISPIEL}.\n"
    "Tipp: Nach join() steht in jeder Abfrage die Karte."
)

# runde: in der Reihenfolge der Liste
assert isinstance(ergebnis, dict) and list(ergebnis) == VIER, (
    f"Die Schlüssel von runde sind {list(ergebnis) if isinstance(ergebnis, dict) else ergebnis!r}, erwartet war {VIER}.\n"
    "Tipp: Bauen Sie das Dictionary nach dem join() in der Reihenfolge der Liste auf."
)

# runde: alle Personen werden gleichzeitig gefragt
assert gleichzeitig(), (
    f"Das Protokoll ist {PROTOKOLL}; alle sollten gefragt werden, bevor die erste Antwort kommt.\n"
    "Tipp: Erst alle Threads mit start() starten, dann in einer zweiten Schleife join()."
)

# runde: gefragt wird aus Abfrage-Threads
arten = {type(thread).__name__ for thread in FRAGENDE}
assert arten == {"Abfrage"} and len(set(map(id, FRAGENDE))) == 4, (
    f"frage wurde aus diesen Threads aufgerufen: {[type(thread).__name__ for thread in FRAGENDE]}; erwartet waren "
    "vier verschiedene Abfrage-Threads.\nTipp: start(), nicht run(), startet den neuen Thread."
)

# runde: andere Karten (nicht fest hinschreiben!)
karten = {"Emil": 13, "Fatma": 13, "Gero": 20}
stelle_ein(karten)
ergebnis = wert_von(lambda: runde(["Gero", "Emil", "Fatma"], "Rechnung als PDF"))
assert ergebnis == {"Gero": 20, "Emil": 13, "Fatma": 13} and list(ergebnis) == ["Gero", "Emil", "Fatma"], (
    f"runde(['Gero', 'Emil', 'Fatma'], …) ergibt {ergebnis!r}, erwartet war {{'Gero': 20, 'Emil': 13, 'Fatma': 13}}."
)

# runde: wartet auch auf die langsamste Antwort
stelle_ein(BEISPIEL, 0.02)
ANTWORTZEIT["Chiara"] = 0.3
ergebnis = wert_von(lambda: runde(VIER, "Export"))
assert ergebnis == BEISPIEL, (
    f"Wenn Chiara erst nach 0.3 Sekunden antwortet, ergibt runde {ergebnis!r}, erwartet war {BEISPIEL}.\n"
    "Tipp: Warten Sie mit join() auf jeden Thread, bevor Sie die Karten einsammeln."
)

# runde: niemand im Team
stelle_ein({})
ergebnis = wert_von(lambda: runde([], "Export"))
assert ergebnis == {}, f"runde([], 'Export') ergibt {ergebnis!r}, erwartet war {{}}."

# aussprache: das Beispiel
ergebnis = wert_von(lambda: aussprache(dict(BEISPIEL)))
assert ergebnis == ("Chiara", "Ben"), (
    f"aussprache({BEISPIEL}) ergibt {ergebnis!r}, erwartet war ('Chiara', 'Ben').\n"
    "Tipp: min(karten, key=karten.get) liefert die Person mit der niedrigsten Karte."
)

# aussprache: bei Gleichstand zählt die erste Person
karten = {"Emil": 3, "Fatma": 1, "Gero": 1, "Hanna": 3}
ergebnis = wert_von(lambda: aussprache(dict(karten)))
assert ergebnis == ("Fatma", "Emil"), f"aussprache({karten}) ergibt {ergebnis!r}, erwartet war ('Fatma', 'Emil')."

# aussprache: alle einig
karten = {"Emil": 5, "Fatma": 5}
ergebnis = wert_von(lambda: aussprache(dict(karten)))
assert ergebnis is None, f"aussprache({karten}) ergibt {ergebnis!r}, erwartet war None, denn alle sind sich einig."

# aussprache: eine einzige Person
ergebnis = wert_von(lambda: aussprache({"Emil": 40}))
assert ergebnis is None, f"aussprache({{'Emil': 40}}) ergibt {ergebnis!r}, erwartet war None."

# aussprache: keine Karten
ergebnis = wert_von(lambda: aussprache({}))
assert ergebnis is None, f"aussprache({{}}) ergibt {ergebnis!r}, erwartet war None.\nTipp: min() einer leeren Folge löst einen Fehler aus."

# Die Ausgabe des Programms
erwartet = f"{BEISPIEL}\n('Chiara', 'Ben')"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Runden
zufall = Zufall(5044)
for _ in range(25):
    personen = [f"P{nummer}" for nummer in zufall.sample(range(50), zufall.randint(0, 6))]
    karten = {person: zufall.choice(WERTE) for person in personen}
    stelle_ein(karten, 0.005)
    ergebnis = wert_von(lambda: runde(personen, "Story"))
    assert ergebnis == karten and list(ergebnis) == personen, f"runde({personen}, …) ergibt {ergebnis!r}, erwartet war {karten}."

# Viele zufällige Kartensätze für aussprache
for _ in range(500):
    karten = {f"P{nummer}": zufall.choice(WERTE[: zufall.randint(1, 10)]) for nummer in range(zufall.randint(0, 6))}
    ergebnis = wert_von(lambda: aussprache(dict(karten)))
    assert ergebnis == vergleich_aussprache(karten), (
        f"aussprache({karten}) ergibt {ergebnis!r}, erwartet war {vergleich_aussprache(karten)}."
    )

# Obere Grenze: 30 Personen, jede antwortet nach 0.2 Sekunden
personen = [f"P{nummer}" for nummer in range(30)]
karten = {person: zufall.choice(WERTE) for person in personen}
stelle_ein(karten, 0.2)
ergebnis = wert_von(lambda: runde(personen, "Story"))
assert ergebnis == karten and gleichzeitig(), (
    f"Bei 30 Personen ergibt runde {ergebnis!r}, erwartet war {karten}; alle sollten gleichzeitig gefragt werden."
)
