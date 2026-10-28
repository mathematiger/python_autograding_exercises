# Automatisch erzeugt aus lehrkraft/muster/2_011_aufwand.py - nicht von Hand ändern.
# vorlage-hash: a42c5a7bdd7808ea
# thema: funktionen
# inhalt: Schlüsselwort-Argumente

# Das Beispiel aus der Aufgabe: zu dritt
ergebnis = aufwand_im_team(10, 3)
assert ergebnis == 3.0, f"aufwand_im_team(10, 3) ergibt {ergebnis!r}, erwartet war 3.0."

# Weitere Teams (nicht fest hinschreiben!)
for story_points, personen, erwartet in [(8, 2, 3.6), (13, 4, 2.9), (10, 1, 9.0), (20, 5, 3.6)]:
    ergebnis = aufwand_im_team(story_points, personen)
    assert ergebnis == erwartet, (
        f"aufwand_im_team({story_points}, {personen}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Geben Sie personen beim Aufruf von aufwand mit Namen an: aufwand(story_points, personen=personen)."
    )

# Das Beispiel aus der Aufgabe: ohne Puffer
ergebnis = aufwand_ohne_puffer(10)
assert ergebnis == 7.5, f"aufwand_ohne_puffer(10) ergibt {ergebnis!r}, erwartet war 7.5."

# Weitere Einträge ohne Puffer
for story_points, erwartet in [(8, 6.0), (13, 9.8), (1, 0.8), (0, 0.0)]:
    ergebnis = aufwand_ohne_puffer(story_points)
    assert ergebnis == erwartet, (
        f"aufwand_ohne_puffer({story_points}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Ohne Puffer heißt puffer=0. Die anderen Werte bleiben die Standardwerte."
    )

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "Allein mit Puffer: 9.0 Tage\nZu dritt: 3.0 Tage\nOhne Puffer: 7.5 Tage"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"

# Die Kollegin ändert ihre Standardwerte: 5 Stunden pro Story Point, 50 Prozent Puffer
aufwand_alt = aufwand


def aufwand(story_points, stunden_pro_punkt=5, puffer=0.5, personen=1):
    """Neue Fassung der Kollegin mit anderen Standardwerten."""
    stunden = story_points * stunden_pro_punkt * (1 + puffer)
    return round(stunden / (8 * personen), 1)


# Ihre Funktionen benutzen die neuen Standardwerte von aufwand
for aufruf, ergebnis, erwartet in [
    ("aufwand_im_team(8, 2)", aufwand_im_team(8, 2), 3.8),
    ("aufwand_im_team(13, 4)", aufwand_im_team(13, 4), 3.0),
    ("aufwand_ohne_puffer(10)", aufwand_ohne_puffer(10), 6.2),
]:
    assert ergebnis == erwartet, (
        f"Mit den neuen Standardwerten der Kollegin ergibt {aufruf} {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Schreiben Sie die Standardwerte nicht ab. Geben Sie beim Aufruf von aufwand nur den Wert an, "
        "der sich ändert, und zwar mit seinem Namen."
    )

aufwand = aufwand_alt
