# Automatisch erzeugt aus lehrkraft/muster/1_005_fahrzeit.py - nicht von Hand ändern.
# vorlage-hash: 0abb81e3d5930986
# thema: texte_zahlen
# inhalt: Ganzzahldivision und Rest

EINGABEN = ["135"]

# Bei Eingabe 135 kommen 2 Stunden und 15 Minuten heraus
assert AUSGABE == "Das sind 2 Stunden und 15 Minuten.", (
    f'Bei Eingabe 135 erwartet: "Das sind 2 Stunden und 15 Minuten." – Ihr Programm: "{AUSGABE}"\n'
    "Tipp: Mit / entsteht eine Kommazahl; für ganze Stunden brauchen Sie //."
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
