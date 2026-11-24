# Automatisch erzeugt aus lehrkraft/muster/5_059_stundenabgleich.py - nicht von Hand ändern.
# vorlage-hash: 251c675156acc7f7
# text-hash: 0060673b762330f0
# thema: fehler
# inhalt: Profiling mit cProfile und pstats

MITARBEITER = [(101, "Ada Berg", "Vertrieb"), (102, "Bo Lang", "IT"), (103, "Cem Koch", "IT")]
BUCHUNGEN = [(102, 7.5), (101, 8.0), (103, 6.0), (999, 4.0), (102, 13.0)]


def rufe(aufruf):
    """Führt aufruf() aus; liefert (Ergebnis, Fehlertext oder None)."""
    try:
        return aufruf(), None
    except Exception as fehler:
        return None, f"{type(fehler).__name__}: {fehler}"


def absturz(fehler):
    """Ergänzt eine Meldung um den Fehlertext, falls es einen gab."""
    return f"\nDer Aufruf löst {fehler} aus." if fehler else ""


def fibonacci(n):
    """Rekursiv und absichtlich ohne Gedächtnis: ruft sich sehr oft selbst auf."""
    return n if n < 2 else fibonacci(n - 1) + fibonacci(n - 2)


def mit_lambda_und_builtins(werte):
    """Benutzt sorted, sum, ein lambda und einen Generator-Ausdruck, aber keine benannte Hilfsfunktion."""
    return sum(wert * 2 for wert in sorted(werte, key=lambda wert: -wert))


def schnell():
    """Eine billige Funktion."""
    return 1


def langsam():
    """Eine teure Funktion: viele Zeilen in einer Schleife."""
    summe = 0
    for zahl in range(200_000):
        summe += zahl % 7
    return summe


def gemischt():
    """Ruft die billige Funktion oft und die teure einmal auf."""
    for _ in range(100):
        schnell()
    return langsam()


def vergleich_summen(buchungen, mitarbeiter):
    """Vergleichslösung: sortiert das Verzeichnis und sucht mit bisect."""
    import bisect

    sortiert = sorted(mitarbeiter)
    nummern = [eintrag[0] for eintrag in sortiert]
    summen = {}
    for nummer, stunden in buchungen:
        if not 0 < stunden <= 12:
            continue
        stelle = bisect.bisect_left(nummern, nummer)
        abteilung = sortiert[stelle][2] if stelle < len(nummern) and nummern[stelle] == nummer else "unbekannt"
        summen[abteilung] = summen.get(abteilung, 0) + stunden
    return summen


# aufrufe: das Beispiel aus der Aufgabe
ergebnis, fehler = rufe(lambda: aufrufe(stunden_je_abteilung_langsam, BUCHUNGEN, MITARBEITER))
erwartet = {"stunden_je_abteilung_langsam": 1, "ist_gueltig": 5, "finde_mitarbeiter": 4}
assert ergebnis == erwartet, (
    f"aufrufe(stunden_je_abteilung_langsam, buchungen, mitarbeiter) ergibt\n{ergebnis!r},\nerwartet war\n{erwartet!r}.\n"
    "Tipp: profil = cProfile.Profile(); profil.runcall(funktion, *argumente); dann pstats.Stats(profil).stats "
    "durchgehen und für jeden Namen ohne < die Zahl aller Aufrufe (zweiter Wert) addieren." + absturz(fehler)
)

# aufrufe: andere Daten (nicht fest hinschreiben!)
buchungen = [(101, 1.0), (101, -2.0), (102, 3.0)]
ergebnis, fehler = rufe(lambda: aufrufe(stunden_je_abteilung_langsam, buchungen, MITARBEITER))
erwartet = {"stunden_je_abteilung_langsam": 1, "ist_gueltig": 3, "finde_mitarbeiter": 2}
assert ergebnis == erwartet, f"aufrufe(stunden_je_abteilung_langsam, {buchungen}, mitarbeiter) ergibt {ergebnis!r}, erwartet war {erwartet!r}." + absturz(fehler)

