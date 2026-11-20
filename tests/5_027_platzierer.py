# Automatisch erzeugt aus lehrkraft/muster/5_027_platzierer.py - nicht von Hand ändern.
# vorlage-hash: 6e6cc45caf4e721f
# text-hash: bb554bfe462d37e1
# thema: kontrollfluss
# inhalt: send: Generator als Koroutine

import types


def sende(p, ram):
    """Schickt ram an den Platzierer; eine Ausnahme wird als Text zurückgegeben."""
    try:
        return p.send(ram)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def platzierer_aufrufe_in_verteile(kapazitaeten, anfragen):
    """Ruft verteile auf und gibt zurück, mit welchen Argumenten verteile dabei platzierer aufruft."""
    global platzierer
    echter_platzierer = platzierer
    aufrufe = []

    def mitzaehlen(kapazitaeten):
        """Merkt sich den Aufruf und reicht ihn an den echten Platzierer weiter."""
        aufrufe.append(dict(kapazitaeten))
        return echter_platzierer(kapazitaeten)

    platzierer = mitzaehlen
    try:
        verteile(kapazitaeten, anfragen)
    finally:
        platzierer = echter_platzierer
    return aufrufe


schritte = []


def testgenerator(start):
    """Ein Generator für den Test: merkt sich jeden Schritt und addiert empfangene Werte."""
    schritte.append("gestartet")
    summe = start
    while True:
        wert = yield summe
        schritte.append(f"empfangen {wert}")
        summe += wert


def vergleich(kapazitaeten, anfragen):
    """Vergleichslösung mit einer Liste von [host, frei] statt eines Generators."""
    hosts = [[host, frei] for host, frei in kapazitaeten.items()]
    entscheidungen = []
    for ram in anfragen:
        passend = [eintrag for eintrag in hosts if eintrag[1] >= ram]
        if passend:
            passend[0][1] -= ram
            entscheidungen.append(passend[0][0])
        else:
            entscheidungen.append(None)
    return entscheidungen


# platzierer liefert einen Generator
p = platzierer({"host1": 64})
assert isinstance(p, types.GeneratorType), (
    f"platzierer({{'host1': 64}}) ergibt ein Objekt vom Typ {type(p).__name__}, erwartet war ein Generator.\n"
    "Tipp: platzierer ist eine Generatorfunktion mit yield, gestartet gibt den Generator zurück."
)

# Der Generator ist schon gestartet: send klappt sofort
ergebnis = sende(platzierer({"host1": 64}), 8)
assert ergebnis == "host1", (
    f"platzierer({{'host1': 64}}).send(8) ergibt {ergebnis!r}, erwartet war 'host1'.\n"
    "Tipp: Ein TypeError „just-started generator“ heißt, dass gestartet next(generator) noch nicht aufruft."
)

# Die erste Anfrage im Beispiel
p = platzierer({"host1": 64, "host2": 32})
ergebnis = sende(p, 48)
assert ergebnis == "host1", f"Erstes send(48) im Beispiel ergibt {ergebnis!r}, erwartet war 'host1'."

# Der Platzierer merkt sich den freien Speicher
p = platzierer({"host1": 64, "host2": 32})
ergebnis = [sende(p, 48), sende(p, 20)]
assert ergebnis == ["host1", "host2"], (
    f"send(48), send(20) im Beispiel ergibt {ergebnis!r}, erwartet war ['host1', 'host2'] (host1 hat nur noch 16 frei).\n"
    "Tipp: Ziehen Sie ram vom freien Speicher des gewählten Hosts ab."
)

# Genau passender Speicher reicht
p = platzierer({"host1": 64, "host2": 32})
ergebnis = [sende(p, 48), sende(p, 20), sende(p, 16)]
assert ergebnis == ["host1", "host2", "host1"], (
    f"send(48), send(20), send(16) ergibt {ergebnis!r}, erwartet war ['host1', 'host2', 'host1'] (16 passt genau auf host1)."
)

# Passt nirgends: None
p = platzierer({"host1": 64, "host2": 32})
ergebnis = [sende(p, ram) for ram in (48, 20, 16, 20)]
assert ergebnis == ["host1", "host2", "host1", None], (
    f"send(48), send(20), send(16), send(20) ergibt {ergebnis!r}, erwartet war ['host1', 'host2', 'host1', None]."
)

# Nach einer Ablehnung geht es normal weiter
p = platzierer({"host1": 64, "host2": 32})
ergebnis = [sende(p, ram) for ram in (48, 20, 16, 20, 12)]
assert ergebnis == ["host1", "host2", "host1", None, "host2"], (
    f"Das ganze Beispiel ergibt {ergebnis!r}, erwartet war ['host1', 'host2', 'host1', None, 'host2'].\n"
    "Tipp: Eine Ablehnung darf nichts verändern, und das Ergebnis der vorigen Anfrage darf nicht stehen bleiben."
)

# Ohne Hosts wird alles abgelehnt
p = platzierer({})
ergebnis = [sende(p, 1), sende(p, 5)]
assert ergebnis == [None, None], f"platzierer({{}}) mit send(1), send(5) ergibt {ergebnis!r}, erwartet war [None, None]."

