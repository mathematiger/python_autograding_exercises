# Automatisch erzeugt aus lehrkraft/muster/2_026_containerspeicher.py - nicht von Hand ändern.
# vorlage-hash: 0ea0c87638665bec
# text-hash: ee3a98a9d949f0f6
# thema: datenstrukturen
# inhalt: get mit Standardwert

def beispiel():
    """Baut die Limits aus dem Beispiel neu."""
    return {"shop": 2048, "datenbank": 8192}


# speicherlimit aus dem Beispiel
limits = beispiel()
ergebnis = (speicherlimit(limits, "shop"), speicherlimit(limits, "datenbank"))
assert ergebnis == (2048, 8192), f"speicherlimit(limits, 'shop') und (…, 'datenbank') ergeben {ergebnis!r}, erwartet war (2048, 8192)."

# Container ohne Eintrag bekommen das Standardlimit
try:
    ergebnis = speicherlimit(limits, "mailer")
except KeyError as fehler:
    ergebnis = f"KeyError: {fehler}"
assert ergebnis == 512, (
    f"speicherlimit(limits, 'mailer') ergibt {ergebnis!r}, erwartet war 512 (STANDARD_MB).\n"
    "Tipp: limits[container] bricht ab, wenn es den Schlüssel nicht gibt; limits.get(container, STANDARD_MB) nicht."
)

# Ein eingetragenes Limit gilt auch, wenn es kleiner als das Standardlimit ist
ergebnis = (speicherlimit({"klein": 1}, "klein"), speicherlimit({"genau": 512}, "genau"), speicherlimit({}, "x"))
assert ergebnis == (1, 512, 512), (
    f"speicherlimit({{'klein': 1}}, 'klein'), speicherlimit({{'genau': 512}}, 'genau') und speicherlimit({{}}, 'x') "
    f"ergeben {ergebnis!r}, erwartet war (1, 512, 512).\n"
    "Tipp: Das Standardlimit gilt nur für Container ohne Eintrag, nicht als Mindestwert."
)

# speicher_pro_host addiert je Host, zuerst nur Container mit eingetragenem Limit
laufend = [("shop", "host-a"), ("datenbank", "host-a")]
ergebnis = speicher_pro_host(limits, laufend)
assert ergebnis == {"host-a": 10240}, (
    f"speicher_pro_host(limits, {laufend}) ergibt {ergebnis!r}, erwartet war {{'host-a': 10240}}.\n"
    "Tipp: Addieren Sie zum bisherigen Wert des Hosts: summe.get(host, 0) + limit."
)

# speicher_pro_host aus dem Beispiel
laufend = [("shop", "host-a"), ("mailer", "host-b"), ("datenbank", "host-a")]
ergebnis = speicher_pro_host(limits, laufend)
assert ergebnis == {"host-a": 10240, "host-b": 512}, (
    f"speicher_pro_host(limits, {laufend}) ergibt {ergebnis!r}, erwartet war {{'host-a': 10240, 'host-b': 512}}.\n"
    "Tipp: Addieren Sie zum bisherigen Wert des Hosts: summe.get(host, 0) + limit."
)

# limits bleibt unverändert
assert limits == beispiel(), (
    f"Nach den Aufrufen ist limits {limits!r}, erwartet war unverändert {beispiel()!r}.\n"
    "Tipp: get liest nur; tragen Sie das Standardlimit nicht in limits ein."
)

# Andere Werte (nicht fest hinschreiben!)
limits = {"wiki": 1024, "chat": 300}
laufend = [("chat", "h1"), ("wiki", "h2"), ("monitor", "h1"), ("backup", "h1")]
ergebnis = speicher_pro_host(limits, laufend)
assert ergebnis == {"h1": 1324, "h2": 1024}, (
    f"speicher_pro_host({limits}, {laufend}) ergibt {ergebnis!r}, erwartet war {{'h1': 1324, 'h2': 1024}}."
)

