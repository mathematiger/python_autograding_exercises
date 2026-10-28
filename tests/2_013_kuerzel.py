# Automatisch erzeugt aus lehrkraft/muster/2_013_kuerzel.py - nicht von Hand ändern.
# vorlage-hash: 1d22023d209eadba

# Das Beispiel aus der Aufgabe
ergebnis = kuerzel("Ware prüfen")
assert ergebnis == "Wrprfn", f'kuerzel("Ware prüfen") ergibt {ergebnis!r}, erwartet war "Wrprfn".'

# Weitere Schritte (nicht fest hinschreiben!)
for schritt, erwartet in [
    ("Paket versenden", "Pktvrsndn"),
    ("Rechnung stellen", "Rchnngstlln"),
    ("Lieferschein drucken", "Lfrschndrckn"),
    ("Retoure buchen", "Rtrbchn"),
]:
    ergebnis = kuerzel(schritt)
    if " " in ergebnis:
        hinweis = "\nTipp: Auch die Leerzeichen gehören nicht ins Kürzel."
    else:
        hinweis = ""
    assert ergebnis == erwartet, f"kuerzel({schritt!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.{hinweis}"

# Großgeschriebene Vokale und Umlaute werden auch entfernt
for schritt, erwartet in [("Ware Ausgeben", "Wrsgbn"), ("Kunde Über Lieferung Informieren", "KndbrLfrngnfrmrn")]:
    ergebnis = kuerzel(schritt)
    assert ergebnis == erwartet, (
        f"kuerzel({schritt!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
        "Tipp: Vokale gibt es auch groß; die Konstante VOKALE enthält alle."
    )

# Der erste Buchstabe bleibt, auch wenn er ein Vokal ist
for schritt, erwartet in [("Auftrag erfassen", "Aftrgrfssn"), ("Übergabe", "Übrgb"), ("ordnen", "ordnn")]:
    ergebnis = kuerzel(schritt)
    assert ergebnis == erwartet, (
        f"kuerzel({schritt!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
        "Tipp: Der erste Buchstabe kommt immer ins Kürzel; nur ab dem zweiten werden Vokale entfernt."
    )

# Ein Name aus einem einzigen Buchstaben bleibt, wie er ist
for schritt in ["A", "X"]:
    ergebnis = kuerzel(schritt)
    assert ergebnis == schritt, f"kuerzel({schritt!r}) ergibt {ergebnis!r}, erwartet war {schritt!r}."

# Ein leerer Name ergibt ein leeres Kürzel
try:
    ergebnis = kuerzel("")
except IndexError as fehler:
    ergebnis = fehler
assert ergebnis == "", (
    f'kuerzel("") ergibt {ergebnis!r}, erwartet war "".\n'
    'Tipp: Bei einem leeren Text gibt es kein schritt[0]. Prüfen Sie diesen Fall zuerst.'
)

# Eine for-Schleife wird benutzt
assert verwendet("for"), "Bauen Sie das Kürzel mit einer for-Schleife über die Zeichen auf."

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "Auftrag erfassen: Aftrgrfssn\nWare kommissionieren: Wrkmmssnrn\nPaket versenden: Pktvrsndn"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
