# Automatisch erzeugt aus lehrkraft/muster/1_005_fahrzeit.py - nicht von Hand ändern.
# vorlage-hash: d9ea4e463fa5912c
# thema: texte_zahlen
# inhalt: Ganzzahldivision und Rest

EINGABEN = ["135"]

# Bei Eingabe 135 kommen 2 Stunden und 15 Minuten heraus
if "." in AUSGABE[:-1]:
    hinweis = "Tipp: Mit / entsteht eine Kommazahl; für ganze Stunden brauchen Sie //."
else:
    hinweis = "Tipp: Die vollen Stunden sind minuten // 60, die übrigen Minuten minuten % 60 (nicht 60 % minuten)."
assert AUSGABE == "Das sind 2 Stunden und 15 Minuten.", (
    f'Bei Eingabe 135 erwartet: "Das sind 2 Stunden und 15 Minuten." – Ihr Programm: "{AUSGABE}"\n{hinweis}'
)

# Bei Eingabe 200 kommen 3 Stunden und 20 Minuten heraus (nicht fest 2 und 15 hinschreiben!)
ausgabe_200 = starte("200")
assert ausgabe_200 == "Das sind 3 Stunden und 20 Minuten.", (
    f'Bei Eingabe 200 erwartet: "Das sind 3 Stunden und 20 Minuten." – Ihr Programm: "{ausgabe_200}"'
)

# Weniger als eine Stunde: 0 Stunden
ausgabe_45 = starte("45")
assert ausgabe_45 == "Das sind 0 Stunden und 45 Minuten.", (
    f'Bei Eingabe 45 erwartet: "Das sind 0 Stunden und 45 Minuten." – Ihr Programm: "{ausgabe_45}"'
)

# Genau volle Stunden: der Rest ist 0
ausgabe_120 = starte("120")
assert ausgabe_120 == "Das sind 2 Stunden und 0 Minuten.", (
    f'Bei Eingabe 120 erwartet: "Das sind 2 Stunden und 0 Minuten." – Ihr Programm: "{ausgabe_120}"\n'
    "Tipp: Die übrigen Minuten berechnet der Rest-Operator %."
)

# Ränder: 0 Minuten und 10 000 Minuten
raender = [(0, "Das sind 0 Stunden und 0 Minuten."), (10000, "Das sind 166 Stunden und 40 Minuten.")]
for minuten_test, erwartet in raender:
    ausgabe = starte(str(minuten_test))
    assert ausgabe == erwartet, f'Bei Eingabe {minuten_test} erwartet: "{erwartet}" – Ihr Programm: "{ausgabe}"'

# 40 zufällige Fahrzeiten zwischen 0 und 10 000 Minuten, aufsteigend (die kleinste falsche fällt zuerst auf)
zufall = Zufall(1005)
fahrzeiten = sorted(zufall.randint(0, 10000) for _ in range(40))
for minuten_test in fahrzeiten:
    # Anders gerechnet als mit // und %: volle Stunden abziehen, solange es geht
    stunden_erwartet = 0
    rest_erwartet = minuten_test
    while rest_erwartet >= 60:
        stunden_erwartet += 1
        rest_erwartet -= 60
    erwartet = f"Das sind {stunden_erwartet} Stunden und {rest_erwartet} Minuten."
    ausgabe = starte(str(minuten_test))
    assert ausgabe == erwartet, f'Bei Eingabe {minuten_test} erwartet: "{erwartet}" – Ihr Programm: "{ausgabe}"'
