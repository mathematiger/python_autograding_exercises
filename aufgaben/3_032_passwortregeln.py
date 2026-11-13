"""Aufgabe 3_032 – Passwortregeln                                Stufe 3 ★★★☆☆

Die IT-Abteilung legt die Passwortrichtlinie für das neue Kundenportal fest.
Jede Regel ist eine Prüffunktion, die ein Passwort bekommt und True liefert,
wenn es die Regel erfüllt. Weil sich die Richtlinie noch oft ändern wird
(mindestens 10 oder doch 12 Zeichen? welche Sonderzeichen?), sollen die
Regeln nicht einzeln von Hand geschrieben werden. Stattdessen gibt es
Funktionen, die Regeln bauen. Vervollständigen Sie:

- `mindestlaenge(anzahl)` liefert eine Prüffunktion, die True ergibt, wenn
  das Passwort mindestens anzahl Zeichen hat.
- `enthaelt_eines(zeichen)` liefert eine Prüffunktion, die True ergibt, wenn
  das Passwort mindestens eines der Zeichen aus dem Text zeichen enthält.
- `verletzte_regeln(regeln, passwort)` bekommt ein Dictionary von
  Regelnamen auf Prüffunktionen und liefert die Liste der Namen aller
  Regeln, die das Passwort nicht erfüllt, in der Reihenfolge des
  Dictionarys.

    lang_genug = mindestlaenge(10)
    lang_genug("Sommer2024")                    →  True
    lang_genug("kurz")                          →  False
    hat_ziffer = enthaelt_eines("0123456789")
    hat_ziffer("ohneZiffer")                    →  False
    regeln = {"Länge": lang_genug, "Ziffer": hat_ziffer,
              "Sonderzeichen": enthaelt_eines("!?#%&*")}
    verletzte_regeln(regeln, "Sommer2024")      →  ["Sonderzeichen"]
    verletzte_regeln(regeln, "kurz!")           →  ["Länge", "Ziffer"]

Grenzen: 0 ≤ anzahl ≤ 100. zeichen ist ein Text mit 1 bis 100 Zeichen,
passwort ein Text mit 0 bis 1000 Zeichen. regeln hat 0 bis 20 Einträge;
die Prüffunktionen darin können auch andere Funktionen sein, die ein
Passwort bekommen und True oder False liefern. Mehrere gebaute Regeln
müssen gleichzeitig nebeneinander funktionieren.

Hintergrund: Funktionen sind in Python Werte wie Zahlen und Listen: Man kann
sie in Variablen und Dictionaries ablegen und anderen Funktionen übergeben
(Aufgabe 3_028). Eine Funktion kann deshalb auch eine Funktion zurückgeben.
Dazu definiert man im Rumpf eine innere Funktion mit def und gibt sie mit
return zurück, ohne Klammern dahinter, also ohne sie aufzurufen:

    def mal(faktor):
        def rechne(zahl):
            return zahl * faktor
        return rechne

    verdoppeln = mal(2)
    verdreifachen = mal(3)
    verdoppeln(5)       →  10
    verdreifachen(5)    →  15

Die innere Funktion darf die Parameter der äußeren benutzen. Sie merkt sich
deren Wert auch dann noch, wenn mal(2) längst fertig ist, und zwar für jeden
Aufruf von mal getrennt: verdoppeln behält faktor 2, verdreifachen faktor 3.
So entstehen aus einer Bauanleitung beliebig viele ähnliche Funktionen.
"""


def mindestlaenge(anzahl):
    """Baut eine Regel: Passwort hat mindestens anzahl Zeichen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def enthaelt_eines(zeichen):
    """Baut eine Regel: Passwort enthält mindestens eines der Zeichen aus zeichen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def verletzte_regeln(regeln, passwort):
    """Namen aller Regeln aus regeln, die passwort nicht erfüllt, in der Reihenfolge von regeln."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


lang_genug = mindestlaenge(10)
hat_ziffer = enthaelt_eines("0123456789")
regeln = {"Länge": lang_genug, "Ziffer": hat_ziffer, "Sonderzeichen": enthaelt_eines("!?#%&*")}
print(verletzte_regeln(regeln, "Sommer2024"))
