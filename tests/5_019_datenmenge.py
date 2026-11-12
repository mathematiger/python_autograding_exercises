# Automatisch erzeugt aus lehrkraft/muster/5_019_datenmenge.py - nicht von Hand ändern.
# vorlage-hash: b063e9c75e772093
# text-hash: f2ab5ab317770086
# thema: klassen
# inhalt: __add__, __radd__, __iadd__

class Fremd:
    """Eine fremde Klasse, die selbst weiß, wie sie sich mit einer Datenmenge verrechnet."""

    def __radd__(self, other):
        return "Fremd.__radd__"

    def __add__(self, other):
        return "Fremd.__add__"

    def __rmul__(self, other):
        return "Fremd.__rmul__"


def ergebnis_von(rechnung):
    """Führt rechnung aus; liefert das Ergebnis oder den Namen der Ausnahme in spitzen Klammern."""
    try:
        return rechnung()
    except Exception as fehler:
        return f"<{type(fehler).__name__}>"


# Datenmenge + Datenmenge aus dem Beispiel
ergebnis = ergebnis_von(lambda: Datenmenge(1500) + Datenmenge(500))
assert ergebnis == Datenmenge(2000), f"Datenmenge(1500) + Datenmenge(500) ergibt {ergebnis!r}, erwartet war Datenmenge(2000)."

# Das Ergebnis ist ein neues Objekt, die Summanden bleiben
a, b = Datenmenge(7), Datenmenge(8)
summe = a + b
assert summe is not a and summe is not b and (a.bytes, b.bytes) == (7, 8), (
    f"a + b soll eine neue Datenmenge liefern und a, b nicht ändern; danach a = {a!r}, b = {b!r}, "
    f"Ergebnis ist {'a' if summe is a else 'b' if summe is b else 'neu'}."
)

# sum über eine Liste braucht __radd__ für die 0
ergebnis = ergebnis_von(lambda: sum([Datenmenge(1500), Datenmenge(500), Datenmenge(1500)]))
assert ergebnis == Datenmenge(3500), (
    f"sum([Datenmenge(1500), Datenmenge(500), Datenmenge(1500)]) ergibt {ergebnis!r}, erwartet war Datenmenge(3500).\n"
    "Tipp: sum fängt mit 0 + liste[0] an; dafür ruft Python Datenmenge.__radd__(0) auf."
)

# sum einer einzelnen Datenmenge liefert eine Datenmenge, sum mit Startwert ebenso
ergebnis = (ergebnis_von(lambda: sum([Datenmenge(42)])), ergebnis_von(lambda: sum([Datenmenge(1)], Datenmenge(2))))
assert ergebnis == (Datenmenge(42), Datenmenge(3)), (
    f"sum([Datenmenge(42)]) und sum([Datenmenge(1)], Datenmenge(2)) ergeben {ergebnis!r}, erwartet war "
    "(Datenmenge(42), Datenmenge(3))."
)

# Mit anderen Typen gibt __add__ NotImplemented zurück, Python löst dann TypeError aus
ergebnisse = {wert: ergebnis_von(lambda: Datenmenge(1).__add__(wert)) for wert in [5, "5", None, 2.5]}
falsch = {repr(wert): e for wert, e in ergebnisse.items() if e is not NotImplemented}
assert not falsch, (
    f"Datenmenge(1).__add__(…) soll NotImplemented zurückgeben, liefert aber: {falsch}.\n"
    "Tipp: return NotImplemented, nicht raise TypeError und nicht NotImplementedError."
)

# Datenmenge + 5 und 5 + Datenmenge lösen einen TypeError aus
ergebnis = (ergebnis_von(lambda: Datenmenge(1) + 5), ergebnis_von(lambda: 5 + Datenmenge(1)),
            ergebnis_von(lambda: "x" + Datenmenge(1)), ergebnis_von(lambda: 1 + Datenmenge(1)))
assert ergebnis == ("<TypeError>",) * 4, (
    f"Datenmenge(1) + 5, 5 + Datenmenge(1), 'x' + Datenmenge(1) und 1 + Datenmenge(1) ergeben {ergebnis!r}, "
    "erwartet war jeweils ein TypeError.\nTipp: __radd__ akzeptiert nur die ganze Zahl 0."
)

