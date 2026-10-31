# Automatisch erzeugt aus lehrkraft/muster/5_007_schnittstelle.py - nicht von Hand ändern.
# vorlage-hash: 6a60c128fbba4b06
# text-hash: 9c27cf2f5a75138e
# thema: klassen
# inhalt: `__setattr__`, `__delattr__`

def ausnahme_bei(aktion):
    """Führt aktion() aus und gibt den Namen der ausgelösten Ausnahme zurück, sonst None."""
    try:
        aktion()
    except Exception as fehler:
        return type(fehler).__name__
    return None


# __init__ legt alle Attribute an, ohne zu protokollieren
s = Schnittstelle("eth0", ip="10.0.0.1")
ergebnis = (s.name, s.ip, s.mtu, s.aktiv, s.protokoll, s.gesperrt)
assert ergebnis == ("eth0", "10.0.0.1", 1500, False, [], False), (
    f"Nach Schnittstelle('eth0', ip='10.0.0.1') sind name, ip, mtu, aktiv, protokoll und gesperrt {ergebnis!r}; "
    "erwartet war ('eth0', '10.0.0.1', 1500, False, [], False).\n"
    "Tipp: In __init__ legen Sie die Attribute mit object.__setattr__(self, name, wert) an, am geprüften "
    "__setattr__ vorbei."
)

# Alle Felder lassen sich in __init__ setzen
s = Schnittstelle("wan", ip="203.0.113.7", mtu=9000, aktiv=True)
assert (s.ip, s.mtu, s.aktiv, s.protokoll) == ("203.0.113.7", 9000, True, []), (
    f"Schnittstelle('wan', ip='203.0.113.7', mtu=9000, aktiv=True) hat ip, mtu, aktiv, protokoll "
    f"{(s.ip, s.mtu, s.aktiv, s.protokoll)!r}."
)

# Das Beispiel aus der Aufgabe
s = Schnittstelle("eth0", ip="10.0.0.1")
s.mtu = 9000
s.aktiv = True
s.aktiv = True
del s.mtu
erwartet = [("mtu", 1500, 9000), ("aktiv", False, True), ("mtu", 9000, 1500)]
assert (s.mtu, s.aktiv, s.protokoll) == (1500, True, erwartet), (
    f"Nach s.mtu = 9000, zweimal s.aktiv = True und del s.mtu sind mtu, aktiv und protokoll "
    f"{(s.mtu, s.aktiv, s.protokoll)!r}; erwartet war (1500, True, {erwartet!r}).\n"
    "Tipp: Ein Eintrag (feld, alt, neu) kommt nur, wenn sich der Wert ändert; del setzt auf den Standardwert zurück."
)

# Unbekannte Felder, name, protokoll und gesperrt lassen sich nicht zuweisen
s = Schnittstelle("eth0")
for feld, wert in [("mut", 1400), ("name", "eth1"), ("protokoll", []), ("gesperrt", True), ("vlan", 10)]:
    art = ausnahme_bei(lambda: setattr(s, feld, wert))
    assert art == "AttributeError" and not hasattr(s, "mut") and not hasattr(s, "vlan") and s.name == "eth0" and s.gesperrt is False, (
        f"s.{feld} = {wert!r} soll einen AttributeError auslösen und nichts ändern; ausgelöst wurde {art}.\n"
        "Tipp: Lassen Sie in __setattr__ nur die Namen aus FELDER durch."
    )
assert s.protokoll == [], f"Abgelehnte Zuweisungen sollen nicht im Protokoll stehen; protokoll ist {s.protokoll!r}."

# Die MTU wird geprüft, auch in __init__
for wert in [67, 9217, 0, -1500, 1500.0, "1500", True, None]:
    s = Schnittstelle("eth0")
    art = ausnahme_bei(lambda: setattr(s, "mtu", wert))
    assert art == "ValueError" and s.mtu == 1500 and s.protokoll == [], (
        f"s.mtu = {wert!r} soll einen ValueError auslösen und weder mtu noch protokoll ändern; ausgelöst wurde {art}, "
        f"mtu ist {s.mtu!r}, protokoll {s.protokoll!r}.\n"
        "Tipp: type(wert) is int schließt True und 1500.0 aus; erlaubt ist 68 <= wert <= 9216. Prüfen Sie, bevor Sie "
        "etwas an protokoll anhängen."
    )
    art = ausnahme_bei(lambda: Schnittstelle("eth0", mtu=wert))
    assert art == "ValueError", f"Schnittstelle('eth0', mtu={wert!r}) soll einen ValueError auslösen; ausgelöst wurde {art}."

# Die Ränder 68 und 9216 sind erlaubt
s = Schnittstelle("eth0", mtu=68)
s.mtu = 9216
assert s.protokoll == [("mtu", 68, 9216)], f"Mit mtu=68 und danach s.mtu = 9216 ist protokoll {s.protokoll!r}."

# del für unbekannte Felder und name: AttributeError
s = Schnittstelle("eth0")
for feld in ["name", "mut", "protokoll", "gesperrt"]:
    art = ausnahme_bei(lambda: delattr(s, feld))
    assert art == "AttributeError" and s.name == "eth0" and isinstance(s.protokoll, list), (
        f"del s.{feld} soll einen AttributeError auslösen; ausgelöst wurde {art}."
    )

# del auf einem Feld mit Standardwert protokolliert nichts
s = Schnittstelle("eth0")
del s.aktiv
del s.ip
assert (s.aktiv, s.ip, s.protokoll) == (False, "0.0.0.0", []), (
    f"del s.aktiv und del s.ip bei Standardwerten ergeben aktiv, ip, protokoll {(s.aktiv, s.ip, s.protokoll)!r}; "
    "erwartet war (False, '0.0.0.0', [])."
)

