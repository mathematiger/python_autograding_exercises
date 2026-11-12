# Automatisch erzeugt aus lehrkraft/muster/1_024_rack.py - nicht von Hand ändern.
# vorlage-hash: d28c1cbabcd056e6
# text-hash: 7652c4b9f6940496
# thema: kontrollfluss
# inhalt: range mit Schrittweite

EINGABEN = ["6"]


def erwartete_ausgabe(hoehe):
    """Baut die erwartete Ausgabe mit einer while-Schleife, die von oben herunterzählt."""
    zeilen = []
    oben = hoehe
    while oben >= 2:
        zeilen.append(f"Server in HE {oben - 1} und {oben}")
        oben = oben - 2
    zeilen.append(f"{hoehe // 2} Server passen in das Rack.")
    return "\n".join(zeilen)


def hinweis_zu(ausgabe, hoehe):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    zeilen = ausgabe.split("\n")
    if "HE 0" in ausgabe:
        return "\nTipp: Es gibt keine HE 0; die unterste ist HE 1. Achten Sie auf das Ende von range."
    if f"und {hoehe + 1}" in ausgabe:
        return f"\nTipp: Das Rack hat nur {hoehe} HE; der oberste Server belegt HE {hoehe - 1} und {hoehe}."
    if len(zeilen) > 1 and zeilen[0] == "Server in HE 1 und 2" and hoehe > 3:
        return "\nTipp: Eingebaut wird von oben nach unten; zählen Sie mit einer negativen Schrittweite rückwärts."
    if ausgabe.count("Server in HE") != hoehe // 2:
        return f"\nTipp: Es sind {hoehe // 2} Server; die Schrittweite muss -2 sein, weil jeder Server zwei HE belegt."
    return ""


# Das Beispiel aus der Aufgabe: Höhe 6
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe(6)), (
    f"Bei Eingabe 6 erwartet:\n{erwartete_ausgabe(6)}\nIhr Programm gibt aus:\n{AUSGABE}{hinweis_zu(AUSGABE, 6)}"
)

# Ungerade Höhe: unten bleibt HE 1 frei
ausgabe = starte("7")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(7)), (
    f"Bei Eingabe 7 erwartet:\n{erwartete_ausgabe(7)}\nIhr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe, 7)}\n"
    "Tipp: Der oberste Server belegt immer die beiden obersten HE, also hoehe - 1 und hoehe."
)

# Eine andere Höhe (nicht fest hinschreiben!)
ausgabe = starte("12")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(12)), (
    f"Bei Eingabe 12 erwartet:\n{erwartete_ausgabe(12)}\nIhr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe, 12)}"
)

# Untere Grenze: Höhe 2 und 3, je ein Server
for hoehe in [2, 3]:
    ausgabe = starte(str(hoehe))
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(hoehe)), (
        f"Bei Eingabe {hoehe} erwartet:\n{erwartete_ausgabe(hoehe)}\nIhr Programm gibt aus:\n{ausgabe}"
        f"{hinweis_zu(ausgabe, hoehe)}"
    )

# Eine for-Schleife mit range wird benutzt
assert verwendet("for") and verwendet("range"), "Benutzen Sie für diese Aufgabe eine for-Schleife mit range(…, …, …)."

# Alle Höhen von 2 bis 48 der Reihe nach, damit die Meldung die kleinste falsche nennt
for hoehe in range(2, 49):
    ausgabe = starte(str(hoehe))
    zeilen = ausgabe.split("\n")
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(hoehe)), (
        f"Bei Eingabe {hoehe} erwartet: {hoehe // 2 + 1} Zeilen, von „Server in HE {hoehe - 1} und {hoehe}“ bis "
        f"„Server in HE {1 + hoehe % 2} und {2 + hoehe % 2}“ und dann „{hoehe // 2} Server passen in das Rack.“. "
        f"Ihr Programm gibt {len(zeilen)} Zeilen aus, die ersten: {zeilen[:2]}, die letzten: {zeilen[-2:]}"
        f"{hinweis_zu(ausgabe, hoehe)}"
    )
