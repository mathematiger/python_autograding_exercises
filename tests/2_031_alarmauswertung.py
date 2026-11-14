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

# neue_codes findet die richtigen Codes (Reihenfolge und Doppelte zählen hier noch nicht)
ergebnis = neue_codes([m("web01", "CPU_HIGH")], daten)
assert isinstance(ergebnis, (list, set)) and sorted(set(ergebnis)) == ["DISK_FULL", "TIMEOUT"], (
    f"neue_codes(<gestern>, <heute aus dem Beispiel>) ergibt {ergebnis!r}, erwartet waren DISK_FULL und TIMEOUT.\n"
    "Tipp: Neu sind die Codes von heute, die gestern nicht vorkamen."
)

# neue_codes aus dem Beispiel
ergebnis = neue_codes([m("web01", "CPU_HIGH")], daten)
assert ergebnis == ["DISK_FULL", "TIMEOUT"], (
    f"neue_codes(<gestern>, <heute aus dem Beispiel>) ergibt {ergebnis!r}, erwartet war ['DISK_FULL', 'TIMEOUT'].\n"
    "Tipp: Sammeln Sie die Codes beider Tage in zwei Mengen; heute - gestern enthält nur die neuen. "
    "TIMEOUT kommt heute zweimal vor, steht im Ergebnis aber nur einmal."
)

# neue_codes gibt die Codes alphabetisch sortiert zurück
ergebnis = neue_codes([], [m("a", "ZONE"), m("b", "ALARM"), m("c", "MAIL")])
assert ergebnis == ["ALARM", "MAIL", "ZONE"], (
    f"neue_codes([], [ZONE, ALARM, MAIL]) ergibt {ergebnis!r}, erwartet war ['ALARM', 'MAIL', 'ZONE'].\n"
    "Tipp: sorted(menge) macht aus der Menge eine sortierte Liste."
)

# kritischster_host aus dem Beispiel: das Gewicht zählt, nicht die Anzahl
ergebnis = kritischster_host(daten, {"DISK_FULL": 5})
assert ergebnis == "db01", (
    f"kritischster_host(<heute aus dem Beispiel>, {{'DISK_FULL': 5}}) ergibt {ergebnis!r}, erwartet war 'db01' "
    "(DISK_FULL zählt 5, TIMEOUT fehlt in gewichte und zählt 1, zusammen 6 gegen 2 bei web01)."
)

# Die übergebenen Daten bleiben unverändert
assert daten == beispiel(), f"Nach den Aufrufen sind die Meldungen {daten!r}, erwartet war unverändert {beispiel()!r}."

# Ein Host mit vielen leichten gegen einen mit einer schweren Meldung: die schwere wiegt mehr
daten = [m("app", "LOG"), m("app", "LOG"), m("app", "LOG"), m("nas", "RAID_DEGRADED")]
ergebnis = kritischster_host(daten, {"RAID_DEGRADED": 4})
assert ergebnis == "nas", (
    f"kritischster_host({daten}, {{'RAID_DEGRADED': 4}}) ergibt {ergebnis!r}, erwartet war 'nas' (4 gegen 3)."
)

# Ein Host mit vielen leichten gegen einen mit einer schweren Meldung: die leichten wiegen mehr
ergebnis = kritischster_host(daten, {"RAID_DEGRADED": 2})
assert ergebnis == "app", (
    f"kritischster_host({daten}, {{'RAID_DEGRADED': 2}}) ergibt {ergebnis!r}, erwartet war 'app' (3 gegen 2)."
)

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

# Groß- und Kleinschreibung zählt bei Codes
ergebnis = neue_codes([m("a", "timeout")], [m("a", "TIMEOUT"), m("a", "timeout")])
assert ergebnis == ["TIMEOUT"], f"neue_codes mit gestern 'timeout' und heute 'TIMEOUT', 'timeout' ergibt {ergebnis!r}, erwartet war ['TIMEOUT']."

# Gestern gab es dieselben Codes: nichts ist neu
ergebnis = neue_codes(beispiel(), [m("x", "TIMEOUT")])
assert ergebnis == [], f"neue_codes(<heute aus dem Beispiel>, [TIMEOUT]) ergibt {ergebnis!r}, erwartet war []."

# alarme_je_host ohne Meldungen
ergebnis = alarme_je_host([])
assert ergebnis == {}, f"alarme_je_host([]) ergibt {ergebnis!r}, erwartet war {{}}."

# neue_codes ohne Meldungen an beiden Tagen
ergebnis = neue_codes([], [])
assert ergebnis == [], f"neue_codes([], []) ergibt {ergebnis!r}, erwartet war []."

# neue_codes ohne Meldungen gestern: alle Codes von heute sind neu
ergebnis = neue_codes([], [m("a", "Z"), m("b", "A")])
assert ergebnis == ["A", "Z"], f"neue_codes([], [Z, A]) ergibt {ergebnis!r}, erwartet war ['A', 'Z']."

# neue_codes ohne Meldungen heute
ergebnis = neue_codes(beispiel(), [])
assert ergebnis == [], f"neue_codes(<Beispiel>, []) ergibt {ergebnis!r}, erwartet war []."