# 0.0 und False sind nicht die ganze Zahl 0
ergebnis = (ergebnis_von(lambda: 0.0 + Datenmenge(1)), ergebnis_von(lambda: False + Datenmenge(1)))
assert ergebnis == ("<TypeError>", "<TypeError>"), (
    f"0.0 + Datenmenge(1) und False + Datenmenge(1) ergeben {ergebnis!r}, erwartet war zweimal ein TypeError.\n"
    "Tipp: Prüfen Sie mit type(other) is int, denn 0.0 == 0 und False == 0 sind beide True."
)

# Eine fremde Klasse bekommt ihre Chance, weil NotImplemented zurückkommt
ergebnis = (ergebnis_von(lambda: Datenmenge(1) + Fremd()), ergebnis_von(lambda: Fremd() + Datenmenge(1)),
            ergebnis_von(lambda: Datenmenge(1) * Fremd()))
assert ergebnis == ("Fremd.__radd__", "Fremd.__add__", "Fremd.__rmul__"), (
    f"Datenmenge(1) + Fremd(), Fremd() + Datenmenge(1) und Datenmenge(1) * Fremd() ergeben {ergebnis!r}, erwartet "
    "war ('Fremd.__radd__', 'Fremd.__add__', 'Fremd.__rmul__').\n"
    "Tipp: Löst __add__ oder __mul__ selbst einen Fehler aus, fragt Python das rechte Objekt nie."
)

# Multiplizieren in beide Richtungen
ergebnis = (ergebnis_von(lambda: Datenmenge(500) * 3), ergebnis_von(lambda: 3 * Datenmenge(500)),
            ergebnis_von(lambda: 0 * Datenmenge(9)))
assert ergebnis == (Datenmenge(1500), Datenmenge(1500), Datenmenge(0)), (
    f"Datenmenge(500) * 3, 3 * Datenmenge(500) und 0 * Datenmenge(9) ergeben {ergebnis!r}, erwartet war "
    "(Datenmenge(1500), Datenmenge(1500), Datenmenge(0)).\nTipp: Für 3 * … braucht es __rmul__."
)

# Multiplizieren mit Kommazahlen, Texten, True und Datenmengen geht nicht
falsch = {}
for wert in [1.5, "3", True, Datenmenge(2), None]:
    for richtung, rechnung in [("rechts", lambda: Datenmenge(4) * wert), ("links", lambda: wert * Datenmenge(4))]:
        ergebnis = ergebnis_von(rechnung)
        if ergebnis != "<TypeError>":
            falsch[f"{wert!r} {richtung}"] = ergebnis
assert not falsch, (
    f"Mit diesen Faktoren kam kein TypeError: {falsch}.\n"
    "Tipp: isinstance(True, int) ist True; schließen Sie bool eigens aus, und geben Sie sonst NotImplemented zurück. "
    "Ein Text mal eine Zahl ergäbe sonst einen Text."
)

# zaehler += datenmenge verändert den Zähler selbst
z = Portzaehler("Gi0/1")
derselbe = z
z += Datenmenge(1500)
z += Datenmenge(500)
assert z is derselbe and (z.gesamt, z.messungen) == (Datenmenge(2000), 2), (
    "Nach z += Datenmenge(1500) und z += Datenmenge(500) erwartet: dasselbe Objekt, gesamt Datenmenge(2000), "
    f"messungen 2; bekommen {'dasselbe' if z is derselbe else 'ein anderes'} Objekt "
    f"{z!r}" + (f" mit gesamt {z.gesamt!r}, messungen {z.messungen!r}." if isinstance(z, Portzaehler) else ".")
    + "\nTipp: __iadd__ muss am Ende return self haben."
)

# Ein zweiter Name sieht die Änderung
z = Portzaehler("Gi0/2")
alle_ports = [z]
z += Datenmenge(10)
assert alle_ports[0].gesamt == Datenmenge(10) and alle_ports[0].messungen == 1, (
    f"Ein Zähler steht auch in einer Liste; nach z += Datenmenge(10) zeigt der Eintrag gesamt "
    f"{alle_ports[0].gesamt!r} und messungen {alle_ports[0].messungen!r}, erwartet war Datenmenge(10) und 1.\n"
    "Tipp: Verändern Sie in __iadd__ das Objekt selbst, statt einen neuen Zähler zu bauen."
)

