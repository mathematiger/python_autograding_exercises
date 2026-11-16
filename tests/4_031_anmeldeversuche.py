# Automatisch erzeugt aus lehrkraft/muster/4_031_anmeldeversuche.py - nicht von Hand ändern.
# vorlage-hash: 7db8900de20503ab
# text-hash: 7332071edbe00451
# thema: datenanalyse
# inhalt: polars: select, filter, Ausdrücke

SCHEMA = {"benutzer": pl.String, "fehlversuche": pl.Int64, "erfolge": pl.Int64, "admin": pl.Boolean}


def beispiel_zeilen():
    """Die Zeilen aus dem Beispiel als Liste von Dictionaries."""
    return [
        {"benutzer": "abauer", "fehlversuche": 1, "erfolge": 4, "admin": False},
        {"benutzer": "root", "fehlversuche": 9, "erfolge": 1, "admin": True},
        {"benutzer": "ckaya", "fehlversuche": 6, "erfolge": 2, "admin": False},
        {"benutzer": "dlang", "fehlversuche": 3, "erfolge": 0, "admin": True},
        {"benutzer": "emeyer", "fehlversuche": 7, "erfolge": 8, "admin": False},
    ]


def tabelle(zeilen):
    """Baut einen DataFrame mit festen Spaltentypen, auch wenn zeilen leer ist."""
    return pl.DataFrame(zeilen, schema=SCHEMA)


def auffaellige_von_hand(zeilen, grenze):
    """Vergleichslösung mit einer Schleife über die Dictionaries."""
    return [{"benutzer": z["benutzer"], "fehlversuche": z["fehlversuche"]} for z in zeilen if z["fehlversuche"] >= grenze]


def quote_von_hand(zeile):
    """Vergleichslösung für die Quote einer Zeile."""
    return zeile["fehlversuche"] / (zeile["fehlversuche"] + zeile["erfolge"])


def sperren_von_hand(zeilen):
    """Vergleichslösung für zu_sperren mit einer Schleife."""
    namen = []
    for z in zeilen:
        if (quote_von_hand(z) > 0.5 and z["fehlversuche"] >= 5) or (z["admin"] and z["fehlversuche"] >= 3):
            namen.append(z["benutzer"])
    return sorted(namen)


def als_zeilen(ergebnis):
    """Wandelt einen DataFrame in eine Liste von Dictionaries; sonst None."""
    if not isinstance(ergebnis, pl.DataFrame):
        return None
    return ergebnis.to_dicts()


def zufallszeilen(zufall, anzahl):
    """Baut anzahl zufällige Konten mit verschiedenen Namen."""
    zeilen = []
    for nummer in range(anzahl):
        fehl = zufall.randint(0, 12)
        erfolg = zufall.randint(0 if fehl else 1, 12)
        zeilen.append({"benutzer": f"konto{nummer:03d}{zufall.choice('xyz')}", "fehlversuche": fehl,
                       "erfolge": erfolg, "admin": zufall.random() < 0.3})
    zufall.shuffle(zeilen)
    return zeilen


# auffaellige filtert die Zeilen aus dem Beispiel
ergebnis = auffaellige(tabelle(beispiel_zeilen()), 6)
namen = ergebnis["benutzer"].to_list() if isinstance(ergebnis, pl.DataFrame) else ergebnis
assert namen == ["root", "ckaya", "emeyer"], (
    f'auffaellige(konten, 6)["benutzer"].to_list() ergibt {namen!r}, erwartet war ["root", "ckaya", "emeyer"].\n'
    'Tipp: konten.filter(pl.col("fehlversuche") >= grenze) behält die passenden Zeilen.'
)

# auffaellige behält nur die Spalten benutzer und fehlversuche
ergebnis = auffaellige(tabelle(beispiel_zeilen()), 6)
spalten = ergebnis.columns if isinstance(ergebnis, pl.DataFrame) else ergebnis
assert spalten == ["benutzer", "fehlversuche"], (
    f"auffaellige(konten, 6) hat die Spalten {spalten!r}, erwartet waren ['benutzer', 'fehlversuche'].\n"
    'Tipp: Hängen Sie .select("benutzer", "fehlversuche") an.'
)

