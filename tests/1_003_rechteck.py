# Automatisch erzeugt aus lehrkraft/muster/1_003_rechteck.py - nicht von Hand ändern.
# vorlage-hash: add0291c044b81c9
# text-hash: 5a9e3f5a1779750a
# thema: texte_zahlen
# inhalt: Rechnen mit Variablen

EINGABEN = ["4", "3"]

# Variable flaeche ist 12
assert flaeche == 12, f"flaeche ist {flaeche!r}, erwartet war 12."

# Variable umfang ist 14
assert umfang == 14, f"umfang ist {umfang!r}, erwartet war 14."

# Ausgabe stimmt
assert AUSGABE == "Fläche: 12\nUmfang: 14", f"Erwartet:\nFläche: 12\nUmfang: 14\nIhr Programm gibt aus:\n{AUSGABE}"

# Ein anderer Raum (nicht fest 12 und 14 hinschreiben!)
ausgabe = starte("7", "5")
erwartet = "Fläche: 35\nUmfang: 24"
if "Umfang: 17" in ausgabe:
    hinweis = "\nTipp: Punkt vor Strich – der Umfang braucht Klammern: 2 * (breite + hoehe)."
else:
    hinweis = ""
assert ausgabe == erwartet, f"Bei den Eingaben 7 und 5 erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}"

# Ränder: kleinster und größter Raum
for breite_test, hoehe_test in [(1, 1), (1000, 1000), (1, 1000)]:
    erwartet = f"Fläche: {breite_test * hoehe_test}\nUmfang: {2 * breite_test + 2 * hoehe_test}"
    ausgabe = starte(str(breite_test), str(hoehe_test))
    assert ausgabe == erwartet, (
        f"Bei den Eingaben {breite_test} und {hoehe_test} erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}"
    )

# 40 zufällige Räume
zufall = Zufall(1003)
for _ in range(40):
    breite_test = zufall.randint(1, 1000)
    hoehe_test = zufall.randint(1, 1000)
    # Umfang als Summe der vier Seiten, anders als die übliche Formel
    erwartet = f"Fläche: {breite_test * hoehe_test}\nUmfang: {breite_test + hoehe_test + breite_test + hoehe_test}"
    ausgabe = starte(str(breite_test), str(hoehe_test))
    assert ausgabe == erwartet, (
        f"Bei den Eingaben {breite_test} und {hoehe_test} erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}"
    )
