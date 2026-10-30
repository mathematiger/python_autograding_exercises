# Automatisch erzeugt aus lehrkraft/muster/2_018_abfrageseiten.py - nicht von Hand ändern.
# vorlage-hash: 66167ff9747a4ee4
# text-hash: 991dc0ae7e6970b0
# thema: datenstrukturen
# inhalt: Slicing und Kopien von Listen

namen = ["Abel", "Bauer", "Celik", "Dorn", "Ernst"]

# Die erste Seite
ergebnis = seite(namen, 1, 2)
assert ergebnis == ["Abel", "Bauer"], f"seite({namen}, 1, 2) ergibt {ergebnis!r}, erwartet war ['Abel', 'Bauer']."

# Weitere Seiten (nicht fest hinschreiben!)
for nummer, groesse, erwartet in [(2, 2, ["Celik", "Dorn"]), (2, 3, ["Dorn", "Ernst"]), (1, 5, namen)]:
    ergebnis = seite(namen, nummer, groesse)
    assert ergebnis == erwartet, (
        f"seite({namen}, {nummer}, {groesse}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Seite nummer beginnt beim Index (nummer - 1) * groesse."
    )

# Die letzte Seite ist kürzer, dahinter kommt nichts mehr
for nummer, groesse, erwartet in [(3, 2, ["Ernst"]), (4, 2, []), (1000000, 1000, [])]:
    try:
        ergebnis = seite(namen, nummer, groesse)
    except IndexError as fehler:
        ergebnis = fehler
    assert ergebnis == erwartet, (
        f"seite({namen}, {nummer}, {groesse}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Ein Slice wie liste[4:6] darf über das Ende hinausreichen."
    )

# Eine leere Abfrage hat nur leere Seiten
ergebnis = seite([], 1, 10)
assert ergebnis == [], f"seite([], 1, 10) ergibt {ergebnis!r}, erwartet war []."

# Die Seite ist eine neue Liste
alle = ["a", "b", "c"]
ergebnis = seite(alle, 1, 3)
assert ergebnis == alle and ergebnis is not alle, (
    'seite(["a", "b", "c"], 1, 3) soll eine neue Liste mit denselben Namen zurückgeben, nicht die Liste selbst.'
)

# mit_korrektur aus dem Beispiel
namen = ["Abel", "Bauer", "Celik", "Dorn", "Ernst"]
ergebnis = mit_korrektur(namen, 2, "Çelik")
erwartet = ["Abel", "Bauer", "Çelik", "Dorn", "Ernst"]
assert ergebnis == erwartet, f'mit_korrektur({namen}, 2, "Çelik") ergibt {ergebnis!r}, erwartet war {erwartet}.'

# Die ursprüngliche Liste bleibt unverändert
namen = ["Abel", "Bauer", "Celik", "Dorn", "Ernst"]
ergebnis = mit_korrektur(namen, 2, "Çelik")
assert namen == ["Abel", "Bauer", "Celik", "Dorn", "Ernst"] and ergebnis is not namen, (
    f'Nach mit_korrektur(namen, 2, "Çelik") ist namen {namen!r}, erwartet war weiterhin '
    "['Abel', 'Bauer', 'Celik', 'Dorn', 'Ernst'].\n"
    "Tipp: kopie = werte gibt derselben Liste nur einen zweiten Namen. Mit werte[:] bekommen Sie eine neue Liste."
)

# Korrektur am Anfang, am Ende und in einer Liste mit nur einem Namen
for werte, index, neu, erwartet in [
    (["x", "y", "z"], 0, "X", ["X", "y", "z"]),
    (["x", "y", "z"], 2, "Z", ["x", "y", "Z"]),
    (["x"], 0, "", [""]),
]:
    vorher = list(werte)
    ergebnis = mit_korrektur(werte, index, neu)
    assert ergebnis == erwartet and werte == vorher, (
        f"mit_korrektur({vorher}, {index}, {neu!r}) ergibt {ergebnis!r}, erwartet war {erwartet}; "
        f"die Liste ist danach {werte!r}, erwartet war sie unverändert {vorher}."
    )