# Keine laufenden Container
ergebnis = speicher_pro_host({"a": 5}, [])
assert ergebnis == {}, f"speicher_pro_host({{'a': 5}}, []) ergibt {ergebnis!r}, erwartet war {{}}."

# Keine Limits
ergebnis = speicher_pro_host({}, [("a", "h")])
assert ergebnis == {"h": 512}, f"speicher_pro_host({{}}, [('a', 'h')]) ergibt {ergebnis!r}, erwartet war {{'h': 512}}."

# speicherlimit benutzt STANDARD_MB (z. B. wenn sich das Standardlimit ändert)
STANDARD_MB = 256
try:
    ergebnis = speicherlimit({}, "neu")
finally:
    STANDARD_MB = 512
assert ergebnis == 256, (
    f"Mit STANDARD_MB = 256 ergibt speicherlimit({{}}, 'neu') {ergebnis!r}, erwartet war 256.\n"
    "Tipp: Schreiben Sie STANDARD_MB statt der Zahl 512."
)

# speicher_pro_host benutzt speicherlimit (z. B. wenn sich das Standardlimit ändert)
STANDARD_MB = 256
try:
    ergebnis = speicher_pro_host({}, [("neu", "h")])
finally:
    STANDARD_MB = 512
assert ergebnis == {"h": 256}, (
    f"Mit STANDARD_MB = 256 ergibt speicher_pro_host({{}}, [('neu', 'h')]) {ergebnis!r}, erwartet war {{'h': 256}}.\n"
    "Tipp: Schreiben Sie STANDARD_MB statt der Zahl 512 und benutzen Sie in speicher_pro_host die Funktion speicherlimit."
)


# Vergleichslösung: erst alle Hosts sammeln, dann für jeden Host die Liste durchgehen
def pro_host_von_hand(limits, laufend):
    """Summiert für jeden Host über alle laufenden Container, mit in statt get."""
    ergebnis = {}
    for _, host in laufend:
        ergebnis[host] = 0
    for container, host in laufend:
        if container in limits:
            ergebnis[host] = ergebnis[host] + limits[container]
        else:
            ergebnis[host] = ergebnis[host] + 512
    return ergebnis


# 300 zufällige Belegungen
zufall = Zufall(2026)
for _ in range(300):
    namen = ["shop", "wiki", "db", "mail", "chat", "log", "cache"]
    limits = {name: zufall.choice([1, 256, 512, 513, 4096, 10**6]) for name in zufall.sample(namen, zufall.randint(0, 5))}
    vorher = dict(limits)
    container = zufall.sample(namen, zufall.randint(0, 7))
    laufend = [(name, zufall.choice(["h1", "h2", "h3"])) for name in container]
    erwartet = pro_host_von_hand(limits, laufend)
    ergebnis = speicher_pro_host(limits, laufend)
    assert ergebnis == erwartet and limits == vorher, (
        f"speicher_pro_host({vorher}, {laufend}) ergibt {ergebnis!r}, erwartet war {erwartet!r}; "
        f"limits ist danach {limits!r}."
    )

# An der oberen Grenze: 10 000 Limits, 100 000 laufende Container auf 50 Hosts
limits = {f"c{nummer}": (nummer * 37) % 10**6 + 1 for nummer in range(0, 200000, 20)}
laufend = [(f"c{nummer}", f"host-{nummer % 50}") for nummer in range(100000)]
ergebnis = speicher_pro_host(limits, laufend)
erwartet = pro_host_von_hand(limits, laufend)
assert ergebnis == erwartet, (
    f"Bei 100 000 Containern auf 50 Hosts ergibt speicher_pro_host für host-0 {ergebnis.get('host-0')!r} "
    f"und insgesamt {len(ergebnis)} Hosts; erwartet waren {erwartet['host-0']} und 50 Hosts."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "2048 512\n{'host-a': 10240, 'host-b': 512}"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
