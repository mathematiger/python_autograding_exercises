# Automatisch erzeugt aus lehrkraft/muster/1_004_fahrenheit.py - nicht von Hand ändern.
# vorlage-hash: 69589ddee72e9cc9

EINGABEN = ["25"]

# Bei Eingabe 25 kommt 77.0 heraus
assert AUSGABE == "Das sind 77.0 Grad Fahrenheit.", (
    f'Bei Eingabe 25 erwartet: "Das sind 77.0 Grad Fahrenheit." – Ihr Programm: "{AUSGABE}"'
)

# Bei Eingabe 0 kommt 32.0 heraus (nicht fest 77.0 hinschreiben!)
ausgabe_null = starte("0")
assert ausgabe_null == "Das sind 32.0 Grad Fahrenheit.", (
    f'Bei Eingabe 0 erwartet: "Das sind 32.0 Grad Fahrenheit." – Ihr Programm: "{ausgabe_null}"'
)

# Auch Kommazahlen funktionieren: 36.5 Grad sind 97.7 Grad Fahrenheit
ausgabe_fieber = starte("36.5")
assert ausgabe_fieber == "Das sind 97.7 Grad Fahrenheit.", (
    f'Bei Eingabe 36.5 erwartet: "Das sind 97.7 Grad Fahrenheit." – Ihr Programm: "{ausgabe_fieber}"\n'
    "Tipp: Wandeln Sie die Eingabe mit float(...) um, nicht mit int(...)."
)