# alarme_je_host mit nur einer Meldung
ergebnis = alarme_je_host([m("fw1", "DROP")])
assert ergebnis == {"fw1": 1}, f"alarme_je_host([fw1 DROP]) ergibt {ergebnis!r}, erwartet war {{'fw1': 1}}."

# kritischster_host mit nur einer Meldung
ergebnis = kritischster_host([m("fw1", "DROP")], {"DROP": 100})
assert ergebnis == "fw1", f"kritischster_host([fw1 DROP], {{'DROP': 100}}) ergibt {ergebnis!r}, erwartet war 'fw1'."


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


# 300 zufällige Tage für alarme_je_host
HOSTS = ["web01", "web02", "db01", "nas", "fw1", "mail"]
CODES = ["CPU_HIGH", "DISK_FULL", "TIMEOUT", "PING_LOST", "RAM_HIGH", "cert_expired"]
zufall = Zufall(2031)
for _ in range(300):
    gestern = [m(zufall.choice(HOSTS), zufall.choice(CODES)) for _ in range(zufall.randint(0, 6))]
    heute = [m(zufall.choice(HOSTS), zufall.choice(CODES)) for _ in range(zufall.randint(1, 10))]
    gewichte = {code: zufall.randint(1, 100) for code in zufall.sample(CODES, zufall.randint(0, 4))}
    vorher = (repr(gestern), repr(heute), repr(gewichte))
    ergebnis = alarme_je_host(heute)
    erwartet = je_host_von_hand(heute)
    assert ergebnis == erwartet, f"alarme_je_host({heute}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    assert (repr(gestern), repr(heute), repr(gewichte)) == vorher, (
        "Die übergebenen Listen oder Dictionaries wurden verändert; sie sollen unverändert bleiben."
    )

# 300 zufällige Tage für neue_codes
zufall = Zufall(2031)
for _ in range(300):
    gestern = [m(zufall.choice(HOSTS), zufall.choice(CODES)) for _ in range(zufall.randint(0, 6))]
    heute = [m(zufall.choice(HOSTS), zufall.choice(CODES)) for _ in range(zufall.randint(1, 10))]
    gewichte = {code: zufall.randint(1, 100) for code in zufall.sample(CODES, zufall.randint(0, 4))}
    vorher = (repr(gestern), repr(heute), repr(gewichte))
    ergebnis = neue_codes(gestern, heute)
    erwartet = neue_von_hand(gestern, heute)
    assert ergebnis == erwartet, f"neue_codes({gestern}, {heute}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    assert (repr(gestern), repr(heute), repr(gewichte)) == vorher, (
        "Die übergebenen Listen oder Dictionaries wurden verändert; sie sollen unverändert bleiben."
    )

# 300 zufällige Tage für kritischster_host
zufall = Zufall(2031)
for _ in range(300):
    gestern = [m(zufall.choice(HOSTS), zufall.choice(CODES)) for _ in range(zufall.randint(0, 6))]
    heute = [m(zufall.choice(HOSTS), zufall.choice(CODES)) for _ in range(zufall.randint(1, 10))]
    gewichte = {code: zufall.randint(1, 100) for code in zufall.sample(CODES, zufall.randint(0, 4))}
    vorher = (repr(gestern), repr(heute), repr(gewichte))
    ergebnis = kritischster_host(heute, gewichte)
    erwartet = kritischster_von_hand(heute, gewichte)
    assert ergebnis == erwartet, (
        f"kritischster_host({heute}, {gewichte}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    )
    assert (repr(gestern), repr(heute), repr(gewichte)) == vorher, (
        "Die übergebenen Listen oder Dictionaries wurden verändert; sie sollen unverändert bleiben."
    )

# Obere Grenze: alarme_je_host bei 10 000 Meldungen von 100 Hosts
heute = [m(f"host{nummer % 100:02d}", f"C{nummer % 137}") for nummer in range(10000)]
gestern = [m("alt", f"C{nummer}") for nummer in range(0, 10000, 2)]
gewichte = {f"C{nummer}": nummer % 100 + 1 for nummer in range(100)}
ergebnis = alarme_je_host(heute)
assert ergebnis == {f"host{nummer:02d}": 100 for nummer in range(100)}, (
    "Bei 10 000 Meldungen von 100 Hosts (host00 bis host99, je 100 Meldungen) erwartet alarme_je_host 100 je Host; "
    f"für host00 kommt {ergebnis.get('host00') if isinstance(ergebnis, dict) else ergebnis!r} heraus."
)

# Obere Grenze: neue_codes bei 10 000 Meldungen
ergebnis = neue_codes(gestern, heute)
erwartet = neue_von_hand(gestern, heute)
assert ergebnis == erwartet, (
    f"Bei 10 000 Meldungen ergibt neue_codes {ergebnis[:5] if isinstance(ergebnis, list) else ergebnis!r}…, "
    f"erwartet war {erwartet[:5]}…"
)

# Obere Grenze: kritischster_host bei 10 000 Meldungen von 100 Hosts mit 100 Gewichten
ergebnis = kritischster_host(heute, gewichte)
erwartet = kritischster_von_hand(heute, gewichte)
assert ergebnis == erwartet, (
    f"Bei 10 000 Meldungen von 100 Hosts ergibt kritischster_host {ergebnis!r}, erwartet war {erwartet!r}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "{'web01': 2, 'db01': 2}\n['DISK_FULL', 'TIMEOUT']\ndb01"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
