"""Aufgabe 5_059 – Stundenabgleich                               Stufe 5 ★★★★★

Die Personalabteilung führt jeden Monatsanfang einen Abgleich durch: Aus
der Zeiterfassung kommen die Buchungen als Paare (personalnummer,
stunden), aus dem Mitarbeiterverzeichnis die Einträge (personalnummer,
name, abteilung). Das Skript summiert die gültigen Stunden je Abteilung,
damit das Controlling sie den Kostenstellen zuordnen kann. Eine Buchung
ist gültig, wenn ihre Stunden größer als 0 und höchstens 12 sind;
Buchungen mit einer Nummer, die nicht im Verzeichnis steht, zählen unter
"unbekannt". Mit 200 Beschäftigten lief das Skript in Sekundenbruchteilen,
nach der Fusion mit einer anderen Firma braucht es eine halbe Stunde.

Statt zu raten, wo die Zeit bleibt, misst man sie mit einem Profiler
(siehe Hintergrund). Das langsame Skript ist vorgegeben. Schreiben Sie:

- `_messung(funktion, argumente)` ist eine Hilfsfunktion für die beiden
  nächsten: Sie ruft funktion(*argumente) unter cProfile auf und gibt
  die Einträge der Auswertung zurück (siehe Hintergrund).
- `aufrufe(funktion, *argumente)` ruft funktion(*argumente) unter
  cProfile auf und gibt ein Dictionary zurück: Name jeder dabei
  aufgerufenen Python-Funktion → wie oft sie aufgerufen wurde (alle
  Aufrufe, auch rekursive). Einträge, deren Name mit "<" beginnt
  (eingebaute Funktionen, <lambda>, <genexpr> …), lassen Sie weg.
- `engpass(funktion, *argumente)` ruft funktion(*argumente) unter
  cProfile auf und gibt den Namen der Python-Funktion zurück, die die
  meiste Eigenzeit (tottime) verbraucht hat, mit derselben Ausnahme.
- `stunden_je_abteilung(buchungen, mitarbeiter)` liefert dasselbe
  Ergebnis wie `stunden_je_abteilung_langsam`, aber in
  O(len(buchungen) + len(mitarbeiter)) Schritten. Behalten Sie
  ist_gueltig bei, ersetzen Sie nur den Engpass.

    mitarbeiter = [(101, "Ada Berg", "Vertrieb"), (102, "Bo Lang", "IT"),
                   (103, "Cem Koch", "IT")]
    buchungen = [(102, 7.5), (101, 8.0), (103, 6.0), (999, 4.0), (102, 13.0)]
    stunden_je_abteilung_langsam(buchungen, mitarbeiter)
        →  {"IT": 13.5, "Vertrieb": 8.0, "unbekannt": 4.0}
    aufrufe(stunden_je_abteilung_langsam, buchungen, mitarbeiter)
        →  {"stunden_je_abteilung_langsam": 1, "ist_gueltig": 5,
            "finde_mitarbeiter": 4}
    engpass(stunden_je_abteilung_langsam, viele_buchungen, viele_mitarbeiter)
        →  "finde_mitarbeiter"

Grenzen: buchungen und mitarbeiter haben je 0 bis 100 000 Einträge;
Personalnummern sind ganze Zahlen von 1 bis 10**7, im Verzeichnis ohne
Doppelte; stunden sind Vielfache von 0.25 von -24 bis 24, abteilung ein
nicht leerer Text. funktion ist eine Python-Funktion, die die übergebenen
Argumente annimmt; bei engpass verbraucht genau eine Funktion deutlich
die meiste Eigenzeit.

Hintergrund: Ein Profiler beobachtet ein laufendes Programm und
notiert für jede Funktion, wie oft sie aufgerufen wurde und wie lange
sie lief. cProfile aus der Standardbibliothek erfasst jeden Aufruf und
jede Rückkehr; das Modul pstats wertet die Messung aus:

    import cProfile
    import pstats

    profil = cProfile.Profile()
    ergebnis = profil.runcall(stunden_je_abteilung_langsam, buchungen, mitarbeiter)
    statistik = pstats.Stats(profil)
    statistik.sort_stats("tottime").print_stats(5)    # die fünf teuersten

       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        20000   14.210    0.001   14.210    0.001 skript.py:31(finde_mitarbeiter)
            1    0.012    0.012   14.231   14.231 skript.py:40(stunden_je_…)
        20000    0.009    0.000    0.009    0.000 skript.py:27(ist_gueltig)

Von der Kommandozeile geht dasselbe mit python -m cProfile -s tottime
skript.py. ncalls ist die Zahl der Aufrufe (bei Rekursion „gesamt/
direkt“, etwa 177/1), tottime die Eigenzeit ohne aufgerufene Funktionen,
cumtime die Zeit einschließlich allem, was die Funktion aufruft. Der
Engpass ist meist die Funktion mit der größten Eigenzeit; eine große
cumtime bei kleiner tottime heißt dagegen nur „ruft etwas Teures auf“.

Für eigene Auswertungen steht alles im Dictionary statistik.stats. Jeder
Schlüssel ist ein Tupel (dateiname, zeile, funktionsname), jeder Wert ein
Tupel (direkte_aufrufe, alle_aufrufe, tottime, cumtime, aufrufer):

    for (datei, zeile, name), (direkt, alle, eigen, gesamt, _) in statistik.stats.items():
        print(name, alle, eigen)

Eingebaute Funktionen stehen dort mit Namen wie "<built-in method
builtins.sum>", Generator-Ausdrücke als "<genexpr>". Ein Name kann in
mehreren Dateien vorkommen; dann zählen Sie die Aufrufe zusammen.

Die Messung selbst kostet Zeit (jeder Aufruf wird protokolliert), und die
Zeiten schwanken von Lauf zu Lauf; verlässlich ist die Größenordnung und
die Zahl der Aufrufe. Hier zeigt sie: finde_mitarbeiter wird für jede
Buchung aufgerufen und geht jedes Mal das ganze Verzeichnis durch, also
O(n · m). Abhilfe wie in Aufgabe 5_058: einmal vorab ein Dictionary
personalnummer → abteilung bauen. Danach misst man noch einmal, denn
oft wird dann eine andere Funktion zum Engpass. Wer innerhalb einer
Funktion wissen will, welche Zeile teuer ist, nimmt einen
zeilenweisen Profiler wie das Paket line_profiler (nicht in der
Standardbibliothek): Er zeigt für jede Zeile Anzahl und Zeit. Die Tests
dieser Aufgabe prüfen die Laufzeit Ihrer schnellen Fassung trotzdem über
gezählte Schritte, nicht über die Uhr.
"""

