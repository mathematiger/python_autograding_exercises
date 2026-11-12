# Automatisch erzeugt aus lehrkraft/muster/5_018_loeschfristen.py - nicht von Hand ändern.
# vorlage-hash: 8e04f88518db3667
# text-hash: 00584b1b5c8acdd3
# thema: datenanalyse
# inhalt: Projekt: bereinigen, verknüpfen, auswerten

def tage(spalte):
    """Wandelt eine Datumsspalte in eine Liste von Texten JJJJ-MM-TT um; None bei einem Typfehler."""
    try:
        return spalte.dt.strftime("%Y-%m-%d").tolist()
    except (AttributeError, TypeError, ValueError):
        return None


def als_csv(zeilen):
    """Baut aus Zeilen (id, kategorie, erstellt, kunde) den CSV-Text für lade."""
    text = "id,kategorie,erstellt,kunde\n"
    for zeile in zeilen:
        text += ",".join(str(wert) for wert in zeile) + "\n"
    return text


def fristen_csv(paare):
    """Baut aus Paaren (kategorie, frist_tage) den CSV-Text für lade."""
    text = "kategorie,frist_tage\n"
    for kategorie, frist in paare:
        text += f"{kategorie},{frist}\n"
    return text


STICHTAG = pd.Timestamp("2025-01-01")

# bereinige aus dem Beispiel
roh = lade(ROHDATEN)
roh_vorher = roh.copy()
daten = bereinige(roh)
assert list(daten.columns) == ["id", "kategorie", "erstellt", "kunde"], (
    f"bereinige liefert die Spalten {list(daten.columns)}, erwartet waren ['id', 'kategorie', 'erstellt', 'kunde']."
)

# bereinige: ids, Kategorien und Daten stimmen
ergebnis = (daten["id"].tolist(), daten["kategorie"].tolist(), tage(daten["erstellt"]))
erwartet = (
    [1, 2, 4, 5, 6],
    ["bewerbung", "rechnung", "newsletter", "chatprotokoll", "bewerbung"],
    ["2024-03-01", "2015-12-31", "2022-06-15", "2024-01-10", "2024-11-20"],
)
assert ergebnis == erwartet, (
    f"bereinige(lade(ROHDATEN)) ergibt ids, kategorien und erstellt {ergebnis!r}, erwartet war {erwartet!r}.\n"
    'Tipp: kategorie mit .str.strip().str.lower(), erstellt mit pd.to_datetime(…, format="%Y-%m-%d", '
    'errors="coerce"), dann dropna(subset=["erstellt"]) und drop_duplicates(subset="id", keep="first").'
)

# bereinige: Index neu nummeriert, roh unverändert
assert daten.index.tolist() == [0, 1, 2, 3, 4] and roh.equals(roh_vorher), (
    f"Nach bereinige ist der Index {daten.index.tolist()} (erwartet [0, 1, 2, 3, 4]), und roh ist "
    f"{'unverändert' if roh.equals(roh_vorher) else 'verändert'} (erwartet unverändert).\n"
    "Tipp: reset_index(drop=True) nummeriert neu; arbeiten Sie mit assign statt roh[...] = …"
)

# Erst ungültige Daten entfernen, dann Dubletten: die gültige zweite Zeile bleibt
roh = lade(als_csv([(7, "rechnung", "2020-02-30", "K-1"), (7, "rechnung", "2020-03-01", "K-1"),
                    (8, "rechnung", "", "K-2"), (9, "Rechnung", "01.03.2020", "K-3")]))
daten = bereinige(roh)
ergebnis = (daten["id"].tolist(), tage(daten["erstellt"]))
assert ergebnis == ([7], ["2020-03-01"]), (
    "Für id 7 mit ungültigem und danach gültigem Datum, id 8 ohne Datum und id 9 mit 01.03.2020 ergibt bereinige "
    f"ids und erstellt {ergebnis!r}, erwartet war ([7], ['2020-03-01']).\n"
    "Tipp: Entfernen Sie zuerst die Zeilen mit ungültigem Datum und erst danach die Dubletten."
)

