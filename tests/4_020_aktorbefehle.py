# Automatisch erzeugt aus lehrkraft/muster/4_020_aktorbefehle.py - nicht von Hand ändern.
# vorlage-hash: 994284f3ca024920
# text-hash: affe56fb972e4f6a
# thema: funktionen
# inhalt: Schlüsselwort-only-Parameter

import inspect


def arten(funktion):
    """Gibt zu jedem Parameter Namen, Art und Standardwert zurück."""
    namen = {
        inspect.Parameter.POSITIONAL_OR_KEYWORD: "normal",
        inspect.Parameter.KEYWORD_ONLY: "nur mit Namen",
    }
    ergebnis = []
    for parameter in inspect.signature(funktion).parameters.values():
        standard = "ohne" if parameter.default is inspect.Parameter.empty else parameter.default
        ergebnis.append((parameter.name, namen.get(parameter.kind, str(parameter.kind)), standard))
    return ergebnis


def ausnahme_bei(aufruf):
    """Führt aufruf() aus und gibt die Ausnahme zurück, oder None, wenn keine kam."""
    try:
        aufruf()
    except Exception as fehler:
        return fehler
    return None


def nachricht(topic, payload, qos=0, retain=False):
    """Baut die erwartete Nachricht."""
    return {"topic": topic, "payload": payload, "qos": qos, "retain": retain}


# Die Parameterlisten sind unverändert
ergebnis = [arten(befehl), arten(rampe), arten(dimme)]
erwartet = [
    [("topic", "normal", "ohne"), ("wert", "normal", "ohne"), ("qos", "nur mit Namen", 0), ("retain", "nur mit Namen", False)],
    [("start", "normal", "ohne"), ("ziel", "normal", "ohne"), ("schritte", "nur mit Namen", "ohne")],
    [
        ("topic", "normal", "ohne"), ("start", "normal", "ohne"), ("ziel", "normal", "ohne"),
        ("schritte", "nur mit Namen", "ohne"), ("qos", "nur mit Namen", 0), ("retain", "nur mit Namen", False),
    ],
]
assert ergebnis == erwartet, (
    f"Die Parameter sind {ergebnis}, erwartet war {erwartet}.\nTipp: Ändern Sie die vorgegebenen Funktionsköpfe nicht."
)

# befehl aus dem Beispiel, mit Standardwerten
ergebnis = befehl("etage2/raum204/jalousie", 75)
erwartet = nachricht("etage2/raum204/jalousie", "75")
assert ergebnis == erwartet, (
    f'befehl("etage2/raum204/jalousie", 75) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n'
    'Tipp: Die Payload ist ein Text: str(75) ist "75".'
)

# befehl mit Namen in beliebiger Reihenfolge
ergebnis = befehl("etage2/raum204/licht", 40, retain=True, qos=1)
erwartet = nachricht("etage2/raum204/licht", "40", 1, True)
assert ergebnis == erwartet, (
    f'befehl("etage2/raum204/licht", 40, retain=True, qos=1) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n'
    "Tipp: Übernehmen Sie qos und retain aus den Parametern, nicht die Standardwerte."
)

# Andere Werte, auch Texte und die Ränder (nicht fest hinschreiben!)
for argumente, optionen, erwartet in [
    (("a/b", "an"), {"qos": 2}, nachricht("a/b", "an", 2)),
    (("lüfter", 0), {"retain": True}, nachricht("lüfter", "0", 0, True)),
    (("x", 100), {"qos": 0, "retain": False}, nachricht("x", "100")),
]:
    ergebnis = befehl(*argumente, **optionen)
    assert ergebnis == erwartet, f"befehl{argumente} mit {optionen} ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Falsches qos: ValueError mit dem Wert
for falsch in [3, -1, 10]:
    fehler = ausnahme_bei(lambda: befehl("a/b", 1, qos=falsch))
    assert isinstance(fehler, ValueError) and str(falsch) in str(fehler), (
        f"befehl('a/b', 1, qos={falsch}) muss einen ValueError auslösen, dessen Meldung {falsch} enthält; "
        f"bekommen: {fehler!r}.\nTipp: Prüfen Sie mit qos not in (0, 1, 2)."
    )

# qos und retain nach Position: TypeError
fehler = ausnahme_bei(lambda: befehl("etage2/raum204/licht", 40, 1))
assert isinstance(fehler, TypeError), (
    f'befehl("etage2/raum204/licht", 40, 1) muss einen TypeError auslösen, weil qos nur mit Namen übergeben werden darf; '
    f"bekommen: {fehler!r}.\nTipp: Der einzelne Stern in der Parameterliste muss stehen bleiben."
)

# rampe aus dem Beispiel: hoch, runter, mit Abrunden
for start, ziel, schritte, erwartet in [(0, 100, 4, [25, 50, 75, 100]), (80, 20, 4, [65, 50, 35, 20]), (0, 10, 3, [3, 6, 10])]:
    ergebnis = rampe(start, ziel, schritte=schritte)
    assert ergebnis == erwartet, (
        f"rampe({start}, {ziel}, schritte={schritte}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Der i-te Wert ist start + (ziel - start) * i // schritte, i läuft von 1 bis schritte."
    )

