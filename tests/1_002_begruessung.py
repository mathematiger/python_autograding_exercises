# Automatisch erzeugt aus lehrkraft/muster/1_002_begruessung.py - nicht von Hand ändern.
# vorlage-hash: c533ef29945b41af
# thema: texte_zahlen
# inhalt: Eingabe und Ausgabe

EINGABEN = ["Anna"]

# Begrüßung bei Eingabe "Anna"
assert AUSGABE == "Hallo Anna!", f'Bei Eingabe "Anna" erwartet: "Hallo Anna!" – Ihr Programm: "{AUSGABE}"'

# Begrüßung bei Eingabe "Bo" (nicht fest "Anna" hinschreiben!)
ausgabe_bo = starte("Bo")
assert ausgabe_bo == "Hallo Bo!", f'Bei Eingabe "Bo" erwartet: "Hallo Bo!" – Ihr Programm: "{ausgabe_bo}"'

# Ränder: ein Name aus einem einzigen Buchstaben und einer aus 30 Buchstaben
for name_test in ["X", "Schwarzenbergerhöfflingmüßiger"]:
    ausgabe = starte(name_test)
    assert ausgabe == f"Hallo {name_test}!", (
        f'Bei Eingabe "{name_test}" erwartet: "Hallo {name_test}!" – Ihr Programm: "{ausgabe}"'
    )

# 40 zufällige Namen
zufall = Zufall(1002)
buchstaben = "abcdefghijklmnopqrstuvwxyzäöüßABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ"
for _ in range(40):
    name_test = "".join(zufall.choices(buchstaben, k=zufall.randint(1, 30)))
    ausgabe = starte(name_test)
    assert ausgabe == f"Hallo {name_test}!", (
        f'Bei Eingabe "{name_test}" erwartet: "Hallo {name_test}!" – Ihr Programm: "{ausgabe}"\n'
        'Tipp: Fügen Sie die Variable name zwischen "Hallo " und "!" ein.'
    )
