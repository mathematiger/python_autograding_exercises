# Automatisch erzeugt aus lehrkraft/muster/5_022_hoststatus.py - nicht von Hand ändern.
# vorlage-hash: 72af989442dc850b
# text-hash: 304376666c783656
# thema: datenstrukturen
# inhalt: Eigenes Mapping mit abc.MutableMapping

def versuche(aufruf):
    """Ruft aufruf() auf; liefert ("ok", Ergebnis) oder (Name der Ausnahme, None)."""
    try:
        return "ok", aufruf()
    except Exception as fehler:
        return type(fehler).__name__, None


def von_hand(name):
    """Vergleichslösung für das Normalisieren mit Slicing."""
    name = name.strip().lower()
    if name.endswith("."):
        name = name[:-1]
    return name


# Die Klasse ist ein MutableMapping und kein dict
assert issubclass(Hoststatus, MutableMapping) and not issubclass(Hoststatus, dict), (
    "Hoststatus soll von collections.abc.MutableMapping erben und nicht von dict."
)

# normalisiere wie beschrieben
for name, erwartet in [("WEB1.firma.de", "web1.firma.de"), ("web1.firma.de.", "web1.firma.de"),
                       ("  Web1.Firma.DE  ", "web1.firma.de"), (" DB2.firma.de. ", "db2.firma.de"), ("a", "a")]:
    ergebnis = versuche(lambda: Hoststatus.normalisiere(name))
    assert ergebnis == ("ok", erwartet), (
        f"Hoststatus.normalisiere({name!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
        "Tipp: Erst strip, dann lower, dann einen Punkt am Ende entfernen."
    )

# Nur ein einzelner Punkt am Ende wird entfernt, Punkte in der Mitte bleiben
ergebnis = versuche(lambda: Hoststatus.normalisiere("mail.firma.de"))
assert ergebnis == ("ok", "mail.firma.de"), f"Hoststatus.normalisiere('mail.firma.de') ergibt {ergebnis!r}, erwartet war 'mail.firma.de'."

# Nicht-Texte lösen TypeError aus
for name in [5, None, 1.5]:
    art, _ = versuche(lambda: Hoststatus.normalisiere(name))
    assert art == "TypeError", f"Hoststatus.normalisiere({name!r}) soll einen TypeError auslösen, bekommen: {art}."

# Das Beispiel aus der Aufgabe
status_test = Hoststatus({"WEB1.firma.de": "ok"})
status_test["web1.firma.de."] = "warnung"
ergebnis = (status_test[" Web1.Firma.DE"], len(status_test), "DB2.firma.de" in status_test)
assert ergebnis == ("warnung", 1, False), (
    "Hoststatus({'WEB1.firma.de': 'ok'}), dann status['web1.firma.de.'] = 'warnung': status[' Web1.Firma.DE'], "
    f"len(status) und 'DB2.firma.de' in status ergeben {ergebnis!r}, erwartet war ('warnung', 1, False).\n"
    "Tipp: Normalisieren Sie den Schlüssel in __getitem__ und __setitem__."
)
ergebnis = (status_test.setdefault("DB2.firma.de.", "ok"), list(status_test))
assert ergebnis == ("ok", ["web1.firma.de", "db2.firma.de"]), (
    f"status.setdefault('DB2.firma.de.', 'ok') und list(status) ergeben {ergebnis!r}, "
    "erwartet war ('ok', ['web1.firma.de', 'db2.firma.de'])."
)
assert status_test == {"web1.firma.de": "warnung", "db2.firma.de": "ok"}, (
    f"status == {{'web1.firma.de': 'warnung', 'db2.firma.de': 'ok'}} ergibt False; status ist {status_test!r}."
)

# Ohne Daten ist das Mapping leer
leer = Hoststatus()
assert len(leer) == 0 and list(leer) == [] and repr(leer) == "Hoststatus({})", (
    f"Hoststatus() hat {len(leer)} Einträge, list ergibt {list(leer)!r} und repr {repr(leer)!r}; "
    "erwartet waren 0, [] und 'Hoststatus({})'."
)

# Zwei Objekte teilen sich keine Daten
erstes = Hoststatus()
zweites = Hoststatus()
erstes["a.de"] = "ok"
assert len(zweites) == 0, "Nach erstes['a.de'] = 'ok' hat ein zweites Hoststatus() auch einen Eintrag. Legen Sie das Dictionary in __init__ an."

# Eine Folge von Paaren als Daten, gleiche Hosts in verschiedenen Schreibweisen
status = Hoststatus([("A.de", 1), ("b.de", 2), ("a.de.", 3)])
assert list(status.items()) == [("a.de", 3), ("b.de", 2)], (
    f"Hoststatus([('A.de', 1), ('b.de', 2), ('a.de.', 3)]) ergibt {list(status.items())!r}, "
    "erwartet war [('a.de', 3), ('b.de', 2)].\nTipp: Übernehmen Sie die Daten mit self.update(daten), dann wird jeder Schlüssel normalisiert."
)

# Ein unbekannter Name löst KeyError aus, get und pop mit Standardwert funktionieren
status = Hoststatus({"web1.firma.de": "ok"})
ergebnis = (versuche(lambda: status["web2.firma.de"])[0], status.get("WEB2.firma.de", "unbekannt"),
            status.get("Web1.Firma.De."), status.pop("nix.de", None))
assert ergebnis == ("KeyError", "unbekannt", "ok", None), (
    f"status['web2.firma.de'], get('WEB2.firma.de', 'unbekannt'), get('Web1.Firma.De.') und pop('nix.de', None) "
    f"ergeben {ergebnis!r}, erwartet war ('KeyError', 'unbekannt', 'ok', None)."
)

