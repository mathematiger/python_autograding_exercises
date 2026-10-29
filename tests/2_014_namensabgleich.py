# Automatisch erzeugt aus lehrkraft/muster/2_014_namensabgleich.py - nicht von Hand ändern.
# vorlage-hash: d8e172057553226a
# thema: texte_zahlen
# inhalt: `split` und `join`

# Das Beispiel aus der Aufgabe
ergebnis = neue_schreibweise("Anna Maria Schulz")
assert ergebnis == "Schulz, Anna Maria", (
    f'neue_schreibweise("Anna Maria Schulz") ergibt {ergebnis!r}, erwartet war "Schulz, Anna Maria".'
)

# Weitere Namen (nicht fest hinschreiben!)
for name, erwartet in [
    ("Jonas Weber", "Weber, Jonas"),
    ("Leyla Nur Demir-Kaya", "Demir-Kaya, Leyla Nur"),
    ("Hans Peter Josef Müller", "Müller, Hans Peter Josef"),
]:
    ergebnis = neue_schreibweise(name)
    assert ergebnis == erwartet, f"neue_schreibweise({name!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Überflüssige Leerzeichen fallen weg, auch am Rand
for name, erwartet in [
    ("  Jonas    Weber ", "Weber, Jonas"),
    ("Anna   Maria  Schulz", "Schulz, Anna Maria"),
    ("   Jörg Groß   ", "Groß, Jörg"),
]:
    ergebnis = neue_schreibweise(name)
    if "  " in ergebnis or ergebnis.startswith(",") or ergebnis.endswith(" "):
        hinweis = '\nTipp: name.split() ohne Argument übergeht mehrere Leerzeichen; name.split(" ") dagegen nicht.'
    else:
        hinweis = ""
    assert ergebnis == erwartet, f"neue_schreibweise({name!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.{hinweis}"

# Ein einzelnes Wort bleibt allein, ohne Komma
for name, erwartet in [("Cher", "Cher"), ("  Prince ", "Prince")]:
    ergebnis = neue_schreibweise(name)
    assert ergebnis == erwartet, (
        f"neue_schreibweise({name!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
        "Tipp: Bei nur einem Wort gibt es keine Vornamen und darum auch kein Komma."
    )

# Ohne Wörter kommt ein leerer Text heraus
for name in ["", "   "]:
    try:
        ergebnis = neue_schreibweise(name)
    except IndexError as fehler:
        ergebnis = fehler
    assert ergebnis == "", (
        f"neue_schreibweise({name!r}) ergibt {ergebnis!r}, erwartet war der leere Text.\n"
        "Tipp: Bei einem Namen ohne Wörter ist die Liste von split leer; dann gibt es kein woerter[-1]."
    )

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "'Anna Maria Schulz' → 'Schulz, Anna Maria'\n"
    "'  Jonas    Weber ' → 'Weber, Jonas'\n"
    "'Cher' → 'Cher'"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"


# Vergleichslösung ohne split und join: Zeichen für Zeichen Wörter sammeln
def schreibweise_von_hand(name):
    """Zerlegt name Zeichen für Zeichen in Wörter und setzt sie neu zusammen."""
    woerter = []
    wort = ""
    for zeichen in name + " ":
        if zeichen == " ":
            if wort != "":
                woerter.append(wort)
            wort = ""
        else:
            wort = wort + zeichen
    if len(woerter) <= 1:
        return "".join(woerter)
    vornamen = woerter[0]
    for vorname in woerter[1:-1]:
        vornamen = vornamen + " " + vorname
    return woerter[-1] + ", " + vornamen


# 500 zufällige Namen mit 0 bis 6 Wörtern und zufälligen Leerzeichen
zufall = Zufall(2014)
silben = ["an", "na", "jo", "nas", "ma", "ri", "a", "schul", "z", "we", "ber", "kö", "nig", "groß", "-"]
for _ in range(500):
    name = " " * zufall.randint(0, 3)
    for _ in range(zufall.randint(0, 6)):
        wort = zufall.choice(silben).capitalize()
        for _ in range(zufall.randint(0, 2)):
            wort = wort + zufall.choice(silben)
        name = name + wort + " " * zufall.randint(1, 3)
    if zufall.random() < 0.5:
        name = name.rstrip(" ")
    erwartet = schreibweise_von_hand(name)
    ergebnis = neue_schreibweise(name)
    assert ergebnis == erwartet, f"neue_schreibweise({name!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# An der oberen Grenze: 1000 Zeichen
for name, erwartet in [
    ("Ab " * 333 + "C", "C, " + " ".join(["Ab"] * 333)),
    (" " * 1000, ""),
    ("x" * 1000, "x" * 1000),
    (" " * 994 + "Bo Li", "Li, Bo"),
]:
    ergebnis = neue_schreibweise(name)
    assert ergebnis == erwartet, (
        f"Bei einem Namen aus 1000 Zeichen, der mit {name[:8]!r} beginnt und mit {name[-8:]!r} endet, "
        f"ergibt neue_schreibweise {ergebnis[:40]!r}…, erwartet war {erwartet[:40]!r}…"
    )
