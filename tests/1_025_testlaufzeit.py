# Automatisch erzeugt aus lehrkraft/muster/1_025_testlaufzeit.py - nicht von Hand ändern.
# vorlage-hash: fafd971b4bce06e9
# text-hash: b89cc2155e17d2e0
# thema: kontrollfluss
# inhalt: Zähler in der Schleife

EINGABEN = ["3", "120", "45", "300"]


def hinweis_zu(ausgabe, laufzeiten):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    if len(laufzeiten) > 1 and ausgabe == f"Gesamtlaufzeit: {laufzeiten[-1]} ms":
        return (
            "\nTipp: Es kommt nur die letzte Laufzeit heraus. Setzen Sie summe = 0 vor die Schleife, nicht hinein, "
            "und schreiben Sie eingerückt in der Schleife summe = summe + dauer statt summe = dauer."
        )
    return ""


# Das Beispiel aus der Aufgabe: drei Tests
assert AUSGABE == "Gesamtlaufzeit: 465 ms", (
    f'Bei den Eingaben 3, 120, 45 und 300 erwartet: "Gesamtlaufzeit: 465 ms" – Ihr Programm: "{AUSGABE}"'
    f"{hinweis_zu(AUSGABE, [120, 45, 300])}"
)

# Andere Laufzeiten (nicht fest 465 hinschreiben!)
ausgabe = starte("2", "7", "8")
assert ausgabe == "Gesamtlaufzeit: 15 ms", (
    f'Bei den Eingaben 2, 7 und 8 erwartet: "Gesamtlaufzeit: 15 ms" – Ihr Programm: "{ausgabe}"{hinweis_zu(ausgabe, [7, 8])}'
)

# Ein einziger Test
ausgabe = starte("1", "250")
assert ausgabe == "Gesamtlaufzeit: 250 ms", (
    f'Bei den Eingaben 1 und 250 erwartet: "Gesamtlaufzeit: 250 ms" – Ihr Programm: "{ausgabe}"'
)

# Kein Test: die Schleife läuft gar nicht, die Summe bleibt 0
try:
    ausgabe = starte("0")
    hinweis = ""
except Exception as fehler:
    # Fehlt summe = 0 vor der Schleife, bricht das Programm bei print mit einem NameError ab
    ausgabe = f"(Abbruch: {fehler})"
    hinweis = "\nTipp: summe muss vor der Schleife auf 0 gesetzt werden, sonst gibt es sie nicht, wenn die Schleife nie läuft."
assert ausgabe == "Gesamtlaufzeit: 0 ms", f'Bei Eingabe 0 erwartet: "Gesamtlaufzeit: 0 ms" – Ihr Programm: "{ausgabe}"{hinweis}'

# Laufzeiten von 0 ms zählen mit
ausgabe = starte("4", "0", "5", "0", "6")
assert ausgabe == "Gesamtlaufzeit: 11 ms", (
    f'Bei den Eingaben 4, 0, 5, 0 und 6 erwartet: "Gesamtlaufzeit: 11 ms" – Ihr Programm: "{ausgabe}"'
    f"{hinweis_zu(ausgabe, [0, 5, 0, 6])}"
)

# 40 zufällige Testläufe
zufall = Zufall(1025)
for _ in range(40):
    laufzeiten = [zufall.randint(0, 100000) for _ in range(zufall.randint(0, 12))]
    # Vergleichsrechnung ohne Schleife
    erwartet = f"Gesamtlaufzeit: {sum(laufzeiten)} ms"
    ausgabe = starte(str(len(laufzeiten)), *[str(dauer) for dauer in laufzeiten])
    assert ausgabe == erwartet, (
        f"Bei {len(laufzeiten)} Tests mit den Laufzeiten {laufzeiten} erwartet: \"{erwartet}\" – Ihr Programm: \"{ausgabe}\""
        f"{hinweis_zu(ausgabe, laufzeiten)}"
    )

# Obere Grenze: 100 Tests mit je 100000 ms
ausgabe = starte("100", *(["100000"] * 100))
assert ausgabe == "Gesamtlaufzeit: 10000000 ms", (
    f'Bei 100 Tests mit je 100000 ms erwartet: "Gesamtlaufzeit: 10000000 ms" – Ihr Programm: "{ausgabe}"'
)