# Löschen mit del und pop in anderer Schreibweise
status = Hoststatus({"a.de": 1, "b.de": 2, "c.de": 3})
del status["A.DE."]
wert = status.pop(" B.de")
ergebnis = (wert, dict(status), versuche(lambda: status.__delitem__("a.de"))[0])
assert ergebnis == (2, {"c.de": 3}, "KeyError"), (
    "Hoststatus({'a.de': 1, 'b.de': 2, 'c.de': 3}), del status['A.DE.'], status.pop(' B.de'), noch einmal del "
    f"status['a.de']: erwartet (2, {{'c.de': 3}}, 'KeyError'), bekommen {ergebnis!r}."
)

# Überschreiben ändert die Reihenfolge nicht
status = Hoststatus()
for name, wert in [("x.de", 1), ("y.de", 2), ("X.DE.", 3)]:
    status[name] = wert
assert list(status.items()) == [("x.de", 3), ("y.de", 2)], (
    f"Nach x.de = 1, y.de = 2, X.DE. = 3 ergibt items() {list(status.items())!r}, erwartet war [('x.de', 3), ('y.de', 2)]."
)

# Ein falscher Schlüsseltyp löst TypeError aus, auch bei in, get und Zuweisung
status = Hoststatus({"a.de": 1})
arten = [versuche(aufruf)[0] for aufruf in [lambda: 5 in status, lambda: status.get(None), lambda: status.__setitem__(7, "ok")]]
assert arten == ["TypeError"] * 3 and len(status) == 1, (
    f"5 in status, status.get(None) und status[7] = 'ok' ergeben {arten!r}, erwartet war dreimal TypeError; "
    f"danach hat status {len(status)} Einträge (erwartet 1)."
)

# update, clear, values und repr
status = Hoststatus()
status.update({"A.de": "ok"}, WEB2="warnung")
werte = list(status.values())
text = repr(status)
status.clear()
erwarteter_text = "Hoststatus({'a.de': 'ok', 'web2': 'warnung'})"
assert werte == ["ok", "warnung"] and text == erwarteter_text and len(status) == 0, (
    f"Nach update({{'A.de': 'ok'}}, WEB2='warnung') ergeben values() {werte!r} und repr {text!r}, nach clear() hat "
    f"status noch {len(status)} Einträge; erwartet waren ['ok', 'warnung'], {erwarteter_text!r} und 0."
)

# Die geerbten Methoden kommen von MutableMapping
selbst = [name for name in ["get", "pop", "setdefault", "update", "__contains__", "keys", "items"] if name in vars(Hoststatus)]
assert selbst == [], f"Hoststatus definiert {selbst} selbst. Lassen Sie diese Methoden weg; MutableMapping liefert sie."

# 2000 zufällige Operationen gegen ein gewöhnliches Dictionary mit normalisierten Schlüsseln
zufall = Zufall(5022)
status = Hoststatus()
vergleich = {}
schritte = []


def zufallsname():
    """Ein Hostname in zufälliger Schreibweise."""
    name = zufall.choice(["web1", "web2", "db1", "mail", "vpn-gw"]) + zufall.choice([".firma.de", ".lan", ""])
    name = "".join(zeichen.upper() if zufall.random() < 0.3 else zeichen for zeichen in name)
    return " " * zufall.randint(0, 3) + name + zufall.choice(["", "."]) + " " * zufall.randint(0, 3)


for _ in range(2000):
    name = zufallsname()
    schluessel = von_hand(name)
    art = zufall.choice(["setzen", "lesen", "loeschen", "in", "get", "pop", "setdefault"])
    schritte = (schritte + [f"{art} {name!r}"])[-5:]
    if art == "setzen":
        wert = zufall.randint(0, 9)
        status[name] = wert
        vergleich[schluessel] = wert
        bekommen, erwartet = None, None
    elif art == "lesen":
        bekommen = versuche(lambda: status[name])
        erwartet = ("ok", vergleich[schluessel]) if schluessel in vergleich else ("KeyError", None)
    elif art == "loeschen":
        bekommen = versuche(lambda: status.__delitem__(name))
        erwartet = ("KeyError", None) if schluessel not in vergleich else ("ok", None)
        vergleich.pop(schluessel, None)
    elif art == "in":
        bekommen, erwartet = name in status, schluessel in vergleich
    elif art == "get":
        bekommen, erwartet = status.get(name, -1), vergleich.get(schluessel, -1)
    elif art == "pop":
        bekommen, erwartet = status.pop(name, -1), vergleich.pop(schluessel, -1)
    else:
        bekommen, erwartet = status.setdefault(name, 5), vergleich.setdefault(schluessel, 5)
    if bekommen != erwartet or list(status.items()) != list(vergleich.items()):
        break
assert bekommen == erwartet and list(status.items()) == list(vergleich.items()), (
    f"Nach den letzten Operationen {'; '.join(schritte)}:\n  Ergebnis {bekommen!r}, erwartet {erwartet!r}\n"
    f"  Inhalt {list(status.items())!r}\n  erwartet {list(vergleich.items())!r}"
)

# Obere Grenze: 10**5 Hosts
gross = Hoststatus((f" HOST{nummer}.Firma.de. ", nummer) for nummer in range(10**5))
assert len(gross) == 10**5 and gross["host99999.firma.de"] == 99999 and next(iter(gross)) == "host0.firma.de", (
    "Bei 10**5 Hosts stimmen len, der letzte Eintrag oder der erste Name nicht."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "Hoststatus({'web1.firma.de': 'warnung', 'db2.firma.de': 'ok'})\nwarnung True"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm gibt aus:\n{AUSGABE}"
