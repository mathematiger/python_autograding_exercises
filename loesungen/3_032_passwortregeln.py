# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_032_passwortregeln.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_032_passwortregeln

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
    def pruefe(passwort):
        """True, wenn passwort mindestens anzahl Zeichen hat."""
        return len(passwort) >= anzahl

    return pruefe


def enthaelt_eines(zeichen):
    """Baut eine Regel: Passwort enthält mindestens eines der Zeichen aus zeichen."""
    def pruefe(passwort):
        """True, wenn eines der Zeichen aus zeichen in passwort vorkommt."""
        for buchstabe in zeichen:
            if buchstabe in passwort:
                return True
        return False

    return pruefe


def verletzte_regeln(regeln, passwort):
    """Namen aller Regeln aus regeln, die passwort nicht erfüllt, in der Reihenfolge von regeln."""
    verletzt = []
    for name, regel in regeln.items():
        if not regel(passwort):
            verletzt.append(name)
    return verletzt


lang_genug = mindestlaenge(10)
hat_ziffer = enthaelt_eines("0123456789")
regeln = {"Länge": lang_genug, "Ziffer": hat_ziffer, "Sonderzeichen": enthaelt_eines("!?#%&*")}
print(verletzte_regeln(regeln, "Sommer2024"))


# Idee: mindestlaenge und enthaelt_eines definieren jeweils eine innere Funktion pruefe(passwort), die den
# Parameter der äußeren Funktion (anzahl bzw. zeichen) benutzt, und geben sie mit return pruefe zurück.
# verletzte_regeln geht mit .items() durch das Dictionary, ruft jede Regel mit dem Passwort auf und
# sammelt die Namen der Regeln, die False liefern.
# Anderer Weg: return lambda passwort: len(passwort) >= anzahl baut die Regel in einer Zeile; für
# enthaelt_eines ginge any(buchstabe in passwort for buchstabe in zeichen). verletzte_regeln als List
# Comprehension: [name for name, regel in regeln.items() if not regel(passwort)].
# Typische Fehler: return pruefe(...) statt return pruefe (dann wird die Regel sofort aufgerufen statt
# zurückgegeben), > statt >= bei der Länge, zeichen in passwort statt jedes einzelne Zeichen prüfen
# (dann müsste der ganze Text zeichen am Stück vorkommen) oder die Länge in einer globalen Variablen
# speichern (dann gilt für alle Regeln die zuletzt gebaute).
# Laufzeit: Eine Längenregel braucht O(1), eine Zeichenregel O(z · p) für z Zeichen und ein Passwort der
# Länge p (jedes in prüft das Passwort durch); verletzte_regeln ruft jede der r Regeln einmal auf.
