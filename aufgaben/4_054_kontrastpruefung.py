"""Aufgabe 4_054 – Kontrastprüfung                               Stufe 4 ★★★★☆

Eine Behörde lässt ihr Bürgerportal auf Barrierefreiheit prüfen. Ein
Punkt der Prüfung ist der Kontrast: Text muss sich deutlich genug vom
Hintergrund abheben, damit ihn auch Menschen mit eingeschränktem
Sehvermögen lesen können. Gemessen wird er über die relative
Leuchtdichte L der beiden Farben, eine Zahl von 0 (Schwarz) bis 1
(Weiß). Ist L1 die hellere und L2 die dunklere Farbe, gilt

    Kontrast = (L1 + 0.05) / (L2 + 0.05)

Das ergibt Werte von 1 (gleiche Farbe) bis 21 (Schwarz auf Weiß). Für
normalen Text verlangt die Richtlinie einen Kontrast von mindestens
4.5, für großen Text mindestens 3. Groß ist Text ab 18 pt, oder ab 14
pt, wenn er fett ist. Die Prüfsoftware liefert je Element eine Zeile:

    seite       element      vorne  hinten  pt  fett
    Anmeldung   Knopf        1.00   0.20    14  True
    Anmeldung   Hinweistext  0.30   1.00    11  False
    Anmeldung   Überschrift  0.10   0.90    20  True
    Start       Fußzeile     0.40   0.05    10  False
    Start       Link         0.15   1.00    12  False
    Start       Banner       1.00   0.45    24  False

vorne ist die Leuchtdichte der Schrift, hinten die des Hintergrunds;
hell kann beides sein. Schreiben Sie vier Funktionen, jede als eine
Kette von Methoden mit assign und, wo gefiltert wird, query. Keine
verändert den DataFrame, den sie bekommt.

- `mit_kontrast(elemente)` gibt eine Kopie mit einer zusätzlichen
  letzten Spalte kontrast zurück, auf zwei Nachkommastellen gerundet.
- `mit_mindestwert(elemente)` gibt wie mit_kontrast eine Kopie zurück,
  dazu die Spalten gross (True oder False) und mindest (3.0 oder 4.5).
  Die beiden folgenden Funktionen bauen darauf auf.
- `verstoesse(elemente)` gibt die Elemente zurück, deren (gerundeter)
  kontrast unter ihrem Mindestwert liegt, mit genau den Spalten seite,
  element, kontrast und mindest (3.0 oder 4.5), sortiert nach seite und
  dann nach element, mit dem Index 0, 1, 2, …
- `knapp(elemente, abstand)` gibt mit denselben Spalten die Elemente
  zurück, die bestehen, aber um weniger als abstand: mindest ≤ kontrast
  < mindest + abstand. Sortiert nach kontrast, bei Gleichstand nach
  element, Index 0, 1, 2, …

    mit_kontrast(elemente)["kontrast"].tolist()
        →  [4.2, 3.0, 6.33, 4.5, 5.25, 2.1]
    verstoesse(elemente).to_dict("records")
        →  [{"seite": "Anmeldung", "element": "Hinweistext", "kontrast": 3.0, "mindest": 4.5},
            {"seite": "Start", "element": "Banner", "kontrast": 2.1, "mindest": 3.0}]
    knapp(elemente, 1.0)["element"].tolist()   →  ["Fußzeile", "Link"]

Grenzen: elemente hat 0 bis 1000 Zeilen und genau die Spalten oben.
vorne und hinten sind Kommazahlen von 0 bis 1, pt ist eine ganze Zahl
von 6 bis 72, fett ist True oder False. seite und element sind nicht
leere Texte, jede Kombination kommt höchstens einmal vor. abstand ist
eine Zahl von 0 bis 5.

Hintergrund: Aus Aufgabe 3_044 kennen Sie neue Spalten mit
df["spalte"] = …; das verändert den DataFrame selbst. In Auswertungen
schreibt man lieber eine Kette von Methoden, von denen jede einen neuen
DataFrame zurückgibt und die alte Tabelle in Ruhe lässt. Zwei Methoden
machen das bequem:

    ergebnis = (
        df.assign(brutto=df["netto"] * 1.19)            # neue Spalte
        .assign(teuer=lambda d: d["brutto"] > 100)      # nutzt brutto
        .query("teuer and lager > 0")                   # Zeilen filtern
        .sort_values("brutto")
        .reset_index(drop=True)
    )

assign(name=wert) hängt eine Spalte an oder ersetzt eine gleichnamige;
mehrere Spalten gehen in einem Aufruf (assign(a=…, b=…)). Gibt man statt
eines Werts eine Funktion an, meist ein lambda (Aufgabe 3_025), ruft
pandas sie mit dem Zwischenergebnis der Kette auf. Nur so kann man auf
eine Spalte zugreifen, die erst ein Glied vorher entstanden ist: In
der zweiten Zeile gibt es brutto in df noch gar nicht, wohl aber in d.

query("…") filtert mit einer Bedingung als Text. Darin stehen
Spaltennamen ohne Anführungszeichen, Vergleiche wie <, ==, and, or und
not, und Rechnungen wie kontrast < mindest + 1. Eine Python-Variable
holt man mit @ hinein: query("preis < @grenze"). Das ist kürzer und
lesbarer als df[(df["a"] > 1) & (df["b"] < 2)] mit Masken (Aufgabe
3_041). Die runden Klammern um die ganze Kette erlauben einen
Zeilenumbruch vor jedem Punkt. Für die hellere von zwei Spalten
liefert df[["a", "b"]].max(axis=1) je Zeile das Maximum.
"""

import pandas as pd


def mit_kontrast(elemente):
    """Gibt eine Kopie mit der zusätzlichen Spalte kontrast (zwei Nachkommastellen) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def mit_mindestwert(elemente):
    """Gibt eine Kopie mit kontrast und mindest (3.0 für großen, 4.5 für normalen Text) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def verstoesse(elemente):
    """Gibt die Elemente zurück, deren Kontrast unter dem Mindestwert liegt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def knapp(elemente, abstand):
    """Gibt die Elemente zurück, die den Mindestwert um weniger als abstand übertreffen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


elemente = pd.DataFrame(
    [
        {"seite": "Anmeldung", "element": "Knopf", "vorne": 1.0, "hinten": 0.2, "pt": 14, "fett": True},
        {"seite": "Anmeldung", "element": "Hinweistext", "vorne": 0.3, "hinten": 1.0, "pt": 11, "fett": False},
        {"seite": "Anmeldung", "element": "Überschrift", "vorne": 0.1, "hinten": 0.9, "pt": 20, "fett": True},
        {"seite": "Start", "element": "Fußzeile", "vorne": 0.4, "hinten": 0.05, "pt": 10, "fett": False},
        {"seite": "Start", "element": "Link", "vorne": 0.15, "hinten": 1.0, "pt": 12, "fett": False},
        {"seite": "Start", "element": "Banner", "vorne": 1.0, "hinten": 0.45, "pt": 24, "fett": False},
    ]
)
print(mit_kontrast(elemente)["kontrast"].tolist())
print(verstoesse(elemente).to_dict("records"))
print(knapp(elemente, 1.0)["element"].tolist())
