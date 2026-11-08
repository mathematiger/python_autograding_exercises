# Automatisch erzeugt aus lehrkraft/muster/2_031_alarmauswertung.py - nicht von Hand ändern.
# vorlage-hash: 2f0484d10b15b3cd
# text-hash: 6d20bf3ae6b5ebcc
# thema: datenstrukturen
# inhalt: Übung: Dictionaries und Mengen

def m(host, code):
    """Baut eine Alarmmeldung für die Tests."""
    return {"host": host, "code": code}


def beispiel():
    """Baut die Meldungen von heute aus dem Beispiel neu."""
    return [m("web01", "CPU_HIGH"), m("db01", "DISK_FULL"), m("web01", "TIMEOUT"), m("db01", "TIMEOUT")]


# alarme_je_host aus dem Beispiel
daten = beispiel()
ergebnis = alarme_je_host(daten)
assert ergebnis == {"web01": 2, "db01": 2}, (
    f"alarme_je_host(<heute aus dem Beispiel>) ergibt {ergebnis!r}, erwartet war {{'web01': 2, 'db01': 2}}.\n"
    "Tipp: anzahl[host] = anzahl.get(host, 0) + 1 zählt auch einen Host, der zum ersten Mal vorkommt."
)

# neue_codes aus dem Beispiel
ergebnis = neue_codes([m("web01", "CPU_HIGH")], daten)
assert ergebnis == ["DISK_FULL", "TIMEOUT"], (
    f"neue_codes(<gestern>, <heute aus dem Beispiel>) ergibt {ergebnis!r}, erwartet war ['DISK_FULL', 'TIMEOUT'].\n"
    "Tipp: Sammeln Sie die Codes beider Tage in zwei Mengen; heute - gestern enthält nur die neuen. "
    "TIMEOUT kommt heute zweimal vor, steht im Ergebnis aber nur einmal."
)

# kritischster_host aus dem Beispiel: das Gewicht zählt, nicht die Anzahl
ergebnis = kritischster_host(daten, {"DISK_FULL": 5})
assert ergebnis == "db01", (
    f"kritischster_host(<heute aus dem Beispiel>, {{'DISK_FULL': 5}}) ergibt {ergebnis!r}, erwartet war 'db01' "
    "(DISK_FULL zählt 5, TIMEOUT fehlt in gewichte und zählt 1, zusammen 6 gegen 2 bei web01)."
)

# Die übergebenen Daten bleiben unverändert
assert daten == beispiel(), f"Nach den Aufrufen sind die Meldungen {daten!r}, erwartet war unverändert {beispiel()!r}."

# Ohne Gewichte zählt jede Meldung 1; bei Gleichstand gewinnt der alphabetisch kleinste Host
ergebnis = kritischster_host(beispiel(), {})
assert ergebnis == "db01", (
    f"kritischster_host(<heute aus dem Beispiel>, {{}}) ergibt {ergebnis!r}, erwartet war 'db01': Beide Hosts "
    "haben die Summe 2, und 'db01' kommt alphabetisch vor 'web01'.\n"
    "Tipp: Bei gleicher Summe gewinnt der Host mit dem kleineren Namen (host < bester), nicht der erste in der Liste."
)

# Gleichstand, bei dem der kleinere Name zuletzt kommt
daten = [m("srv9", "A"), m("srv2", "B"), m("srv5", "A")]
ergebnis = kritischster_host(daten, {"A": 3, "B": 3})
assert ergebnis == "srv2", f"kritischster_host({daten}, {{'A': 3, 'B': 3}}) ergibt {ergebnis!r}, erwartet war 'srv2'."

# Ein einziger Host mit vielen leichten gegen einen mit einer schweren Meldung
daten = [m("app", "LOG"), m("app", "LOG"), m("app", "LOG"), m("nas", "RAID_DEGRADED")]
ergebnis = (kritischster_host(daten, {"RAID_DEGRADED": 4}), kritischster_host(daten, {"RAID_DEGRADED": 2}))
assert ergebnis == ("nas", "app"), (
    f"Für {daten} ergeben kritischster_host mit RAID_DEGRADED 4 und mit 2 {ergebnis!r}, erwartet war ('nas', 'app')."
)

# Groß- und Kleinschreibung zählt bei Codes
ergebnis = neue_codes([m("a", "timeout")], [m("a", "TIMEOUT"), m("a", "timeout")])
assert ergebnis == ["TIMEOUT"], f"neue_codes mit gestern 'timeout' und heute 'TIMEOUT', 'timeout' ergibt {ergebnis!r}, erwartet war ['TIMEOUT']."

# Gestern gab es dieselben Codes: nichts ist neu
ergebnis = neue_codes(beispiel(), [m("x", "TIMEOUT")])
assert ergebnis == [], f"neue_codes(<heute aus dem Beispiel>, [TIMEOUT]) ergibt {ergebnis!r}, erwartet war []."

