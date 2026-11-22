# Automatisch erzeugt aus lehrkraft/muster/3_039_versionsnummer.py - nicht von Hand ändern.
# vorlage-hash: 507a9a5ab5098d80
# text-hash: 4788aa5afa974bb6
# thema: klassen
# inhalt: __str__ und __eq__

def vergleiche(a, b):
    """Gibt a == b zurück; eine Ausnahme wird als Text zurückgegeben."""
    try:
        return a == b
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


class Fremd:
    """Ein Objekt mit den Attributen major, minor und patch, das keine Version ist."""

    major, minor, patch = 2, 4, 1


# __init__ speichert die drei Zahlen
v = Version(2, 4, 1)
gefunden = [getattr(v, name, "(fehlt)") for name in ("major", "minor", "patch")]
assert gefunden == [2, 4, 1], (
    f"Version(2, 4, 1) hat major, minor, patch = {gefunden}, erwartet war [2, 4, 1].\n"
    "Tipp: Speichern Sie die Parameter in __init__ mit self.major = major und so weiter."
)

# Ohne patch ist patch 0
v = Version(3, 1)
assert getattr(v, "patch", "(fehlt)") == 0, f"Version(3, 1) hat patch = {getattr(v, 'patch', '(fehlt)')!r}, erwartet war 0."

# str liefert einen Text mit den drei Zahlen
text = str(Version(2, 4, 1))
assert vergleichbar(text) == vergleichbar("2 4 1") or text == "2.4.1", (
    f"str(Version(2, 4, 1)) ergibt {text!r}, erwartet war '2.4.1'.\n"
    'Tipp: __str__ gibt einen Text zurück, etwa f"{self.major}.{self.minor}.{self.patch}".'
)

# str hat genau die Form Major.Minor.Patch
text = str(Version(2, 4, 1))
assert text == "2.4.1", f"str(Version(2, 4, 1)) ergibt {text!r}, erwartet war genau '2.4.1' mit Punkten und ohne Leerzeichen."

# str einer anderen Version (nicht fest hinschreiben!)
text = str(Version(10, 0, 23))
assert text == "10.0.23", f"str(Version(10, 0, 23)) ergibt {text!r}, erwartet war '10.0.23'."

# str ohne patch
text = str(Version(1, 7))
assert text == "1.7.0", f"str(Version(1, 7)) ergibt {text!r}, erwartet war '1.7.0'."

# print benutzt __str__
assert vergleichbar(AUSGABE.splitlines()[0] if AUSGABE else "") == vergleichbar("2.4.1"), (
    f"print(Version(2, 4, 1)) gibt {AUSGABE.splitlines()[0] if AUSGABE else ''!r} aus, erwartet war 2.4.1."
)

# Ein f-String benutzt __str__
text = f"{Version(5, 6, 7)}"
assert text == "5.6.7", (
    f'f"{{Version(5, 6, 7)}}" ergibt {text!r}, erwartet war \'5.6.7\'.\n'
    "Tipp: __str__ muss den Text mit return zurückgeben, nicht mit print ausgeben."
)

# Gleiche Versionen sind gleich
ergebnis = vergleiche(Version(2, 4, 1), Version(2, 4, 1))
assert ergebnis == True, (
    f"Version(2, 4, 1) == Version(2, 4, 1) ergibt {ergebnis!r}, erwartet war True.\n"
    "Tipp: Ohne __eq__ vergleicht Python nur, ob es dasselbe Objekt ist."
)

# Ein anderer Major-Wert macht die Versionen verschieden
ergebnis = vergleiche(Version(2, 4, 1), Version(3, 4, 1))
assert ergebnis == False, f"Version(2, 4, 1) == Version(3, 4, 1) ergibt {ergebnis!r}, erwartet war False."

# Ein anderer Minor-Wert macht die Versionen verschieden
ergebnis = vergleiche(Version(2, 4, 1), Version(2, 5, 1))
assert ergebnis == False, f"Version(2, 4, 1) == Version(2, 5, 1) ergibt {ergebnis!r}, erwartet war False."

# Ein anderer Patch-Wert macht die Versionen verschieden
ergebnis = vergleiche(Version(2, 4, 1), Version(2, 4))
assert ergebnis == False, f"Version(2, 4, 1) == Version(2, 4) ergibt {ergebnis!r}, erwartet war False (patch 1 gegen 0)."

# Vertauschte Zahlen sind nicht gleich
ergebnis = vergleiche(Version(1, 2, 3), Version(3, 2, 1))
assert ergebnis == False, f"Version(1, 2, 3) == Version(3, 2, 1) ergibt {ergebnis!r}, erwartet war False."

# != und in benutzen __eq__
ergebnis = [Version(2, 4, 1) != Version(2, 4, 1), Version(2, 4, 1) in [Version(1, 0), Version(2, 4, 1)]]
assert ergebnis == [False, True], (
    f"Version(2, 4, 1) != Version(2, 4, 1) und Version(2, 4, 1) in [Version(1, 0), Version(2, 4, 1)] ergeben "
    f"{ergebnis!r}, erwartet war [False, True]."
)

# Vergleich mit einem Text: False, kein Fehler
ergebnis = vergleiche(Version(2, 4, 1), "2.4.1")
assert ergebnis is False, (
    f'Version(2, 4, 1) == "2.4.1" ergibt {ergebnis!r}, erwartet war False.\n'
    "Tipp: Prüfen Sie mit isinstance(andere, Version), ob andere überhaupt eine Version ist."
)

# Vergleich mit None: False, kein Fehler
ergebnis = vergleiche(Version(2, 4, 1), None)
assert ergebnis is False, f"Version(2, 4, 1) == None ergibt {ergebnis!r}, erwartet war False."

# Vergleich mit einem Objekt, das zufällig dieselben Attribute hat
ergebnis = vergleiche(Version(2, 4, 1), Fremd())
assert ergebnis is False, f"Version(2, 4, 1) == Fremd() (keine Version, aber gleiche Attribute) ergibt {ergebnis!r}, erwartet war False."

# Die Ausgabe des Programms
assert vergleichbar(AUSGABE) == vergleichbar("2.4.1\nTrue False"), f"Erwartete Ausgabe:\n2.4.1\nTrue False\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Versionen
zufall = Zufall(3039)
for runde in range(500):
    a = (zufall.randint(0, 3), zufall.randint(0, 3), zufall.randint(0, 3))
    b = zufall.choice([a, (zufall.randint(0, 3), zufall.randint(0, 3), zufall.randint(0, 3))])
    ergebnis = vergleiche(Version(*a), Version(*b))
    assert ergebnis == (a == b), f"Version{a} == Version{b} ergibt {ergebnis!r}, erwartet war {a == b}."
    text = str(Version(*a))
    assert text == ".".join(str(zahl) for zahl in a), f"str(Version{a}) ergibt {text!r}, erwartet war {'.'.join(str(zahl) for zahl in a)!r}."

# Obere Grenze: große Zahlen
text = str(Version(10**6, 10**6, 10**6))
ergebnis = vergleiche(Version(10**6, 10**6, 10**6), Version(10**6, 10**6, 10**6 - 1))
assert (text, ergebnis) == ("1000000.1000000.1000000", False), (
    f"str(Version(10**6, 10**6, 10**6)) ergibt {text!r} und der Vergleich mit Version(10**6, 10**6, 10**6 - 1) "
    f"{ergebnis!r}; erwartet war '1000000.1000000.1000000' und False."
)
