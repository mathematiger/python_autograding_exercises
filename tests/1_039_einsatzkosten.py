# Automatisch erzeugt aus lehrkraft/muster/1_039_einsatzkosten.py - nicht von Hand ändern.
# vorlage-hash: 332f8d6356b68fbc
# text-hash: 561fcf10c4074b78
# thema: funktionen
# inhalt: Mehrere Parameter

EINGABEN = ["3"]


def erwartete_ausgabe(stunden):
    """Baut die erwartete Ausgabe für so viele Arbeitsstunden, ohne die Funktion des Programms."""
    return (
        f"Vor Ort, Junior: {stunden * 45 + 30} Euro\n"
        f"Vor Ort, Senior: {stunden * 70 + 30} Euro\n"
        f"Fernwartung, Senior: {stunden * 70} Euro"
    )


def meldung(stunden, ausgabe):
    """Baut die Fehlermeldung mit Eingabe, erwarteter und tatsächlicher Ausgabe."""
    return f"Bei Eingabe {stunden} erwartet:\n{erwartete_ausgabe(stunden)}\nIhr Programm gibt aus:\n{ausgabe}"


# einsatzkosten(3, 45, 30) liefert 165
ergebnis = einsatzkosten(3, 45, 30)
if ergebnis is None:
    hinweis = "\nTipp: Die Funktion liefert None. Geben Sie das Ergebnis mit return zurück statt mit print."
else:
    hinweis = "\nTipp: Die Kosten sind stunden * stundensatz + anfahrt."
assert ergebnis == 165, f"einsatzkosten(3, 45, 30) ergibt {ergebnis!r}, erwartet war 3 * 45 + 30 = 165.{hinweis}"

# Andere Werte: einsatzkosten(5, 80, 40) liefert 440 (nicht fest hinschreiben!)
ergebnis = einsatzkosten(5, 80, 40)
assert ergebnis == 440, f"einsatzkosten(5, 80, 40) ergibt {ergebnis!r}, erwartet war 5 * 80 + 40 = 440."

# Die Reihenfolge der Parameter stimmt: stunden, stundensatz, anfahrt
ergebnis = einsatzkosten(2, 50, 10)
assert ergebnis == 110, (
    f"einsatzkosten(2, 50, 10) ergibt {ergebnis!r}, erwartet war 2 * 50 + 10 = 110.\n"
    "Tipp: Legen Sie die Parameter genau in der Reihenfolge stunden, stundensatz, anfahrt fest."
)

# Fernwartung: ohne Anfahrt nur die Arbeitszeit
ergebnis = einsatzkosten(4, 70, 0)
assert ergebnis == 280, f"einsatzkosten(4, 70, 0) ergibt {ergebnis!r}, erwartet war 4 * 70 + 0 = 280."

# Ohne Arbeitszeit bleibt nur die Anfahrt
ergebnis = einsatzkosten(0, 45, 30)
assert ergebnis == 30, f"einsatzkosten(0, 45, 30) ergibt {ergebnis!r}, erwartet war 0 * 45 + 30 = 30."

# Das Beispiel aus der Aufgabe
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe(3)), meldung(3, AUSGABE)

# Andere Arbeitsstunden
ausgabe = starte("7")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(7)), meldung(7, ausgabe)

# Kein Einsatz: 0 Stunden
ausgabe = starte("0")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(0)), meldung(0, ausgabe)

# Viele zufällige Werte für alle drei Parameter
zufall = Zufall(1039)
for _ in range(60):
    stunden = zufall.randint(0, 40)
    satz = zufall.randint(20, 150)
    anfahrt = zufall.choice([0, zufall.randint(1, 100)])
    ergebnis = einsatzkosten(stunden, satz, anfahrt)
    assert ergebnis == stunden * satz + anfahrt, (
        f"einsatzkosten({stunden}, {satz}, {anfahrt}) ergibt {ergebnis!r}, erwartet war {stunden * satz + anfahrt}."
    )

# Alle erlaubten Eingaben im ganzen Programm, bis zur oberen Grenze 40
for stunden in range(41):
    ausgabe = starte(str(stunden))
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(stunden)), meldung(stunden, ausgabe)
