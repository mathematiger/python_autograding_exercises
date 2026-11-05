# Automatisch erzeugt aus lehrkraft/muster/1_028_ortsangaben.py - nicht von Hand ändern.
# vorlage-hash: a64acd018d760c30
# text-hash: f609492a091331f4
# thema: kontrollfluss
# inhalt: for über eine Liste

EINGABEN = ["Paderborn"]

ORTE = ["Paderborn", "Bielefeld", "paderborn", "Detmold", "PADERBORN", "bielefeld", "Lemgo"]


def erwartete_ausgabe(gesucht):
    """Baut die erwartete Ausgabe mit einer while-Schleife über die Indizes."""
    zeilen = []
    index = 0
    while index < len(ORTE):
        if ORTE[index].upper() == gesucht.upper():
            zeilen.append("Treffer: " + ORTE[index])
        index = index + 1
    zeilen.append(f"{len(zeilen)} Einträge zu {gesucht}")
    return "\n".join(zeilen)


def hinweis_zu(ausgabe, gesucht):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    erwartet = erwartete_ausgabe(gesucht)
    if ausgabe.count("Treffer:") < erwartet.count("Treffer:"):
        return (
            "\nTipp: Es fehlen Treffer. Vergleichen Sie beide Seiten in Kleinbuchstaben: "
            "ort.lower() == gesucht.lower()."
        )
    klein = f"Treffer: {gesucht.lower()}\n"
    if ausgabe.count(klein) > erwartet.count(klein):
        return "\nTipp: Geben Sie den Eintrag so aus, wie er in der Liste steht, nicht in Kleinbuchstaben."
    if ausgabe.startswith("0 Einträge") and erwartet.count("Treffer:") > 0:
        return "\nTipp: treffer = treffer + 1 gehört eingerückt unter das if in der Schleife."
    return ""


def meldung(gesucht, ausgabe):
    """Baut die Fehlermeldung mit Eingabe, erwarteter und tatsächlicher Ausgabe."""
    return (
        f"Bei Eingabe {gesucht} erwartet:\n{erwartete_ausgabe(gesucht)}\nIhr Programm gibt aus:\n{ausgabe}"
        f"{hinweis_zu(ausgabe, gesucht)}"
    )


# Das Beispiel aus der Aufgabe
assert AUSGABE == erwartete_ausgabe("Paderborn"), meldung("Paderborn", AUSGABE)

# Ein anderer Ort (nicht fest hinschreiben!)
ausgabe = starte("Bielefeld")
assert ausgabe == erwartete_ausgabe("Bielefeld"), meldung("Bielefeld", ausgabe)

# Die Eingabe selbst ist klein- oder großgeschrieben
for gesucht in ["paderborn", "DETMOLD", "lEMGO"]:
    ausgabe = starte(gesucht)
    assert ausgabe == erwartete_ausgabe(gesucht), meldung(gesucht, ausgabe)

# Ein Ort, der gar nicht vorkommt
ausgabe = starte("Hamburg")
assert ausgabe == erwartete_ausgabe("Hamburg"), meldung("Hamburg", ausgabe)

# Nur ganze Einträge zählen, nicht Teile davon
for gesucht in ["Pader", "Bielefelder", "L"]:
    ausgabe = starte(gesucht)
    assert ausgabe == erwartete_ausgabe(gesucht), (
        meldung(gesucht, ausgabe) + "\nTipp: Vergleichen Sie mit ==, nicht mit in."
    )

# Eine for-Schleife über die Liste wird benutzt
assert verwendet("for") and not verwendet("range"), (
    "Benutzen Sie eine for-Schleife direkt über die Liste: for ort in orte: (ohne range)."
)

# 40 zufällige Schreibweisen von Orten aus der Liste und anderen Orten
zufall = Zufall(1028)
for _ in range(40):
    ort = zufall.choice(["paderborn", "bielefeld", "detmold", "lemgo", "minden", "herford", "x", "abcdefghijklmnopqrstuvwxyzabcd"])
    gesucht = "".join(zufall.choice([zeichen.lower(), zeichen.upper()]) for zeichen in ort)
    ausgabe = starte(gesucht)
    assert ausgabe == erwartete_ausgabe(gesucht), meldung(gesucht, ausgabe)
