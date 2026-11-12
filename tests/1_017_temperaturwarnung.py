# Automatisch erzeugt aus lehrkraft/muster/1_017_temperaturwarnung.py - nicht von Hand ändern.
# vorlage-hash: bbb1bece45333178
# text-hash: 02fb941d15467d4b
# thema: kontrollfluss
# inhalt: if-Anweisung

EINGABEN = ["85"]

WARNUNG = "Warnung: Die CPU ist zu heiß!"


def erwartete_ausgabe(grad):
    """Baut die Ausgabe, die bei der Temperatur grad erwartet wird."""
    if grad > 80:
        return f"Gemessen: {grad} Grad\n{WARNUNG}\nMessung gespeichert."
    return f"Gemessen: {grad} Grad\nMessung gespeichert."


# Das Beispiel aus der Aufgabe: 85 Grad sind zu heiß
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe(85)), (
    f"Bei Eingabe 85 erwartet:\n{erwartete_ausgabe(85)}\nIhr Programm gibt aus:\n{AUSGABE}"
)

# Bei 60 Grad kommt keine Warnung (nicht fest hinschreiben!)
ausgabe = starte("60")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(60)), (
    f"Bei Eingabe 60 erwartet:\n{erwartete_ausgabe(60)}\nIhr Programm gibt aus:\n{ausgabe}\n"
    "Tipp: Die Warnung gehört eingerückt unter ein if, damit sie nur bei mehr als 80 Grad erscheint."
)

# 81 Grad sind schon zu heiß
ausgabe = starte("81")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(81)), (
    f"Bei Eingabe 81 erwartet:\n{erwartete_ausgabe(81)}\nIhr Programm gibt aus:\n{ausgabe}\n"
    "Tipp: Die Warnung kommt bei jeder Temperatur über 80 Grad, also mit temperatur > 80."
)

# Genau 80 Grad sind noch in Ordnung
ausgabe = starte("80")
if WARNUNG in ausgabe:
    hinweis = "\nTipp: Bei genau 80 Grad soll keine Warnung kommen; vergleichen Sie mit > statt >=."
else:
    hinweis = ""
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(80)), (
    f"Bei Eingabe 80 erwartet:\n{erwartete_ausgabe(80)}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}"
)

# „Messung gespeichert.“ steht immer am Schluss, auch ohne Warnung
ausgabe = starte("20")
assert ausgabe.endswith("Messung gespeichert."), (
    f"Bei Eingabe 20 fehlt die letzte Zeile „Messung gespeichert.“; Ihr Programm gibt aus:\n{ausgabe}\n"
    "Tipp: Rücken Sie nur die Warnung ein, nicht die Zeile danach."
)

# Ränder: 0 und 120 Grad
for grad in [0, 120]:
    ausgabe = starte(str(grad))
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(grad)), (
        f"Bei Eingabe {grad} erwartet:\n{erwartete_ausgabe(grad)}\nIhr Programm gibt aus:\n{ausgabe}"
    )

# Ein if wird benutzt
assert verwendet("if"), "Benutzen Sie für die Warnung ein if."

# 40 zufällige Temperaturen von 0 bis 120 Grad
zufall = Zufall(1017)
for _ in range(40):
    grad = zufall.randint(0, 120)
    ausgabe = starte(str(grad))
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(grad)), (
        f"Bei Eingabe {grad} erwartet:\n{erwartete_ausgabe(grad)}\nIhr Programm gibt aus:\n{ausgabe}"
    )
