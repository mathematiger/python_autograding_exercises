# Automatisch erzeugt aus lehrkraft/muster/1_009_umgedrehte_uhr.py - nicht von Hand ändern.
# vorlage-hash: d9a9cdcdcb70b2be
# thema: texte_zahlen
# inhalt: Im Kreis zählen mit %

EINGABEN = ["14:20"]

# Bei Eingabe 14:20 liest man auf der umgedrehten Uhr 8 Uhr und 50 Minuten ab
assert "Um 180° gedreht: 8 Uhr und 50 Minuten" in AUSGABE.splitlines(), (
    'Bei Eingabe 14:20 erwartet die Zeile: "Um 180° gedreht: 8 Uhr und 50 Minuten"\n'
    f"Ihr Programm:\n{AUSGABE}\n"
    "Tipp: Bei einer halben Drehung rückt der Stundenzeiger 6 Stunden und der Minutenzeiger 30 Minuten weiter."
)

# Abends über die volle Stunde: 21:45 wird zu 3 Uhr und 15 Minuten (nicht fest 8 und 50 hinschreiben!)
ausgabe_abend = starte("21:45")
assert "Um 180° gedreht: 3 Uhr und 15 Minuten" in ausgabe_abend.splitlines(), (
    'Bei Eingabe 21:45 erwartet die Zeile: "Um 180° gedreht: 3 Uhr und 15 Minuten"\n'
    f"Ihr Programm:\n{ausgabe_abend}\n"
    "Tipp: 45 + 30 sind mehr als 60 Minuten. Mit % 60 und % 12 laufen die Zeiger im Kreis."
)

# Auf dem Zifferblatt steht 12, nicht 0: 6:40 wird zu 12 Uhr und 10 Minuten
ausgabe_zwoelf = starte("6:40")
assert "Um 180° gedreht: 12 Uhr und 10 Minuten" in ausgabe_zwoelf.splitlines(), (
    'Bei Eingabe 6:40 erwartet die Zeile: "Um 180° gedreht: 12 Uhr und 10 Minuten"\n'
    f"Ihr Programm:\n{ausgabe_zwoelf}\n"
    "Tipp: (6 + 6) % 12 ergibt 0, auf der Uhr steht aber 12. Siehe den Trick mit - 1 und + 1 im Hintergrund."
)

# Volle Stunde: 12:00 wird zu 6 Uhr und 30 Minuten
ausgabe_mittag = starte("12:00")
assert "Um 180° gedreht: 6 Uhr und 30 Minuten" in ausgabe_mittag.splitlines(), (
    'Bei Eingabe 12:00 erwartet die Zeile: "Um 180° gedreht: 6 Uhr und 30 Minuten"\n'
    f"Ihr Programm:\n{ausgabe_mittag}"
)

# Zusatz: Bei 14:20 liest man nach 90° Drehung 5 Uhr und 35 Minuten ab
assert "Um 90° gedreht: 5 Uhr und 35 Minuten" in AUSGABE.splitlines(), (
    'Zusatz: Bei Eingabe 14:20 erwartet die Zeile: "Um 90° gedreht: 5 Uhr und 35 Minuten"\n'
    f"Ihr Programm:\n{AUSGABE}\n"
    "Tipp: 90° sind eine Viertelrunde im Uhrzeigersinn: Wohin zeigt dann ein Zeiger, der vorher auf die 12 zeigte?"
)

# Zusatz: Bei 14:20 liest man nach 270° Drehung 11 Uhr und 5 Minuten ab
assert "Um 270° gedreht: 11 Uhr und 5 Minuten" in AUSGABE.splitlines(), (
    'Zusatz: Bei Eingabe 14:20 erwartet die Zeile: "Um 270° gedreht: 11 Uhr und 5 Minuten"\n'
    f"Ihr Programm:\n{AUSGABE}\n"
    "Tipp: 270° sind drei Viertelrunden. Haben Sie vielleicht 90° und 270° vertauscht?"
)