# aufrufe: ohne eingebaute Funktionen, lambda und Generator-Ausdrücke
ergebnis, fehler = rufe(lambda: aufrufe(mit_lambda_und_builtins, [3, 1, 2]))
assert ergebnis == {"mit_lambda_und_builtins": 1}, (
    f"aufrufe(mit_lambda_und_builtins, [3, 1, 2]) ergibt {ergebnis!r}, erwartet war {{'mit_lambda_und_builtins': 1}}: "
    "sorted, sum, <lambda> und <genexpr> gehören nicht dazu.\nTipp: Lassen Sie jeden Namen weg, der mit < beginnt."
    + absturz(fehler)
)

# aufrufe: rekursive Aufrufe zählen mit
ergebnis, fehler = rufe(lambda: aufrufe(fibonacci, 10))
assert ergebnis == {"fibonacci": 177}, (
    f"aufrufe(fibonacci, 10) ergibt {ergebnis!r}, erwartet war {{'fibonacci': 177}}.\n"
    "Tipp: Nehmen Sie aus pstats die Zahl aller Aufrufe (der zweite Wert), nicht die der direkten (der erste)."
    + absturz(fehler)
)

# aufrufe: eine Funktion ohne weitere Aufrufe, und Argumente werden weitergereicht
ergebnis, fehler = rufe(lambda: aufrufe(ist_gueltig, (5, 3.0)))
assert ergebnis == {"ist_gueltig": 1}, f"aufrufe(ist_gueltig, (5, 3.0)) ergibt {ergebnis!r}, erwartet war {{'ist_gueltig': 1}}." + absturz(fehler)

# aufrufe: leere Buchungen
ergebnis, fehler = rufe(lambda: aufrufe(stunden_je_abteilung_langsam, [], MITARBEITER))
assert ergebnis == {"stunden_je_abteilung_langsam": 1}, (
    f"aufrufe(stunden_je_abteilung_langsam, [], mitarbeiter) ergibt {ergebnis!r}, erwartet war "
    "{'stunden_je_abteilung_langsam': 1}." + absturz(fehler)
)

# engpass: die teure Funktion, auch wenn die billige öfter läuft
ergebnis, fehler = rufe(lambda: engpass(gemischt))
assert ergebnis == "langsam", (
    f"engpass(gemischt) ergibt {ergebnis!r}, erwartet war 'langsam': schnell läuft 100-mal, aber fast ohne Zeit."
    + (
        "\nTipp: gemischt hat zwar die größte Gesamtzeit (cumtime), weil es langsam aufruft, aber selbst kaum "
        "Eigenzeit (tottime, der dritte Wert in pstats)."
        if ergebnis == "gemischt"
        else "\nTipp: Vergleichen Sie die Eigenzeit (tottime, der dritte Wert in pstats), nicht die Zahl der Aufrufe."
    )
    + absturz(fehler)
)

# engpass: das Beispiel, finde_mitarbeiter ist der Engpass
viele_mitarbeiter = [(nummer, f"Person {nummer}", f"Abteilung {nummer % 7}") for nummer in range(1, 1001)]
viele_buchungen = [(nummer * 7 % 1000 + 1, 8.0) for nummer in range(1000)]
ergebnis, fehler = rufe(lambda: engpass(stunden_je_abteilung_langsam, viele_buchungen, viele_mitarbeiter))
assert ergebnis == "finde_mitarbeiter", (
    f"engpass(stunden_je_abteilung_langsam, 1000 Buchungen, 1000 Beschäftigte) ergibt {ergebnis!r}, erwartet war "
    "'finde_mitarbeiter'." + absturz(fehler)
)

# stunden_je_abteilung: das Beispiel
ergebnis, fehler = rufe(lambda: stunden_je_abteilung(BUCHUNGEN, MITARBEITER))
assert ergebnis == {"IT": 13.5, "Vertrieb": 8.0, "unbekannt": 4.0}, (
    f"stunden_je_abteilung(buchungen, mitarbeiter) ergibt {ergebnis!r}, erwartet war "
    "{'IT': 13.5, 'Vertrieb': 8.0, 'unbekannt': 4.0}." + absturz(fehler)
)

