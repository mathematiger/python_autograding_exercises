# Automatisch erzeugt aus lehrkraft/muster/3_026_verteiler.py - nicht von Hand ändern.
# vorlage-hash: 347c2871730b24a2
# text-hash: 54eef5c657fb1020
# thema: funktionen
# inhalt: map und filter

def art(wert):
    """Beschreibt den Typ eines Ergebnisses für die Fehlermeldung."""
    if isinstance(wert, (map, filter)):
        return f"ein {type(wert).__name__}-Objekt statt einer Liste (machen Sie mit list(...) eine Liste daraus)"
    return repr(wert)


# bereinige aus dem Beispiel
eingabe = ["  Ada@Firma.de", "", "ben@web.de ", "   ", "CEM@mail"]
ergebnis = bereinige(eingabe)
erwartet = ["ada@firma.de", "ben@web.de", "cem@mail"]
assert ergebnis == erwartet, (
    f"bereinige({eingabe}) ergibt {art(ergebnis)}, erwartet war {erwartet!r}.\n"
    "Tipp: Erst mit map jeden Eintrag strip() und lower() bearbeiten, dann mit filter die leeren entfernen."
)

# ungueltige aus dem Beispiel
ergebnis = ungueltige(["ada@firma.de", "ben@web.de", "cem@mail"])
assert ergebnis == ["cem@mail"], (
    f'ungueltige(["ada@firma.de", "ben@web.de", "cem@mail"]) ergibt {art(ergebnis)}, erwartet war ["cem@mail"].\n'
    "Tipp: filter behält die Elemente, für die die Funktion True liefert; Sie wollen die, für die ist_gueltig "
    "False liefert."
)

# domains aus dem Beispiel
ergebnis = domains(["ada@firma.de", "ben@web.de"])
assert ergebnis == ["firma.de", "web.de"], (
    f'domains(["ada@firma.de", "ben@web.de"]) ergibt {art(ergebnis)}, erwartet war ["firma.de", "web.de"].\n'
    'Tipp: adresse.split("@") liefert eine Liste mit zwei Teilen; die Domain ist der zweite.'
)

# Leerzeichen in der Mitte bleiben, nur der Rand wird entfernt
eingabe = [" a b@c.de ", "X@Y.Z"]
ergebnis = bereinige(eingabe)
assert ergebnis == ["a b@c.de", "x@y.z"], (
    f"bereinige({eingabe}) ergibt {art(ergebnis)}, erwartet war ['a b@c.de', 'x@y.z'].\n"
    'Tipp: strip() entfernt nur Leerzeichen am Rand; replace(" ", "") würde auch die in der Mitte entfernen.'
)

# Nur leere Einträge und leere Listen
ergebnis = (bereinige(["", "  ", "     "]), bereinige([]), ungueltige([]), domains([]))
assert ergebnis == ([], [], [], []), (
    f'bereinige(["", "  ", "     "]), bereinige([]), ungueltige([]) und domains([]) ergeben '
    f"{', '.join(art(wert) for wert in ergebnis)}, "
    "erwartet war ([], [], [], [])."
)

# Alle Adressen sind ungültig, die Reihenfolge bleibt
adressen = ["@firma.de", "a@b", "a@.de", "a@b.", "a@@b.de", "ab.de"]
ergebnis = ungueltige(adressen)
assert ergebnis == adressen, f"ungueltige({adressen}) ergibt {art(ergebnis)}, erwartet war {adressen!r} (alle ungültig)."

# Keine Adresse ist ungültig
adressen = ["z@x.de", "a@b.c", "m.n@o.p.q"]
ergebnis = ungueltige(adressen)
assert ergebnis == [], f"ungueltige({adressen}) ergibt {art(ergebnis)}, erwartet war [] (alle gültig)."

