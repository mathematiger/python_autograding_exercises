# Automatisch erzeugt aus lehrkraft/muster/3_009_raid.py - nicht von Hand ändern.
# vorlage-hash: b96ed9cc8e69d395

# Das Beispiel aus der Aufgabe: RAID 5 mit vier Platten zu 8 TB
ergebnis = nutzkapazitaet(5, 4, 8)
assert ergebnis == 24, f"nutzkapazitaet(5, 4, 8) ergibt {ergebnis!r}, erwartet war 24."

# Alle Level rechnen richtig (nicht fest hinschreiben!)
for level, anzahl, groesse, erwartet in [
    (0, 2, 4, 8),
    (0, 5, 2, 10),
    (0, 3, 1, 3),
    (1, 2, 4, 4),
    (1, 3, 6, 6),
    (5, 3, 2, 4),
    (5, 6, 10, 50),
    (6, 4, 8, 16),
    (6, 7, 3, 15),
    (5, 4, 1.5, 4.5),
]:
    try:
        ergebnis = nutzkapazitaet(level, anzahl, groesse)
    except ValueError as ausnahme:
        ergebnis = ausnahme
    assert ergebnis == erwartet, (
        f"nutzkapazitaet({level}, {anzahl}, {groesse}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Schauen Sie in der Tabelle der Aufgabe nach, wie das Level rechnet und wie viele Platten es braucht."
    )

# Unbekannte Level lösen ValueError mit dem Level in der Meldung aus
for level in [2, 3, 10, -1]:
    try:
        ergebnis = nutzkapazitaet(level, 4, 8)
        fehler = None
    except ValueError as ausnahme:
        fehler = ausnahme
    assert fehler is not None and str(fehler) == f"Unbekanntes RAID-Level: {level}", (
        f'nutzkapazitaet({level}, 4, 8) muss einen ValueError mit der Meldung "Unbekanntes RAID-Level: {level}" '
        f"auslösen; Ausnahme: {fehler!r}.\n"
        'Tipp: raise ValueError(f"Unbekanntes RAID-Level: {level}") setzt das Level in die Meldung ein.'
    )

# Zu wenige Platten lösen ValueError mit der Mindestzahl in der Meldung aus
for level, anzahl, mindestens in [(0, 1, 2), (1, 1, 2), (5, 2, 3), (6, 3, 4), (6, 2, 4), (6, 0, 4)]:
    try:
        ergebnis = nutzkapazitaet(level, anzahl, 8)
        fehler = None
    except ValueError as ausnahme:
        fehler = ausnahme
    erwartete_meldung = f"RAID {level} braucht mindestens {mindestens} Platten"
    assert fehler is not None and str(fehler) == erwartete_meldung, (
        f'nutzkapazitaet({level}, {anzahl}, 8) muss einen ValueError mit der Meldung "{erwartete_meldung}" '
        f"auslösen; Ausnahme: {fehler!r}.\n"
        "Tipp: Prüfen Sie die Vorbedingungen am Anfang der Funktion, bevor Sie rechnen."
    )

# Genau die Mindestzahl an Platten ist erlaubt
for level, anzahl, erwartet in [(0, 2, 16), (1, 2, 8), (5, 3, 16), (6, 4, 16)]:
    try:
        ergebnis = nutzkapazitaet(level, anzahl, 8)
    except ValueError as ausnahme:
        ergebnis = ausnahme
    assert ergebnis == erwartet, (
        f"nutzkapazitaet({level}, {anzahl}, 8) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        f"Tipp: {anzahl} Platten sind für RAID {level} genau genug; verboten ist nur eine kleinere Anzahl."
    )

# Größe 0 oder negativ löst ValueError aus
for groesse in [0, -4]:
    try:
        ergebnis = nutzkapazitaet(5, 4, groesse)
        fehler = None
    except ValueError as ausnahme:
        fehler = ausnahme
    assert fehler is not None and str(fehler) == "Die Plattengröße muss positiv sein", (
        f'nutzkapazitaet(5, 4, {groesse}) muss einen ValueError mit der Meldung "Die Plattengröße muss positiv sein" '
        f"auslösen; Ausnahme: {fehler!r}."
    )

# Das Level wird vor der Anzahl geprüft
try:
    nutzkapazitaet(7, 1, 8)
    fehler = None
except ValueError as ausnahme:
    fehler = ausnahme
assert fehler is not None and str(fehler) == "Unbekanntes RAID-Level: 7", (
    'nutzkapazitaet(7, 1, 8) muss einen ValueError mit der Meldung "Unbekanntes RAID-Level: 7" auslösen; '
    f"Ausnahme: {fehler!r}.\nTipp: Prüfen Sie das Level zuerst."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "RAID 5 mit 4 x 8 TB: 24 TB\n"
    "RAID 1 mit 2 x 4 TB: 4 TB\n"
    "RAID 6 mit 2 x 8 TB: Fehler – RAID 6 braucht mindestens 4 Platten\n"
    "RAID 3 mit 4 x 8 TB: Fehler – Unbekanntes RAID-Level: 3"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
