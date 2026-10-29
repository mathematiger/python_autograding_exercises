# Automatisch erzeugt aus lehrkraft/muster/1_016_sprintplan.py - nicht von Hand ändern.
# vorlage-hash: bf4759437325a5b8
# thema: kontrollfluss
# inhalt: Vergleiche mit `>`, `==`, `<`

EINGABEN = ["34", "30"]

# Das Beispiel aus der Aufgabe: überplant
erwartet = "Überplant: True\nGenau passend: False\nLuft übrig: False"
assert AUSGABE == erwartet, f"Bei den Eingaben 34 und 30 erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{AUSGABE}"

# Weniger geplant, als das Team schafft (nicht fest True, False, False hinschreiben!)
ausgabe = starte("21", "30")
erwartet = "Überplant: False\nGenau passend: False\nLuft übrig: True"
assert ausgabe == erwartet, f"Bei den Eingaben 21 und 30 erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}"

# Genau so viel geplant, wie das Team schafft
ausgabe = starte("30", "30")
erwartet = "Überplant: False\nGenau passend: True\nLuft übrig: False"
if ausgabe.startswith("Überplant: True"):
    hinweis = "\nTipp: Überplant ist das Team nur bei mehr Punkten als der Kapazität, also mit > statt >=."
elif ausgabe.endswith("Luft übrig: True"):
    hinweis = "\nTipp: Luft gibt es nur bei weniger Punkten als der Kapazität, also mit < statt <=."
else:
    hinweis = ""
assert ausgabe == erwartet, f"Bei den Eingaben 30 und 30 erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}"

# Ein Punkt mehr oder weniger als die Kapazität
for geplant_test, kapazitaet_test, erwartet in [
    ("31", "30", "Überplant: True\nGenau passend: False\nLuft übrig: False"),
    ("29", "30", "Überplant: False\nGenau passend: False\nLuft übrig: True"),
]:
    ausgabe = starte(geplant_test, kapazitaet_test)
    assert ausgabe == erwartet, (
        f"Bei den Eingaben {geplant_test} und {kapazitaet_test} erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}"
    )

# Ränder: 0 und 200
for geplant_test, kapazitaet_test, erwartet in [
    ("0", "0", "Überplant: False\nGenau passend: True\nLuft übrig: False"),
    ("0", "200", "Überplant: False\nGenau passend: False\nLuft übrig: True"),
    ("200", "0", "Überplant: True\nGenau passend: False\nLuft übrig: False"),
    ("200", "200", "Überplant: False\nGenau passend: True\nLuft übrig: False"),
]:
    ausgabe = starte(geplant_test, kapazitaet_test)
    assert ausgabe == erwartet, (
        f"Bei den Eingaben {geplant_test} und {kapazitaet_test} erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}"
    )

# Zahlen mit unterschiedlich vielen Ziffern werden als Zahlen verglichen, nicht als Texte
ausgabe = starte("9", "100")
erwartet = "Überplant: False\nGenau passend: False\nLuft übrig: True"
assert ausgabe == erwartet, (
    f"Bei den Eingaben 9 und 100 erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}\n"
    'Tipp: Vergleichen Sie die Zahlen geplant und kapazitaet; als Texte wäre "9" > "100", weil 9 nach 1 kommt.'
)

# 40 zufällige Pläne; jeder vierte genau passend
zufall = Zufall(1016)
for runde in range(40):
    kapazitaet_test = zufall.randint(0, 200)
    geplant_test = kapazitaet_test if runde % 4 == 0 else zufall.randint(0, 200)
    # Vergleichsrechnung über die Differenz statt mit < und >
    differenz = geplant_test - kapazitaet_test
    erwartet = (
        f"Überplant: {differenz > 0}\n"
        f"Genau passend: {differenz == 0}\n"
        f"Luft übrig: {differenz < 0}"
    )
    ausgabe = starte(str(geplant_test), str(kapazitaet_test))
    assert ausgabe == erwartet, (
        f"Bei den Eingaben {geplant_test} und {kapazitaet_test} erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}"
    )
