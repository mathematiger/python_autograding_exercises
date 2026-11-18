# Automatisch erzeugt aus lehrkraft/muster/2_043_kontrollsumme.py - nicht von Hand ändern.
# vorlage-hash: c04bef9a1f0b248d
# text-hash: a03536995a38709b
# thema: texte_zahlen
# inhalt: Kommazahlen vergleichen

def in_cent(betrag):
    """Rechnet einen Betrag mit höchstens zwei Nachkommastellen exakt in ganze Cent um."""
    return round(betrag * 100)


def summe_stimmt_von_hand(betraege, kontrollsumme):
    """Vergleichslösung: rechnet in ganzen Cent, da gibt es keine Rundungsfehler."""
    summe = 0
    for betrag in betraege:
        summe = summe + in_cent(betrag)
    return summe == in_cent(kontrollsumme)


# fast_gleich: 0.1 + 0.2 und 0.3 sind fast gleich
ergebnis = fast_gleich(0.1 + 0.2, 0.3)
if ergebnis is False:
    hinweis = "\nTipp: Vergleichen Sie nicht mit ==, sondern prüfen Sie, ob abs(a - b) < TOLERANZ ist."
else:
    hinweis = ""
assert ergebnis is True, f"fast_gleich(0.1 + 0.2, 0.3) ergibt {ergebnis!r}, erwartet war True.{hinweis}"

# fast_gleich: 19.99 und 20.0 unterscheiden sich um einen Cent
ergebnis = fast_gleich(19.99, 20.0)
assert ergebnis is False, (
    f"fast_gleich(19.99, 20.0) ergibt {ergebnis!r}, erwartet war False, denn ein Cent ist mehr als TOLERANZ.\n"
    "Tipp: Benutzen Sie die Konstante TOLERANZ (0.005), keine größere Zahl."
)

# fast_gleich: auch, wenn die erste Zahl größer ist
ergebnis = fast_gleich(20.0, 19.99)
assert ergebnis is False, (
    f"fast_gleich(20.0, 19.99) ergibt {ergebnis!r}, erwartet war False.\n"
    "Tipp: 19.99 - 20.0 ist negativ und damit immer kleiner als TOLERANZ. abs(a - b) liefert den Abstand "
    "ohne Vorzeichen."
)

# fast_gleich: gleiche Zahlen sind fast gleich
ergebnis = fast_gleich(42.0, 42.0)
assert ergebnis is True, f"fast_gleich(42.0, 42.0) ergibt {ergebnis!r}, erwartet war True."

# fast_gleich: knapp unter und knapp über der Toleranz
for a, b, erwartet in [(1.0, 1.004, True), (1.0, 1.006, False), (-3.0, -3.004, True), (-3.0, -2.994, False)]:
    ergebnis = fast_gleich(a, b)
    assert ergebnis is erwartet, f"fast_gleich({a}, {b}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# fast_gleich: ein Abstand von genau TOLERANZ ist nicht mehr „weniger als TOLERANZ“
ergebnis = fast_gleich(0.0, 0.005)
assert ergebnis is False, (
    f"fast_gleich(0.0, 0.005) ergibt {ergebnis!r}, erwartet war False, denn der Abstand ist genau TOLERANZ und "
    "nicht weniger.\nTipp: Vergleichen Sie mit <, nicht mit <=."
)

# summe_stimmt: das Beispiel mit 0.1 und 0.2
ergebnis = summe_stimmt([0.1, 0.2], 0.3)
assert ergebnis is True, (
    f"summe_stimmt([0.1, 0.2], 0.3) ergibt {ergebnis!r}, erwartet war True.\n"
    "Tipp: Vergleichen Sie die Summe mit fast_gleich, nicht mit ==."
)

# summe_stimmt: drei Beträge, die genau aufgehen
ergebnis = summe_stimmt([12.5, 7.49, 0.01], 20.0)
assert ergebnis is True, f"summe_stimmt([12.5, 7.49, 0.01], 20.0) ergibt {ergebnis!r}, erwartet war True."

# summe_stimmt: ein Cent fehlt
ergebnis = summe_stimmt([12.5, 7.49], 20.0)
assert ergebnis is False, (
    f"summe_stimmt([12.5, 7.49], 20.0) ergibt {ergebnis!r}, erwartet war False (ein Cent fehlt).\n"
    "Tipp: Ist die Summe kleiner als die Kontrollsumme, ist summe - kontrollsumme negativ; prüfen Sie den "
    "Abstand mit abs(...)."
)

# summe_stimmt: ein Cent zu viel
ergebnis = summe_stimmt([12.5, 7.49, 0.02], 20.0)
assert ergebnis is False, (
    f"summe_stimmt([12.5, 7.49, 0.02], 20.0) ergibt {ergebnis!r}, erwartet war False (ein Cent zu viel)."
)

# summe_stimmt: Gutschriften sind negativ
ergebnis = summe_stimmt([100.0, -0.7, -0.1, -0.2], 99.0)
assert ergebnis is True, f"summe_stimmt([100.0, -0.7, -0.1, -0.2], 99.0) ergibt {ergebnis!r}, erwartet war True."

# summe_stimmt: die leere Liste hat die Summe 0
ergebnis_null = summe_stimmt([], 0.0)
ergebnis_cent = summe_stimmt([], 0.01)
assert ergebnis_null is True and ergebnis_cent is False, (
    f"summe_stimmt([], 0.0) ergibt {ergebnis_null!r} (erwartet True), summe_stimmt([], 0.01) ergibt "
    f"{ergebnis_cent!r} (erwartet False)."
)

# summe_stimmt: zehnmal 0.1 sind 1.0, obwohl die Summe 0.9999999999999999 ist
ergebnis = summe_stimmt([0.1] * 10, 1.0)
assert ergebnis is True, f"summe_stimmt([0.1] * 10, 1.0) ergibt {ergebnis!r}, erwartet war True."

# summe_stimmt: viele zufällige Dateien, mit und ohne Abweichung
zufall = Zufall(2043)
for runde in range(300):
    cents = [zufall.randint(-10_000_000, 10_000_000) for _ in range(zufall.randint(0, 30))]
    betraege = [cent / 100 for cent in cents]
    abweichung = zufall.choice([0, 0, 0, 1, -1, 2, -3, 100])
    kontrollsumme = (sum(cents) + abweichung) / 100
    erwartet = summe_stimmt_von_hand(betraege, kontrollsumme)
    ergebnis = summe_stimmt(betraege, kontrollsumme)
    assert ergebnis is erwartet, f"summe_stimmt({betraege}, {kontrollsumme}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Obere Grenze: 10 000 Beträge bis 100 000 Euro, einmal passend und einmal mit einem Cent Abweichung
cents = [((nummer * 7919) % 20_000_001) - 10_000_000 for nummer in range(10_000)]
betraege = [cent / 100 for cent in cents]
passend = summe_stimmt(betraege, sum(cents) / 100)
daneben = summe_stimmt(betraege, (sum(cents) + 1) / 100)
assert passend is True and daneben is False, (
    f"Bei 10 000 Beträgen mit der Summe {sum(cents) / 100} ergibt summe_stimmt mit der richtigen Kontrollsumme "
    f"{passend!r} (erwartet True) und mit einem Cent mehr {daneben!r} (erwartet False)."
)

# Die Ausgabe des Programms stimmt
assert vergleichbar(AUSGABE) == vergleichbar("False True False"), (
    f'Erwartete Ausgabe: "False True False" – Ihr Programm: "{AUSGABE}"'
)
