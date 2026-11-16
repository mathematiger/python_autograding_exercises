# Automatisch erzeugt aus lehrkraft/muster/5_024_speicheranzeige.py - nicht von Hand ändern.
# vorlage-hash: 51592057ef1d3443
# text-hash: 825d631f34debd6d
# thema: klassen
# inhalt: __format__ mit eigener format_spec

GROESSEN = ["B", "KiB", "MiB", "GiB", "TiB"]


def formatiert(wert, format_spec):
    """Liefert format(wert, format_spec) oder eine Beschreibung des Fehlers."""
    try:
        return format(wert, format_spec)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def von_hand(anzahl_bytes, genauigkeit=None, einheit=None):
    """Vergleichslösung: sucht die Einheit über eine Liste der Grenzen."""
    if einheit is None:
        grenzen = [1024**k for k in range(5)]
        einheit = GROESSEN[sum(1 for grenze in grenzen[1:] if anzahl_bytes >= grenze)]
    k = GROESSEN.index(einheit)
    if k == 0:
        return f"{anzahl_bytes} B"
    stellen = 1 if genauigkeit is None else genauigkeit
    return format(anzahl_bytes / 1024**k, f".{stellen}f") + " " + einheit


def zahl_und_einheit(text):
    """Zerlegt "7.5 GiB" in (7.5, "GiB"); None, wenn das nicht geht."""
    teile = str(text).split()
    if len(teile) != 2:
        return None
    try:
        return float(teile[0]), teile[1]
    except ValueError:
        return None


def loest_valueerror_aus(wert, format_spec):
    """Gibt True zurück, wenn format(wert, format_spec) einen ValueError auslöst."""
    try:
        format(wert, format_spec)
    except ValueError:
        return True
    except Exception:
        return False
    return False


RAM = 8053063680

# __init__ speichert die Anzahl Bytes
assert Speicher(RAM).anzahl_bytes == RAM, f"Speicher({RAM}).anzahl_bytes ergibt {Speicher(RAM).anzahl_bytes!r}, erwartet war {RAM}."

# Feste Einheit: Zahl und Einheit stimmen (Form noch locker)
ergebnis = formatiert(Speicher(RAM), ".2GiB")
assert zahl_und_einheit(ergebnis) == (7.5, "GiB"), (
    f'format(Speicher({RAM}), ".2GiB") ergibt {ergebnis!r}, erwartet war die Zahl 7.5 und die Einheit GiB.\n'
    "Tipp: Schreiben Sie __format__(self, format_spec); f-Strings und format() rufen es auf. "
    "Teilen Sie die Bytes durch 1024**3 für GiB."
)

# Feste Einheit mit der verlangten Genauigkeit: "7.50 GiB"
ergebnis = formatiert(Speicher(RAM), ".2GiB")
assert ergebnis == "7.50 GiB", (
    f'format(Speicher({RAM}), ".2GiB") ergibt {ergebnis!r}, erwartet war genau "7.50 GiB" '
    "(zwei Nachkommastellen, ein Leerzeichen, die Einheit)."
)

# Andere Einheiten und Genauigkeiten (nicht fest hinschreiben!)
for format_spec, erwartet in [(".0MiB", "7680 MiB"), (".3KiB", "7864320.000 KiB"), (".4TiB", "0.0073 TiB")]:
    ergebnis = formatiert(Speicher(RAM), format_spec)
    assert ergebnis == erwartet, f"format(Speicher({RAM}), {format_spec!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Ohne Genauigkeit gilt eine Nachkommastelle
ergebnis = formatiert(Speicher(1536), "KiB")
assert ergebnis == "1.5 KiB", f'format(Speicher(1536), "KiB") ergibt {ergebnis!r}, erwartet war "1.5 KiB".'

# In der Einheit B steht eine ganze Zahl
ergebnis = formatiert(Speicher(RAM), "B")
assert ergebnis == "8053063680 B", f'format(Speicher({RAM}), "B") ergibt {ergebnis!r}, erwartet war "8053063680 B".'

# Auch mit Genauigkeit bleibt B ganzzahlig
ergebnis = formatiert(Speicher(1536), ".2B")
assert ergebnis == "1536 B", (
    f'format(Speicher(1536), ".2B") ergibt {ergebnis!r}, erwartet war "1536 B": Bytes haben keine Nachkommastellen.'
)

# Ohne Einheit wird die passende gewählt
ergebnis = formatiert(Speicher(RAM), ".2")
assert ergebnis == "7.50 GiB", (
    f'format(Speicher({RAM}), ".2") ergibt {ergebnis!r}, erwartet war "7.50 GiB".\n'
    "Tipp: Ohne Einheit nehmen Sie die größte, in der die Zahl mindestens 1 ist."
)

# Ganz ohne format_spec: f"{ram}"
ergebnis = formatiert(Speicher(RAM), "")
assert ergebnis == "7.5 GiB", (
    f'f"{{Speicher({RAM})}}" ergibt {ergebnis!r}, erwartet war "7.5 GiB".\n'
    "Tipp: Auch die leere format_spec landet bei __format__."
)

