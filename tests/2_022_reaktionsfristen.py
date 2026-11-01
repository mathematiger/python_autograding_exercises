# Automatisch erzeugt aus lehrkraft/muster/2_022_reaktionsfristen.py - nicht von Hand ändern.
# vorlage-hash: 40c08c751400d282
# text-hash: 1903f6a9a26dc967
# thema: kontrollfluss
# inhalt: zip

nummern = ["T-101", "T-102", "T-103", "T-104"]
fristen = [60, 240, 60, 30]
reaktionen = [45, 300, 60, 31]

# verletzte_tickets aus dem Beispiel; genau zur Frist ist rechtzeitig
ergebnis = verletzte_tickets(nummern, fristen, reaktionen)
assert ergebnis == ["T-102", "T-104"], (
    f"verletzte_tickets(...) ergibt für das Beispiel {ergebnis!r}, erwartet war ['T-102', 'T-104'].\n"
    "Tipp: T-103 wurde nach genau 60 Minuten beantwortet, das ist noch rechtzeitig: verletzt ist nur reaktion > frist."
)

# Andere Tickets (nicht fest hinschreiben!)
for liste_n, liste_f, liste_r, erwartet in [
    (["A", "B", "C"], [10, 20, 30], [11, 19, 31], ["A", "C"]),
    (["A", "B", "C"], [10, 20, 30], [0, 20, 30], []),
    (["X"], [1], [100000], ["X"]),
    (["Z", "Y"], [10000, 5], [10000, 6], ["Y"]),
]:
    ergebnis = verletzte_tickets(liste_n, liste_f, liste_r)
    assert ergebnis == erwartet, (
        f"verletzte_tickets({liste_n}, {liste_f}, {liste_r}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Vergleichen Sie Frist und Reaktionszeit desselben Tickets; zip(nummern, fristen, reaktionen) liefert sie zusammen."
    )

# Keine Tickets
ergebnis = verletzte_tickets([], [], [])
assert ergebnis == [], f"verletzte_tickets([], [], []) ergibt {ergebnis!r}, erwartet war []."

# einhaltungsquote aus dem Beispiel
ergebnis = einhaltungsquote(fristen, reaktionen)
assert ergebnis == 50, f"einhaltungsquote({fristen}, {reaktionen}) ergibt {ergebnis!r}, erwartet war 50."

# Abgerundet, alle und keins eingehalten
for liste_f, liste_r, erwartet in [
    ([60, 60, 60], [1, 2, 99], 66),
    ([60, 60, 60], [99, 99, 1], 33),
    ([5, 5], [5, 0], 100),
    ([5, 5], [6, 7], 0),
    ([1], [1], 100),
    ([10] * 7, [1, 1, 1, 1, 1, 1, 11], 85),
]:
    ergebnis = einhaltungsquote(liste_f, liste_r)
    assert ergebnis == erwartet and type(ergebnis) is int, (
        f"einhaltungsquote({liste_f}, {liste_r}) ergibt {ergebnis!r}, erwartet war die ganze Zahl {erwartet}.\n"
        "Tipp: Rechnen Sie eingehalten * 100 // anzahl; // rundet ab und liefert eine ganze Zahl."
    )

# Ohne Tickets None
ergebnis = einhaltungsquote([], [])
assert ergebnis is None, (
    f"einhaltungsquote([], []) ergibt {ergebnis!r}, erwartet war None.\n"
    "Tipp: Prüfen Sie zuerst, ob es überhaupt Tickets gibt; sonst teilen Sie durch 0."
)

# Die Listen bleiben unverändert
liste_n, liste_f, liste_r = ["A", "B"], [10, 20], [30, 5]
verletzte_tickets(liste_n, liste_f, liste_r)
einhaltungsquote(liste_f, liste_r)
assert (liste_n, liste_f, liste_r) == (["A", "B"], [10, 20], [30, 5]), (
    f"Nach den Auswertungen sind die Listen {liste_n}, {liste_f} und {liste_r}; sie sollen unverändert bleiben."
)

# zip wird benutzt
assert verwendet("zip"), "Benutzen Sie zip(...), um die Listen gemeinsam zu durchlaufen."


# Vergleichslösung: über die Indizes
def verletzt_von_hand(liste_n, liste_f, liste_r):
    """Geht die Indizes durch und sammelt die Nummern zu später Tickets."""
    return [liste_n[i] for i in range(len(liste_n)) if liste_r[i] > liste_f[i]]


def quote_von_hand(liste_f, liste_r):
    """Zählt die rechtzeitigen Tickets über die Indizes und rechnet die abgerundete Quote."""
    if not liste_f:
        return None
    rechtzeitig = len([i for i in range(len(liste_f)) if liste_r[i] <= liste_f[i]])
    return (rechtzeitig * 100) // len(liste_f)


# 300 zufällige Monatsberichte
zufall = Zufall(2022)
for _ in range(300):
    anzahl = zufall.randint(0, 8)
    liste_n = [f"T-{nummer}" for nummer in zufall.sample(range(1000), anzahl)]
    liste_f = [zufall.choice([zufall.randint(1, 20), zufall.randint(1, 10000)]) for _ in range(anzahl)]
    liste_r = [zufall.choice([frist, frist + 1, zufall.randint(0, 25), zufall.randint(0, 100000)]) for frist in liste_f]
    ergebnis = verletzte_tickets(liste_n, liste_f, liste_r)
    erwartet = verletzt_von_hand(liste_n, liste_f, liste_r)
    assert ergebnis == erwartet, (
        f"verletzte_tickets({liste_n}, {liste_f}, {liste_r}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    )
    ergebnis = einhaltungsquote(liste_f, liste_r)
    erwartet = quote_von_hand(liste_f, liste_r)
    assert ergebnis == erwartet, f"einhaltungsquote({liste_f}, {liste_r}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# An der oberen Grenze: 100 000 Tickets
gross_n = [f"T-{nummer:06d}" for nummer in range(100000)]
gross_f = [(nummer * 37) % 10000 + 1 for nummer in range(100000)]
gross_r = [(nummer * 53) % 100001 for nummer in range(100000)]
ergebnis_verletzt = verletzte_tickets(gross_n, gross_f, gross_r)
ergebnis_quote = einhaltungsquote(gross_f, gross_r)
erwartet_verletzt = verletzt_von_hand(gross_n, gross_f, gross_r)
erwartet_quote = quote_von_hand(gross_f, gross_r)
assert ergebnis_verletzt == erwartet_verletzt and ergebnis_quote == erwartet_quote, (
    f"Bei 100 000 Tickets ergibt verletzte_tickets {len(ergebnis_verletzt)} Nummern und einhaltungsquote "
    f"{ergebnis_quote!r}; erwartet waren {len(erwartet_verletzt)} Nummern und {erwartet_quote}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "['T-102', 'T-104']\n50"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
