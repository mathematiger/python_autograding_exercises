# Automatisch erzeugt aus lehrkraft/muster/1_022_loeschen.py - nicht von Hand ändern.
# vorlage-hash: 3a3a0773b3d1a963
# text-hash: bed91ced548c942a
# thema: kontrollfluss
# inhalt: for über range(n)

EINGABEN = ["3"]


def erwartete_ausgabe(anzahl):
    """Baut die erwartete Ausgabe bei anzahl Durchgängen, Zeile für Zeile mit while statt for."""
    zeilen = []
    zaehler = 1
    while zaehler <= anzahl:
        zeilen.append(f"Durchgang {zaehler} von {anzahl}: überschrieben")
        zaehler = zaehler + 1
    zeilen.append("Löschen abgeschlossen.")
    return "\n".join(zeilen)


def hinweis_zu(ausgabe, anzahl):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    if " : überschrieben" in ausgabe:
        return "\nTipp: print mit Kommas setzt ein Leerzeichen vor den Doppelpunkt; setzen Sie die Zeile mit einem f-String zusammen (Aufgabe 1_010)."
    if f"Durchgang 0 von {anzahl}" in ausgabe:
        return "\nTipp: range fängt bei 0 an; geben Sie nummer + 1 aus, damit ab 1 gezählt wird."
    if ausgabe.count("Löschen abgeschlossen.") > 1:
        return "\nTipp: Die letzte Zeile gehört nicht in die Schleife."
    if ausgabe.count("überschrieben") != anzahl:
        return f"\nTipp: Es müssen genau {anzahl} Durchgänge sein; range(durchgaenge) liefert so viele Zahlen."
    return ""


# Das Beispiel aus der Aufgabe: 3 Durchgänge
assert AUSGABE == erwartete_ausgabe(3), (
    f"Bei Eingabe 3 erwartet:\n{erwartete_ausgabe(3)}\nIhr Programm gibt aus:\n{AUSGABE}{hinweis_zu(AUSGABE, 3)}"
)

# 7 Durchgänge (nicht fest hinschreiben!)
ausgabe = starte("7")
assert ausgabe == erwartete_ausgabe(7), (
    f"Bei Eingabe 7 erwartet:\n{erwartete_ausgabe(7)}\nIhr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe, 7)}"
)

# Untere Grenze: ein einziger Durchgang
ausgabe = starte("1")
assert ausgabe == erwartete_ausgabe(1), (
    f"Bei Eingabe 1 erwartet:\n{erwartete_ausgabe(1)}\nIhr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe, 1)}"
)

# Eine for-Schleife wird benutzt
assert verwendet("for"), "Benutzen Sie für diese Aufgabe eine for-Schleife mit range."

# Alle Anzahlen von 1 bis 35 der Reihe nach, damit die Meldung die kleinste falsche nennt
for anzahl in range(1, 36):
    ausgabe = starte(str(anzahl))
    assert ausgabe == erwartete_ausgabe(anzahl), (
        f"Bei Eingabe {anzahl} erwartet:\n{erwartete_ausgabe(anzahl)}\nIhr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe, anzahl)}"
    )

# Obere Grenze: 35 Durchgänge
ausgabe = starte("35")
zeilen = ausgabe.split("\n")
assert ausgabe == erwartete_ausgabe(35), (
    f"Bei Eingabe 35 erwartet: 36 Zeilen, von „Durchgang 1 von 35: überschrieben“ bis „Durchgang 35 von 35: überschrieben“ "
    f"und dann „Löschen abgeschlossen.“. Ihr Programm gibt {len(zeilen)} Zeilen aus, die ersten: {zeilen[:2]}, "
    f"die letzten: {zeilen[-2:]}{hinweis_zu(ausgabe, 35)}"
)