# loeschtermine aus dem Beispiel
daten = bereinige(lade(ROHDATEN))
daten_vorher = daten.copy()
fristen = lade(FRISTEN)
termine = loeschtermine(daten, fristen).sort_values("id")
ergebnis = (termine["id"].tolist(), tage(termine["loeschen_ab"]))
erwartet = ([1, 2, 4, 6], ["2024-08-28", "2025-12-28", "2024-06-14", "2025-05-19"])
assert ergebnis == erwartet, (
    f"loeschtermine(daten, fristen) ergibt ids und loeschen_ab {ergebnis!r}, erwartet war {erwartet!r}.\n"
    'Tipp: daten.merge(fristen, on="kategorie") und loeschen_ab = erstellt + pd.to_timedelta(frist_tage, unit="D").'
)

# faellige aus dem Beispiel
ergebnis = faellige(daten, fristen, STICHTAG)
werte = (list(ergebnis.columns), ergebnis["id"].tolist(), ergebnis["kategorie"].tolist(), tage(ergebnis["loeschen_ab"]))
erwartet = (["id", "kategorie", "loeschen_ab"], [4, 1], ["newsletter", "bewerbung"], ["2024-06-14", "2024-08-28"])
assert werte == erwartet, (
    f"faellige(daten, fristen, 2025-01-01) ergibt Spalten, ids, kategorien und loeschen_ab {werte!r}, "
    f"erwartet war {erwartet!r}."
)

# ohne_frist und bericht aus dem Beispiel
ergebnis = (ohne_frist(daten, fristen), bericht(daten, fristen, STICHTAG).values.tolist())
erwartet = ([5], [["bewerbung", 2, 1], ["newsletter", 1, 1], ["rechnung", 1, 0]])
assert ergebnis == erwartet, f"ohne_frist und bericht ergeben {ergebnis!r}, erwartet war {erwartet!r}."

# bericht hat genau die drei Spalten, und daten und fristen bleiben unverändert
spalten = list(bericht(daten, fristen, STICHTAG).columns)
assert spalten == ["kategorie", "datensaetze", "faellig"] and daten.equals(daten_vorher) and fristen.equals(lade(FRISTEN)), (
    f"bericht liefert die Spalten {spalten} (erwartet ['kategorie', 'datensaetze', 'faellig']); daten und fristen "
    "sollen unverändert bleiben."
)

# Genau am Stichtag fällig; Frist 0 Tage
roh = lade(als_csv([(1, "a", "2024-12-31", "K"), (2, "a", "2024-12-30", "K"), (3, "b", "2025-01-01", "K"),
                    (4, "b", "2025-01-02", "K")]))
daten = bereinige(roh)
fristen = lade(fristen_csv([("a", 1), ("b", 0)]))
ergebnis = (faellige(daten, fristen, STICHTAG)["id"].tolist(), bericht(daten, fristen, STICHTAG).values.tolist())
erwartet = ([2, 1, 3], [["a", 2, 2], ["b", 2, 1]])
assert ergebnis == erwartet, (
    "Mit Fristen a: 1 Tag, b: 0 Tage und Stichtag 2025-01-01 ergeben faellige(…)['id'] und bericht(…) "
    f"{ergebnis!r}, erwartet war {erwartet!r}.\nTipp: Am Stichtag selbst ist ein Datensatz schon fällig "
    "(loeschen_ab <= stichtag); sortiert wird nach loeschen_ab, dann nach id."
)

# Gleicher Löschtermin: nach id sortiert
roh = lade(als_csv([(30, "x", "2020-05-05", "K"), (10, "x", "2020-05-05", "K"), (20, "y", "2020-05-04", "K")]))
fristen = lade(fristen_csv([("x", 10), ("y", 11)]))
ergebnis = faellige(bereinige(roh), fristen, STICHTAG)["id"].tolist()
assert ergebnis == [10, 20, 30], (
    f"Drei Datensätze mit demselben Löschtermin ergeben bei faellige die ids {ergebnis!r}, erwartet war [10, 20, 30]."
)

