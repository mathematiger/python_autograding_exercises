# Automatisch erzeugt aus lehrkraft/muster/4_015_review_status.py - nicht von Hand ändern.
# vorlage-hash: d0392b7e760ffed2
# text-hash: 3d3b8c328c570fea
# thema: klassen
# inhalt: `enum.Enum`

import enum

ERWARTET = [
    ("ENTWURF", "Entwurf"),
    ("IN_PRUEFUNG", "In Prüfung"),
    ("FREIGEGEBEN", "Freigegeben"),
    ("ABGELEHNT", "Abgelehnt"),
    ("ZUSAMMENGEFUEHRT", "Zusammengeführt"),
]

# Status ist eine Aufzählung mit den fünf Mitgliedern in der richtigen Reihenfolge
mitglieder = [(status.name, status.value) for status in Status] if issubclass(Status, enum.Enum) else None
assert mitglieder == ERWARTET, (
    f"Status hat die Mitglieder (Name, Wert) {mitglieder}; erwartet war {ERWARTET}.\n"
    "Tipp: class Status(Enum): mit einer Zeile NAME = \"Anzeigetext\" pro Mitglied."
)

# Nachschlagen über Wert und Name, Mitglieder sind keine Texte
assert Status("In Prüfung") is Status.IN_PRUEFUNG and Status["ABGELEHNT"] is Status.ABGELEHNT and Status.ENTWURF != "Entwurf", (
    "Status(\"In Prüfung\") soll Status.IN_PRUEFUNG sein, Status[\"ABGELEHNT\"] soll Status.ABGELEHNT sein, und "
    "Status.ENTWURF soll ungleich dem Text \"Entwurf\" sein (eine gewöhnliche Enum, keine StrEnum)."
)

# Alle erlaubten Wechsel klappen
erlaubt = [
    (Status.ENTWURF, Status.IN_PRUEFUNG),
    (Status.IN_PRUEFUNG, Status.FREIGEGEBEN),
    (Status.IN_PRUEFUNG, Status.ABGELEHNT),
    (Status.ABGELEHNT, Status.ENTWURF),
    (Status.FREIGEGEBEN, Status.ZUSAMMENGEFUEHRT),
]
for aktuell, neu in erlaubt:
    try:
        ergebnis = wechsle(aktuell, neu)
    except (ValueError, TypeError) as fehler:
        ergebnis = fehler
    assert ergebnis is neu, f"wechsle({aktuell}, {neu}) ergibt {ergebnis!r}, erwartet war {neu}."

# Jeder andere Wechsel löst einen ValueError aus, der beide Anzeigetexte nennt
for aktuell in Status:
    for neu in Status:
        if (aktuell, neu) in erlaubt:
            continue
        try:
            wechsle(aktuell, neu)
            meldung = None
        except ValueError as fehler:
            meldung = str(fehler)
        assert meldung is not None and aktuell.value in meldung and neu.value in meldung, (
            f"wechsle({aktuell}, {neu}) soll einen ValueError auslösen, der {aktuell.value!r} und {neu.value!r} nennt; "
            f"Meldung: {meldung!r}.\nTipp: Schlagen Sie in UEBERGAENGE[aktuell] nach; den Anzeigetext liefert .value."
        )

# Kein Status: TypeError, auch für den passenden Text
for neu in ["In Prüfung", None, 1]:
    try:
        wechsle(Status.ENTWURF, neu)
        fehlerart = None
    except Exception as fehler:
        fehlerart = type(fehler).__name__
    assert fehlerart == "TypeError", (
        f"wechsle(Status.ENTWURF, {neu!r}) soll einen TypeError auslösen; ausgelöst wurde {fehlerart}.\n"
        "Tipp: Prüfen Sie mit isinstance(neu, Status), bevor Sie in UEBERGAENGE nachschlagen."
    )

# status_aus_text ohne Rücksicht auf Groß- und Kleinschreibung und Leerzeichen am Rand
for text, erwartet in [
    ("Freigegeben", Status.FREIGEGEBEN),
    ("  in prüfung ", Status.IN_PRUEFUNG),
    ("ZUSAMMENGEFÜHRT", Status.ZUSAMMENGEFUEHRT),
    ("\tentwurf\n", Status.ENTWURF),
    ("aBgElEhNt", Status.ABGELEHNT),
]:
    try:
        ergebnis = status_aus_text(text)
    except ValueError as fehler:
        ergebnis = fehler
    assert ergebnis is erwartet, (
        f"status_aus_text({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Vergleichen Sie text.strip().lower() mit status.value.lower() für jeden status in Status."
    )

