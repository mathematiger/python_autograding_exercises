# Automatisch erzeugt aus lehrkraft/muster/4_072_cloudkosten.py - nicht von Hand ändern.
# vorlage-hash: 4e18509e87cd2174
# text-hash: 9a63d1db26e82cd9
# thema: datenanalyse
# inhalt: pandas: to_datetime, .dt, resample

from datetime import datetime, timedelta

ZEILEN = [
    ("20.11.2026 08:00", "test-01", 0.40),
    ("20.11.2026 13:00", "test-02", 0.85),
    ("20.11.2026 20:00", "test-01", 0.40),
    ("21.11.2026 10:00", "test-02", 0.85),
    ("23.11.2026 06:00", "test-02", 0.85),
    ("23.11.2026 07:00", "test-01", 0.40),
    ("23.11.2026 18:00", "test-02", 0.85),
    ("23.11.2026 19:00", "test-01", 0.40),
]


def als_csv(zeilen):
    """Schreibt Zeilen (zeitpunkt, vm, kosten) als CSV-Text mit Kopfzeile."""
    text = "zeitpunkt,vm,kosten_eur\n"
    for zeitpunkt, vm, kosten in zeilen:
        text += f"{zeitpunkt},{vm},{kosten:.2f}\n"
    return text


def tabelle(zeilen):
    """Baut den DataFrame, den lade liefern soll, ohne die Funktion der Lernenden."""
    abrechnung = pd.read_csv(io.StringIO(als_csv(zeilen)))
    abrechnung["zeitpunkt"] = pd.to_datetime(abrechnung["zeitpunkt"], format="%d.%m.%Y %H:%M")
    return abrechnung