# Gleich viele fällige: nach kategorie sortiert
roh = lade(als_csv([(1, "zeugnis", "2000-01-01", "K"), (2, "akte", "2000-01-01", "K"), (3, "mail", "2024-12-01", "K")]))
fristen = lade(fristen_csv([("zeugnis", 1), ("akte", 1), ("mail", 365), ("fax", 3)]))
ergebnis = bericht(bereinige(roh), fristen, STICHTAG).values.tolist()
assert ergebnis == [["akte", 1, 1], ["zeugnis", 1, 1], ["mail", 1, 0]], (
    f"bericht ergibt {ergebnis!r}, erwartet war [['akte', 1, 1], ['zeugnis', 1, 1], ['mail', 1, 0]].\n"
    "Tipp: sort_values([\"faellig\", \"kategorie\"], ascending=[False, True]); Kategorien ohne Datensatz (fax) "
    "kommen nicht vor."
)

# Leere Rohdaten
daten = bereinige(lade(als_csv([])))
fristen = lade(FRISTEN)
ergebnis = (len(daten), len(faellige(daten, fristen, STICHTAG)), ohne_frist(daten, fristen),
            len(bericht(daten, fristen, STICHTAG)))
assert ergebnis == (0, 0, [], 0), (
    f"Bei leeren Rohdaten ergeben len(bereinige(…)), len(faellige(…)), ohne_frist(…) und len(bericht(…)) "
    f"{ergebnis!r}, erwartet war (0, 0, [], 0)."
)

# Alle Kategorien ohne Frist
daten = bereinige(lade(als_csv([(9, "fotos", "2020-01-01", "K"), (3, "Fotos", "2021-01-01", "K")])))
ergebnis = (ohne_frist(daten, lade(FRISTEN)), len(bericht(daten, lade(FRISTEN), STICHTAG)))
assert ergebnis == ([3, 9], 0), (
    f"Bei zwei Datensätzen der Kategorie fotos ohne Frist ergeben ohne_frist und len(bericht(…)) {ergebnis!r}, "
    "erwartet war ([3, 9], 0)."
)


# Vergleichslösung in reinem Python
def auswertung_von_hand(zeilen, paare, stichtag):
    """Rechnet bereinigen, faellige, ohne_frist und bericht mit Schleifen und datetime nach."""
    import datetime

    frist_von = dict(paare)
    gesehen = set()
    sauber = []
    for nummer, kategorie, erstellt, _ in zeilen:
        try:
            datum = datetime.datetime.strptime(erstellt, "%Y-%m-%d")
        except ValueError:
            continue
        if nummer in gesehen:
            continue
        gesehen.add(nummer)
        sauber.append((nummer, kategorie.strip().lower(), datum))
    grenze = stichtag.to_pydatetime()
    faellig = []
    ohne = []
    zaehler = {}
    for nummer, kategorie, datum in sauber:
        if kategorie not in frist_von:
            ohne.append(nummer)
            continue
        termin = datum + datetime.timedelta(days=frist_von[kategorie])
        anzahl, faellige_anzahl = zaehler.get(kategorie, (0, 0))
        if termin <= grenze:
            faellig.append((termin, nummer))
            faellige_anzahl += 1
        zaehler[kategorie] = (anzahl + 1, faellige_anzahl)
    zeilen_bericht = [[kategorie, anzahl, fa] for kategorie, (anzahl, fa) in zaehler.items()]
    zeilen_bericht.sort(key=lambda zeile: (-zeile[2], zeile[0]))
    return [nummer for _, nummer in sorted(faellig)], sorted(ohne), zeilen_bericht, [nummer for nummer, _, _ in sauber]


def zufallsdaten(zufall, anzahl):
    """Erzeugt anzahl zufällige Rohzeilen mit Leerzeichen, Schreibweisen, ungültigen Daten und Dubletten."""
    kategorien = ["bewerbung", "rechnung", "newsletter", "kontakt", "fotos"]
    zeilen = []
    for _ in range(anzahl):
        kategorie = zufall.choice(kategorien)
        kategorie = zufall.choice([kategorie, kategorie.upper(), kategorie.capitalize(), f" {kategorie}  "])
        jahr, monat, tag = zufall.randint(1990, 2030), zufall.randint(1, 12), zufall.randint(1, 31)
        erstellt = zufall.choice([f"{jahr}-{monat:02d}-{tag:02d}"] * 4 + ["", "unbekannt", f"{tag:02d}.{monat:02d}.{jahr}"])
        zeilen.append((zufall.randint(1, anzahl + 3), kategorie, erstellt, f"K-{zufall.randint(1, 99)}"))
    return zeilen


