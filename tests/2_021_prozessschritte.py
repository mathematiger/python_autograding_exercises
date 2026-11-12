# Automatisch erzeugt aus lehrkraft/muster/2_021_prozessschritte.py - nicht von Hand ändern.
# vorlage-hash: e9a5ddafe468c742
# text-hash: 4c4af591b67f61a1
# thema: kontrollfluss
# inhalt: enumerate

dauern = [5, 42, 18, 42, 7]

# zu_lange aus dem Beispiel
ergebnis = zu_lange(dauern, 15)
assert ergebnis == [2, 3, 4], (
    f"zu_lange([5, 42, 18, 42, 7], 15) ergibt {ergebnis!r}, erwartet war [2, 3, 4].\n"
    "Tipp: Die Schritte werden ab 1 gezählt; enumerate(dauern, start=1) beginnt bei 1."
)

# Genau soll Minuten sind noch in Ordnung
for soll, erwartet in [(42, []), (41, [2, 4]), (18, [2, 4]), (17, [2, 3, 4])]:
    ergebnis = zu_lange(dauern, soll)
    assert ergebnis == erwartet, (
        f"zu_lange([5, 42, 18, 42, 7], {soll}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: „länger als soll“ heißt dauer > soll; genau soll Minuten zählen nicht."
    )

# Ränder: soll 0, alle Dauern 0, nur ein Schritt
for liste, soll, erwartet in [([0, 3, 0, 1], 0, [2, 4]), ([0, 0, 0], 0, []), ([10000], 9999, [1]), ([10000], 10000, [])]:
    ergebnis = zu_lange(liste, soll)
    assert ergebnis == erwartet, f"zu_lange({liste}, {soll}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# engpass aus dem Beispiel: bei Gleichstand zählt der erste
ergebnis = engpass(dauern)
assert ergebnis == 2, (
    f"engpass([5, 42, 18, 42, 7]) ergibt {ergebnis!r}, erwartet war 2.\n"
    "Tipp: Schritt 2 und 4 dauern beide 42 Minuten; der erste zählt, ersetzen Sie also nur bei >, nicht bei >=."
)

# Der Engpass am Anfang, am Ende, nur ein Schritt, alle gleich
for liste, erwartet in [([9, 3, 4], 1), ([1, 2, 30], 3), ([0], 1), ([7, 7, 7], 1), ([0, 0, 1], 3)]:
    ergebnis = engpass(liste)
    assert ergebnis == erwartet, (
        f"engpass({liste}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Geben Sie die Nummer des Schritts zurück (ab 1), nicht seine Dauer und nicht den Index ab 0."
    )

# Die Liste bleibt unverändert
liste = [3, 1, 2]
zu_lange(liste, 1)
engpass(liste)
assert liste == [3, 1, 2], f"Nach zu_lange und engpass ist die Liste {liste!r}, sie soll unverändert [3, 1, 2] sein."

# enumerate wird benutzt
assert verwendet("enumerate"), "Benutzen Sie für diese Aufgabe enumerate."

# max() und liste.index(...) werden nicht benutzt, wie im Text verlangt
assert not verwendet("max") and not verwendet("index"), (
    "Lösen Sie engpass ohne max() und liste.index(...): Merken Sie sich in der Schleife mit enumerate "
    "die Nummer und die Dauer des bisher längsten Schritts."
)


# Vergleichslösung mit while und eigenem Zähler
def zu_lange_von_hand(liste, soll):
    """Zählt die Position mit while selbst mit."""
    gefunden = []
    position = 0
    while position < len(liste):
        if liste[position] > soll:
            gefunden.append(position + 1)
        position = position + 1
    return gefunden


# 300 zufällige Messreihen für zu_lange
zufall = Zufall(2021)
for _ in range(300):
    liste = [zufall.randint(0, 30) for _ in range(zufall.randint(1, 8))]
    soll = zufall.randint(0, 30)
    erwartet = zu_lange_von_hand(liste, soll)
    ergebnis = zu_lange(liste, soll)
    assert ergebnis == erwartet, f"zu_lange({liste}, {soll}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# 300 zufällige Messreihen für engpass
zufall = Zufall(2021)
for _ in range(300):
    liste = [zufall.randint(0, 30) for _ in range(zufall.randint(1, 8))]
    soll = zufall.randint(0, 30)
    erwartet = liste.index(max(liste)) + 1
    ergebnis = engpass(liste)
    assert ergebnis == erwartet, f"engpass({liste}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# An der oberen Grenze: zu_lange bei 100 000 Schritten
gross = [(nummer * 37) % 10001 for nummer in range(100000)]
erwartet = zu_lange_von_hand(gross, 9990)
ergebnis = zu_lange(gross, 9990)
assert ergebnis == erwartet, (
    f"Bei 100 000 Schritten liefert zu_lange(…, 9990) {len(ergebnis)} Nummern, die ersten {ergebnis[:3]}; "
    f"erwartet waren {len(erwartet)} Nummern, die ersten {erwartet[:3]}."
)

# An der oberen Grenze: engpass bei 100 000 Schritten
spitze = engpass(gross)
assert spitze == gross.index(10000) + 1, (
    f"Bei 100 000 Schritten liefert engpass {spitze!r}, erwartet war {gross.index(10000) + 1}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "[2, 3, 4]\n2"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
