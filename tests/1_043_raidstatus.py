# Automatisch erzeugt aus lehrkraft/muster/1_043_raidstatus.py - nicht von Hand ändern.
# vorlage-hash: f38ef96297d51a70
# text-hash: bfa6ecee7fa6a4e8
# thema: texte_zahlen
# inhalt: Zeichen zählen mit for

EINGABEN = ["UU_U_U"]


def erwartet(status):
    """Die erwartete Ausgabe zu einem Status-Text; gezählt mit count statt mit einer Schleife."""
    kaputt = status.count("_")
    return f"Platten: {len(status)}\nAusgefallen: {kaputt}\nLaufen: {len(status) - kaputt}"


def meldung(status, ausgabe):
    """Fehlermeldung mit erwarteter und tatsächlicher Ausgabe."""
    return f'Bei Eingabe "{status}" erwartet:\n{erwartet(status)}\nIhr Programm gibt aus:\n{ausgabe}'


# Im Beispiel sind zwei Platten ausgefallen
if vergleichbar("Ausgefallen: 4") in vergleichbar(AUSGABE):
    hinweis = '\nTipp: Gezählt werden die Unterstriche "_", nicht die U.'
elif vergleichbar("Ausgefallen: 0") in vergleichbar(AUSGABE):
    hinweis = '\nTipp: Erhöhen Sie ausgefallen um 1, wenn zeichen == "_" ist.'
elif vergleichbar("Ausgefallen: 1") in vergleichbar(AUSGABE):
    hinweis = "\nTipp: ausgefallen = ausgefallen + 1 erhöht den Zähler; ausgefallen = 1 setzt ihn nur auf 1."
else:
    hinweis = ""
assert vergleichbar("Ausgefallen: 2") in vergleichbar(AUSGABE), meldung("UU_U_U", AUSGABE) + hinweis

# Die ganze Ausgabe im Beispiel
assert vergleichbar(AUSGABE) == vergleichbar(erwartet("UU_U_U")), meldung("UU_U_U", AUSGABE)

# Ein anderer Verbund mit drei Ausfällen (nicht fest 2 hinschreiben!)
ausgabe = starte("_U__UUUU")
assert vergleichbar(ausgabe) == vergleichbar(erwartet("_U__UUUU")), meldung("_U__UUUU", ausgabe)

# Alle Platten laufen
ausgabe = starte("UUUU")
assert vergleichbar(ausgabe) == vergleichbar(erwartet("UUUU")), (
    meldung("UUUU", ausgabe) + "\nTipp: Zählen Sie nur, wenn das Zeichen ein Unterstrich ist."
)

# Alle Platten sind ausgefallen
ausgabe = starte("___")
assert vergleichbar(ausgabe) == vergleichbar(erwartet("___")), meldung("___", ausgabe)

# Ausfälle ganz vorn und ganz hinten werden mitgezählt
ausgabe = starte("_UUUUUU_")
assert vergleichbar(ausgabe) == vergleichbar(erwartet("_UUUUUU_")), (
    meldung("_UUUUUU_", ausgabe) + "\nTipp: Prüfen Sie in jedem Durchgang, ob zeichen ein Unterstrich ist, auch beim ersten und letzten Zeichen."
)

# Nur eine Platte, einmal laufend und einmal ausgefallen
for status in ["U", "_"]:
    ausgabe = starte(status)
    assert vergleichbar(ausgabe) == vergleichbar(erwartet(status)), meldung(status, ausgabe)

# Gezählt wird mit der Schleife, nicht mit count()
assert not verwendet("count"), "Ihr Programm verwendet count(). Zählen Sie hier selbst mit if und dem Zähler in der Schleife."

# 40 zufällige Verbünde
zufall = Zufall(1043)
for _ in range(40):
    status = "".join(zufall.choice("U_") for _ in range(zufall.randint(1, 30)))
    ausgabe = starte(status)
    assert vergleichbar(ausgabe) == vergleichbar(erwartet(status)), meldung(status, ausgabe)

# Obere Grenze: 30 Platten
status = "U_" * 15
ausgabe = starte(status)
assert vergleichbar(ausgabe) == vergleichbar(erwartet(status)), meldung(status, ausgabe)
