# Automatisch erzeugt aus lehrkraft/muster/3_017_logauswertung.py - nicht von Hand ändern.
# vorlage-hash: 9b7253b2aea1315a
# text-hash: adf707aff2c97ce2
# thema: kontrollfluss
# inhalt: List Comprehension

zeilen = [
    "04:30:12 INFO Sicherung gestartet",
    "04:31:05 FEHLER Festplatte /dev/sdb voll",
    "04:32:40 WARNUNG CPU-Temperatur 81 Grad",
    "04:35:00 FEHLER Dienst mail antwortet nicht",
]

# meldungen aus dem Beispiel: der ganze Text, auch mit Leerzeichen
ergebnis = meldungen(zeilen, "FEHLER")
erwartet = ["Festplatte /dev/sdb voll", "Dienst mail antwortet nicht"]
assert ergebnis == erwartet, (
    f"meldungen(zeilen, 'FEHLER') ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: zeile.split(' ', 2) liefert genau drei Teile; der Text ist der dritte, mit allen Leerzeichen darin."
)

# Andere Stufen (nicht fest hinschreiben!); eine Stufe ohne Meldungen
for stufe, erwartet in [("INFO", ["Sicherung gestartet"]), ("WARNUNG", ["CPU-Temperatur 81 Grad"]), ("KRITISCH", [])]:
    ergebnis = meldungen(zeilen, stufe)
    assert ergebnis == erwartet, f"meldungen(zeilen, {stufe!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Die Stufe muss genau passen, ein Wort im Text zählt nicht
liste = ["1 INFO FEHLER behoben", "2 FEHLERHAFT x", "3 FEHLER y", "4 INFO FEHLER"]
ergebnis = meldungen(liste, "FEHLER")
assert ergebnis == ["y"], (
    f"meldungen({liste}, 'FEHLER') ergibt {ergebnis!r}, erwartet war ['y'].\n"
    "Tipp: Vergleichen Sie den zweiten Teil der Zeile mit ==; „FEHLER“ in zeile findet das Wort auch im Text."
)

# Keine Zeilen
ergebnis = meldungen([], "INFO")
assert ergebnis == [], f"meldungen([], 'INFO') ergibt {ergebnis!r}, erwartet war []."

# auslastung aus dem Beispiel und abgerundet
for anfragen, kapazitaet, erwartet in [
    ([150, 600, 480, 0], 600, [25, 100, 80, 0]),
    ([1, 2, 3], 3, [33, 66, 100]),
    ([999999, 1], 10**6, [99, 0]),
    ([], 5, []),
    ([7], 7, [100]),
]:
    ergebnis = auslastung(anfragen, kapazitaet)
    assert ergebnis == erwartet, (
        f"auslastung({anfragen}, {kapazitaet}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: anfrage * 100 // kapazitaet rundet ab und ergibt ganze Zahlen; erst malnehmen, dann teilen."
    )

# spitzen aus dem Beispiel; genau die Grenze zählt nicht
for anfragen, grenze, erwartet in [
    ([150, 600, 480, 0], 450, [1, 2]),
    ([150, 600, 480, 0], 480, [1]),
    ([150, 600, 480, 0], 600, []),
    ([150, 600, 480, 0], 0, [0, 1, 2]),
    ([5, 5, 5], 4, [0, 1, 2]),
    ([], 0, []),
]:
    ergebnis = spitzen(anfragen, grenze)
    assert ergebnis == erwartet, (
        f"spitzen({anfragen}, {grenze}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Gesucht sind die Positionen, nicht die Werte: [position for position, anfrage in enumerate(anfragen) if …]."
    )

# Die Listen bleiben unverändert
liste = ["1 INFO a b", "2 FEHLER c"]
werte = [3, 9, 1]
meldungen(liste, "INFO")
auslastung(werte, 9)
spitzen(werte, 2)
assert liste == ["1 INFO a b", "2 FEHLER c"] and werte == [3, 9, 1], (
    f"Nach den Auswertungen sind die Listen {liste!r} und {werte!r}; sie sollen unverändert bleiben."
)

# List Comprehensions statt for-Schleife und append
assert not verwendet("for") and not verwendet("append"), (
    "Schreiben Sie die drei Funktionen ohne for-Schleife und ohne append, jede mit einer List Comprehension "
    "der Form [ausdruck for x in liste if bedingung]."
)


