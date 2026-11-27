# Automatisch erzeugt aus lehrkraft/muster/2_051_datenkontingent.py - nicht von Hand ändern.
# vorlage-hash: 78a4e19d9d2e7006
# text-hash: 6762d158473e790d
# thema: texte_zahlen
# inhalt: Schaltjahr, Tage im Monat

import calendar


def wert_von(funktion, *argumente):
    """Ruft die Funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def ungefaehr(ergebnis, erwartet):
    """Prüft, ob ergebnis eine Zahl ist, die bis auf Rundungsfehler erwartet entspricht."""
    return isinstance(ergebnis, (int, float)) and abs(ergebnis - erwartet) < 1e-9


def vergleich_tage(jahr, monat):
    """Vergleichslösung mit dem Modul calendar."""
    return calendar.monthrange(jahr, monat)[1]


# ist_schaltjahr im Beispiel: 2024 ist ein Schaltjahr
ergebnis = wert_von(ist_schaltjahr, 2024)
assert ergebnis == True, f"ist_schaltjahr(2024) ergibt {ergebnis!r}, erwartet war True (2024 ist durch 4 teilbar)."

# Ein Jahr, das nicht durch 4 teilbar ist, ist kein Schaltjahr
ergebnis = [wert_von(ist_schaltjahr, jahr) for jahr in [2023, 2025, 2026]]
assert ergebnis == [False, False, False], (
    f"ist_schaltjahr für 2023, 2025 und 2026 ergibt {ergebnis!r}, erwartet war [False, False, False]."
)

# Andere durch 4 teilbare Jahre (nicht fest 2024 hinschreiben!)
ergebnis = [wert_von(ist_schaltjahr, jahr) for jahr in [1996, 2028, 4]]
assert ergebnis == [True, True, True], f"ist_schaltjahr für 1996, 2028 und 4 ergibt {ergebnis!r}, erwartet war [True, True, True]."

# Durch 100 teilbare Jahre sind keine Schaltjahre: 1900
ergebnis = wert_von(ist_schaltjahr, 1900)
assert ergebnis == False, (
    f"ist_schaltjahr(1900) ergibt {ergebnis!r}, erwartet war False.\n"
    "Tipp: 1900 ist zwar durch 4 teilbar, aber auch durch 100 und nicht durch 400."
)

# Weitere durch 100, aber nicht durch 400 teilbare Jahre
ergebnis = [wert_von(ist_schaltjahr, jahr) for jahr in [100, 1700, 2100, 9900]]
assert ergebnis == [False, False, False, False], (
    f"ist_schaltjahr für 100, 1700, 2100 und 9900 ergibt {ergebnis!r}, erwartet war viermal False."
)

# Durch 400 teilbare Jahre sind doch Schaltjahre: 2000
ergebnis = [wert_von(ist_schaltjahr, jahr) for jahr in [2000, 1600, 400]]
assert ergebnis == [True, True, True], (
    f"ist_schaltjahr für 2000, 1600 und 400 ergibt {ergebnis!r}, erwartet war [True, True, True].\n"
    "Tipp: Durch 400 teilbare Jahre sind Schaltjahre, obwohl sie auch durch 100 teilbar sind."
)

# ist_schaltjahr gibt True oder False zurück, nicht 1, 0 oder einen Text
ergebnis = [wert_von(ist_schaltjahr, jahr) for jahr in [2024, 2023]]
assert ergebnis[0] is True and ergebnis[1] is False, (
    f"ist_schaltjahr(2024) und ist_schaltjahr(2023) ergeben {ergebnis!r}, erwartet war genau True und False."
)

# tage_im_monat im Beispiel: Februar 2024 hat 29 Tage
ergebnis = wert_von(tage_im_monat, 2024, 2)
assert ergebnis == 29, f"tage_im_monat(2024, 2) ergibt {ergebnis!r}, erwartet war 29 (2024 ist ein Schaltjahr)."

# Monate mit 31 Tagen
ergebnis = [wert_von(tage_im_monat, 2025, monat) for monat in [1, 3, 5, 7, 8, 10, 12]]
assert ergebnis == [31] * 7, (
    f"tage_im_monat(2025, monat) für Januar, März, Mai, Juli, August, Oktober und Dezember ergibt {ergebnis!r}, "
    "erwartet war siebenmal 31."
)

# Monate mit 30 Tagen
ergebnis = [wert_von(tage_im_monat, 2025, monat) for monat in [4, 6, 9, 11]]
assert ergebnis == [30, 30, 30, 30], (
    f"tage_im_monat(2025, monat) für April, Juni, September und November ergibt {ergebnis!r}, erwartet war viermal 30."
)

# Februar in einem gewöhnlichen Jahr
ergebnis = wert_von(tage_im_monat, 2025, 2)
assert ergebnis == 28, f"tage_im_monat(2025, 2) ergibt {ergebnis!r}, erwartet war 28."

# Februar in den Jahren 1900 und 2000
ergebnis = [wert_von(tage_im_monat, 1900, 2), wert_von(tage_im_monat, 2000, 2)]
assert ergebnis == [28, 29], (
    f"tage_im_monat(1900, 2) und tage_im_monat(2000, 2) ergeben {ergebnis!r}, erwartet war [28, 29].\n"
    "Tipp: Rufen Sie für den Februar ist_schaltjahr(jahr) auf."
)

# Im Schaltjahr ändern sich die anderen Monate nicht
ergebnis = [wert_von(tage_im_monat, 2024, monat) for monat in [1, 3, 4, 12]]
assert ergebnis == [31, 31, 30, 31], f"tage_im_monat(2024, monat) für 1, 3, 4 und 12 ergibt {ergebnis!r}, erwartet war [31, 31, 30, 31]."

# tagesanteil im Beispiel
ergebnis = wert_von(tagesanteil, 300, 2025, 4)
assert ungefaehr(ergebnis, 10), f"tagesanteil(300, 2025, 4) ergibt {ergebnis!r}, erwartet war 10.0 (300 GB auf 30 Tage)."

# tagesanteil im Februar eines Schaltjahrs und eines gewöhnlichen Jahrs
ergebnis = [wert_von(tagesanteil, 290, 2024, 2), wert_von(tagesanteil, 280, 2023, 2)]
assert ungefaehr(ergebnis[0], 10) and ungefaehr(ergebnis[1], 10), f"tagesanteil(290, 2024, 2) und tagesanteil(280, 2023, 2) ergeben {ergebnis!r}, erwartet war [10.0, 10.0]."

# tagesanteil ohne Kontingent und mit einer krummen Zahl
ergebnis = [wert_von(tagesanteil, 0, 2025, 1), wert_von(tagesanteil, 100, 2025, 1)]
assert ungefaehr(ergebnis[0], 0) and ungefaehr(ergebnis[1], 100 / 31), (
    f"tagesanteil(0, 2025, 1) und tagesanteil(100, 2025, 1) ergeben {ergebnis!r}, erwartet war [0.0, {100 / 31}].\n"
    "Tipp: Teilen Sie mit /, nicht mit //."
)

# Ohne calendar und datetime
benutzt = [name for name in ["isleap", "monthrange", "date"] if verwendet(name)]
assert benutzt == [], f"Ihr Code verwendet {benutzt}. Rechnen Sie die Regeln selbst aus, ohne calendar und datetime."

# Die Ausgabe des Programms
erwartet = "True\nFalse\n29\n30\n10.0"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Jahre und Monate, verglichen mit dem Modul calendar
zufall = Zufall(2051)
for _ in range(500):
    jahr = zufall.choice([zufall.randint(1, 9999), zufall.randint(1, 99) * 100, zufall.randint(1, 2499) * 4])
    monat = zufall.randint(1, 12)
    kontingent = zufall.randint(0, 100000)
    ergebnis = [wert_von(ist_schaltjahr, jahr), wert_von(tage_im_monat, jahr, monat)]
    erwartet = [calendar.isleap(jahr), vergleich_tage(jahr, monat)]
    assert ergebnis == erwartet, (
        f"Für jahr = {jahr}, monat = {monat} ergeben ist_schaltjahr und tage_im_monat {ergebnis!r}, erwartet war {erwartet!r}."
    )
    ergebnis = wert_von(tagesanteil, kontingent, jahr, monat)
    erwartet = kontingent / vergleich_tage(jahr, monat)
    assert ungefaehr(ergebnis, erwartet), (
        f"tagesanteil({kontingent}, {jahr}, {monat}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    )

# Ränder: die Jahre 1 und 9999
ergebnis = [wert_von(ist_schaltjahr, 1), wert_von(ist_schaltjahr, 9999)]
assert ergebnis == [False, False], f"ist_schaltjahr(1) und ist_schaltjahr(9999) ergeben {ergebnis!r}, erwartet war [False, False]."

# Ränder: das größte Kontingent
ergebnis = wert_von(tagesanteil, 100000, 9999, 12)
assert ungefaehr(ergebnis, 100000 / 31), f"tagesanteil(100000, 9999, 12) ergibt {ergebnis!r}, erwartet war {100000 / 31}."

# Obere Grenze: alle Jahre von 1 bis 9999
falsch = [jahr for jahr in range(1, 10000) if wert_von(ist_schaltjahr, jahr) != calendar.isleap(jahr)]
assert falsch == [], f"ist_schaltjahr irrt sich in {len(falsch)} Jahren zwischen 1 und 9999, zuerst bei {falsch[:5]}."
