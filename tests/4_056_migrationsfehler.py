# Automatisch erzeugt aus lehrkraft/muster/4_056_migrationsfehler.py - nicht von Hand ändern.
# vorlage-hash: 276f619a734814fa
# text-hash: ad4c5c3718ea0b52
# thema: fehler
# inhalt: eigene Fehlerklassen, Hierarchie

def ausnahme_von(aufruf):
    """Führt den Aufruf aus und gibt die ausgelöste Ausnahme zurück, sonst den Text "keine Ausnahme"."""
    try:
        aufruf()
    except Exception as fehler:
        return fehler
    return "keine Ausnahme"


def wert_von(aufruf):
    """Führt den Aufruf aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def beschreibe(fehler):
    """Name der Klasse und Meldung einer Ausnahme, zum Anzeigen."""
    if isinstance(fehler, Exception):
        return f"{type(fehler).__name__}({str(fehler)!r})"
    return repr(fehler)


def host(ram, kerne, wartung=False):
    """Ein Host-Eintrag."""
    return {"ram_frei": ram, "kerne_frei": kerne, "wartung": wartung}


def vm(name, ram, kerne):
    """Ein VM-Eintrag."""
    return {"name": name, "ram": ram, "kerne": kerne}


def klasse(name):
    """Die Klasse aus dem Programm oder None, wenn es sie nicht gibt."""
    gefunden = globals().get(name)
    return gefunden if isinstance(gefunden, type) else None


# Die fünf Klassen gibt es, und alle sind Ausnahmen
fehlend = [name for name in ["MigrationsFehler", "HostInWartung", "KapazitaetsFehler", "ZuWenigRam", "ZuWenigKerne"] if klasse(name) is None or not issubclass(klasse(name), Exception)]
assert fehlend == [], f"Es fehlen die Ausnahmeklassen {fehlend} (oder sie erben nicht von Exception).\nTipp: class MigrationsFehler(Exception): …"

# Die Hierarchie stimmt
falsch = []
for kind, eltern in [("MigrationsFehler", "Exception"), ("HostInWartung", "MigrationsFehler"), ("KapazitaetsFehler", "MigrationsFehler"), ("ZuWenigRam", "KapazitaetsFehler"), ("ZuWenigKerne", "KapazitaetsFehler")]:
    oben = Exception if eltern == "Exception" else klasse(eltern)
    if klasse(kind) is None or oben is None or klasse(kind).__bases__ != (oben,):
        falsch.append(f"{kind} soll direkt von {eltern} erben")
assert falsch == [], "\n".join(falsch) + "\nTipp: Die Oberklasse steht in Klammern hinter dem Klassennamen."

# HostInWartung und ZuWenigRam sind keine Unterarten voneinander
assert not issubclass(klasse("HostInWartung"), klasse("KapazitaetsFehler")) and not issubclass(klasse("ZuWenigRam"), klasse("HostInWartung")), (
    "HostInWartung soll nicht von KapazitaetsFehler erben und umgekehrt."
)

# MigrationsFehler speichert vm und die Meldung
fehler = wert_von(lambda: MigrationsFehler("app-7", "Umzug abgebrochen"))
assert getattr(fehler, "vm", None) == "app-7" and str(fehler) == "Umzug abgebrochen", (
    f"MigrationsFehler('app-7', 'Umzug abgebrochen') hat vm={getattr(fehler, 'vm', None)!r} und die Meldung {str(fehler)!r}, "
    "erwartet waren 'app-7' und 'Umzug abgebrochen'.\nTipp: super().__init__(meldung) und self.vm = vm"
)

# HostInWartung: Attribute und Meldung
fehler = wert_von(lambda: HostInWartung("web-2", "esx-3"))
assert (getattr(fehler, "vm", None), getattr(fehler, "host", None)) == ("web-2", "esx-3"), (
    f"HostInWartung('web-2', 'esx-3') hat vm={getattr(fehler, 'vm', None)!r} und host={getattr(fehler, 'host', None)!r}, erwartet waren 'web-2' und 'esx-3'."
)

# HostInWartung: die Meldung
assert vergleichbar(str(fehler)) == vergleichbar("esx-3 ist in Wartung, web-2 kann nicht umziehen"), (
    f"Die Meldung von HostInWartung('web-2', 'esx-3') ist {str(fehler)!r}, erwartet war 'esx-3 ist in Wartung, web-2 kann nicht umziehen'."
)

# ZuWenigRam: Attribute und Meldung
fehler = wert_von(lambda: ZuWenigRam("db-1", 8))
assert (getattr(fehler, "vm", None), getattr(fehler, "fehlend", None)) == ("db-1", 8) and vergleichbar(str(fehler)) == vergleichbar("db-1: es fehlen 8 GB RAM"), (
    f"ZuWenigRam('db-1', 8) hat vm={getattr(fehler, 'vm', None)!r}, fehlend={getattr(fehler, 'fehlend', None)!r} und die Meldung {str(fehler)!r}.\n"
    "Tipp: ZuWenigRam ruft super().__init__(vm, fehlend, meldung) auf, KapazitaetsFehler speichert fehlend."
)

# ZuWenigKerne: Attribute und Meldung
fehler = wert_von(lambda: ZuWenigKerne("ci-4", 3))
assert (getattr(fehler, "vm", None), getattr(fehler, "fehlend", None)) == ("ci-4", 3) and vergleichbar(str(fehler)) == vergleichbar("ci-4: es fehlen 3 Kerne"), (
    f"ZuWenigKerne('ci-4', 3) hat vm={getattr(fehler, 'vm', None)!r}, fehlend={getattr(fehler, 'fehlend', None)!r} und die Meldung {str(fehler)!r}."
)

# KapazitaetsFehler direkt: alle drei Angaben
fehler = wert_von(lambda: KapazitaetsFehler("x", 5, "zu klein"))
assert (getattr(fehler, "vm", None), getattr(fehler, "fehlend", None), str(fehler)) == ("x", 5, "zu klein"), (
    f"KapazitaetsFehler('x', 5, 'zu klein') ergibt vm, fehlend, Meldung {(getattr(fehler, 'vm', None), getattr(fehler, 'fehlend', None), str(fehler))!r}."
)

# pruefe_umzug im Beispiel: ZuWenigRam mit 8 GB
hosts_test = {"esx-1": host(64, 8), "esx-3": host(256, 32, True)}
fehler = ausnahme_von(lambda: pruefe_umzug(vm("db-1", 72, 4), "esx-1", hosts_test))
assert type(fehler).__name__ == "ZuWenigRam" and getattr(fehler, "fehlend", None) == 8, (
    f"pruefe_umzug(db, 'esx-1', hosts) löst {beschreibe(fehler)} aus, erwartet war ZuWenigRam mit fehlend 8.\n"
    "Tipp: raise ZuWenigRam(vm['name'], vm['ram'] - host['ram_frei'])"
)

# pruefe_umzug: ein passender Umzug gibt None zurück und ändert nichts
ergebnis = wert_von(lambda: pruefe_umzug(vm("web-2", 16, 4), "esx-1", hosts_test))
assert ergebnis is None and hosts_test["esx-1"] == host(64, 8), (
    f"pruefe_umzug(web, 'esx-1', hosts) ergibt {ergebnis!r} und danach {hosts_test['esx-1']}, erwartet war None und keine Änderung."
)

# pruefe_umzug: ein Host in Wartung
fehler = ausnahme_von(lambda: pruefe_umzug(vm("web-2", 16, 4), "esx-3", hosts_test))
assert type(fehler).__name__ == "HostInWartung" and getattr(fehler, "host", None) == "esx-3", (
    f"pruefe_umzug(web, 'esx-3', hosts) löst {beschreibe(fehler)} aus, erwartet war HostInWartung für esx-3."
)

# pruefe_umzug: zu wenige Kerne (nicht fest hinschreiben!)
fehler = ausnahme_von(lambda: pruefe_umzug(vm("ci-4", 32, 11), "esx-1", hosts_test))
assert type(fehler).__name__ == "ZuWenigKerne" and getattr(fehler, "fehlend", None) == 3 and getattr(fehler, "vm", None) == "ci-4", (
    f"pruefe_umzug(vm mit 11 Kernen, 'esx-1' mit 8 freien) löst {beschreibe(fehler)} aus, erwartet war ZuWenigKerne mit fehlend 3."
)

# pruefe_umzug: Reihenfolge Wartung vor RAM vor Kernen
reihenfolge = [
    type(ausnahme_von(lambda: pruefe_umzug(vm("a", 999, 99), "esx-3", {"esx-3": host(1, 1, True)}))).__name__,
    type(ausnahme_von(lambda: pruefe_umzug(vm("a", 999, 99), "esx-1", {"esx-1": host(1, 1)}))).__name__,
]
assert reihenfolge == ["HostInWartung", "ZuWenigRam"], (
    f"Wenn alles fehlt, lösen die Prüfungen {reihenfolge} aus, erwartet war ['HostInWartung', 'ZuWenigRam'].\nTipp: Prüfen Sie Wartung, dann RAM, dann Kerne."
)

# pruefe_umzug: genau so viel frei wie nötig reicht
ergebnis = wert_von(lambda: pruefe_umzug(vm("genau", 64, 8), "esx-1", {"esx-1": host(64, 8)}))
assert ergebnis is None, f"Mit genau 64 GB und 8 Kernen frei ergibt pruefe_umzug {ergebnis!r}, erwartet war None.\nTipp: Zu klein ist ein Host nur bei >."

# pruefe_umzug: ein unbekannter Host löst KeyError aus
fehler = ausnahme_von(lambda: pruefe_umzug(vm("a", 1, 1), "esx-99", hosts_test))
assert isinstance(fehler, KeyError), f"pruefe_umzug für einen unbekannten Host löst {beschreibe(fehler)} aus, erwartet war KeyError."

def gleicher_bericht(ihr, erwartet):
    """Vergleicht zwei Berichte; die selbst formulierten Meldungen in "zu_klein" nur locker."""
    if not isinstance(ihr, dict) or set(ihr) != set(erwartet):
        return False
    if ihr["geplant"] != erwartet["geplant"] or ihr["wartung"] != erwartet["wartung"]:
        return False
    if not isinstance(ihr["zu_klein"], list) or len(ihr["zu_klein"]) != len(erwartet["zu_klein"]):
        return False
    return all(vergleichbar(a) == vergleichbar(b) for a, b in zip(ihr["zu_klein"], erwartet["zu_klein"]))


# plane_umzuege im Beispiel
hosts_test = {"esx-1": host(64, 8), "esx-3": host(256, 32, True)}
db_test, web_test = vm("db-1", 72, 4), vm("web-2", 16, 4)
ergebnis = wert_von(lambda: plane_umzuege([(web_test, "esx-1"), (web_test, "esx-3"), (db_test, "esx-1")], hosts_test))
erwartet = {"geplant": ["web-2"], "zu_klein": ["db-1: es fehlen 24 GB RAM"], "wartung": ["esx-3"]}
assert gleicher_bericht(ergebnis, erwartet), (
    f"plane_umzuege im Beispiel ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
    "Tipp: except KapazitaetsFehler as fehler: … str(fehler); except HostInWartung as fehler: … fehler.host"
)

# plane_umzuege im Beispiel: die freien Werte von esx-1 sind gesunken
assert hosts_test["esx-1"] == host(48, 4) and hosts_test["esx-3"] == host(256, 32, True), (
    f"Nach plane_umzuege ist hosts {hosts_test}, erwartet war esx-1 mit 48 GB und 4 Kernen frei, esx-3 unverändert.\n"
    "Tipp: Ziehen Sie RAM und Kerne nur ab, wenn pruefe_umzug keinen Fehler ausgelöst hat (else-Zweig)."
)

# plane_umzuege: ein späterer Auftrag sieht die schon gebuchten Umzüge
hosts_test = {"h": host(32, 8)}
auftraege = [(vm("a", 20, 2), "h"), (vm("b", 20, 2), "h"), (vm("c", 12, 8), "h"), (vm("d", 12, 6), "h")]
ergebnis = wert_von(lambda: plane_umzuege(auftraege, hosts_test))
erwartet = {"geplant": ["a", "d"], "zu_klein": ["b: es fehlen 8 GB RAM", "c: es fehlen 2 Kerne"], "wartung": []}
assert gleicher_bericht(ergebnis, erwartet), f"plane_umzuege mit vier VMs auf einem Host ergibt {ergebnis!r}, erwartet war {erwartet}."

# plane_umzuege: jeder Host in Wartung steht nur einmal im Bericht
hosts_test = {"w1": host(100, 100, True), "w2": host(100, 100, True), "ok": host(100, 100)}
auftraege = [(vm("a", 1, 1), "w2"), (vm("b", 1, 1), "w1"), (vm("c", 1, 1), "w2"), (vm("d", 1, 1), "ok")]
ergebnis = wert_von(lambda: plane_umzuege(auftraege, hosts_test))
erwartet = {"geplant": ["d"], "zu_klein": [], "wartung": ["w2", "w1"]}
assert ergebnis == erwartet, f"plane_umzuege mit zwei Hosts in Wartung ergibt {ergebnis!r}, erwartet war {erwartet}."

# plane_umzuege: keine Aufträge
ergebnis = wert_von(lambda: plane_umzuege([], {"h": host(1, 1)}))
assert ergebnis == {"geplant": [], "zu_klein": [], "wartung": []}, f"plane_umzuege([], hosts) ergibt {ergebnis!r}."

# plane_umzuege: ein unbekannter Host (KeyError) fliegt weiter
ergebnis = wert_von(lambda: plane_umzuege([(vm("a", 1, 1), "fehlt")], {"h": host(1, 1)}))
assert isinstance(ergebnis, str) and ergebnis.startswith("KeyError"), (
    f"plane_umzuege mit einem unbekannten Host ergibt {ergebnis!r}; erwartet war, dass der KeyError weiterfliegt.\n"
    "Tipp: Fangen Sie nur Ihre eigenen Fehlerklassen ab, nicht Exception."
)

# Ein Aufrufer kann alle Umzugsfehler mit except MigrationsFehler fangen
gefangen = []
for aufruf in [lambda: pruefe_umzug(vm("a", 1, 1), "w", {"w": host(9, 9, True)}), lambda: pruefe_umzug(vm("a", 99, 1), "h", {"h": host(9, 9)}), lambda: pruefe_umzug(vm("a", 1, 99), "h", {"h": host(9, 9)})]:
    try:
        aufruf()
        gefangen.append("nichts")
    except MigrationsFehler as fehler:
        gefangen.append(type(fehler).__name__)
    except Exception as fehler:
        gefangen.append(f"nicht gefangen: {type(fehler).__name__}")
assert gefangen == ["HostInWartung", "ZuWenigRam", "ZuWenigKerne"], f"except MigrationsFehler fängt {gefangen}, erwartet waren alle drei Fehlerarten."

# Die Ausgabe des Programms
erwartet = (
    "ZuWenigRam db-1: es fehlen 8 GB RAM\n"
    "{'geplant': ['web-2'], 'zu_klein': ['db-1: es fehlen 24 GB RAM'], 'wartung': ['esx-3']}\n"
    "{'ram_frei': 48, 'kerne_frei': 4, 'wartung': False}"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"


def vergleich_planung(auftraege, hosts):
    """Vergleichslösung ohne Ausnahmen: rechnet den Bericht direkt aus."""
    bericht = {"geplant": [], "zu_klein": [], "wartung": []}
    for maschine, ziel in auftraege:
        frei = hosts[ziel]
        if frei["wartung"]:
            if ziel not in bericht["wartung"]:
                bericht["wartung"].append(ziel)
        elif maschine["ram"] > frei["ram_frei"]:
            bericht["zu_klein"].append(f"{maschine['name']}: es fehlen {maschine['ram'] - frei['ram_frei']} GB RAM")
        elif maschine["kerne"] > frei["kerne_frei"]:
            bericht["zu_klein"].append(f"{maschine['name']}: es fehlen {maschine['kerne'] - frei['kerne_frei']} Kerne")
        else:
            frei["ram_frei"] -= maschine["ram"]
            frei["kerne_frei"] -= maschine["kerne"]
            bericht["geplant"].append(maschine["name"])
    return bericht


def kopie(hosts):
    """Eine Kopie der Hosts, deren Einträge unabhängig sind."""
    return {name: dict(werte) for name, werte in hosts.items()}


# Viele zufällige Planungen
zufall = Zufall(4056)
for _ in range(200):
    hosts_zufall = {f"esx-{n}": host(zufall.randint(0, 300), zufall.randint(0, 40), zufall.random() < 0.2) for n in range(zufall.randint(1, 5))}
    auftraege = [(vm(f"vm-{n}", zufall.randint(1, 128), zufall.randint(1, 16)), zufall.choice(list(hosts_zufall))) for n in range(zufall.randint(0, 15))]
    ihre, vergleich = kopie(hosts_zufall), kopie(hosts_zufall)
    ergebnis = wert_von(lambda: plane_umzuege(auftraege, ihre))
    erwartet = vergleich_planung(auftraege, vergleich)
    assert gleicher_bericht(ergebnis, erwartet) and ihre == vergleich, f"Für hosts={hosts_zufall} und {auftraege} ergibt plane_umzuege {ergebnis!r}, erwartet war {erwartet}."

# Obere Grenze: 1000 Aufträge auf 100 Hosts
hosts_gross = {f"esx-{n}": host(zufall.randint(0, 4096), zufall.randint(0, 4096), n % 10 == 0) for n in range(100)}
auftraege = [(vm(f"vm-{n}", zufall.randint(1, 1024), zufall.randint(1, 1024)), f"esx-{zufall.randint(0, 99)}") for n in range(1000)]
ihre, vergleich = kopie(hosts_gross), kopie(hosts_gross)
ergebnis = wert_von(lambda: plane_umzuege(auftraege, ihre))
assert gleicher_bericht(ergebnis, vergleich_planung(auftraege, vergleich)) and ihre == vergleich, "Bei 1000 Aufträgen auf 100 Hosts stimmt plane_umzuege nicht."
