# Automatisch erzeugt aus lehrkraft/muster/2_045_zeitschlitze.py - nicht von Hand ändern.
# vorlage-hash: f740ab9921aabc63
# text-hash: d78d935de1dc47d8
# thema: algorithmen
# inhalt: Rekursion: Fibonacci

def vergleich(n):
    """Vergleichslösung mit einer Liste aller Werte von 0 bis n."""
    werte = [1, 1]
    while len(werte) <= n:
        werte.append(werte[-1] + werte[-2])
    return werte[n]


def ruft_sich_selbst_auf(n):
    """Zählt, wie oft belegungen_rekursiv beim Aufruf mit n sich selbst aufruft."""
    global belegungen_rekursiv
    original = belegungen_rekursiv
    innere = []

    def mitzaehlen(k):
        """Merkt sich den inneren Aufruf und reicht ihn an die echte Funktion weiter."""
        innere.append(k)
        return original(k)

    belegungen_rekursiv = mitzaehlen
    try:
        original(n)
    finally:
        belegungen_rekursiv = original
    return len(innere)


def ergebnis_von(funktion, n):
    """Ruft funktion(n) auf; ein RecursionError wird als Text zurückgegeben."""
    try:
        return funktion(n)
    except RecursionError:
        return "RecursionError"


# Rekursiv: drei Schlitze haben 3 Belegungen
ergebnis = ergebnis_von(belegungen_rekursiv, 3)
assert ergebnis == 3, f"belegungen_rekursiv(3) ergibt {ergebnis!r}, erwartet war 3."

# Rekursiv: vier Schlitze haben 5 Belegungen (nicht fest hinschreiben!)
ergebnis = ergebnis_von(belegungen_rekursiv, 4)
assert ergebnis == 5, f"belegungen_rekursiv(4) ergibt {ergebnis!r}, erwartet war 3 + 2 = 5."

# Rekursiv: ein Schlitz hat genau eine Belegung
ergebnis = ergebnis_von(belegungen_rekursiv, 1)
assert ergebnis == 1, (
    f"belegungen_rekursiv(1) ergibt {ergebnis!r}, erwartet war 1.\n"
    "Tipp: Für n = 1 ist n - 2 = -1; fangen Sie diesen Fall mit einer Abbruchbedingung ab."
)

# Rekursiv: kein Schlitz hat genau eine (die leere) Belegung
ergebnis = ergebnis_von(belegungen_rekursiv, 0)
assert ergebnis == 1, f"belegungen_rekursiv(0) ergibt {ergebnis!r}, erwartet war 1."

# Rekursiv: die Funktion ruft sich selbst auf
anzahl = ruft_sich_selbst_auf(5)
assert anzahl > 0, (
    "belegungen_rekursiv(5) ruft sich nicht selbst auf. Lösen Sie diese Fassung rekursiv mit "
    "belegungen_rekursiv(n - 1) + belegungen_rekursiv(n - 2)."
)

# Rekursiv: alle Werte von 0 bis 20
for n in range(21):
    ergebnis = ergebnis_von(belegungen_rekursiv, n)
    assert ergebnis == vergleich(n), f"belegungen_rekursiv({n}) ergibt {ergebnis!r}, erwartet war {vergleich(n)}."

# Schleife: zehn Schlitze haben 89 Belegungen
ergebnis = belegungen_schleife(10)
assert ergebnis == 89, f"belegungen_schleife(10) ergibt {ergebnis!r}, erwartet war 89."

# Schleife: andere Werte (nicht fest hinschreiben!)
ergebnis = [belegungen_schleife(n) for n in (2, 3, 7)]
assert ergebnis == [2, 3, 21], f"belegungen_schleife für 2, 3 und 7 ergibt {ergebnis!r}, erwartet war [2, 3, 21]."

# Schleife: die Ränder 0 und 1
ergebnis = [belegungen_schleife(0), belegungen_schleife(1)]
assert ergebnis == [1, 1], f"belegungen_schleife(0) und belegungen_schleife(1) ergeben {ergebnis!r}, erwartet war [1, 1]."

# Schleife: ohne sich selbst aufzurufen, und mit for oder while
assert verwendet("for") or verwendet("while"), "Schreiben Sie belegungen_schleife mit einer for- oder while-Schleife."

# Schleife: viele zufällige Werte
zufall = Zufall(2045)
for n in sorted(zufall.sample(range(5001), 60)):
    ergebnis = belegungen_schleife(n)
    assert ergebnis == vergleich(n), f"belegungen_schleife({n}) ergibt eine falsche Zahl (erwartet {vergleich(n)})."

# Schleife: für n = 4000 nur etwa n Durchläufe, nicht exponentiell viele Aufrufe
ergebnis, schritte = zaehle_schritte(belegungen_schleife, 4000)
assert ergebnis == vergleich(4000) and schritte <= 3 * 4000 + 50, (
    f"belegungen_schleife(4000) braucht {schritte} ausgeführte Zeilen; erwartet waren höchstens "
    f"{3 * 4000 + 50}, also etwa eine Zeile je Schlitz.\n"
    "Tipp: Merken Sie sich in der Schleife nur die beiden letzten Werte und rechnen Sie von unten nach oben."
)

# Schleife: obere Grenze n = 5000
ergebnis = belegungen_schleife(5000)
assert ergebnis == vergleich(5000), (
    f"belegungen_schleife(5000) ergibt eine falsche Zahl; erwartet war eine Zahl mit {len(str(vergleich(5000)))} Ziffern."
)