# 60 zufällige Exporte
zufall = Zufall(5018)
for _ in range(60):
    zeilen = zufallsdaten(zufall, zufall.randint(0, 25))
    paare = [(kategorie, zufall.randint(0, 5000)) for kategorie in ["bewerbung", "rechnung", "newsletter", "kontakt"]
             if zufall.random() < 0.8]
    if not paare:
        paare = [("rechnung", 3650)]
    stichtag = pd.Timestamp(f"{zufall.randint(1995, 2035)}-{zufall.randint(1, 12):02d}-15")
    daten = bereinige(lade(als_csv(zeilen)))
    fristen = lade(fristen_csv(paare))
    erwartet_faellig, erwartet_ohne, erwartet_bericht, erwartet_ids = auswertung_von_hand(zeilen, paare, stichtag)
    ergebnis = (daten["id"].tolist(), faellige(daten, fristen, stichtag)["id"].tolist(), ohne_frist(daten, fristen),
                bericht(daten, fristen, stichtag).values.tolist())
    erwartet = (erwartet_ids, erwartet_faellig, erwartet_ohne, erwartet_bericht)
    assert ergebnis == erwartet, (
        f"Für die Rohdaten {zeilen}, die Fristen {paare} und den Stichtag {stichtag.date()} ergeben die ids nach "
        f"bereinige, faellige(…)['id'], ohne_frist und bericht(…).values.tolist() {ergebnis!r}, erwartet war {erwartet!r}."
    )

# Obere Grenze: 100 000 Zeilen
zufall = Zufall(50180)
zeilen = zufallsdaten(zufall, 100000)
paare = [("bewerbung", 180), ("rechnung", 3650), ("newsletter", 730), ("kontakt", 36500)]
daten = bereinige(lade(als_csv(zeilen)))
fristen = lade(fristen_csv(paare))
erwartet_faellig, erwartet_ohne, erwartet_bericht, erwartet_ids = auswertung_von_hand(zeilen, paare, STICHTAG)
bekommen_faellig = faellige(daten, fristen, STICHTAG)["id"].tolist()
bekommen_ohne = ohne_frist(daten, fristen)
ergebnis = (len(daten), bekommen_faellig == erwartet_faellig, bekommen_ohne == erwartet_ohne,
            bericht(daten, fristen, STICHTAG).values.tolist())
erwartet = (len(erwartet_ids), True, True, erwartet_bericht)
assert ergebnis == erwartet, (
    "Bei 100 000 Rohzeilen ergeben len(bereinige(…)), faellige stimmt, ohne_frist stimmt und bericht "
    f"{ergebnis!r}, erwartet war {erwartet!r}.\n"
    f"  faellige: {len(bekommen_faellig)} ids, die ersten {bekommen_faellig[:5]}; "
    f"erwartet {len(erwartet_faellig)}, die ersten {erwartet_faellig[:5]}\n"
    f"  ohne_frist: {len(bekommen_ohne)} ids, die ersten {bekommen_ohne[:5]}; "
    f"erwartet {len(erwartet_ohne)}, die ersten {erwartet_ohne[:5]}"
)

# Keine Schleife über die Zeilen
import inspect

schleifen = {}
for funktion in [bereinige, loeschtermine, faellige, ohne_frist, bericht]:
    try:
        quelltext = inspect.getsource(funktion)
    except (OSError, TypeError):
        quelltext = ""
    gefunden = [stueck for stueck in ["iterrows", "itertuples", "to_dict", "range(len("] if stueck in quelltext]
    if gefunden:
        schleifen[funktion.__name__] = gefunden
assert schleifen == {}, (
    f"Laut Aufgabe ohne Schleife über die Zeilen, gefunden: {schleifen}.\n"
    "Tipp: Bearbeiten Sie ganze Spalten auf einmal (.str, isin, merge, groupby), wie im Hintergrund gezeigt."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "[1, 2, 4, 5, 6]\n[4, 1]\n[5]\n[['bewerbung', 2, 1], ['newsletter', 1, 1], ['rechnung', 1, 0]]"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
