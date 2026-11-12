# Automatisch erzeugt aus lehrkraft/muster/1_028_fehlende_werte.py - nicht von Hand ändern.
# vorlage-hash: 6f44d848160fbd47
# text-hash: b1576d11dc0a2669
# thema: kontrollfluss
# inhalt: for über eine Liste

EINGABEN = ["0211 4711,NULL,030 1234,NULL,NULL,089 555"]


def erwartete_ausgabe(werte):
    """Baut die erwartete Ausgabe mit count statt einer Schleife."""
    fehlend = werte.count("NULL")
    vollstaendig = (len(werte) - fehlend) / len(werte) * 100
    return f"{fehlend} von {len(werte)} Telefonnummern fehlen.\nVollständigkeit: {vollstaendig:.1f} %"


def hinweis_zu(ausgabe, werte):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    fehlend = werte.count("NULL")
    # Steht fehlend = 0 in der Schleife, zählt am Ende nur noch der letzte Wert
    nur_letzter = 1 if werte[-1] == "NULL" else 0
    if fehlend != nur_letzter and ausgabe.startswith(f"{nur_letzter} von {len(werte)} "):
        return (
            "\nTipp: Zählt Ihr Programm nur den letzten Wert? fehlend = 0 steht schon vor der Schleife; "
            "steht es noch einmal in der Schleife, fängt der Zähler bei jedem Wert neu an."
        )
    if fehlend != 1 and ausgabe.startswith(f"1 von {len(werte)} "):
        return (
            "\nTipp: Es wird höchstens einmal gezählt. Rücken Sie fehlend = fehlend + 1 unter das if in der "
            "Schleife ein und schreiben Sie fehlend = fehlend + 1 statt fehlend = 1."
        )
    if fehlend != len(werte) and ausgabe.startswith(f"{len(werte)} von {len(werte)} "):
        return '\nTipp: Es wird jeder Wert gezählt. Zählen Sie nur, wenn der Wert gleich "NULL" ist.'
    if fehlend > 0 and ausgabe.startswith(f"0 von {len(werte)} "):
        return '\nTipp: Vergleichen Sie jedes Element der Liste mit "NULL", in Großbuchstaben und mit Anführungszeichen.'
    return ""


def meldung(werte, ausgabe):
    """Baut die Fehlermeldung mit Eingabe, erwarteter und tatsächlicher Ausgabe."""
    return (
        f"Bei der Eingabe {','.join(werte)} erwartet:\n{erwartete_ausgabe(werte)}\n"
        f"Ihr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe, werte)}"
    )


# Das Beispiel aus der Aufgabe: drei von sechs fehlen
BEISPIEL = ["0211 4711", "NULL", "030 1234", "NULL", "NULL", "089 555"]
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe(BEISPIEL)), meldung(BEISPIEL, AUSGABE)

# Andere Spalte (nicht fest hinschreiben!)
spalte = ["NULL", "040 99887", "0711 23", "06221 5"]
ausgabe = starte(",".join(spalte))
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(spalte)), meldung(spalte, ausgabe)

# Keine Telefonnummer fehlt
spalte = ["0351 1", "0361 22", "0391 333"]
ausgabe = starte(",".join(spalte))
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(spalte)), meldung(spalte, ausgabe)

# Alle Telefonnummern fehlen
spalte = ["NULL", "NULL", "NULL", "NULL", "NULL"]
ausgabe = starte(",".join(spalte))
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(spalte)), meldung(spalte, ausgabe)

# Nur ein einziger Wert, und der fehlt
spalte = ["NULL"]
ausgabe = starte(",".join(spalte))
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(spalte)), meldung(spalte, ausgabe)

# Nur ein einziger Wert, und der ist da
spalte = ["0800 123 456"]
ausgabe = starte(",".join(spalte))
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(spalte)), meldung(spalte, ausgabe)

# Eine for-Schleife wird benutzt
assert verwendet("for"), "Benutzen Sie für diese Aufgabe eine for-Schleife über die Liste nummern."

# 40 zufällige Spalten
zufall = Zufall(1028)
for _ in range(40):
    spalte = []
    for _ in range(zufall.randint(1, 15)):
        if zufall.random() < 0.4:
            spalte.append("NULL")
        else:
            spalte.append(f"0{zufall.randint(20, 9999)} {zufall.randint(1, 999999)}")
    ausgabe = starte(",".join(spalte))
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(spalte)), meldung(spalte, ausgabe)

# Obere Grenze: 50 Werte, jeder dritte fehlt
spalte = []
for zahl in range(50):
    if zahl % 3 == 0:
        spalte.append("NULL")
    else:
        spalte.append(f"030 {1000 + zahl}")
ausgabe = starte(",".join(spalte))
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(spalte)), meldung(spalte, ausgabe)
