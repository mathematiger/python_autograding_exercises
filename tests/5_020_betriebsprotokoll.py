# Automatisch erzeugt aus lehrkraft/muster/5_020_betriebsprotokoll.py - nicht von Hand ändern.
# vorlage-hash: 9e269110d1592de4
# text-hash: 06a0417cf7cfde0c
# thema: klassen
# inhalt: __call__ und Dekorator-Klassen

def ergebnis_von(aufruf, *args, **kwargs):
    """Ruft aufruf auf; liefert das Ergebnis oder den Namen der Ausnahme in spitzen Klammern."""
    try:
        return aufruf(*args, **kwargs)
    except Exception as fehler:
        return f"<{type(fehler).__name__}>"


# Platzierungsregel aus dem Beispiel: die passenden VMs
regel = Platzierungsregel(kerne=8, ram=32)
ergebnis = list(filter(regel, [("web", 2, 8), ("db", 8, 64), ("cache", 4, 16)]))
assert ergebnis == [("web", 2, 8), ("cache", 4, 16)], (
    f"filter(Platzierungsregel(kerne=8, ram=32), <Beispiel>) ergibt {ergebnis!r}, "
    "erwartet war [('web', 2, 8), ('cache', 4, 16)].\n"
    "Tipp: __call__ bekommt die VM als Tupel (name, kerne, ram) und gibt True zurück, wenn sie passt."
)

# Platzierungsregel aus dem Beispiel: gefragt zählt jeden Aufruf
assert ergebnis == [("web", 2, 8), ("cache", 4, 16)] and regel.gefragt == 3, (
    f"filter(Platzierungsregel(kerne=8, ram=32), <Beispiel>) ergibt {ergebnis!r} und gefragt {regel.gefragt!r}, "
    "erwartet war [('web', 2, 8), ('cache', 4, 16)] und 3.\n"
    "Tipp: __call__ bekommt die VM als Tupel (name, kerne, ram) und zählt bei jedem Aufruf self.gefragt hoch."
)

# Genau passend zählt, eins zu viel nicht
regel = Platzierungsregel(kerne=4, ram=16)
ergebnis = [regel(vm) for vm in [("a", 4, 16), ("b", 5, 16), ("c", 4, 17), ("d", 0, 0)]]
assert ergebnis == [True, False, False, True], (
    f"Platzierungsregel(kerne=4, ram=16) für (4, 16), (5, 16), (4, 17) und (0, 0) ergibt {ergebnis}, "
    "erwartet war [True, False, False, True].\nTipp: Höchstens heißt <=; beide Bedingungen müssen gelten."
)

# Jede Regel zählt für sich, auch wenn die VM nicht passt
voll = Platzierungsregel(kerne=0, ram=0)
leer = Platzierungsregel(kerne=10**6, ram=10**6)
for vm in [("x", 1, 1), ("y", 10**6, 10**6)]:
    voll(vm)
    voll(vm)
    leer(vm)
assert (voll.gefragt, leer.gefragt) == (4, 2) and voll(("z", 0, 0)) is True and leer(("z", 10**6, 10**6)) is True, (
    f"Zwei Regeln, die eine viermal, die andere zweimal gefragt, zählen {voll.gefragt!r} und {leer.gefragt!r}, "
    "erwartet war 4 und 2; außerdem passt eine VM ohne Kerne und RAM auf jeden Host, eine mit 10**6 genau auf "
    "einen Host mit 10**6.\nTipp: Speichern Sie den Zähler am Objekt (self.gefragt), nicht in der Klasse."
)

# Die Regel ist aufrufbar und gibt bool zurück
regel = Platzierungsregel(kerne=2, ram=4)
ergebnis = regel(("m", 1, 1))
assert callable(regel) and ergebnis is True, f"Platzierungsregel(2, 4)(('m', 1, 1)) ergibt {ergebnis!r}, erwartet war True."