# auffaellige mit einer anderen Grenze (nicht fest hinschreiben!)
ergebnis = als_zeilen(auffaellige(tabelle(beispiel_zeilen()), 3))
erwartet = auffaellige_von_hand(beispiel_zeilen(), 3)
assert ergebnis == erwartet, f"auffaellige(konten, 3).to_dicts() ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Genau grenze Fehlversuche zählen schon als auffällig
ergebnis = als_zeilen(auffaellige(tabelle(beispiel_zeilen()), 9))
assert ergebnis == [{"benutzer": "root", "fehlversuche": 9}], (
    f"auffaellige(konten, 9).to_dicts() ergibt {ergebnis!r}, erwartet war [{{'benutzer': 'root', 'fehlversuche': 9}}].\n"
    "Tipp: Mindestens grenze heißt >= grenze."
)

# Grenze 0: alle Konten sind auffällig
ergebnis = als_zeilen(auffaellige(tabelle(beispiel_zeilen()), 0))
erwartet = auffaellige_von_hand(beispiel_zeilen(), 0)
assert ergebnis == erwartet, f"auffaellige(konten, 0).to_dicts() ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# mit_quote aus dem Beispiel
ergebnis = mit_quote(tabelle(beispiel_zeilen()))
quoten = ergebnis["quote"].to_list() if isinstance(ergebnis, pl.DataFrame) and "quote" in ergebnis.columns else ergebnis
erwartet = [quote_von_hand(z) for z in beispiel_zeilen()]
assert isinstance(quoten, list) and len(quoten) == 5 and all(abs(a - b) < 1e-9 for a, b in zip(quoten, erwartet)), (
    f'mit_quote(konten)["quote"].to_list() ergibt {quoten!r}, erwartet war {erwartet!r}.\n'
    'Tipp: pl.col("fehlversuche") / (pl.col("fehlversuche") + pl.col("erfolge")), mit .alias("quote") benannt.'
)

# mit_quote behält alle Spalten und hängt quote hinten an
ergebnis = mit_quote(tabelle(beispiel_zeilen()))
spalten = ergebnis.columns if isinstance(ergebnis, pl.DataFrame) else ergebnis
assert spalten == ["benutzer", "fehlversuche", "erfolge", "admin", "quote"], (
    f"mit_quote(konten) hat die Spalten {spalten!r}, erwartet waren alle vier und dahinter quote.\n"
    "Tipp: with_columns behält die vorhandenen Spalten, select nicht."
)

# mit_quote lässt die übergebene Tabelle unverändert
daten = tabelle(beispiel_zeilen())
mit_quote(daten)
auffaellige(daten, 5)
assert daten.columns == list(SCHEMA) and daten.to_dicts() == beispiel_zeilen(), (
    f"Nach mit_quote und auffaellige hat konten die Spalten {daten.columns}, erwartet war die Tabelle unverändert."
)

# zu_sperren aus dem Beispiel
ergebnis = zu_sperren(tabelle(beispiel_zeilen()))
assert ergebnis == ["ckaya", "dlang", "root"], (
    f"zu_sperren(konten) ergibt {ergebnis!r}, erwartet war ['ckaya', 'dlang', 'root'] (alphabetisch, als Liste)."
)

# zu_sperren: hohe Quote allein reicht nicht, es braucht auch 5 Fehlversuche
zeilen = [
    {"benutzer": "fwolf", "fehlversuche": 4, "erfolge": 0, "admin": False},
    {"benutzer": "gnagel", "fehlversuche": 5, "erfolge": 4, "admin": False},
    {"benutzer": "hott", "fehlversuche": 5, "erfolge": 5, "admin": False},
]
ergebnis = zu_sperren(tabelle(zeilen))
assert ergebnis == ["gnagel"], (
    f"zu_sperren mit {zeilen} ergibt {ergebnis!r}, erwartet war ['gnagel']: fwolf hat nur 4 Fehlversuche, "
    "hott genau die Quote 0.5, die nicht über 0.5 liegt."
)