# Zusatz: Bei 9:00 zeigt die um 90° gedrehte Uhr 12 Uhr und 15 Minuten
ausgabe_neun = starte("9:00")
assert "Um 90° gedreht: 12 Uhr und 15 Minuten" in ausgabe_neun.splitlines(), (
    'Zusatz: Bei Eingabe 9:00 erwartet die Zeile: "Um 90° gedreht: 12 Uhr und 15 Minuten"\n'
    f"Ihr Programm:\n{ausgabe_neun}\n"
    "Tipp: Auch hier muss aus 0 eine 12 werden."
)

# Zusatz: Bei 9:00 zeigt die um 270° gedrehte Uhr 6 Uhr und 45 Minuten
assert "Um 270° gedreht: 6 Uhr und 45 Minuten" in ausgabe_neun.splitlines(), (
    'Zusatz: Bei Eingabe 9:00 erwartet die Zeile: "Um 270° gedreht: 6 Uhr und 45 Minuten"\n'
    f"Ihr Programm:\n{ausgabe_neun}"
)

# Zusatz: Bei 21:45 läuft auch der Minutenzeiger der um 90° gedrehten Uhr über die volle Stunde
assert "Um 90° gedreht: 12 Uhr und 0 Minuten" in ausgabe_abend.splitlines(), (
    'Zusatz: Bei Eingabe 21:45 erwartet die Zeile: "Um 90° gedreht: 12 Uhr und 0 Minuten"\n'
    f"Ihr Programm:\n{ausgabe_abend}\n"
    "Tipp: 45 + 15 sind 60 Minuten, auf der Uhr steht dann 0. Rechnen Sie % 60."
)

# Hilfsfunktion für die folgenden Tests, anders gerechnet als mit Stunden und Minuten: über die Winkel der Zeiger
def abgelesen(stunde_test, minute_test, drehung):
    """Liefert die Zeile, die man bei der um drehung Grad gedrehten Uhr abliest."""
    # Winkel in halben Grad, damit alles ganzzahlig bleibt: Der Stundenzeiger schafft 60 halbe Grad pro Stunde
    # und einen halben pro Minute, der Minutenzeiger 12 halbe Grad pro Minute. Volle Runde: 720 halbe Grad.
    stundenzeiger = ((stunde_test % 12) * 60 + minute_test + 2 * drehung) % 720
    minutenzeiger = (minute_test * 12 + 2 * drehung) % 720
    zahl = stundenzeiger // 60
    if zahl == 0:
        zahl = 12
    return f"Um {drehung}° gedreht: {zahl} Uhr und {minutenzeiger // 12} Minuten"

# Ränder: Mitternacht 0:00 und eine Minute davor, 23:59
for stunde_test, minute_test in [(0, 0), (23, 59)]:
    uhrzeit_test = f"{stunde_test}:{minute_test:02d}"
    ausgabe = starte(uhrzeit_test)
    erwartet = abgelesen(stunde_test, minute_test, 180)
    assert erwartet in ausgabe.splitlines(), (
        f'Bei Eingabe {uhrzeit_test} erwartet die Zeile: "{erwartet}"\nIhr Programm:\n{ausgabe}'
    )

# 40 zufällige Uhrzeiten zwischen 0:00 und 23:59, um 180° gedreht
zufall = Zufall(1009)
for _ in range(40):
    stunde_test = zufall.randint(0, 23)
    minute_test = zufall.randint(0, 59)
    uhrzeit_test = f"{stunde_test}:{minute_test:02d}"
    ausgabe = starte(uhrzeit_test)
    erwartet = abgelesen(stunde_test, minute_test, 180)
    assert erwartet in ausgabe.splitlines(), (
        f'Bei Eingabe {uhrzeit_test} erwartet die Zeile: "{erwartet}"\nIhr Programm:\n{ausgabe}'
    )

# Zusatz: 40 zufällige Uhrzeiten, um 90° und um 270° gedreht
for _ in range(40):
    stunde_test = zufall.randint(0, 23)
    minute_test = zufall.randint(0, 59)
    uhrzeit_test = f"{stunde_test}:{minute_test:02d}"
    ausgabe = starte(uhrzeit_test)
    for drehung in [90, 270]:
        erwartet = abgelesen(stunde_test, minute_test, drehung)
        assert erwartet in ausgabe.splitlines(), (
            f'Zusatz: Bei Eingabe {uhrzeit_test} erwartet die Zeile: "{erwartet}"\nIhr Programm:\n{ausgabe}'
        )
