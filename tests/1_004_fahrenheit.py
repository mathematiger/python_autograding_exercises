# Automatisch erzeugt aus lehrkraft/muster/1_004_fahrenheit.py - nicht von Hand ändern.
# vorlage-hash: 65322aabe987ec3c
# text-hash: 88a4d787e113d0e7
# thema: texte_zahlen
# inhalt: Eingabe in Zahl umwandeln

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
try:
    ausgabe_fieber = starte("36.5")
    hinweis = "Tipp: Prüfen Sie die Formel: Fahrenheit = Celsius * 9 / 5 + 32."
except Exception as fehler:
    # Ein Abbruch, etwa durch int("36.5"), soll den passenden Tipp bekommen statt nur der Fehlermeldung
    ausgabe_fieber = f"(Abbruch: {fehler})"
    hinweis = 'Tipp: Wandeln Sie die Eingabe mit float(...) um, nicht mit int(...); int("36.5") geht nicht.'
assert ausgabe_fieber == "Das sind 97.7 Grad Fahrenheit.", (
    f'Bei Eingabe 36.5 erwartet: "Das sind 97.7 Grad Fahrenheit." – Ihr Programm: "{ausgabe_fieber}"\n{hinweis}'
)

# Hilfsfunktion für die folgenden Tests: Kommazahlen dürfen in der letzten Stelle abweichen
# (bei -6.5 ergibt celsius * 1.8 + 32 die Zahl 20.299999999999997 statt 20.3, beides ist richtig).
def fahrenheit_in(ausgabe):
    """Liest die Zahl aus "Das sind … Grad Fahrenheit."; None, wenn die Ausgabe anders aussieht."""
    vorne = "Das sind "
    hinten = " Grad Fahrenheit."
    if not (ausgabe.startswith(vorne) and ausgabe.endswith(hinten)):
        return None
    try:
        return float(ausgabe[len(vorne) : -len(hinten)])
    except ValueError:
        return None

# Ränder: -50 Grad sind -58 Grad Fahrenheit, 50 Grad sind 122 Grad Fahrenheit
for celsius_test, erwartet in [("-50", -58.0), ("50", 122.0)]:
    ausgabe = starte(celsius_test)
    assert fahrenheit_in(ausgabe) == erwartet, (
        f'Bei Eingabe {celsius_test} erwartet: "Das sind {erwartet} Grad Fahrenheit." – Ihr Programm: "{ausgabe}"'
    )

# 40 zufällige Temperaturen zwischen -50 und 50 Grad
zufall = Zufall(1004)
for _ in range(40):
    zehntel = zufall.randint(-500, 500)
    celsius_test = str(zehntel / 10)
    # In Hundertstel gerechnet, damit kein Rundungsfehler entsteht: 0.1 Grad Celsius sind 0.18 Grad Fahrenheit.
    erwartet = (zehntel * 18 + 3200) / 100
    ausgabe = starte(celsius_test)
    wert = fahrenheit_in(ausgabe)
    assert wert is not None and abs(wert - erwartet) < 0.000001, (
        f'Bei Eingabe {celsius_test} erwartet: "Das sind {erwartet} Grad Fahrenheit." – Ihr Programm: "{ausgabe}"'
    )
