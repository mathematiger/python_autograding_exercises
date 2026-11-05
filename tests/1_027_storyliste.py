# Automatisch erzeugt aus lehrkraft/muster/1_027_storyliste.py - nicht von Hand ändern.
# vorlage-hash: e97c80c02c82ae33
# text-hash: 1a46034b9408c42e
# thema: datenstrukturen
# inhalt: Listen anlegen und lesen

EINGABEN = ["2"]

STORIES = ["Login-Seite", "Passwort vergessen", "Profilbild", "Suche", "Export als PDF"]


def erwartet_bei(platz):
    """Baut die erwartete Ausgabe für einen Platz von 1 bis 5."""
    return f"Platz {platz} von 5: {STORIES[platz - 1]}"


def hinweis_zu(ausgabe, platz):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    if platz < 5 and ausgabe.endswith(STORIES[platz]):
        return "\nTipp: Der Index beginnt bei 0; die Story auf Platz 2 ist stories[1], also stories[platz - 1]."
    return ""


# Die Liste stories enthält die fünf Stories in der richtigen Reihenfolge
assert stories == STORIES, (
    f"stories ist {stories!r}, erwartet war die Liste {STORIES!r}.\n"
    "Tipp: Schreiben Sie die Texte in Anführungszeichen, durch Kommas getrennt, in eckige Klammern."
)

# Bei Eingabe 2 kommt "Passwort vergessen" heraus
assert AUSGABE == erwartet_bei(2), (
    f'Bei Eingabe 2 erwartet: "{erwartet_bei(2)}" – Ihr Programm: "{AUSGABE}"{hinweis_zu(AUSGABE, 2)}'
)

# Platz 1 ist die erste Story der Liste (nicht fest hinschreiben!)
ausgabe = starte("1")
assert ausgabe == erwartet_bei(1), (
    f'Bei Eingabe 1 erwartet: "{erwartet_bei(1)}" – Ihr Programm: "{ausgabe}"{hinweis_zu(ausgabe, 1)}'
)

# Platz 5 ist die letzte Story der Liste
try:
    ausgabe = starte("5")
    hinweis = ""
except Exception as fehler:
    # stories[5] gibt es nicht: der Abbruch soll den passenden Tipp bekommen
    ausgabe = f"(Abbruch: {fehler})"
    hinweis = "\nTipp: Bei fünf Stories ist der letzte Index 4. Ziehen Sie vom Platz 1 ab: stories[platz - 1]."
assert ausgabe == erwartet_bei(5), f'Bei Eingabe 5 erwartet: "{erwartet_bei(5)}" – Ihr Programm: "{ausgabe}"{hinweis}'

# Die Anzahl kommt aus len, nicht aus einer fest hingeschriebenen 5
assert verwendet("len"), "Bestimmen Sie die Anzahl der Stories mit len(stories), statt 5 hinzuschreiben."

# Alle Plätze von 1 bis 5 in zufälliger Reihenfolge, auch mehrfach
zufall = Zufall(1027)
for _ in range(20):
    platz = zufall.randint(1, 5)
    ausgabe = starte(str(platz))
    assert ausgabe == erwartet_bei(platz), (
        f'Bei Eingabe {platz} erwartet: "{erwartet_bei(platz)}" – Ihr Programm: "{ausgabe}"{hinweis_zu(ausgabe, platz)}'
    )