# Nach sperren() geht nichts mehr, auch nicht mit dem gleichen Wert
s = Schnittstelle("eth0", ip="10.0.0.1")
s.mtu = 1400
s.sperren()
arten = [
    ausnahme_bei(lambda: setattr(s, "ip", "10.0.0.2")),
    ausnahme_bei(lambda: setattr(s, "mtu", 1400)),
    ausnahme_bei(lambda: delattr(s, "mtu")),
    ausnahme_bei(lambda: setattr(s, "gesperrt", False)),
]
assert arten == ["AttributeError"] * 4 and (s.ip, s.mtu, s.gesperrt, s.protokoll) == ("10.0.0.1", 1400, True, [("mtu", 1500, 1400)]), (
    f"Nach sperren() lösen Zuweisungen und del {arten} aus, erwartet war jedes Mal AttributeError; ip, mtu, gesperrt "
    f"und protokoll sind {(s.ip, s.mtu, s.gesperrt, s.protokoll)!r}.\n"
    "Tipp: Speichern Sie gesperrt in sperren() mit object.__setattr__; prüfen Sie es zuerst in __setattr__ und __delattr__."
)

# Zwei Schnittstellen haben getrennte Protokolle
a = Schnittstelle("eth0")
b = Schnittstelle("eth1")
a.aktiv = True
assert (a.protokoll, b.protokoll) == ([("aktiv", False, True)], []), (
    f"Nach a.aktiv = True sind die Protokolle von a und b {a.protokoll!r} und {b.protokoll!r}; "
    "jede Schnittstelle braucht ihre eigene Liste."
)

# Auch += geht über die Prüfung
s = Schnittstelle("eth0", mtu=9200)
art = ausnahme_bei(lambda: exec("s.mtu += 100", {"s": s}))
s.mtu -= 200
assert (art, s.mtu, s.protokoll) == ("ValueError", 9000, [("mtu", 9200, 9000)]), (
    f"s.mtu += 100 bei 9200 und danach s.mtu -= 200 ergeben {art}, mtu {s.mtu!r}, protokoll {s.protokoll!r}; "
    "erwartet waren ValueError, 9000 und [('mtu', 9200, 9000)]."
)

# 300 zufällige Abläufe, verglichen mit einem Dictionary
zufall = Zufall(5007)
STANDARD = {"ip": "0.0.0.0", "mtu": 1500, "aktiv": False}
for _ in range(300):
    s = Schnittstelle("eth0")
    werte = dict(STANDARD)
    protokoll = []
    gesperrt = False
    schritte = []
    for _ in range(zufall.randint(0, 12)):
        art = zufall.choice(["setzen", "setzen", "setzen", "loeschen", "fremd", "sperren"])
        feld = zufall.choice(["ip", "mtu", "aktiv"])
        wert = {"ip": zufall.choice(["0.0.0.0", "10.0.0.1", "10.0.0.2"]), "aktiv": zufall.choice([True, False]), "mtu": zufall.choice([67, 68, 1500, 9000, 9216, 9217, True])}[feld]
        if art == "setzen":
            schritte.append(f"s.{feld} = {wert!r}")
            erwartet = "AttributeError" if gesperrt else ("ValueError" if feld == "mtu" and (type(wert) is not int or not 68 <= wert <= 9216) else None)
            ergebnis = ausnahme_bei(lambda: setattr(s, feld, wert))
            if erwartet is None:
                if werte[feld] != wert:
                    protokoll.append((feld, werte[feld], wert))
                werte[feld] = wert
        elif art == "loeschen":
            schritte.append(f"del s.{feld}")
            erwartet = "AttributeError" if gesperrt else None
            ergebnis = ausnahme_bei(lambda: delattr(s, feld))
            if erwartet is None:
                if werte[feld] != STANDARD[feld]:
                    protokoll.append((feld, werte[feld], STANDARD[feld]))
                werte[feld] = STANDARD[feld]
        elif art == "fremd":
            schritte.append("s.mut = 1400")
            erwartet = "AttributeError"
            ergebnis = ausnahme_bei(lambda: setattr(s, "mut", 1400))
        else:
            schritte.append("s.sperren()")
            erwartet = None
            ergebnis = ausnahme_bei(s.sperren)
            gesperrt = True
        assert ergebnis == erwartet, f"Nach {'; '.join(schritte)} löst der letzte Schritt {ergebnis} aus, erwartet war {erwartet}."
    zustand = {"ip": s.ip, "mtu": s.mtu, "aktiv": s.aktiv}
    assert (zustand, s.protokoll, s.gesperrt) == (werte, protokoll, gesperrt), (
        f"Nach {'; '.join(schritte) or 'nichts'} sind Felder, protokoll und gesperrt {(zustand, s.protokoll, s.gesperrt)!r}; "
        f"erwartet war {(werte, protokoll, gesperrt)!r}."
    )

# An der oberen Grenze: 100 000 Zuweisungen
s = Schnittstelle("eth0")
for nummer in range(100000):
    s.mtu = 1000 + nummer % 3
assert len(s.protokoll) == 100000 and s.protokoll[0] == ("mtu", 1500, 1000) and s.protokoll[-1] == ("mtu", 1002, 1000), (
    f"Nach 100 000 wechselnden Zuweisungen an mtu hat protokoll {len(s.protokoll)} Einträge, erwartet waren 100000."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "eth0 10.0.0.1 1500 True\n"
    "[('mtu', 1500, 9000), ('aktiv', False, True), ('mtu', 9000, 1500)]\n"
    "gesperrt"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