# Leere Listen
ergebnis = (alarme_je_host([]), neue_codes([], []), neue_codes([], [m("a", "Z"), m("b", "A")]), neue_codes(beispiel(), []))
assert ergebnis == ({}, [], ["A", "Z"], []), (
    f"alarme_je_host([]), neue_codes([], []), neue_codes([], [Z, A]) und neue_codes(<Beispiel>, []) ergeben "
    f"{ergebnis!r}, erwartet war ({{}}, [], ['A', 'Z'], [])."
)

# Nur eine Meldung
ergebnis = (alarme_je_host([m("fw1", "DROP")]), kritischster_host([m("fw1", "DROP")], {"DROP": 100}))
assert ergebnis == ({"fw1": 1}, "fw1"), f"Mit einer einzigen Meldung ergeben die Funktionen {ergebnis!r}, erwartet war ({{'fw1': 1}}, 'fw1')."


# Vergleichslösungen: mit Listen und count statt Dictionaries und Mengen
def je_host_von_hand(meldungen):
    """Zählt mit count über die Liste der Hosts."""
    hosts = [meldung["host"] for meldung in meldungen]
    ergebnis = {}
    for host in hosts:
        ergebnis[host] = hosts.count(host)
    return ergebnis


def neue_von_hand(gestern, heute):
    """Sucht neue Codes mit in auf Listen."""
    alte = [meldung["code"] for meldung in gestern]
    neue = []
    for meldung in heute:
        if meldung["code"] not in alte and meldung["code"] not in neue:
            neue.append(meldung["code"])
    neue.sort()
    return neue


def kritischster_von_hand(meldungen, gewichte):
    """Rechnet für jeden Host die Summe einzeln aus und nimmt den sortiert ersten der besten."""
    hosts = sorted(set(meldung["host"] for meldung in meldungen))
    summen = []
    for host in hosts:
        summe = 0
        for meldung in meldungen:
            if meldung["host"] == host:
                summe += gewichte[meldung["code"]] if meldung["code"] in gewichte else 1
        summen.append(summe)
    return hosts[summen.index(max(summen))]


# 300 zufällige Tage
zufall = Zufall(2031)
HOSTS = ["web01", "web02", "db01", "nas", "fw1", "mail"]
CODES = ["CPU_HIGH", "DISK_FULL", "TIMEOUT", "PING_LOST", "RAM_HIGH", "cert_expired"]
for _ in range(300):
    gestern = [m(zufall.choice(HOSTS), zufall.choice(CODES)) for _ in range(zufall.randint(0, 6))]
    heute = [m(zufall.choice(HOSTS), zufall.choice(CODES)) for _ in range(zufall.randint(1, 10))]
    gewichte = {code: zufall.randint(1, 100) for code in zufall.sample(CODES, zufall.randint(0, 4))}
    vorher = (repr(gestern), repr(heute), repr(gewichte))
    ergebnis = alarme_je_host(heute)
    erwartet = je_host_von_hand(heute)
    assert ergebnis == erwartet, f"alarme_je_host({heute}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    ergebnis = neue_codes(gestern, heute)
    erwartet = neue_von_hand(gestern, heute)
    assert ergebnis == erwartet, f"neue_codes({gestern}, {heute}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    ergebnis = kritischster_host(heute, gewichte)
    erwartet = kritischster_von_hand(heute, gewichte)
    assert ergebnis == erwartet, (
        f"kritischster_host({heute}, {gewichte}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    )
    assert (repr(gestern), repr(heute), repr(gewichte)) == vorher, (
        "Die übergebenen Listen oder Dictionaries wurden verändert; sie sollen unverändert bleiben."
    )

# Obere Grenze: 10 000 Meldungen von 100 Hosts mit 100 Gewichten
heute = [m(f"host{nummer % 100:02d}", f"C{nummer % 137}") for nummer in range(10000)]
gestern = [m("alt", f"C{nummer}") for nummer in range(0, 10000, 2)]
gewichte = {f"C{nummer}": nummer % 100 + 1 for nummer in range(100)}
ergebnis = (alarme_je_host(heute), neue_codes(gestern, heute), kritischster_host(heute, gewichte))
erwartet = ({f"host{nummer:02d}": 100 for nummer in range(100)}, neue_von_hand(gestern, heute),
            kritischster_von_hand(heute, gewichte))
assert ergebnis == erwartet, (
    "Bei 10 000 Meldungen von 100 Hosts stimmt mindestens eine Funktion nicht: erwartet "
    f"neue_codes {erwartet[1][:5]}… und kritischster_host {erwartet[2]!r}, bekommen "
    f"{ergebnis[1][:5] if isinstance(ergebnis[1], list) else ergebnis[1]!r}… und {ergebnis[2]!r}"
    f"{'' if ergebnis[0] == erwartet[0] else '; alarme_je_host zählt nicht 100 je Host'}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "{'web01': 2, 'db01': 2}\n['DISK_FULL', 'TIMEOUT']\ndb01"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