@Protokolliert
def neu_starten(host, *, warten=0):
    """Startet einen Host neu."""
    if host == "":
        raise ValueError("Kein Host angegeben")
    return f"{host} neu gestartet nach {warten} s"


# Das Ergebnis der Funktion kommt durch
ergebnis = ergebnis_von(neu_starten, "esx01", warten=30)
assert ergebnis == "esx01 neu gestartet nach 30 s", (
    f'neu_starten("esx01", warten=30) ergibt {ergebnis!r}, erwartet war "esx01 neu gestartet nach 30 s".\n'
    "Tipp: __call__ muss das Ergebnis von self.funktion(*args, **kwargs) zurückgeben."
)

# Der Aufruf steht im Protokoll, mit Positions- und Schlüsselwortargumenten
assert neu_starten.aufrufe == [(("esx01",), {"warten": 30})], (
    f"Nach neu_starten('esx01', warten=30) ist aufrufe {getattr(neu_starten, 'aufrufe', None)!r}, erwartet war "
    "[(('esx01',), {'warten': 30})].\nTipp: Hängen Sie das Paar (args, kwargs) an, args ist schon ein Tupel."
)

# Name, Docstring und __wrapped__ werden übernommen
ergebnis = (neu_starten.__name__, neu_starten.__doc__, getattr(neu_starten, "__wrapped__", None) is not None)
assert ergebnis == ("neu_starten", "Startet einen Host neu.", True), (
    f"__name__, __doc__ und __wrapped__ des dekorierten Objekts ergeben {ergebnis!r}, erwartet war "
    "('neu_starten', 'Startet einen Host neu.', True).\nTipp: functools.update_wrapper(self, funktion) in __init__."
)

# Eine Ausnahme der Funktion läuft weiter
ergebnis = ergebnis_von(neu_starten, "")
assert ergebnis == "<ValueError>", (
    f'neu_starten("") ergibt {ergebnis!r}, erwartet war ein ValueError.\n'
    "Tipp: Fangen Sie die Ausnahme nicht endgültig ab; werfen Sie sie im except mit raise weiter."
)

# Eine Ausnahme wird gezählt und trotzdem protokolliert
assert ergebnis == "<ValueError>" and neu_starten.fehler == 1 and neu_starten.aufrufe[-1] == (("",), {}), (
    f'neu_starten("") ergibt {ergebnis!r}, fehler ist {neu_starten.fehler!r}, letzter Eintrag in aufrufe '
    f"{neu_starten.aufrufe[-1]!r}; erwartet war ein ValueError, fehler 1 und (('',), {{}}).\n"
    "Tipp: Protokollieren Sie vor dem Aufruf, zählen Sie im except und werfen Sie mit raise weiter."
)

# Erfolgreiche Aufrufe zählen nicht als Fehler
ergebnis_von(neu_starten, "esx02")
assert (len(neu_starten.aufrufe), neu_starten.fehler) == (3, 1), (
    f"Nach drei Aufrufen, einer davon mit Fehler, ist len(aufrufe) {len(neu_starten.aufrufe)} und fehler "
    f"{neu_starten.fehler!r}, erwartet war 3 und 1."
)


@Protokolliert
def ohne_argumente():
    """Liefert immer 42."""
    return 42


# Jede dekorierte Funktion hat ihr eigenes Protokoll
ohne_argumente()
assert ohne_argumente.aufrufe == [((), {})] and len(neu_starten.aufrufe) == 3, (
    f"ohne_argumente.aufrufe ist {ohne_argumente.aufrufe!r} und neu_starten hat {len(neu_starten.aufrufe)} Einträge; "
    "erwartet war [((), {})] und 3.\nTipp: Legen Sie aufrufe in __init__ auf self an, nicht als Klassenattribut."
)

# Das dekorierte Objekt ist eine Instanz von Protokolliert und aufrufbar
assert isinstance(ohne_argumente, Protokolliert) and callable(ohne_argumente), (
    "@Protokolliert soll die Funktion durch ein Protokolliert-Objekt ersetzen, das aufrufbar ist."
)