# Bei einer unveränderlichen Datenmenge baut += ein neues Objekt
a = Datenmenge(1)
alt = a
a += Datenmenge(2)
assert a == Datenmenge(3) and alt == Datenmenge(1) and alt is not a, (
    f"Nach a = Datenmenge(1), alt = a und a += Datenmenge(2) ist a {a!r} und alt {alt!r}; erwartet war a "
    "Datenmenge(3) und alt unverändert Datenmenge(1).\nTipp: Datenmenge braucht kein __iadd__, und __add__ darf "
    "self nicht verändern."
)

# Mit anderen Typen gibt __iadd__ NotImplemented zurück, der Zähler bleibt
z = Portzaehler("Gi0/3")
rueckgaben = [ergebnis_von(lambda: z.__iadd__(wert)) for wert in [5, "x", None]]
assert all(rueckgabe is NotImplemented for rueckgabe in rueckgaben) and (z.gesamt, z.messungen) == (Datenmenge(0), 0), (
    f"z.__iadd__(5), z.__iadd__('x') und z.__iadd__(None) ergeben {rueckgaben!r}, erwartet war dreimal "
    f"NotImplemented; der Zähler danach: gesamt {z.gesamt!r}, messungen {z.messungen!r}, erwartet Datenmenge(0) und 0."
)


def plus_gleich(wert):
    """Führt zaehler += wert auf einem neuen Zähler aus und gibt den Zähler zurück."""
    zaehler = Portzaehler("Gi0/4")
    zaehler += wert
    return zaehler


# zaehler += 5 löst einen TypeError aus
fehler = [ergebnis_von(lambda: plus_gleich(wert)) for wert in [5, "x", None]]
assert fehler == ["<TypeError>"] * 3, (
    f"zaehler += 5, zaehler += 'x' und zaehler += None ergeben {fehler!r}, erwartet war dreimal ein TypeError.\n"
    "Tipp: Gibt __iadd__ NotImplemented zurück, versucht Python zaehler + 5; das gibt es nicht, also TypeError."
)

# Viele zufällige Rechnungen gegen eine Nachrechnung mit ganzen Zahlen
zufall = Zufall(5019)
for _ in range(300):
    werte = [zufall.randint(0, 10**18) for _ in range(zufall.randint(0, 8))]
    faktor = zufall.randint(0, 10**6)
    mengen = [Datenmenge(wert) for wert in werte]
    ergebnis = ergebnis_von(lambda: sum(mengen))
    erwartet = Datenmenge(sum(werte)) if werte else 0
    assert ergebnis == erwartet, f"sum({mengen}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    if werte:
        ergebnis = (ergebnis_von(lambda: mengen[0] * faktor), ergebnis_von(lambda: faktor * mengen[-1]))
        erwartet = (Datenmenge(werte[0] * faktor), Datenmenge(werte[-1] * faktor))
        assert ergebnis == erwartet, (
            f"{mengen[0]!r} * {faktor} und {faktor} * {mengen[-1]!r} ergeben {ergebnis!r}, erwartet war {erwartet!r}."
        )
    z = Portzaehler("Te1/0/1")
    for menge in mengen:
        z += menge
    assert (z.gesamt, z.messungen) == (Datenmenge(sum(werte)), len(werte)), (
        f"Nach z += … für {mengen} zeigt der Zähler gesamt {z.gesamt!r}, messungen {z.messungen!r}; erwartet "
        f"Datenmenge({sum(werte)}) und {len(werte)}."
    )

# Obere Grenze: 10**18 Bytes mal 10**6
ergebnis = ergebnis_von(lambda: 10**6 * Datenmenge(10**18) + Datenmenge(10**18) * 10**6)
assert ergebnis == Datenmenge(2 * 10**24), f"10**6 * Datenmenge(10**18) + Datenmenge(10**18) * 10**6 ergibt {ergebnis!r}, erwartet war Datenmenge({2 * 10**24})."

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "Datenmenge(2000) Datenmenge(3500) Datenmenge(1500)\nDatenmenge(2000) 2"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
