"""Aufgabe 5_006 – Anmelderisiko                                   Stufe 5 ★★★★★

Ein Anmeldedienst protokolliert jede erfolgreiche Anmeldung: welches
Konto, wie viele Fehlversuche mit falschem Passwort vorausgingen, aus
welchem Land die Anmeldung kam und zu welcher Stunde. Ein
Sicherheitswerkzeug vergibt jeder Anmeldung Risikopunkte, damit das
Sicherheitsteam auffällige Konten zuerst prüft:

- 10 Punkte für jeden Fehlversuch,
- 30 Punkte, wenn das Land nicht "DE" ist,
- 20 Punkte, wenn die Stunde vor 6 Uhr liegt (0 bis 5).

Die Regel steht schon als Funktion `risiko_zeile(zeile)` im Code; sie
bekommt eine Zeile des DataFrames und gibt deren Punkte zurück. Das
Protokoll eines Tages hat aber Hunderttausende Zeilen, und die Auswertung
soll schnell sein. Schreiben Sie drei Funktionen:

- `risiko_mit_apply(anmeldungen)` wendet risiko_zeile mit apply auf
  jede Zeile an und gibt die Punkte als Series zurück. Diese Fassung
  dient als Vergleich.
- `risiko_vektorisiert(anmeldungen)` liefert dieselbe Series (gleiche
  Werte, gleicher Index, ganze Zahlen), rechnet aber mit ganzen Spalten,
  ohne für jede Zeile Python-Code auszuführen.
- `verdaechtige_konten(anmeldungen, schwelle)` gibt die Konten mit
  mindestens einer Anmeldung von schwelle oder mehr Punkten zurück, als
  alphabetisch sortierte Liste ohne Doppelte. Sie verwendet
  risiko_vektorisiert.

    anmeldungen = pd.DataFrame({
        "konto":        ["kaya", "nowak", "kaya", "admin"],
        "fehlversuche": [0, 3, 1, 7],
        "land":         ["DE", "DE", "BR", "DE"],
        "stunde":       [9, 3, 14, 2],
    })
    risiko_vektorisiert(anmeldungen).tolist()    →  [0, 50, 40, 90]
    verdaechtige_konten(anmeldungen, 50)         →  ["admin", "nowak"]

Grenzen: anmeldungen hat die Spalten konto (nicht leere Texte),
fehlversuche (ganze Zahlen von 0 bis 1000), land (zwei Großbuchstaben)
und stunde (ganze Zahlen von 0 bis 23) und 1 bis 100 000 Zeilen. Der
Index besteht aus verschiedenen ganzen Zahlen, aber nicht unbedingt 0, 1,
2, … (etwa nach einem Filter). schwelle ist eine ganze Zahl von 0 bis
10 100. risiko_vektorisiert und verdaechtige_konten sollen eine Zahl von
ausgeführten Python-Zeilen brauchen, die nicht mit der Zahl der Zeilen
wächst.

Hintergrund: DataFrame.apply(funktion, axis=1) ruft funktion für jede
Zeile einmal auf und sammelt die Ergebnisse in einer Series mit dem
Index des DataFrames. Das ist bequem, weil man die Regel wie gewohnt mit
if schreiben kann:

    df.apply(lambda zeile: zeile["a"] + zeile["b"], axis=1)

Es ist aber langsam: pandas baut für jede Zeile eine eigene kleine Series
und ruft die Python-Funktion auf; bei 100 000 Zeilen läuft der Körper
100 000-mal in Python. Vektorisiert heißt, ganze Spalten auf einmal zu
verrechnen, wie bei numpy (Aufgabe 3_013): df["a"] + df["b"] addiert
Zeile für Zeile, aber in C. Das ist oft hundertmal schneller.

Die Bedingungen der Regel werden dabei zu Masken (Aufgabe 3_014):
df["land"] != "DE" ist eine Series aus True und False. Weil True als 1
und False als 0 rechnet, ergibt (df["land"] != "DE") * 30 genau die 30
Punkte dort, wo die Bedingung gilt, und 0 sonst. Für „wenn, dann x, sonst
y“ mit beliebigen Werten gibt es np.where(maske, x, y); das liefert aber
ein numpy-Array ohne Index, das man mit pd.Series(…, index=df.index)
wieder zur Series macht. Alle Rechnungen zwischen Series richten sich
nach dem Index, darum bleibt er bei df["a"] * 10 + df["b"] erhalten.

Mit einer Maske wählt df.loc[maske, "spalte"] die Werte einer Spalte in
den Zeilen aus, in denen die Maske True ist.

Merkregel: apply mit axis=1 ist der letzte Ausweg für Regeln, die sich
nicht als Spaltenrechnung schreiben lassen. Alles, was aus +, *,
Vergleichen und Masken besteht, schreibt man vektorisiert.
"""

import pandas as pd


def risiko_zeile(zeile):
    """Berechnet die Risikopunkte einer Anmeldung; zeile ist eine Zeile des DataFrames."""
    punkte = zeile["fehlversuche"] * 10
    if zeile["land"] != "DE":
        punkte += 30
    if zeile["stunde"] < 6:
        punkte += 20
    return punkte


def risiko_mit_apply(anmeldungen):
    """Gibt die Risikopunkte aller Anmeldungen zurück, berechnet mit apply und risiko_zeile."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def risiko_vektorisiert(anmeldungen):
    """Gibt die Risikopunkte aller Anmeldungen zurück, berechnet mit ganzen Spalten."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def verdaechtige_konten(anmeldungen, schwelle):
    """Gibt die Konten mit mindestens einer Anmeldung ab schwelle Punkten sortiert und ohne Doppelte zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


anmeldungen = pd.DataFrame(
    {
        "konto": ["kaya", "nowak", "kaya", "admin"],
        "fehlversuche": [0, 3, 1, 7],
        "land": ["DE", "DE", "BR", "DE"],
        "stunde": [9, 3, 14, 2],
    }
)
print(risiko_mit_apply(anmeldungen).tolist())
print(risiko_vektorisiert(anmeldungen).tolist())
print(verdaechtige_konten(anmeldungen, 50))