# f-Strings und str.format benutzen __format__
ram = Speicher(RAM)
ergebnis = (f"{ram:.1MiB}", "{:.1MiB}".format(ram))
assert ergebnis == ("7680.0 MiB", "7680.0 MiB"), (
    f'f"{{ram:.1MiB}}" und "{{:.1MiB}}".format(ram) ergeben {ergebnis!r}, erwartet war beide Male "7680.0 MiB".'
)

# str liefert dasselbe wie die leere format_spec
try:
    ergebnis = str(Speicher(1536))
except Exception as fehler:
    ergebnis = f"{type(fehler).__name__}: {fehler}"
assert ergebnis == "1.5 KiB", f'str(Speicher(1536)) ergibt {ergebnis!r}, erwartet war "1.5 KiB".'

# Unter 1024 Bytes: Einheit B
ergebnis = formatiert(Speicher(500), "")
assert ergebnis == "500 B", f'f"{{Speicher(500)}}" ergibt {ergebnis!r}, erwartet war "500 B".'

# Genau an der Grenze: 1023 Bytes und 1024 Bytes
ergebnis = (formatiert(Speicher(1023), ""), formatiert(Speicher(1024), ""))
assert ergebnis == ("1023 B", "1.0 KiB"), (
    f'f"{{Speicher(1023)}}" und f"{{Speicher(1024)}}" ergeben {ergebnis!r}, erwartet war ("1023 B", "1.0 KiB").\n'
    "Tipp: Bei genau 1024 Bytes ist die Zahl in KiB genau 1, das reicht schon (>=, nicht >)."
)

# Null Bytes
ergebnis = formatiert(Speicher(0), "")
assert ergebnis == "0 B", f'f"{{Speicher(0)}}" ergibt {ergebnis!r}, erwartet war "0 B".'

# Genauigkeit 0 und 9
ergebnis = (formatiert(Speicher(1536), ".0KiB"), formatiert(Speicher(1536), ".9KiB"))
assert ergebnis == ("2 KiB", "1.500000000 KiB"), (
    f'format(Speicher(1536), ".0KiB") und ".9KiB" ergeben {ergebnis!r}, erwartet war ("2 KiB", "1.500000000 KiB").'
)

# Größte Einheit TiB, auch weit über 1024 TiB
ergebnis = formatiert(Speicher(2**60), "")
assert ergebnis == "1048576.0 TiB", f'f"{{Speicher(2**60)}}" ergibt {ergebnis!r}, erwartet war "1048576.0 TiB".'

# Unbekannte Einheit löst ValueError aus
assert loest_valueerror_aus(Speicher(RAM), "MB"), (
    f'format(Speicher({RAM}), "MB") ergibt {formatiert(Speicher(RAM), "MB")!r}, erwartet war ein ValueError.'
)

# Kleingeschriebene Einheit ist ungültig
assert loest_valueerror_aus(Speicher(RAM), "gib"), (
    f'format(Speicher({RAM}), "gib") ergibt {formatiert(Speicher(RAM), "gib")!r}, erwartet war ein ValueError.'
)

# Falsch aufgebaute Genauigkeit löst ValueError aus
for format_spec in [".", ".xGiB", "2GiB", ".12GiB", "GiB.2", ".2f", " GiB", "GiB "]:
    assert loest_valueerror_aus(Speicher(RAM), format_spec), (
        f"format(Speicher({RAM}), {format_spec!r}) ergibt {formatiert(Speicher(RAM), format_spec)!r}, "
        "erwartet war ein ValueError."
    )

# belegung aus dem Beispiel
ergebnis = belegung("web01", Speicher(RAM), Speicher(16 * 1024**3))
assert ergebnis == "web01: 7.5 GiB von 16 GiB belegt", (
    f'belegung("web01", Speicher({RAM}), Speicher(16 * 1024**3)) ergibt {ergebnis!r}, '
    'erwartet war "web01: 7.5 GiB von 16 GiB belegt".\nTipp: f"{belegt:.1GiB}" ruft Ihr __format__ auf.'
)

# belegung mit anderen Werten
ergebnis = belegung("db02", Speicher(512 * 1024**2), Speicher(2 * 1024**3))
assert ergebnis == "db02: 0.5 GiB von 2 GiB belegt", (
    f'belegung("db02", <512 MiB>, <2 GiB>) ergibt {ergebnis!r}, erwartet war "db02: 0.5 GiB von 2 GiB belegt".'
)

# 300 zufällige Größen und format_specs
zufall = Zufall(5024)
for _ in range(300):
    anzahl = zufall.randint(0, 1024 ** zufall.randint(0, 5) * 3)
    genauigkeit = zufall.choice([None, 0, 1, 2, 5])
    einheit = zufall.choice([None, "B", "KiB", "MiB", "GiB", "TiB"])
    format_spec = ("" if genauigkeit is None else f".{genauigkeit}") + (einheit or "")
    ergebnis = formatiert(Speicher(anzahl), format_spec)
    erwartet = von_hand(anzahl, genauigkeit, einheit)
    assert ergebnis == erwartet, f"format(Speicher({anzahl}), {format_spec!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "7.5 GiB | 7.50 GiB | 7680 MiB | 8053063680 B\nweb01: 7.5 GiB von 16 GiB belegt"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