# Unbekannte Texte und Namen statt Anzeigetexten lösen ValueError aus
for text in ["frei gegeben", "", "IN_PRUEFUNG", "Entwurf.", "In  Prüfung"]:
    try:
        ergebnis = status_aus_text(text)
    except ValueError:
        ergebnis = "ValueError"
    assert ergebnis == "ValueError", (
        f"status_aus_text({text!r}) soll einen ValueError auslösen, ergibt aber {ergebnis!r}."
    )

# statistik aus dem Beispiel, mit allen fünf Status in der Reihenfolge der Aufzählung
ergebnis = statistik([Status.ENTWURF, Status.ABGELEHNT, Status.ENTWURF])
erwartet = {Status.ENTWURF: 2, Status.IN_PRUEFUNG: 0, Status.FREIGEGEBEN: 0, Status.ABGELEHNT: 1, Status.ZUSAMMENGEFUEHRT: 0}
assert ergebnis == erwartet and list(ergebnis) == list(Status), (
    f"statistik([ENTWURF, ABGELEHNT, ENTWURF]) ergibt {ergebnis!r}, erwartet war {erwartet} in dieser Reihenfolge.\n"
    "Tipp: Legen Sie zuerst für jeden status in Status den Zähler 0 an."
)

# statistik einer leeren Liste
ergebnis = statistik([])
assert ergebnis == {status: 0 for status in Status}, f"statistik([]) ergibt {ergebnis!r}, erwartet war 0 für jeden Status."

# 300 zufällige Abläufe, nachgespielt mit den Namen
NAECHSTE = {
    "ENTWURF": ["IN_PRUEFUNG"],
    "IN_PRUEFUNG": ["FREIGEGEBEN", "ABGELEHNT"],
    "ABGELEHNT": ["ENTWURF"],
    "FREIGEGEBEN": ["ZUSAMMENGEFUEHRT"],
    "ZUSAMMENGEFUEHRT": [],
}
zufall = Zufall(4015)
for _ in range(300):
    name = zufall.choice(list(NAECHSTE))
    ziel = zufall.choice(list(NAECHSTE))
    try:
        ergebnis = wechsle(Status[name], Status[ziel]).name
    except ValueError:
        ergebnis = "ValueError"
    erwartet = ziel if ziel in NAECHSTE[name] else "ValueError"
    assert ergebnis == erwartet, f"wechsle(Status.{name}, Status.{ziel}) ergibt {ergebnis}, erwartet war {erwartet}."
    wert = dict(ERWARTET)[ziel]
    text = " " * zufall.randint(0, 3) + "".join(zufall.choice([zeichen.lower(), zeichen.upper()]) for zeichen in wert) + " " * zufall.randint(0, 3)
    ergebnis = status_aus_text(text)
    assert ergebnis is Status[ziel], f"status_aus_text({text!r}) ergibt {ergebnis!r}, erwartet war Status.{ziel}."
    namen = [zufall.choice(list(NAECHSTE)) for _ in range(zufall.randint(0, 10))]
    erwartet = [namen.count(name) for name, _ in ERWARTET]
    ergebnis = statistik([Status[name] for name in namen])
    assert list(ergebnis.values()) == erwartet and list(ergebnis) == list(Status), (
        f"statistik mit {namen} ergibt {ergebnis!r}, erwartet waren die Anzahlen {erwartet} in der Reihenfolge der Aufzählung."
    )

# An der oberen Grenze: 100 000 Status
zustaende = [list(Status)[nummer % 7 % 5] for nummer in range(100000)]
ergebnis = statistik(zustaende)
erwartet = [28571, 28571, 14286, 14286, 14286]
assert list(ergebnis.values()) == erwartet, (
    f"statistik mit 100 000 Status ergibt die Anzahlen {list(ergebnis.values())}, erwartet waren {erwartet}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "FREIGEGEBEN Freigegeben\n"
    "{<Status.ENTWURF: 'Entwurf'>: 2, <Status.IN_PRUEFUNG: 'In Prüfung'>: 0, <Status.FREIGEGEBEN: 'Freigegeben'>: 0, "
    "<Status.ABGELEHNT: 'Abgelehnt'>: 1, <Status.ZUSAMMENGEFUEHRT: 'Zusammengeführt'>: 0}"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
