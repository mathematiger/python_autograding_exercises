# Automatisch erzeugt aus lehrkraft/muster/1_017_temperaturwarnung.py - nicht von Hand ändern.
# vorlage-hash: bbb1bece45333178
# text-hash: 0d572cf2a368da06
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
assert AUSGABE == erwartete_ausgabe(85), (
    f"Bei Eingabe 85 erwartet:\n{erwartete_ausgabe(85)}\nIhr Programm gibt aus:\n{AUSGABE}"
)

# Bei 60 Grad kommt keine Warnung (nicht fest hinschreiben!)
ausgabe = starte("60")
assert ausgabe == erwartete_ausgabe(60), (
    f"Bei Eingabe 60 erwartet:\n{erwartete_ausgabe(60)}\nIhr Programm gibt aus:\n{ausgabe}\n"
    "Tipp: Die Warnung gehört eingerückt unter ein if, damit sie nur bei mehr als 80 Grad erscheint."
)

# Genau 80 Grad sind noch in Ordnung, 81 Grad nicht mehr
for grad in [80, 81]:
    ausgabe = starte(str(grad))
    if grad == 80 and WARNUNG in ausgabe:
        hinweis = "\nTipp: Bei genau 80 Grad soll keine Warnung kommen; vergleichen Sie mit > statt >=."
    else:
        hinweis = ""
    assert ausgabe == erwartete_ausgabe(grad), (
        f"Bei Eingabe {grad} erwartet:\n{erwartete_ausgabe(grad)}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}"
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
    assert ausgabe == erwartete_ausgabe(grad), (
        f"Bei Eingabe {grad} erwartet:\n{erwartete_ausgabe(grad)}\nIhr Programm gibt aus:\n{ausgabe}"
    )

# Ein if wird benutzt
assert verwendet("if"), "Benutzen Sie für die Warnung ein if."

# 40 zufällige Temperaturen von 0 bis 120 Grad
zufall = Zufall(1017)
for _ in range(40):
    grad = zufall.randint(0, 120)
    ausgabe = starte(str(grad))
    assert ausgabe == erwartete_ausgabe(grad), (
        f"Bei Eingabe {grad} erwartet:\n{erwartete_ausgabe(grad)}\nIhr Programm gibt aus:\n{ausgabe}"
    )