# Doppelte Einträge bleiben doppelt
eingabe = ["a@b.de", " A@B.DE", "a@b.de"]
ergebnis = (bereinige(eingabe), domains(["a@b.de", "c@b.de"]))
erwartet = (["a@b.de", "a@b.de", "a@b.de"], ["b.de", "b.de"])
assert ergebnis == erwartet, (
    f"bereinige({eingabe}) und domains(['a@b.de', 'c@b.de']) ergeben {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Doppelte werden nicht entfernt; eine Menge würde außerdem die Reihenfolge durcheinanderbringen."
)

# Die übergebene Liste bleibt unverändert
eingabe = [" X@y.de", ""]
bereinige(eingabe)
assert eingabe == [" X@y.de", ""], f"Nach bereinige(...) ist die Eingabe {eingabe!r}, erwartet war unverändert."

# map wird benutzt
assert verwendet("map"), "Benutzen Sie map, um jeden Eintrag zu bearbeiten (in bereinige und domains)."

# filter wird benutzt
assert verwendet("filter"), "Benutzen Sie filter, um Einträge auszuwählen (in bereinige und ungueltige)."


# Vergleichslösungen mit Schleifen
def bereinige_von_hand(eintraege):
    """Bereinigt mit einer Schleife."""
    ergebnis = []
    for eintrag in eintraege:
        sauber = eintrag.strip().lower()
        if sauber:
            ergebnis.append(sauber)
    return ergebnis


def domain_von_hand(adresse):
    """Sucht das @ von hinten."""
    stelle = len(adresse) - 1
    while adresse[stelle] != "@":
        stelle -= 1
    return adresse[stelle + 1 :]


# 300 zufällige Formulare
zufall = Zufall(3026)
ZEICHEN = "abcxyzABCXYZ019.-_@"
for _ in range(300):
    eintraege = []
    for _ in range(zufall.randint(0, 10)):
        kern = "".join(zufall.choice(ZEICHEN) for _ in range(zufall.randint(0, 12)))
        eintraege.append(" " * zufall.randint(0, 3) + kern + " " * zufall.randint(0, 3))
    vorher = list(eintraege)
    ergebnis = bereinige(eintraege)
    erwartet = bereinige_von_hand(vorher)
    assert ergebnis == erwartet, f"bereinige({vorher}) ergibt {art(ergebnis)}, erwartet war {erwartet!r}."
    ergebnis = ungueltige(erwartet)
    erwartet_ungueltig = [adresse for adresse in erwartet if not ist_gueltig(adresse)]
    assert ergebnis == erwartet_ungueltig, (
        f"ungueltige({erwartet}) ergibt {art(ergebnis)}, erwartet war {erwartet_ungueltig!r}."
    )
    gueltig = [adresse for adresse in erwartet if ist_gueltig(adresse)]
    ergebnis = domains(gueltig)
    erwartet_domains = [domain_von_hand(adresse) for adresse in gueltig]
    assert ergebnis == erwartet_domains, f"domains({gueltig}) ergibt {art(ergebnis)}, erwartet war {erwartet_domains!r}."

# Obere Grenze: 100 000 Einträge, jeder dritte leer
eintraege = []
for nummer in range(100000):
    if nummer % 3 == 0:
        eintraege.append("   ")
    else:
        eintraege.append(f" Kunde{nummer}@Firma{nummer % 10}.de ")
ergebnis = bereinige(eintraege)
erwartet = bereinige_von_hand(eintraege)
assert ergebnis == erwartet, (
    f"bereinige mit 100 000 Einträgen liefert {len(ergebnis) if isinstance(ergebnis, list) else art(ergebnis)} "
    f"Adressen, erwartet waren {len(erwartet)}, beginnend mit {erwartet[:2]}."
)

# Obere Grenze: ungueltige und domains mit 66 666 Adressen
ergebnis = (ungueltige(erwartet), domains(erwartet)[-1:])
assert ergebnis == ([], ["firma8.de"]), (
    f"Für die 66 666 bereinigten Adressen ergeben ungueltige(...) und domains(...)[-1:] {ergebnis!r}, "
    "erwartet war ([], ['firma8.de'])."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "['ada@firma.de', 'ben@web.de', 'cem@mail']\n['cem@mail']\n['firma.de', 'web.de']"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