# Vergleichslösungen mit while, anders als der verlangte Weg
def meldungen_von_hand(liste, stufe):
    """Sucht in jeder Zeile die ersten beiden Leerzeichen mit find und vergleicht die Stufe dazwischen."""
    gefunden = []
    index = 0
    while index < len(liste):
        zeile = liste[index]
        erstes = zeile.find(" ")
        zweites = zeile.find(" ", erstes + 1)
        if zeile[erstes + 1 : zweites] == stufe:
            gefunden.append(zeile[zweites + 1 :])
        index += 1
    return gefunden


def spitzen_von_hand(werte, grenze):
    """Geht die Positionen mit while durch."""
    gefunden = []
    position = 0
    while position < len(werte):
        if werte[position] > grenze:
            gefunden.append(position)
        position += 1
    return gefunden


# 300 zufällige Logs und Messreihen
zufall = Zufall(3017)
STUFEN = ["INFO", "WARNUNG", "FEHLER", "KRITISCH"]
WOERTER = ["Dienst", "mail", "INFO", "FEHLER", "voll", "81", "Grad", "/dev/sda"]
for _ in range(300):
    liste = []
    for _ in range(zufall.randint(0, 6)):
        uhrzeit = f"{zufall.randint(0, 23):02d}:{zufall.randint(0, 59):02d}:{zufall.randint(0, 59):02d}"
        text = " ".join(zufall.choice(WOERTER) for _ in range(zufall.randint(1, 4)))
        liste.append(f"{uhrzeit} {zufall.choice(STUFEN)} {text}")
    stufe = zufall.choice(STUFEN)
    ergebnis = meldungen(liste, stufe)
    erwartet = meldungen_von_hand(liste, stufe)
    assert ergebnis == erwartet, f"meldungen({liste}, {stufe!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    kapazitaet = zufall.choice([1, 3, 7, zufall.randint(1, 10**6)])
    werte = [zufall.randint(0, kapazitaet) for _ in range(zufall.randint(0, 6))]
    grenze = zufall.randint(0, kapazitaet)
    ergebnis = auslastung(werte, kapazitaet)
    erwartet = [int(wert * 100 / kapazitaet + 1e-9) for wert in werte]
    assert ergebnis == erwartet, f"auslastung({werte}, {kapazitaet}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    ergebnis = spitzen(werte, grenze)
    erwartet = spitzen_von_hand(werte, grenze)
    assert ergebnis == erwartet, f"spitzen({werte}, {grenze}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# An der oberen Grenze: 100 000 Zeilen und Messwerte
gross_zeilen = [f"{nummer:06d} {STUFEN[nummer % 4]} Meldung {nummer}" for nummer in range(100000)]
gross_werte = [(nummer * 7919) % 1000001 for nummer in range(100000)]
ergebnis_meldungen = meldungen(gross_zeilen, "KRITISCH")
ergebnis_auslastung = auslastung(gross_werte, 10**6)
ergebnis_spitzen = spitzen(gross_werte, 999990)
erwartet_spitzen = spitzen_von_hand(gross_werte, 999990)
assert (
    len(ergebnis_meldungen) == 25000
    and ergebnis_meldungen[:2] == ["Meldung 3", "Meldung 7"]
    and len(ergebnis_auslastung) == 100000
    and ergebnis_auslastung[:3] == [0, 0, 1]
    and ergebnis_spitzen == erwartet_spitzen
), (
    f"Bei 100 000 Einträgen ergibt meldungen(…, 'KRITISCH') {len(ergebnis_meldungen)} Texte, beginnend mit "
    f"{ergebnis_meldungen[:2]}, auslastung {len(ergebnis_auslastung)} Werte, beginnend mit {ergebnis_auslastung[:3]}, "
    f"und spitzen {len(ergebnis_spitzen)} Positionen; erwartet waren 25000 Texte, beginnend mit "
    f"['Meldung 3', 'Meldung 7'], 100000 Werte, beginnend mit [0, 0, 1], und {len(erwartet_spitzen)} Positionen."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "['Festplatte /dev/sdb voll', 'Dienst mail antwortet nicht']\n[25, 100, 80, 0]\n[1, 2]"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