# Abrunden auch beim Herunterdimmen und Ränder
for start, ziel, schritte, erwartet in [
    (10, 0, 3, [6, 3, 0]),
    (50, 50, 3, [50, 50, 50]),
    (0, 100, 1, [100]),
    (100, 0, 1, [0]),
    (0, 1, 2, [0, 1]),
]:
    ergebnis = rampe(start, ziel, schritte=schritte)
    assert ergebnis == erwartet, (
        f"rampe({start}, {ziel}, schritte={schritte}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: // rundet auch bei negativen Zahlen ab: -10 // 3 ist -4; benutzen Sie genau die Formel aus der Aufgabe."
    )

# schritte nur mit Namen und ohne Standardwert
fehler_position = ausnahme_bei(lambda: rampe(0, 100, 4))
fehler_ohne = ausnahme_bei(lambda: rampe(0, 100))
assert isinstance(fehler_position, TypeError) and isinstance(fehler_ohne, TypeError), (
    f"rampe(0, 100, 4) und rampe(0, 100) müssen einen TypeError auslösen; bekommen: {fehler_position!r} und {fehler_ohne!r}."
)

# dimme aus dem Beispiel
ergebnis = dimme("flur/licht", 0, 100, schritte=2, qos=1)
erwartet = [nachricht("flur/licht", "50", 1), nachricht("flur/licht", "100", 1)]
assert ergebnis == erwartet, (
    f'dimme("flur/licht", 0, 100, schritte=2, qos=1) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n'
    "Tipp: Reichen Sie qos und retain mit Namen an befehl weiter: befehl(topic, wert, qos=qos, retain=retain)."
)

# dimme mit retain und mit Standardwerten
ergebnis = (dimme("a", 30, 0, schritte=3, retain=True), dimme("b", 0, 0, schritte=1))
erwartet = ([nachricht("a", "20", 0, True), nachricht("a", "10", 0, True), nachricht("a", "0", 0, True)], [nachricht("b", "0")])
assert ergebnis == erwartet, (
    f'dimme("a", 30, 0, schritte=3, retain=True) und dimme("b", 0, 0, schritte=1) ergeben {ergebnis!r}, erwartet war {erwartet!r}.\n'
    "Tipp: Reichen Sie auch retain mit Namen an befehl weiter."
)

# dimme mit falschem qos: ValueError mit dem Wert
fehler = ausnahme_bei(lambda: dimme("a", 0, 10, schritte=2, qos=5))
assert isinstance(fehler, ValueError) and "5" in str(fehler), (
    f"dimme('a', 0, 10, schritte=2, qos=5) muss wie befehl einen ValueError mit 5 in der Meldung auslösen; bekommen: {fehler!r}."
)

# dimme benutzt rampe und befehl
quelltext = inspect.getsource(dimme)
assert "rampe(" in quelltext and "befehl(" in quelltext, (
    "dimme soll die Werte mit rampe(…) berechnen und die Nachrichten mit befehl(…) bauen, statt beides noch einmal zu programmieren."
)


# Vergleichslösung: Werte über Brüche und Abrunden mit math.floor
def rampe_von_hand(start, ziel, schritte):
    """Rechnet jeden Zwischenwert mit fractions.Fraction exakt aus und rundet dann ab."""
    import fractions
    import math

    return [math.floor(start + fractions.Fraction((ziel - start) * i, schritte)) for i in range(1, schritte + 1)]


# 300 zufällige Rampen und Befehle
zufall = Zufall(4020)
for _ in range(300):
    start = zufall.randint(0, 100)
    ziel = zufall.randint(0, 100)
    schritte = zufall.choice([1, 2, 3, 7, zufall.randint(1, 120)])
    qos = zufall.randint(0, 2)
    retain = zufall.choice([True, False])
    erwartet = rampe_von_hand(start, ziel, schritte)
    ergebnis = rampe(start, ziel, schritte=schritte)
    assert ergebnis == erwartet, f"rampe({start}, {ziel}, schritte={schritte}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    ergebnis = dimme("raum/licht", start, ziel, schritte=schritte, qos=qos, retain=retain)
    erwartet = [nachricht("raum/licht", str(wert), qos, retain) for wert in erwartet]
    assert ergebnis == erwartet, (
        f"dimme('raum/licht', {start}, {ziel}, schritte={schritte}, qos={qos}, retain={retain}) ergibt "
        f"{ergebnis[:3]!r} …, erwartet war {erwartet[:3]!r} …"
    )

# An der oberen Grenze: 10 000 Schritte
ergebnis = dimme("halle/licht", 100, 0, schritte=10000, qos=2, retain=True)
erwartet = [nachricht("halle/licht", str(wert), 2, True) for wert in rampe_von_hand(100, 0, 10000)]
assert ergebnis == erwartet, (
    f"dimme('halle/licht', 100, 0, schritte=10000, qos=2, retain=True) liefert {len(ergebnis)} Befehle, "
    f"die ersten {ergebnis[:2]!r}; erwartet waren 10000, die ersten {erwartet[:2]!r}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "{'topic': 'etage2/raum204/jalousie', 'payload': '75', 'qos': 0, 'retain': False}\n"
    "[25, 50, 75, 100] [65, 50, 35, 20] [3, 6, 10]\n2"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
