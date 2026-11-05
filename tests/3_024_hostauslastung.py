# Automatisch erzeugt aus lehrkraft/muster/3_024_hostauslastung.py - nicht von Hand ändern.
# vorlage-hash: 76e46054055c8f5f
# text-hash: dc3038ecd54ef8e7
# thema: kontrollfluss
# inhalt: Übung: Comprehensions und Generatoren

import ast
import inspect
import textwrap


def bauweise(funktion):
    """Gibt die Menge der Knotentypen im Syntaxbaum der Funktion zurück, leer, wenn der Quelltext fehlt."""
    try:
        baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))
    except (OSError, TypeError, SyntaxError):
        return set()
    return {type(knoten) for knoten in ast.walk(baum)}


def beispiel():
    """Baut VMs und Kapazitäten aus dem Beispiel neu."""
    vms = [("web1", "host-a", 4096, True), ("web2", "host-a", 4096, False), ("db1", "host-b", 16384, True), ("mail", "host-a", 2048, True)]
    return vms, {"host-a": 8192, "host-b": 32768, "host-c": 16384}


# Vergleichslösung: alles in einer einzigen for-Schleife mit einem Dictionary für die Summen
def von_hand(vms, kapazitaet, grenze):
    """Berechnet die vier Antworten ohne Comprehensions."""
    namen = []
    hosts = set()
    belegt = {}
    for host in kapazitaet:
        belegt[host] = 0
    for name, host, ram, laeuft in vms:
        if laeuft:
            namen.append(name)
            hosts.add(host)
            belegt[host] = belegt[host] + ram
    prozent = {}
    for host in kapazitaet:
        prozent[host] = round(100 * belegt[host] / kapazitaet[host], 1)
    unter = True
    for wert in prozent.values():
        if wert > grenze:
            unter = False
    return namen, hosts, prozent, unter


# Das Beispiel aus der Aufgabe
vms, kapazitaet = beispiel()
ergebnis = (laufende(vms), belegte_hosts(vms), auslastung(vms, kapazitaet))
erwartet = (["web1", "db1", "mail"], {"host-a", "host-b"}, {"host-a": 75.0, "host-b": 50.0, "host-c": 0.0})
assert ergebnis == erwartet, (
    f"Für das Beispiel ergeben laufende, belegte_hosts und auslastung {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Nur laufende VMs belegen Speicher; Hosts ohne laufende VM haben die Auslastung 0.0."
)

# alle_unter aus dem Beispiel
ergebnis = (alle_unter(vms, kapazitaet, 80), alle_unter(vms, kapazitaet, 70))
assert ergebnis == (True, False), (
    f"alle_unter(vms, kapazitaet, 80) und (…, 70) ergeben {ergebnis!r}, erwartet war (True, False)."
)

# Genau an der Grenze liegt nicht darüber
ergebnis = (alle_unter(vms, kapazitaet, 75), alle_unter(vms, kapazitaet, 74))
assert ergebnis == (True, False), (
    f"Bei einer höchsten Auslastung von genau 75.0 % ergeben alle_unter(…, 75) und (…, 74) {ergebnis!r}, erwartet war "
    "(True, False).\nTipp: Genau gleich grenze ist erlaubt: vergleichen Sie mit <=."
)

# Die Ergebnistypen stimmen
typen = (type(laufende(vms)).__name__, type(belegte_hosts(vms)).__name__, type(auslastung(vms, kapazitaet)).__name__)
assert typen == ("list", "set", "dict"), (
    f"laufende, belegte_hosts und auslastung geben {typen} zurück, erwartet war ('list', 'set', 'dict')."
)

# Die übergebenen Daten bleiben unverändert
assert (vms, kapazitaet) == beispiel(), "Die Funktionen sollen vms und kapazitaet nicht verändern."

# Andere Werte (nicht fest hinschreiben!), auch überbucht und mit gerundeter Prozentzahl
vms = [("a", "h1", 1000, True), ("b", "h1", 2000, True), ("c", "h2", 1, True), ("d", "h2", 5, False)]
kapazitaet = {"h1": 2400, "h2": 3}
ergebnis = (laufende(vms), belegte_hosts(vms), auslastung(vms, kapazitaet), alle_unter(vms, kapazitaet, 125))
erwartet = (["a", "b", "c"], {"h1", "h2"}, {"h1": 125.0, "h2": 33.3}, True)
assert ergebnis == erwartet, f"Für {vms} und {kapazitaet} ergeben die vier Funktionen {ergebnis!r}, erwartet war {erwartet!r}."