# Das übergebene Dictionary bleibt unverändert
kapazitaeten = {"host1": 64, "host2": 32}
p = platzierer(kapazitaeten)
sende(p, 48)
sende(p, 20)
assert kapazitaeten == {"host1": 64, "host2": 32}, (
    f"Nach zwei Anfragen ist das übergebene Dictionary {kapazitaeten!r}, erwartet war unverändert {{'host1': 64, 'host2': 32}}.\n"
    "Tipp: Arbeiten Sie im Generator mit einer Kopie, etwa dict(kapazitaeten)."
)

# Zwei Platzierer sind unabhängig
eins = platzierer({"h": 10})
zwei = platzierer({"h": 10})
ergebnis = [sende(eins, 10), sende(zwei, 10), sende(eins, 1)]
assert ergebnis == ["h", "h", None], (
    f"Zwei Platzierer mit {{'h': 10}}: eins.send(10), zwei.send(10), eins.send(1) ergibt {ergebnis!r}, erwartet war ['h', 'h', None]."
)

# verteile im Beispiel
ergebnis = verteile({"a": 8, "b": 8}, [4, 6, 4, 6])
assert ergebnis == ["a", "b", "a", None], f"verteile({{'a': 8, 'b': 8}}, [4, 6, 4, 6]) ergibt {ergebnis!r}, erwartet war ['a', 'b', 'a', None]."

# verteile ohne Anfragen
ergebnis = verteile({"a": 8}, [])
assert ergebnis == [], f"verteile({{'a': 8}}, []) ergibt {ergebnis!r}, erwartet war []."

# verteile benutzt platzierer
aufrufe = platzierer_aufrufe_in_verteile({"a": 8}, [1])
assert aufrufe == [{"a": 8}], (
    f"verteile({{'a': 8}}, [1]) ruft platzierer mit {aufrufe!r} auf, erwartet war genau ein Aufruf mit {{'a': 8}}.\n"
    "Tipp: Erzeugen Sie mit platzierer(kapazitaeten) einen Platzierer und schicken Sie ihm jede Anfrage mit send."
)

# gestartet startet einen beliebigen Generator genau einmal
gestarteter = gestartet(testgenerator)(5)
ergebnis = (list(schritte), sende(gestarteter, 3))
assert ergebnis == (["gestartet"], 8), (
    f"gestartet(testgenerator)(5): Schritte direkt danach {ergebnis[0]!r}, dann send(3) ergibt {ergebnis[1]!r}; "
    "erwartet waren ['gestartet'] und 8.\nTipp: Rufen Sie in der Hülle genau einmal next(generator) auf."
)

# gestartet behält Name und Docstring
ergebnis = (gestartet(testgenerator).__name__, gestartet(testgenerator).__doc__)
assert ergebnis == ("testgenerator", testgenerator.__doc__), (
    f"gestartet(testgenerator) hat den Namen {ergebnis[0]!r} und den Docstring {ergebnis[1]!r}; "
    "erwartet waren 'testgenerator' und dessen Docstring.\nTipp: Schreiben Sie @functools.wraps(generatorfunktion) über die Hülle."
)

# platzierer ist mit gestartet dekoriert und behält seinen Namen
assert platzierer.__name__ == "platzierer", f"platzierer.__name__ ist {platzierer.__name__!r}, erwartet war 'platzierer'."

# Die Ausgabe des Programms
assert vergleichbar(AUSGABE) == vergleichbar("host1 host2 host1 None host2\n['a', 'b', 'a', None]"), (
    f"Erwartete Ausgabe:\nhost1 host2 host1 None host2\n['a', 'b', 'a', None]\nIhr Programm:\n{AUSGABE}"
)

# Viele zufällige Rechenzentren
zufall = Zufall(5027)
for runde in range(300):
    kapazitaeten = {}
    for nummer in range(zufall.randint(0, 5)):
        kapazitaeten[f"h{nummer}"] = zufall.choice([0, zufall.randint(0, 64), zufall.randint(0, 10**4)])
    anfragen = [zufall.choice([zufall.randint(1, 16), zufall.randint(1, 10**4)]) for _ in range(zufall.randint(0, 10))]
    erwartet = vergleich(kapazitaeten, anfragen)
    ergebnis = verteile(kapazitaeten, anfragen)
    assert ergebnis == erwartet, f"verteile({kapazitaeten!r}, {anfragen!r})\n  ergibt   {ergebnis!r}\n  erwartet {erwartet!r}"

# Obere Grenze: 50 Hosts und 20 000 Anfragen
kapazitaeten = {f"host{nummer:02d}": zufall.randint(0, 10**4) for nummer in range(50)}
anfragen = [zufall.randint(1, 40) for _ in range(20000)]
erwartet = vergleich(kapazitaeten, anfragen)
ergebnis = verteile(kapazitaeten, anfragen)
assert ergebnis == erwartet, (
    f"Bei 50 Hosts und 20 000 Anfragen weicht verteile ab; erste Abweichung bei Anfrage Nummer "
    f"{next((i for i, (a, b) in enumerate(zip(ergebnis, erwartet)) if a != b), min(len(ergebnis), len(erwartet)))}."
)