# zu_sperren: Admin-Konten ab genau 3 Fehlversuchen
zeilen = [
    {"benutzer": "admin2", "fehlversuche": 2, "erfolge": 0, "admin": True},
    {"benutzer": "admin3", "fehlversuche": 3, "erfolge": 50, "admin": True},
    {"benutzer": "nutzer3", "fehlversuche": 3, "erfolge": 0, "admin": False},
]
ergebnis = zu_sperren(tabelle(zeilen))
assert ergebnis == ["admin3"], (
    f"zu_sperren mit {zeilen} ergibt {ergebnis!r}, erwartet war ['admin3']: Admin-Konten ab 3 Fehlversuchen, "
    "egal wie hoch die Quote ist; Konten ohne Admin-Rechte erst ab 5."
)

# Leere Tabelle
leer = tabelle([])
ergebnis = (als_zeilen(auffaellige(leer, 3)), zu_sperren(leer))
assert ergebnis == ([], []), f"Bei einer leeren Tabelle ergeben auffaellige(…).to_dicts() und zu_sperren {ergebnis!r}, erwartet war ([], [])."

# Leere Tabelle: mit_quote hat trotzdem die Spalte quote
ergebnis = mit_quote(leer)
spalten = ergebnis.columns if isinstance(ergebnis, pl.DataFrame) else ergebnis
assert spalten == ["benutzer", "fehlversuche", "erfolge", "admin", "quote"], (
    f"mit_quote(<leere Tabelle>) hat die Spalten {spalten!r}, erwartet waren alle vier und quote."
)

# Ränder: nur Fehlversuche oder nur Erfolge, Werte bis 10**6
zeilen = [
    {"benutzer": "a", "fehlversuche": 10**6, "erfolge": 0, "admin": False},
    {"benutzer": "b", "fehlversuche": 0, "erfolge": 10**6, "admin": True},
]
ergebnis = mit_quote(tabelle(zeilen))["quote"].to_list()
assert ergebnis == [1.0, 0.0], f"mit_quote mit {zeilen} ergibt die Quoten {ergebnis!r}, erwartet war [1.0, 0.0]."

# Mit Ausdrücken von polars statt einer Schleife
assert verwendet("filter") and verwendet("with_columns") and not verwendet("iter_rows") and not verwendet("to_dicts"), (
    "Arbeiten Sie mit den Methoden filter, select und with_columns und Ausdrücken mit pl.col, "
    "nicht mit einer Schleife über iter_rows oder to_dicts."
)

# 200 zufällige Tabellen
zufall = Zufall(4031)
for _ in range(200):
    zeilen = zufallszeilen(zufall, zufall.randint(0, 12))
    grenze = zufall.randint(0, 13)
    daten = tabelle(zeilen)
    ergebnis = als_zeilen(auffaellige(daten, grenze))
    erwartet = auffaellige_von_hand(zeilen, grenze)
    assert ergebnis == erwartet, f"auffaellige(<{zeilen}>, {grenze}).to_dicts() ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    ergebnis = zu_sperren(daten)
    erwartet = sperren_von_hand(zeilen)
    assert ergebnis == erwartet, f"zu_sperren(<{zeilen}>) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Obere Grenze: 100 000 Konten
zeilen = zufallszeilen(zufall, 100000)
daten = tabelle(zeilen)
ergebnis = (auffaellige(daten, 12).height, len(zu_sperren(daten)))
erwartet = (len(auffaellige_von_hand(zeilen, 12)), len(sperren_von_hand(zeilen)))
assert ergebnis == erwartet, (
    f"Bei 100 000 Konten ergeben auffaellige(…, 12).height und len(zu_sperren(…)) {ergebnis}, erwartet war {erwartet}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "['root', 'ckaya', 'emeyer']\n['ckaya', 'dlang', 'root']"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