# Zwei Vorschauen nacheinander sind voneinander unabhängig
namen = ["Abel", "Bauer"]
erste = mit_korrektur(namen, 0, "Adler")
zweite = mit_korrektur(namen, 1, "Brandt")
assert (erste, zweite, namen) == (["Adler", "Bauer"], ["Abel", "Brandt"], ["Abel", "Bauer"]), (
    f"Nach erste = mit_korrektur(namen, 0, 'Adler') und zweite = mit_korrektur(namen, 1, 'Brandt') mit "
    f"namen = ['Abel', 'Bauer'] sind erste, zweite und namen {erste!r}, {zweite!r}, {namen!r}; "
    "erwartet waren ['Adler', 'Bauer'], ['Abel', 'Brandt'] und ['Abel', 'Bauer']."
)


# Vergleichslösung: Seite mit einer Schleife über alle Indizes
def seite_von_hand(ergebnisse, nummer, groesse):
    """Sammelt alle Einträge, deren Index auf die Seite nummer fällt."""
    gefunden = []
    for index in range(len(ergebnisse)):
        if index // groesse + 1 == nummer:
            gefunden.append(ergebnisse[index])
    return gefunden


# 500 zufällige Abfragen
zufall = Zufall(2018)
for _ in range(500):
    werte = [zufall.choice(["Abel", "Bauer", "Celik", "Dorn", "Ernst", "Fuchs"]) for _ in range(zufall.randint(0, 30))]
    groesse = zufall.randint(1, 8)
    nummer = zufall.randint(1, 8)
    erwartet = seite_von_hand(werte, nummer, groesse)
    ergebnis = seite(werte, nummer, groesse)
    assert ergebnis == erwartet, f"seite({werte}, {nummer}, {groesse}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    if werte:
        vorher = list(werte)
        index = zufall.randrange(len(werte))
        erwartet = vorher[:index] + ["Neu"] + vorher[index + 1 :]
        ergebnis = mit_korrektur(werte, index, "Neu")
        assert ergebnis == erwartet and werte == vorher, (
            f'mit_korrektur({vorher}, {index}, "Neu") ergibt {ergebnis!r}, erwartet war {erwartet}; '
            f"die Liste ist danach {werte!r}, erwartet war sie unverändert."
        )

# An der oberen Grenze: 100 000 Namen, 1000 pro Seite
gross = [f"Kunde {nummer}" for nummer in range(100000)]
for nummer, erwartet_erster, erwartet_anzahl in [(1, "Kunde 0", 1000), (100, "Kunde 99000", 1000), (101, None, 0)]:
    ergebnis = seite(gross, nummer, 1000)
    erster = ergebnis[0] if ergebnis else None
    assert (erster, len(ergebnis)) == (erwartet_erster, erwartet_anzahl), (
        f"Bei 100 000 Namen und 1000 pro Seite ergibt seite(…, {nummer}, 1000) {len(ergebnis)} Einträge, "
        f"der erste {erster!r}; erwartet waren {erwartet_anzahl} Einträge, der erste {erwartet_erster!r}."
    )
ergebnis = mit_korrektur(gross, 99999, "Letzte")
assert ergebnis[-1] == "Letzte" and gross[-1] == "Kunde 99999" and len(ergebnis) == 100000, (
    "mit_korrektur bei 100 000 Namen und index 99999 soll eine neue Liste mit 'Letzte' am Ende liefern und "
    f"die alte unverändert lassen; neues Ende {ergebnis[-1]!r}, altes Ende {gross[-1]!r}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "['Ernst']\n"
    "['Abel', 'Bauer', 'Çelik', 'Dorn', 'Ernst']\n"
    "['Abel', 'Bauer', 'Celik', 'Dorn', 'Ernst']"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
