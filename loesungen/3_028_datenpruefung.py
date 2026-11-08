# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_028_datenpruefung.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_028_datenpruefung

"""Aufgabe 3_028 – Datenprüfung                                  Stufe 3 ★★★☆☆

Bevor eine Firma Kundendaten aus einem alten System in ihre neue
Datenbank übernimmt, prüft sie die Datenqualität. Die Daten sind eine
Tabelle als Liste von Dictionaries (Aufgabe 2_032). Welche Schritte
zum Bereinigen nötig sind und welche Regeln gelten, ist bei jeder
Spalte und jeder Übernahme anders. Deshalb sollen die Werkzeuge nicht
selbst wissen, was zu tun ist: Sie bekommen die Schritte und Regeln
als Funktionen übergeben. Schreiben Sie drei Funktionen:

- `kette(wert, schritte)` wendet die Funktionen der Liste schritte
  nacheinander auf wert an, die erste zuerst, und gibt das Ergebnis
  zurück. Ist schritte leer, kommt wert unverändert zurück.
- `bereinige_spalte(zeilen, name, schritte)` gibt eine neue Liste mit
  neuen Dictionaries zurück, in denen der Wert der Spalte name durch
  kette(wert, schritte) ersetzt ist; alle anderen Spalten bleiben.
- `verstoesse(zeilen, regeln)` bekommt eine Liste von Paaren
  (regelname, regel). Jede regel ist eine Funktion, die eine Zeile
  bekommt und True liefert, wenn die Zeile in Ordnung ist. Zurück
  kommt eine Liste von Paaren (zeilennummer, regelname) für jede Regel,
  die eine Zeile nicht erfüllt; die Zeilen zählen ab 1. Sortiert ist
  sie nach Zeile, innerhalb einer Zeile in der Reihenfolge der Regeln.

    kunden = [{"name": "  ada  LANG", "plz": "33098"},
              {"name": "ben", "plz": "3310"}]
    kette("  ada  LANG", [str.strip, str.title])        →  "Ada  Lang"
    bereinige_spalte(kunden, "name", [str.strip, str.title])
        →  [{"name": "Ada  Lang", "plz": "33098"}, {"name": "Ben", "plz": "3310"}]
    regeln = [("plz fünfstellig", lambda z: len(z["plz"]) == 5),
              ("name vorhanden", lambda z: z["name"] != "")]
    verstoesse(kunden, regeln)                         →  [(2, "plz fünfstellig")]

Grenzen: 0 ≤ len(zeilen) ≤ 10 000, alle Zeilen haben dieselben
Schlüssel, name ist einer davon. schritte hat 0 bis 10 Funktionen mit
einem Parameter, regeln 0 bis 10 Paare mit verschiedenen Namen. Die
Funktionen verändern ihre Argumente nicht. zeilen bleibt unverändert,
auch die Dictionaries darin.

Hintergrund: In Python ist eine Funktion ein Wert wie eine Zahl oder
ein Text. Man kann sie einer Variablen zuweisen, in eine Liste legen
und einer anderen Funktion als Argument übergeben. Entscheidend ist
der Unterschied zwischen dem Namen und dem Aufruf: len ist die
Funktion selbst, len("abc") ruft sie auf und liefert 3. Übergeben
wird deshalb ohne Klammern; aufgerufen wird erst innen, über den Namen
des Parameters:

    def zweimal(funktion, wert):
        return funktion(funktion(wert))

    zweimal(lambda x: x * 3, 2)       →  18
    zweimal(str.upper, "ok")          →  "OK"
    schritte = [abs, str]             # eine Liste von Funktionen
    for schritt in schritte:          # nacheinander aufrufen
        wert = schritt(wert)

So schreibt man ein Werkzeug einmal und entscheidet erst beim Aufruf,
was es genau tut; map und filter (Aufgabe 3_026) und sorted mit key
(Aufgabe 3_027) sind genau so gebaut. str.strip und str.title sind
die Methoden strip und title als Funktion mit einem Parameter:
str.title("ben") ist dasselbe wie "ben".title() und liefert "Ben".
Eine flache Kopie eines Dictionarys macht dict(zeile) (Aufgabe 2_018).
"""


def kette(wert, schritte):
    """Wendet die Funktionen aus schritte der Reihe nach auf wert an."""
    for schritt in schritte:
        wert = schritt(wert)
    return wert


def bereinige_spalte(zeilen, name, schritte):
    """Gibt neue Zeilen zurück, in denen die Spalte name mit kette bearbeitet ist."""
    neue = []
    for zeile in zeilen:
        kopie = dict(zeile)
        kopie[name] = kette(zeile[name], schritte)
        neue.append(kopie)
    return neue


def verstoesse(zeilen, regeln):
    """Gibt (zeilennummer, regelname) für jede verletzte Regel zurück, Zeilen ab 1 gezählt."""
    gefunden = []
    for nummer, zeile in enumerate(zeilen, start=1):
        for regelname, regel in regeln:
            if not regel(zeile):
                gefunden.append((nummer, regelname))
    return gefunden


kunden = [{"name": "  ada  LANG", "plz": "33098"}, {"name": "ben", "plz": "3310"}]
print(kette("  ada  LANG", [str.strip, str.title]))
print(bereinige_spalte(kunden, "name", [str.strip, str.title]))
regeln = [("plz fünfstellig", lambda z: len(z["plz"]) == 5), ("name vorhanden", lambda z: z["name"] != "")]
print(verstoesse(kunden, regeln))


# Idee: kette ruft in einer Schleife jede Funktion mit dem bisherigen Ergebnis auf, wert = schritt(wert).
# bereinige_spalte kopiert jede Zeile mit dict(zeile) und setzt in der Kopie die Spalte name auf
# kette(zeile[name], schritte); so bleibt das Original unberührt. verstoesse geht mit enumerate(zeilen, start=1)
# durch die Zeilen und darin durch die Paare (regelname, regel); liefert regel(zeile) False, wird das Paar
# (nummer, regelname) angehängt.
#
# Anderer Weg: kette rekursiv: kette(schritte[0](wert), schritte[1:]), mit leerer Liste als Abbruch.
# bereinige_spalte als List Comprehension mit {**zeile, name: kette(zeile[name], schritte)}.
#
# Typische Fehler: schritt() ohne Argument oder den Wert nicht weiterreichen (dann zählt nur der letzte
# Schritt), die Zeile selbst verändern (zeile[name] = …), die Zeilen ab 0 zählen, Verstöße melden, wenn die
# Regel True liefert, oder erst alle Zeilen für Regel 1 durchgehen (falsche Reihenfolge).
#
# Laufzeit: bereinige_spalte ruft für jede der n Zeilen die s Schritte auf, O(n · s); verstoesse ruft jede der
# r Regeln für jede Zeile auf, O(n · r), jeweils mal der Kosten einer Funktion.
