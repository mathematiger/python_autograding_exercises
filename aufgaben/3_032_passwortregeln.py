"""Aufgabe 3_032 – Passwortregeln                               Stufe 3 ★★★☆☆

Ein Unternehmen hat für verschiedene Systeme verschiedene
Passwortrichtlinien: Für das WLAN der Gäste reichen 8 Zeichen, für das
Mitarbeiterkonto müssen es 12 sein und mindestens eine Ziffer, für die
Administratorkonten 16 Zeichen und mindestens ein Sonderzeichen. Statt für
jede Richtlinie eine eigene Prüffunktion zu schreiben, soll eine einzige
Funktion die passende Prüffunktion bauen.

Schreiben Sie `baue_pruefer(mindestlaenge, pflichtzeichen)`. Sie prüft
selbst noch kein Passwort, sondern liefert eine neue Funktion zurück. Diese
neue Funktion bekommt ein Passwort und liefert True, wenn

- das Passwort mindestens mindestlaenge Zeichen lang ist und
- mindestens eines der Zeichen aus dem Text pflichtzeichen enthält. Ist
  pflichtzeichen der leere Text "", gibt es diese Regel nicht.

Sonst liefert sie False.

    gaeste = baue_pruefer(8, "")
    mitarbeiter = baue_pruefer(12, "0123456789")
    gaeste("sonnenschein")          →  True
    mitarbeiter("sonnenschein")     →  False   (keine Ziffer)
    mitarbeiter("sonnenschein7")    →  True
    gaeste("kurz")                  →  False

Grenzen: 0 ≤ mindestlaenge ≤ 100, pflichtzeichen hat 0 bis 40 Zeichen,
ein Passwort hat 0 bis 1000 Zeichen. Es können beliebig viele Prüfer
nebeneinander existieren, und jeder behält seine eigene Richtlinie.

Hintergrund: Funktionen sind in Python Werte wie Zahlen oder Texte: Man kann
sie in Variablen speichern, an andere Funktionen übergeben (Aufgabe 3_028)
und auch mit return zurückgeben. Definiert man eine Funktion innerhalb einer
anderen, kann die innere die Parameter der äußeren benutzen, und zwar auch
noch, wenn die äußere längst fertig ist:

    def baue_begruessung(gruss):
        def begruesse(name):
            return gruss + ", " + name
        return begruesse          # ohne Klammern: die Funktion selbst

    hallo = baue_begruessung("Hallo")
    hallo("Ada")                  →  "Hallo, Ada"

Wichtig ist, dass return begruesse ohne Klammern dasteht: Mit Klammern würde
die innere Funktion sofort aufgerufen und ihr Ergebnis zurückgegeben. Jeder
Aufruf von baue_begruessung baut eine eigene innere Funktion mit ihrem
eigenen gruss.
"""


def baue_pruefer(mindestlaenge, pflichtzeichen):
    """Liefert eine Funktion, die ein Passwort gegen diese Richtlinie prüft."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


gaeste = baue_pruefer(8, "")
mitarbeiter = baue_pruefer(12, "0123456789")
print(gaeste("sonnenschein"), mitarbeiter("sonnenschein"), mitarbeiter("sonnenschein7"))