import cProfile
import pstats


def ist_gueltig(buchung):
    """Prüft, ob die Stunden einer Buchung größer als 0 und höchstens 12 sind."""
    _, stunden = buchung
    return 0 < stunden <= 12


def finde_mitarbeiter(nummer, mitarbeiter):
    """Sucht den Eintrag mit der Personalnummer nummer; None, wenn es keinen gibt."""
    for eintrag in mitarbeiter:
        if eintrag[0] == nummer:
            return eintrag
    return None


def stunden_je_abteilung_langsam(buchungen, mitarbeiter):
    """Summiert die gültigen Stunden je Abteilung (langsam: sucht jede Nummer im ganzen Verzeichnis)."""
    summen = {}
    for buchung in buchungen:
        if not ist_gueltig(buchung):
            continue
        eintrag = finde_mitarbeiter(buchung[0], mitarbeiter)
        abteilung = "unbekannt" if eintrag is None else eintrag[2]
        summen[abteilung] = summen.get(abteilung, 0) + buchung[1]
    return summen


def _messung(funktion, argumente):
    """Ruft funktion(*argumente) unter cProfile auf und gibt die Einträge aus pstats zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def aufrufe(funktion, *argumente):
    """Gibt zu jeder aufgerufenen Python-Funktion zurück, wie oft sie aufgerufen wurde."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def engpass(funktion, *argumente):
    """Gibt den Namen der Python-Funktion mit der größten Eigenzeit zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def stunden_je_abteilung(buchungen, mitarbeiter):
    """Summiert die gültigen Stunden je Abteilung in O(n + m) Schritten."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


mitarbeiter = [(101, "Ada Berg", "Vertrieb"), (102, "Bo Lang", "IT"), (103, "Cem Koch", "IT")]
buchungen = [(102, 7.5), (101, 8.0), (103, 6.0), (999, 4.0), (102, 13.0)]
print(stunden_je_abteilung_langsam(buchungen, mitarbeiter))
print(aufrufe(stunden_je_abteilung_langsam, buchungen, mitarbeiter))
print(stunden_je_abteilung(buchungen, mitarbeiter))

viele_mitarbeiter = [(nummer, f"Person {nummer}", f"Abteilung {nummer % 7}") for nummer in range(1, 1001)]
viele_buchungen = [(nummer * 7 % 1000 + 1, 8.0) for nummer in range(1000)]
print(engpass(stunden_je_abteilung_langsam, viele_buchungen, viele_mitarbeiter))
