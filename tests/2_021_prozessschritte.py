# Automatisch erzeugt aus lehrkraft/muster/2_021_prozessschritte.py - nicht von Hand ändern.
# vorlage-hash: 08ce1c27a62faef7
# text-hash: f16027511e2687de
# thema: kontrollfluss
# inhalt: enumerate

dauern = [4, 12, 35, 8, 35]

# zu_lange aus dem Beispiel
ergebnis = zu_lange(dauern, 10)
assert ergebnis == [2, 3, 5], (
    f"zu_lange({dauern}, 10) ergibt {ergebnis!r}, erwartet war [2, 3, 5].\n"
    "Tipp: Die Schritte sind ab 1 nummeriert; enumerate(dauern, start=1) zählt so."
)

# Andere Sollwerte (nicht fest hinschreiben!); genau soll ist nicht zu lang
for soll, erwartet in [(35, []), (34, [3, 5]), (12, [3, 5]), (11, [2, 3, 5]), (1, [1, 2, 3, 4, 5])]:
    ergebnis = zu_lange(dauern, soll)
    assert ergebnis == erwartet, (
        f"zu_lange({dauern}, {soll}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Zu lang ist nur, was länger als soll dauert, nicht genau soll."
    )

# zu_lange mit leerer Liste und mit einem Schritt
for liste, soll, erwartet in [([], 5, []), ([7], 6, [1]), ([7], 7, [])]:
    ergebnis = zu_lange(liste, soll)
    assert ergebnis == erwartet, f"zu_lange({liste}, {soll}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# engpass aus dem Beispiel: bei zwei gleich langen Schritten zählt der erste
ergebnis = engpass(dauern)
assert ergebnis == 3, (
    f"engpass({dauern}) ergibt {ergebnis!r}, erwartet war 3.\n"
    "Tipp: Schritt 3 und Schritt 5 dauern beide 35 Minuten; ersetzen Sie den bisher besten nur bei echt größerer Dauer."
)

# engpass an anderen Stellen: am Anfang, am Ende, nur ein Schritt
for liste, erwartet in [([50, 3, 3], 1), ([1, 2, 3, 4], 4), ([9], 1), ([5, 5, 5], 1), ([1, 10**6, 10**6], 2)]:
    ergebnis = engpass(liste)
    assert ergebnis == erwartet, (
        f"engpass({liste}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Die Nummer zählt ab 1; der erste Schritt hat die Nummer 1."
    )

# engpass bei leerer Liste
ergebnis = engpass([])
assert ergebnis is None, f"engpass([]) ergibt {ergebnis!r}, erwartet war None."

# Die Liste bleibt unverändert
liste = [3, 1, 2]
zu_lange(liste, 1)
engpass(liste)
assert liste == [3, 1, 2], f"Nach zu_lange und engpass ist die Liste {liste!r}, sie soll unverändert [3, 1, 2] sein."

# enumerate wird benutzt
assert verwendet("enumerate"), "Benutzen Sie enumerate(...), um Nummer und Dauer zugleich zu bekommen."


# Vergleichslösungen: über die Indizes mit while
def zu_lange_von_hand(liste, soll):
    """Geht die Indizes mit while durch und sammelt index + 1 bei zu langen Schritten."""
    gefunden = []
    index = 0
    while index < len(liste):
        if liste[index] > soll:
            gefunden.append(index + 1)
        index = index + 1
    return gefunden


def engpass_von_hand(liste):
    """Sucht die größte Dauer mit max und dann ihre erste Position mit index."""
    if len(liste) == 0:
        return None
    return liste.index(max(liste)) + 1


# 300 zufällige Prozesse
zufall = Zufall(2021)
for _ in range(300):
    liste = [zufall.choice([zufall.randint(1, 10), zufall.randint(1, 10**6)]) for _ in range(zufall.randint(0, 8))]
    soll = zufall.choice([zufall.randint(1, 10), zufall.randint(1, 10**6)])
    ergebnis = zu_lange(liste, soll)
    erwartet = zu_lange_von_hand(liste, soll)
    assert ergebnis == erwartet, f"zu_lange({liste}, {soll}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    ergebnis = engpass(liste)
    erwartet = engpass_von_hand(liste)
    assert ergebnis == erwartet, f"engpass({liste}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# An der oberen Grenze: 100 000 Schritte
gross = [(nummer * 7919) % 10**6 + 1 for nummer in range(100000)]
ergebnis_lange = zu_lange(gross, 999990)
ergebnis_engpass = engpass(gross)
erwartet_lange = zu_lange_von_hand(gross, 999990)
erwartet_engpass = engpass_von_hand(gross)
assert ergebnis_lange == erwartet_lange and ergebnis_engpass == erwartet_engpass, (
    f"Bei 100 000 Schritten ergibt zu_lange(…, 999990) {len(ergebnis_lange)} Nummern, die ersten "
    f"{ergebnis_lange[:3]}, und engpass {ergebnis_engpass!r}; erwartet waren {len(erwartet_lange)} Nummern, "
    f"die ersten {erwartet_lange[:3]}, und {erwartet_engpass}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "[2, 3, 5]\n3"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
