# Automatisch erzeugt aus lehrkraft/muster/2_040_lizenzbits.py - nicht von Hand ändern.
# vorlage-hash: 61ad335bd82067da
# text-hash: bce61cc3d0e7bf63
# thema: algorithmen
# inhalt: Binärdarstellung von Hand

def binaer_vergleich(zahl):
    """Vergleichslösung mit der eingebauten Funktion bin (in der Aufgabe selbst nicht erlaubt)."""
    return bin(zahl)[2:]


def hinweis_zu(zahl, ergebnis):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    erwartet = binaer_vergleich(zahl)
    if ergebnis == erwartet[::-1]:
        return "\nTipp: Das erste berechnete Bit ist das letzte der Darstellung; setzen Sie neue Bits vorn an: str(bit) + text."
    if isinstance(ergebnis, str) and ergebnis.lstrip("0") == erwartet:
        return "\nTipp: Die Darstellung soll keine führenden Nullen haben."
    if not isinstance(ergebnis, str):
        return "\nTipp: Geben Sie einen Text zurück, etwa \"1101\", keine Zahl und keine Liste."
    return ""


def meldung(zahl, ergebnis):
    """Baut die Fehlermeldung mit Eingabe, Ergebnis und erwartetem Text."""
    return f"binaer({zahl}) ergibt {ergebnis!r}, erwartet war {binaer_vergleich(zahl)!r}.{hinweis_zu(zahl, ergebnis)}"


# Das Beispiel aus der Aufgabe: 13 ist binär 1101
ergebnis = binaer(13)
assert ergebnis == "1101", meldung(13, ergebnis)

# Eine andere Zahl: 6 ist binär 110, die 0 am Ende gehört dazu (nicht fest hinschreiben!)
ergebnis = binaer(6)
assert ergebnis == "110", meldung(6, ergebnis)

# Die Reihenfolge der Bits stimmt: 11 ist 1011, nicht 1101
ergebnis = binaer(11)
assert ergebnis == "1011", meldung(11, ergebnis)

# Zweierpotenzen: eine 1 und dann nur Nullen
for zahl in [2, 8, 1024]:
    ergebnis = binaer(zahl)
    assert ergebnis == binaer_vergleich(zahl), meldung(zahl, ergebnis)

# Die Zahl 1
ergebnis = binaer(1)
assert ergebnis == "1", meldung(1, ergebnis)

# Die Zahl 0 ist "0", nicht der leere Text
ergebnis = binaer(0)
assert ergebnis == "0", meldung(0, ergebnis) + (
    "\nTipp: Bei 0 läuft die Schleife kein einziges Mal; behandeln Sie diesen Fall vorher." if ergebnis == "" else ""
)

# Die fertigen Umwandlungen werden nicht benutzt
assert not verwendet("bin") and not verwendet("format"), (
    "Ihr Code benutzt bin(...) oder format(...). Rechnen Sie die Bits selbst mit % 2 und // 2 aus."
)

# Die Bits werden einzeln ausgerechnet: bei 64 Bits braucht es deutlich mehr als eine Handvoll Schritte
ergebnis, schritte = zaehle_schritte(binaer, 2**64 - 1)
assert ergebnis == "1" * 64 and schritte >= 64, (
    f"binaer(2**64 - 1) ergibt {ergebnis!r} in {schritte} Schritten; erwartet waren 64 Einsen, "
    "Bit für Bit mit einer Schleife ausgerechnet (mindestens 64 Schritte).\n"
    'Tipp: Ein f-String wie f"{zahl:b}" ist hier nicht erlaubt; rechnen Sie mit % 2 und // 2.'
)

# Alle Zahlen von 0 bis 300
for zahl in range(301):
    ergebnis = binaer(zahl)
    assert ergebnis == binaer_vergleich(zahl), meldung(zahl, ergebnis)

# 500 zufällige Zahlen bis 2**64 - 1
zufall = Zufall(2040)
for _ in range(500):
    zahl = zufall.randint(0, 2 ** zufall.randint(1, 64) - 1)
    ergebnis = binaer(zahl)
    assert ergebnis == binaer_vergleich(zahl), meldung(zahl, ergebnis)

# Obere Grenze: 2**64 - 1 sind 64 Einsen, 2**63 eine Eins und 63 Nullen
for zahl in [2**64 - 1, 2**63]:
    ergebnis = binaer(zahl)
    assert ergebnis == binaer_vergleich(zahl), meldung(zahl, ergebnis)