def wert_von(funktion, argument):
    """Ruft funktion auf (DataFrames als Kopie); ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(argument.copy() if isinstance(argument, pd.DataFrame) else argument)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def zeit_von(text):
    """Vergleichslösung: liest einen Zeitpunkt mit strptime."""
    return datetime.strptime(text, "%d.%m.%Y %H:%M")


def vergleich_ausserhalb(zeilen):
    """Vergleichslösung für ausserhalb, Zeile für Zeile mit datetime."""
    ergebnis = []
    for text, vm, kosten in zeilen:
        zeit = zeit_von(text)
        ergebnis.append(zeit.weekday() >= 5 or zeit.hour < 7 or zeit.hour >= 19)
    return ergebnis


def vergleich_kosten(zeilen):
    """Vergleichslösung für ausserhalb_kosten in Cent, damit nichts falsch rundet."""
    cent = 0
    for (text, vm, kosten), draussen in zip(zeilen, vergleich_ausserhalb(zeilen)):
        if draussen:
            cent += round(kosten * 100)
    return cent / 100


def vergleich_tage(zeilen):
    """Vergleichslösung für kosten_je_tag: Liste von (Datum als Text, Kosten), jeder Tag vom ersten bis zum letzten."""
    if not zeilen:
        return []
    cent = {}
    for text, vm, kosten in zeilen:
        tag = zeit_von(text).date()
        cent[tag] = cent.get(tag, 0) + round(kosten * 100)
    tag, letzter = min(cent), max(cent)
    ergebnis = []
    while tag <= letzter:
        ergebnis.append((str(tag), cent.get(tag, 0) / 100))
        tag += timedelta(days=1)
    return ergebnis


def tage_von(ergebnis):
    """Macht aus einer Serie mit Zeitpunkten als Index eine Liste von (Datum als Text, Wert)."""
    if not isinstance(ergebnis, pd.Series):
        return ergebnis
    try:
        return [(str(pd.Timestamp(tag).date()), round(float(wert), 2)) for tag, wert in ergebnis.items()]
    except (TypeError, ValueError) as fehler:
        return f"Serie mit unerwartetem Index ({type(fehler).__name__}: {fehler})"


def zufallszeilen(zufall, anzahl):
    """Erzeugt zufällige Abrechnungszeilen über einige Tage, in zufälliger Reihenfolge."""
    beginn = datetime(2026, 1, 1) + timedelta(days=zufall.randint(0, 3000))
    zeilen = []
    for _ in range(anzahl):
        zeit = beginn + timedelta(hours=zufall.randint(0, 24 * 20))
        zeilen.append((f"{zeit:%d.%m.%Y %H:%M}", f"test-{zufall.randint(1, 9):02d}", zufall.randint(0, 10000) / 100))
    return zeilen


# lade: das Beispiel hat die drei Spalten
ergebnis = wert_von(lade, als_csv(ZEILEN))
spalten = list(ergebnis.columns) if isinstance(ergebnis, pd.DataFrame) else ergebnis
assert spalten == ["zeitpunkt", "vm", "kosten_eur"], (
    f"lade(text) ergibt einen DataFrame mit den Spalten {spalten!r}, erwartet waren ['zeitpunkt', 'vm', 'kosten_eur'].\n"
    "Tipp: pd.read_csv(io.StringIO(text))."
)

# lade: zeitpunkt ist ein Zeitpunkt, kein Text
art = str(ergebnis["zeitpunkt"].dtype) if isinstance(ergebnis, pd.DataFrame) else ergebnis
assert isinstance(ergebnis, pd.DataFrame) and pd.api.types.is_datetime64_any_dtype(ergebnis["zeitpunkt"]), (
    f"Die Spalte zeitpunkt hat den Datentyp {art}, erwartet war datetime64.\n"
    'Tipp: abrechnung["zeitpunkt"] = pd.to_datetime(abrechnung["zeitpunkt"], format="%d.%m.%Y %H:%M").'
)

# lade: die Zeitpunkte des Beispiels
zeiten = [str(zeit) for zeit in ergebnis["zeitpunkt"]] if isinstance(ergebnis, pd.DataFrame) else ergebnis
erwartet = [str(zeit_von(text)) for text, vm, kosten in ZEILEN]
assert zeiten == erwartet, f"lade(text) liest die Zeitpunkte\n{zeiten}\nerwartet waren\n{erwartet}"

# lade: Tag vor Monat, auch wenn der Tag 12 oder kleiner ist
zeilen = [("05.12.2026 08:00", "test-01", 0.4), ("07.12.2026 09:00", "test-01", 0.4)]
ergebnis = wert_von(lade, als_csv(zeilen))
zeiten = [str(zeit) for zeit in ergebnis["zeitpunkt"]] if isinstance(ergebnis, pd.DataFrame) else ergebnis
assert zeiten == ["2026-12-05 08:00:00", "2026-12-07 09:00:00"], (
    f"lade liest '05.12.2026 08:00' und '07.12.2026 09:00' als {zeiten}, erwartet waren der 5. und 7. Dezember.\n"
    'Tipp: Ohne format= rät pandas und hält 05.12. für den 12. Mai; geben Sie format="%d.%m.%Y %H:%M" an.'
)

# lade: die Kosten sind Zahlen
ergebnis = wert_von(lade, als_csv(ZEILEN))
kosten = ergebnis["kosten_eur"].tolist() if isinstance(ergebnis, pd.DataFrame) else ergebnis
assert kosten == [kosten for zeitpunkt, vm, kosten in ZEILEN], f"Die Spalte kosten_eur ist {kosten!r}, erwartet waren die Zahlen aus dem Text."

# lade: eine Abrechnung ohne Zeilen
ergebnis = wert_von(lade, als_csv([]))
assert isinstance(ergebnis, pd.DataFrame) and len(ergebnis) == 0 and "zeitpunkt" in ergebnis.columns, (
    f"lade mit nur der Kopfzeile ergibt {ergebnis!r}, erwartet war ein leerer DataFrame mit den drei Spalten."
)

# ausserhalb: das Beispiel
ergebnis = wert_von(ausserhalb, tabelle(ZEILEN))
werte = ergebnis.tolist() if isinstance(ergebnis, pd.Series) else ergebnis
assert werte == vergleich_ausserhalb(ZEILEN), (
    f"ausserhalb(abrechnung).tolist() ergibt {werte!r},\nerwartet war {vergleich_ausserhalb(ZEILEN)}.\n"
    "Tipp: abrechnung['zeitpunkt'].dt.day_of_week >= 5 ist Samstag oder Sonntag; verknüpfen Sie die Bedingungen mit |."
)

# ausserhalb: Sonntag mitten am Tag
zeilen = [("22.11.2026 12:00", "test-01", 1.0)]
ergebnis = wert_von(ausserhalb, tabelle(zeilen))
werte = ergebnis.tolist() if isinstance(ergebnis, pd.Series) else ergebnis
assert werte == [True], (
    f"Für Sonntag, 22.11.2026, 12:00 ergibt ausserhalb {werte!r}, erwartet war [True].\n"
    "Tipp: day_of_week zählt ab Montag = 0, Sonntag ist 6."
)

# ausserhalb: Grenzen der Kernarbeitszeit
zeilen = [
    ("24.11.2026 06:00", "a", 1.0), ("24.11.2026 07:00", "a", 1.0),
    ("24.11.2026 18:00", "a", 1.0), ("24.11.2026 19:00", "a", 1.0),
    ("24.11.2026 00:00", "a", 1.0), ("24.11.2026 23:00", "a", 1.0),
]
ergebnis = wert_von(ausserhalb, tabelle(zeilen))
werte = ergebnis.tolist() if isinstance(ergebnis, pd.Series) else ergebnis
assert werte == [True, False, False, True, True, True], (
    f"Für einen Dienstag um 6, 7, 18, 19, 0 und 23 Uhr ergibt ausserhalb {werte!r}, "
    "erwartet war [True, False, False, True, True, True].\nTipp: 07:00 gehört dazu, 19:00 nicht mehr (< 7, >= 19)."
)

# ausserhalb_kosten: das Beispiel
ergebnis = wert_von(ausserhalb_kosten, tabelle(ZEILEN))
assert isinstance(ergebnis, (int, float)) and abs(ergebnis - 2.5) < 0.001, (
    f"ausserhalb_kosten(abrechnung) ergibt {ergebnis!r}, erwartet war 2.5.\n"
    'Tipp: abrechnung.loc[maske, "kosten_eur"].sum().'
)

# ausserhalb_kosten: andere Zeilen (nicht fest hinschreiben!)
zeilen = ZEILEN + [("22.11.2026 15:00", "test-03", 3.10), ("24.11.2026 12:00", "test-03", 3.10)]
ergebnis = wert_von(ausserhalb_kosten, tabelle(zeilen))
assert isinstance(ergebnis, (int, float)) and abs(ergebnis - 5.6) < 0.001, (
    f"Mit zwei Zeilen mehr (Sonntag und Dienstag mittags, je 3.10) ergibt ausserhalb_kosten {ergebnis!r}, erwartet war 5.6."
)

# ausserhalb_kosten: auf Cent gerundet
zeilen = [("21.11.2026 10:00", "a", 0.1), ("21.11.2026 11:00", "a", 0.2)]
ergebnis = wert_von(ausserhalb_kosten, tabelle(zeilen))
assert ergebnis == 0.3, (
    f"ausserhalb_kosten für 0.10 und 0.20 € ergibt {ergebnis!r}, erwartet war 0.3.\n"
    "Tipp: Kommazahlen summieren sich zu 0.30000000000000004; runden Sie mit round(summe, 2)."
)

# ausserhalb_kosten: alles in der Kernarbeitszeit
zeilen = [("24.11.2026 10:00", "a", 2.0)]
ergebnis = wert_von(ausserhalb_kosten, tabelle(zeilen))
assert ergebnis == 0, f"Wenn alles in der Kernarbeitszeit liegt, ergibt ausserhalb_kosten {ergebnis!r}, erwartet war 0."

# kosten_je_tag: das Beispiel
ergebnis = wert_von(kosten_je_tag, tabelle(ZEILEN))
erwartet = vergleich_tage(ZEILEN)
assert tage_von(ergebnis) == erwartet, (
    f"kosten_je_tag(abrechnung) ergibt\n{ergebnis}\nerwartet waren die Tage und Kosten {erwartet}.\n"
    'Tipp: abrechnung.resample("D", on="zeitpunkt")["kosten_eur"].sum() – ohne die Spalte vm, sonst hängt pandas '
    "deren Texte aneinander."
)

# kosten_je_tag: Tage ohne Zeilen kommen mit 0 vor
zeilen = [("01.12.2026 09:00", "a", 1.0), ("04.12.2026 09:00", "a", 2.0)]
ergebnis = wert_von(kosten_je_tag, tabelle(zeilen))
assert tage_von(ergebnis) == vergleich_tage(zeilen), (
    f"kosten_je_tag für den 1. und 4. Dezember ergibt\n{ergebnis}\nerwartet waren {vergleich_tage(zeilen)}.\n"
    "Tipp: resample legt auch die leeren Tage dazwischen an; groupby nach dem Datum tut das nicht."
)

# kosten_je_tag: unsortierte Zeilen über einen Monatswechsel
zeilen = [("01.12.2026 09:00", "a", 1.25), ("29.11.2026 23:00", "b", 0.5), ("30.11.2026 00:00", "b", 0.5)]
ergebnis = wert_von(kosten_je_tag, tabelle(zeilen))
assert tage_von(ergebnis) == vergleich_tage(zeilen), f"kosten_je_tag ergibt\n{ergebnis}\nerwartet waren {vergleich_tage(zeilen)}."

# kosten_je_tag: auf Cent gerundet
zeilen = [("01.12.2026 09:00", "a", 0.1), ("01.12.2026 10:00", "a", 0.2)]
ergebnis = wert_von(kosten_je_tag, tabelle(zeilen))
werte = ergebnis.tolist() if isinstance(ergebnis, pd.Series) else ergebnis
assert werte == [0.3], f"kosten_je_tag für 0.10 und 0.20 € an einem Tag ergibt {werte!r}, erwartet war [0.3].\nTipp: .round(2)."

# kosten_je_tag: eine Abrechnung ohne Zeilen
ergebnis = wert_von(kosten_je_tag, tabelle([]))
assert isinstance(ergebnis, pd.Series) and len(ergebnis) == 0, f"kosten_je_tag ohne Zeilen ergibt {ergebnis!r}, erwartet war eine leere Serie."

# Ohne Python-Schleife
assert not verwendet("for") and not verwendet("while") and not verwendet("apply") and not verwendet("iterrows"), (
    "Ihr Code benutzt eine Schleife, apply oder iterrows. Rechnen Sie mit .dt, Masken und resample auf ganzen Spalten."
)

# Die Ausgabe des Programms
erwartet = "[False, False, True, True, True, False, False, True]\n2.5\n[1.65, 0.85, 0.0, 2.5]"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Abrechnungen
zufall = Zufall(4072)
for _ in range(40):
    zeilen = zufallszeilen(zufall, zufall.randint(1, 15))
    abrechnung = wert_von(lade, als_csv(zeilen))
    if isinstance(abrechnung, str):
        abrechnung = tabelle(zeilen)
    ergebnis = wert_von(ausserhalb, abrechnung)
    werte = ergebnis.tolist() if isinstance(ergebnis, pd.Series) else ergebnis
    assert werte == vergleich_ausserhalb(zeilen), f"Für die Zeilen {zeilen}\nergibt ausserhalb {werte!r}"
    ergebnis = wert_von(ausserhalb_kosten, abrechnung)
    assert isinstance(ergebnis, (int, float)) and abs(ergebnis - vergleich_kosten(zeilen)) < 0.001, (
        f"Für die Zeilen {zeilen}\nergibt ausserhalb_kosten {ergebnis!r}, erwartet war {vergleich_kosten(zeilen)}."
    )
    ergebnis = wert_von(kosten_je_tag, abrechnung)
    assert tage_von(ergebnis) == vergleich_tage(zeilen), (
        f"Für die Zeilen {zeilen}\nergibt kosten_je_tag {tage_von(ergebnis)!r},\nerwartet war {vergleich_tage(zeilen)}."
    )

# Obere Grenze: 10 000 Zeilen
zeilen = zufallszeilen(zufall, 10000)
abrechnung = wert_von(lade, als_csv(zeilen))
stimmt = isinstance(abrechnung, pd.DataFrame)
stimmt = stimmt and abs(wert_von(ausserhalb_kosten, abrechnung) - vergleich_kosten(zeilen)) < 0.001
stimmt = stimmt and tage_von(wert_von(kosten_je_tag, abrechnung)) == vergleich_tage(zeilen)
assert stimmt, "Bei 10 000 Zeilen stimmen ausserhalb_kosten oder kosten_je_tag nicht (die kleineren Tests oben zeigen, wo)."