# Randfälle: keine VMs, keine laufende VM, grenze 0
for vms, kapazitaet, grenze in [([], {"h": 10}, 0), ([("x", "h", 5, False)], {"h": 10, "g": 1}, 0), ([("x", "h", 1, True)], {"h": 10**7}, 0)]:
    ergebnis = (laufende(vms), belegte_hosts(vms), auslastung(vms, kapazitaet), alle_unter(vms, kapazitaet, grenze))
    erwartet = von_hand(vms, kapazitaet, grenze)
    assert ergebnis == erwartet, (
        f"Für vms={vms}, kapazitaet={kapazitaet}, grenze={grenze} ergeben die vier Funktionen {ergebnis!r}, "
        f"erwartet war {erwartet!r}.\nTipp: Eine leere Menge ist set(), und all(...) über nichts Falsches ist True."
    )

# Comprehensions und Generator-Ausdrücke werden benutzt, keine for- oder while-Anweisung
for funktion, verlangt, beschreibung in [
    (laufende, {ast.ListComp, ast.GeneratorExp}, "einer List Comprehension [… for … in … if …]"),
    (belegte_hosts, {ast.SetComp, ast.GeneratorExp}, "einer Set Comprehension {… for … in … if …}"),
    (auslastung, {ast.DictComp}, "einer Dict Comprehension {host: … for host, … in kapazitaet.items()}"),
    (alle_unter, {ast.GeneratorExp}, "einem Generator-Ausdruck in all(… for …)"),
]:
    knotentypen = bauweise(funktion)
    assert verlangt & knotentypen and ast.For not in knotentypen and ast.While not in knotentypen, (
        f"{funktion.__name__} soll mit {beschreibung} arbeiten, ohne for- oder while-Anweisung."
    )

# Die Summe in auslastung ist ein Generator-Ausdruck, keine Liste
knotentypen = bauweise(auslastung)
assert ast.GeneratorExp in knotentypen and ast.ListComp not in knotentypen, (
    "auslastung soll die Speicher eines Hosts mit sum(… for …) addieren, ohne eine Liste in eckigen Klammern zu bauen."
)

# 300 zufällige Rechenzentren
zufall = Zufall(3024)
for _ in range(300):
    hosts = zufall.sample(["h1", "h2", "h3", "h4"], zufall.randint(1, 4))
    kapazitaet = {host: zufall.choice([1, 3, 1000, 4096, 10**7]) for host in hosts}
    vms = [(f"vm{nummer}", zufall.choice(hosts), zufall.choice([1, 7, 512, 4096, 10**6]), zufall.random() < 0.7) for nummer in range(zufall.randint(0, 8))]
    grenze = zufall.choice([0, 50, 100, 1000])
    kopie = list(vms)
    erwartet = von_hand(kopie, kapazitaet, grenze)
    ergebnis = (laufende(vms), belegte_hosts(vms), auslastung(vms, kapazitaet), alle_unter(vms, kapazitaet, grenze))
    assert ergebnis == erwartet, (
        f"Für vms={kopie}, kapazitaet={kapazitaet}, grenze={grenze} ergeben laufende, belegte_hosts, auslastung und "
        f"alle_unter {ergebnis!r}, erwartet war {erwartet!r}."
    )

# An der oberen Grenze: 10 000 VMs auf 50 Hosts
kapazitaet = {f"host-{nummer:02d}": 10**7 - nummer for nummer in range(50)}
vms = [(f"vm{nummer}", f"host-{nummer % 50:02d}", (nummer * 7919) % 10**6 + 1, nummer % 3 != 0) for nummer in range(10000)]
ergebnis = (len(laufende(vms)), len(belegte_hosts(vms)), auslastung(vms, kapazitaet), alle_unter(vms, kapazitaet, 1000))
namen, hosts, prozent, unter = von_hand(vms, kapazitaet, 1000)
assert ergebnis == (len(namen), len(hosts), prozent, unter), (
    f"Mit 10 000 VMs auf 50 Hosts ergeben len(laufende), len(belegte_hosts) und alle_unter(…, 1000) "
    f"{ergebnis[0]}, {ergebnis[1]} und {ergebnis[3]}, auslastung für host-00 {ergebnis[2].get('host-00')!r}; "
    f"erwartet waren {len(namen)}, {len(hosts)}, {unter} und {prozent['host-00']!r}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "['web1', 'db1', 'mail']\n['host-a', 'host-b']\n{'host-a': 75.0, 'host-b': 50.0, 'host-c': 0.0}\nTrue False"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