# Andere Ausnahmen laufen genauso weiter
@Protokolliert
def teile(a, b):
    """Teilt a durch b."""
    return a / b


ergebnisse = (ergebnis_von(teile, 1, 0), ergebnis_von(teile, 1, "x"), ergebnis_von(teile, 6, b=3))
assert ergebnisse == ("<ZeroDivisionError>", "<TypeError>", 2.0) and teile.fehler == 2, (
    f"teile(1, 0), teile(1, 'x') und teile(6, b=3) ergeben {ergebnisse!r} mit fehler {teile.fehler!r}, "
    "erwartet war ('<ZeroDivisionError>', '<TypeError>', 2.0) und fehler 2."
)

# 300 zufällige Aufrufe einer protokollierten Funktion gegen eine Nachrechnung
zufall = Zufall(5020)


@Protokolliert
def platz(kerne, ram=0, *, host="esx"):
    """Wirft bei negativem RAM einen Fehler, sonst liefert es eine Beschreibung."""
    if ram < 0:
        raise ValueError("RAM negativ")
    return (host, kerne, ram)


regel = Platzierungsregel(kerne=zufall.randint(0, 64), ram=zufall.randint(0, 512))
WERTE = []
for nummer in range(300):
    kerne = zufall.randint(0, 64)
    WERTE.append((kerne, zufall.randint(-5, 512)))
erwartete_aufrufe = []
erwartete_fehler = 0
for nummer, (kerne, ram) in enumerate(WERTE):
    if nummer % 3 == 0:
        args, kwargs = (kerne,), {"ram": ram}
    elif nummer % 3 == 1:
        args, kwargs = (kerne, ram), {"host": f"esx{nummer}"}
    else:
        args, kwargs = (kerne, ram), {}
    erwartete_aufrufe.append((args, kwargs))
    ergebnis = ergebnis_von(platz, *args, **kwargs)
    erwartet = "<ValueError>" if ram < 0 else (kwargs.get("host", "esx"), kerne, ram)
    erwartete_fehler += ram < 0
    assert ergebnis == erwartet, f"platz(*{args}, **{kwargs}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# 300 zufällige VMs für eine Platzierungsregel
for kerne, ram in WERTE:
    passt = regel(("vm", kerne, max(ram, 0)))
    assert passt == (kerne <= regel.kerne and max(ram, 0) <= regel.ram), (
        f"Platzierungsregel(kerne={regel.kerne}, ram={regel.ram}) für ({kerne}, {max(ram, 0)}) ergibt {passt!r}."
    )

# Nach den 300 zufälligen Aufrufen stimmen Protokoll, Fehlerzahl und gefragt
assert platz.aufrufe == erwartete_aufrufe and platz.fehler == erwartete_fehler and regel.gefragt == 300, (
    f"Nach 300 Aufrufen hat das Protokoll {len(platz.aufrufe)} Einträge und fehler {platz.fehler!r}, die Regel "
    f"gefragt {regel.gefragt!r}; erwartet waren 300 Einträge in der Reihenfolge der Aufrufe, fehler "
    f"{erwartete_fehler} und gefragt 300."
)

# Obere Grenze: Werte bis 10**6
vm = ("gross", 10**6, 10**6)
ergebnis = (Platzierungsregel(kerne=10**6, ram=10**6)(vm), Platzierungsregel(kerne=10**6, ram=10**6 - 1)(vm))
assert ergebnis == (True, False), (
    f"Die VM {vm} auf Hosts mit (10**6, 10**6) und (10**6, 10**6 - 1) ergibt {ergebnis!r}, erwartet war (True, False)."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "[('web', 2, 8), ('cache', 4, 16)] 3\nweb läuft mit 8 GB\n[(('web',), {'ram': 8})] starte_vm"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