# stunden_je_abteilung: ungültige Buchungen zählen nicht, auch nicht 0 und 12.25
buchungen = [(101, 0.0), (101, 12.0), (102, 12.25), (103, -3.0), (103, 0.25)]
ergebnis, fehler = rufe(lambda: stunden_je_abteilung(buchungen, MITARBEITER))
assert ergebnis == {"Vertrieb": 12.0, "IT": 0.25}, (
    f"stunden_je_abteilung({buchungen}, mitarbeiter) ergibt {ergebnis!r}, erwartet war {{'Vertrieb': 12.0, 'IT': 0.25}}.\n"
    "Tipp: Behalten Sie die Prüfung mit ist_gueltig bei." + absturz(fehler)
)

# stunden_je_abteilung: unbekannte Nummern und ein leeres Verzeichnis
ergebnis, fehler = rufe(lambda: (stunden_je_abteilung([(5, 1.0), (6, 2.0)], []), stunden_je_abteilung([], MITARBEITER)))
assert ergebnis == ({"unbekannt": 3.0}, {}), (
    f"stunden_je_abteilung ohne Verzeichnis und ohne Buchungen ergibt {ergebnis!r}, erwartet war ({{'unbekannt': 3.0}}, {{}})."
    + absturz(fehler)
)

# stunden_je_abteilung: ruft finde_mitarbeiter nicht mehr auf
ergebnis, fehler = rufe(lambda: aufrufe(stunden_je_abteilung, BUCHUNGEN, MITARBEITER))
assert ergebnis is not None and "finde_mitarbeiter" not in ergebnis, (
    f"Ihr Profil von stunden_je_abteilung zeigt {ergebnis!r}: finde_mitarbeiter wird noch aufgerufen und geht jedes "
    "Mal das ganze Verzeichnis durch.\nTipp: Bauen Sie einmal vorab ein Dictionary personalnummer → abteilung."
    + absturz(fehler)
)

zufall = Zufall(5059)

# Viele zufällige Daten im Vergleich mit der langsamen Fassung
for _ in range(100):
    nummern = zufall.sample(range(1, 60), zufall.randint(0, 20))
    mitarbeiter = [(nummer, f"P{nummer}", zufall.choice(["IT", "Vertrieb", "Lager", "Einkauf"])) for nummer in nummern]
    buchungen = [(zufall.randint(1, 70), zufall.randint(-96, 96) / 4) for _ in range(zufall.randint(0, 30))]
    ergebnis, fehler = rufe(lambda: stunden_je_abteilung(buchungen, mitarbeiter))
    erwartet = vergleich_summen(buchungen, mitarbeiter)
    assert ergebnis == erwartet, (
        f"stunden_je_abteilung({buchungen}, {mitarbeiter}) ergibt {ergebnis!r}, erwartet war {erwartet!r}." + absturz(fehler)
    )

# Laufzeit: O(n + m) Schritte
def daten(anzahl):
    """anzahl Beschäftigte und anzahl Buchungen."""
    mitarbeiter = [(nummer, f"P{nummer}", f"A{nummer % 5}") for nummer in range(1, anzahl + 1)]
    buchungen = [(nummer * 7 % anzahl + 1, 8.0) for nummer in range(anzahl)]
    return buchungen, mitarbeiter


_, schritte_klein = zaehle_schritte(stunden_je_abteilung, *daten(500))
ergebnis, schritte_gross = zaehle_schritte(stunden_je_abteilung, *daten(2000))
assert ergebnis == vergleich_summen(*daten(2000)) and schritte_gross <= 5 * schritte_klein + 50, (
    f"stunden_je_abteilung braucht für 500 Buchungen und Beschäftigte {schritte_klein} Schritte, für 2000 "
    f"{schritte_gross}; bei O(n + m) wäre es etwa das Vierfache."
)

# Obere Grenze: je 100000 Buchungen und Beschäftigte
buchungen, mitarbeiter = daten(100_000)
ergebnis, fehler = rufe(lambda: stunden_je_abteilung(buchungen, mitarbeiter))
assert ergebnis == {f"A{rest}": 160_000.0 for rest in range(5)}, (
    f"stunden_je_abteilung mit je 100000 Einträgen ergibt {str(ergebnis)[:120]}, erwartet waren 160000.0 Stunden "
    "in jeder der Abteilungen A0 bis A4." + absturz(fehler)
)
