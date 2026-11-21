# Automatisch erzeugt aus lehrkraft/muster/1_041_einmalcode.py - nicht von Hand ändern.
# vorlage-hash: 72db839ae40d09d4
# text-hash: 1b8880463043eaa1
# thema: algorithmen
# inhalt: Zufall mit randint und seed

EINGABEN = ["42"]


def erwarteter_code(startzahl):
    """Zieht den Code so, wie das Programm es nach random.seed(startzahl) tun soll."""
    return Zufall(startzahl).randint(100000, 999999)


def satz(startzahl):
    """Die erwartete Ausgabe zur Startzahl."""
    return f"Ihr Einmalcode: {erwarteter_code(startzahl)}"


def code_stimmt(startzahl, ausgabe):
    """Prüft, ob der erwartete Code zur Startzahl in der Ausgabe steht; der Wortlaut drumherum zählt nicht."""
    return erwarteter_code(startzahl) in zahlen_in(ausgabe)


def meldung(startzahl, ausgabe):
    """Fehlermeldung mit erwartetem Code und tatsächlicher Ausgabe."""
    return f"Bei der Startzahl {startzahl} erwartet: Code {erwarteter_code(startzahl)} – Ihr Programm: \"{ausgabe}\""


def zahlen_in(ausgabe):
    """Alle ganzen Zahlen, die in der Ausgabe stehen."""
    zahlen = []
    for wort in vergleichbar(ausgabe).replace(":", " ").split():
        ziffern = "".join(zeichen for zeichen in wort if zeichen.isdigit())
        if ziffern:
            zahlen.append(int(ziffern))
    return zahlen


# Bei der Startzahl 42 steht der Code 770487 in der Ausgabe
assert "770487" in AUSGABE, (
    f'Bei der Startzahl 42 erwartet: "Ihr Einmalcode: 770487" – Ihr Programm: "{AUSGABE}"\n'
    "Tipp: Ziehen Sie den Code mit random.randint(100000, 999999), genau einmal und nach random.seed."
)

# Bei der Startzahl 42 lautet die ganze Zeile "Ihr Einmalcode: 770487"
assert vergleichbar(AUSGABE) == vergleichbar(satz(42)), (
    f'Bei der Startzahl 42 erwartet: "{satz(42)}" – Ihr Programm: "{AUSGABE}"'
)

# Eine andere Startzahl gibt einen anderen Code (nicht fest 770487 hinschreiben!)
ausgabe = starte("7")
assert code_stimmt(7, ausgabe), meldung(7, ausgabe)

# Dieselbe Startzahl gibt denselben Code
ausgaben = [starte("2024"), starte("2024")]
assert ausgaben[0] == ausgaben[1] and code_stimmt(2024, ausgaben[0]), (
    f'Zweimal die Startzahl 2024 ergibt "{ausgaben[0]}" und "{ausgaben[1]}", '
    f"erwartet war beide Male der Code {erwarteter_code(2024)}."
)

# Ränder der Startzahl: 0 und 1000000
for startzahl in [0, 1000000]:
    ausgabe = starte(str(startzahl))
    assert code_stimmt(startzahl, ausgabe), meldung(startzahl, ausgabe)

# Der Code ist immer sechsstellig: 200 Startzahlen
for startzahl in range(200):
    ausgabe = starte(str(startzahl))
    zahlen = zahlen_in(ausgabe)
    assert len(zahlen) == 1 and 100000 <= zahlen[0] <= 999999, (
        f'Bei der Startzahl {startzahl} gibt Ihr Programm "{ausgabe}" aus; erwartet war genau ein Code von '
        "100000 bis 999999."
    )

# Bei der Startzahl 406683 würde randint(100000, 1000000) die siebenstellige Zahl 1000000 ziehen
ausgabe = starte("406683")
assert code_stimmt(406683, ausgabe), (
    meldung(406683, ausgabe) + "\n"
    "Tipp: randint(a, b) schließt b mit ein; die Obergrenze für sechsstellige Codes ist 999999."
)

# 40 zufällige Startzahlen
zufall = Zufall(1041)
for _ in range(40):
    startzahl = zufall.randint(0, 1000000)
    ausgabe = starte(str(startzahl))
    assert code_stimmt(startzahl, ausgabe), (
        meldung(startzahl, ausgabe) + "\n"
        "Tipp: Prüfen Sie die Grenzen: random.randint(100000, 999999)."
    )
