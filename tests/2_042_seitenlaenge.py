# Automatisch erzeugt aus lehrkraft/muster/2_042_seitenlaenge.py - nicht von Hand ändern.
# vorlage-hash: 1c73d09238ca2478
# text-hash: 91fc8446e6695067
# thema: algorithmen
# inhalt: Wurzel per Bisektion

def genau_genug(x, flaeche):
    """True, wenn x eine Zahl ≥ 0 ist, deren Quadrat höchstens GENAUIGKEIT von flaeche abweicht."""
    return isinstance(x, (int, float)) and x >= 0 and abs(x * x - flaeche) < GENAUIGKEIT


def meldung(flaeche, x, erwartet):
    """Baut die Fehlermeldung mit Eingabe, Ergebnis und ungefähr erwarteter Seitenlänge."""
    if isinstance(x, (int, float)):
        quadrat = f", ihr Quadrat ist {x * x!r}"
    else:
        quadrat = " (keine Zahl; fehlt das return?)"
    return (
        f"seitenlaenge({flaeche!r}) ergibt {x!r}{quadrat}; erwartet war ungefähr {erwartet}, "
        f"und das Quadrat darf höchstens {GENAUIGKEIT} von {flaeche!r} abweichen."
    )


# Das Beispiel aus der Aufgabe: 2500 Quadratmeter ergeben etwa 50 Meter
x = seitenlaenge(2500)
assert genau_genug(x, 2500), meldung(2500, x, 50.0)

# Eine Fläche, deren Wurzel keine ganze Zahl ist (nicht fest 50 hinschreiben!)
x = seitenlaenge(2)
assert genau_genug(x, 2), meldung(2, x, 1.41421)

# Weitere Flächen
for flaeche, erwartet in [(10, 3.16228), (7.5, 2.73861), (123456, 351.36306)]:
    x = seitenlaenge(flaeche)
    assert genau_genug(x, flaeche), meldung(flaeche, x, erwartet)

# Fläche genau 1
x = seitenlaenge(1)
assert genau_genug(x, 1), meldung(1, x, 1.0)

# Fläche unter 1: die Wurzel ist größer als die Fläche selbst
x = seitenlaenge(0.25)
assert genau_genug(x, 0.25), (
    meldung(0.25, x, 0.5) + "\nTipp: Bei Flächen unter 1 liegt die Wurzel über der Fläche; nehmen Sie als "
    "obere Grenze max(flaeche, 1)."
)

# Fläche 0
x = seitenlaenge(0)
assert genau_genug(x, 0), meldung(0, x, 0.0)

# Keine fertige Wurzelfunktion
assert not verwendet("sqrt") and not verwendet("pow"), (
    "Ihr Code benutzt sqrt(...) oder pow(...). Nähern Sie die Wurzel stattdessen selbst mit Bisektion an."
)

# Eine while-Schleife wird benutzt
assert verwendet("while"), "Benutzen Sie für die Bisektion eine while-Schleife, die läuft, bis es genau genug ist."

# Der Bereich wird halbiert: auch bei 10**6 nur wenige Schritte
x, schritte = zaehle_schritte(seitenlaenge, 10**6)
assert genau_genug(x, 10**6) and schritte <= 500, (
    f"seitenlaenge(10**6) ergibt {x!r} nach {schritte} ausgeführten Zeilen; erwartet war ungefähr 1000.0 "
    "mit höchstens 500 Zeilen (die Musterlösung braucht etwa 200).\n"
    "Tipp: Halbieren Sie bei jedem Durchlauf den Bereich zwischen tief und hoch, statt in kleinen Schritten zu raten."
)

# 300 zufällige Flächen, große und kleine
zufall = Zufall(2042)
for runde in range(300):
    if runde % 3 == 0:
        flaeche = zufall.uniform(0, 1)
    elif runde % 3 == 1:
        flaeche = zufall.randint(0, 10**6)
    else:
        flaeche = round(zufall.uniform(0, 1000), 2)
    x = seitenlaenge(flaeche)
    # Vergleichswert mit ** 0.5, nur für die Meldung
    assert genau_genug(x, flaeche), meldung(flaeche, x, round(flaeche**0.5, 5))

# Obere Grenze: 10**6 Quadratmeter ergeben etwa 1000 Meter
x = seitenlaenge(10**6)
assert genau_genug(x, 10**6), meldung(10**6, x, 1000.0)

# Die Ausgabe des Programms stimmt
assert vergleichbar(AUSGABE) == vergleichbar("50.0"), f'Erwartete Ausgabe: "50.0" – Ihr Programm: "{AUSGABE}"'
