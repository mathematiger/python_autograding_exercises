"""Aufgabe 4_023 – Kostendeckel                                 Stufe 4 ★★★★☆

Eine Schule will neue Rechner für zwei Computerräume beschaffen. Die
Verwaltung hat dafür kleine Rechenfunktionen geschrieben: Gesamtkosten
beim Kauf über fünf Jahre (Anschaffung plus Strom und Wartung), Kosten
beim Leasing, Kosten für Software-Lizenzen. Zwei Regeln gelten für
alle diese Funktionen: Beträge werden auf eine feste Zahl von
Nachkommastellen gerundet, und kein Ergebnis darf über dem Budget des
jeweiligen Postens liegen, sonst muss die Schulleitung gefragt werden.
Statt die Regeln in jede Funktion zu schreiben, sollen zwei
Dekoratoren mit Argumenten sie übernehmen. Vervollständigen Sie:

- `runde(stellen)` gibt einen Dekorator zurück. Die damit dekorierte
  Funktion gibt round(ergebnis, stellen) des ursprünglichen Ergebnisses
  zurück. stellen muss eine ganze Zahl von 0 bis 4 sein, sonst löst
  schon runde(stellen) einen ValueError aus.
- `budget(grenze)` gibt einen Dekorator zurück. Die damit dekorierte
  Funktion gibt das Ergebnis unverändert zurück, wenn es höchstens
  grenze ist. Ist es größer, löst sie einen ValueError aus, dessen
  Meldung den Namen der Funktion, das Ergebnis und die Grenze nennt.
  Ist grenze negativ, löst schon budget(grenze) einen ValueError aus.
  Die dekorierte Funktion hat außerdem das Attribut budget mit der
  Grenze.

Beide Hüllfunktionen reichen alle Argumente weiter und übernehmen mit
functools.wraps Namen und Docstring.

    @budget(25000)
    @runde(2)
    def kauf(anzahl, preis, betrieb_pro_jahr, jahre=5):
        return anzahl * preis + jahre * betrieb_pro_jahr

    kauf(30, 649.99, 1200)      →  25499.7  →  ValueError: kauf: 25499.7 liegt über dem Budget von 25000
    kauf(28, 649.99, 1200)      →  24199.72
    kauf.budget                 →  25000
    runde(7)                    →  ValueError

Grenzen: stellen und grenze sind ganze Zahlen oder Kommazahlen; stellen
ist nur gültig, wenn es eine ganze Zahl (int, aber nicht bool) von 0
bis 4 ist. grenze ist eine Zahl von -10**9 bis 10**9, auch 0. Die
dekorierten Funktionen geben Zahlen von -10**9 bis 10**9 zurück und
bekommen beliebige Argumente nach Position und nach Namen. Ein Ergebnis,
das genau gleich grenze ist, ist erlaubt. Bis zu 100 000 Aufrufe
hintereinander.

Hintergrund: Ein Dekorator ist eine Funktion, die eine Funktion bekommt
und eine Hüllfunktion zurückgibt (Aufgabe 4_022). Soll man ihn
einstellen können, etwa mit einer Grenze, braucht man eine Ebene mehr:
eine Funktion, die die Einstellung bekommt und erst den Dekorator
zurückgibt. Hinter dem @ steht dann ein Aufruf:

    @budget(25000)
    def kauf(...):
        ...

bedeutet genau

    def kauf(...):
        ...
    kauf = budget(25000)(kauf)

Zuerst läuft budget(25000) und liefert den eigentlichen Dekorator, dann
wird dieser mit kauf aufgerufen. Das sind drei verschachtelte
Funktionen, jede eine Closure (Aufgabe 4_021) über die Variablen der
äußeren:

    import functools

    def wiederhole(anzahl):                  # bekommt die Einstellung
        def dekorator(funktion):             # bekommt die Funktion
            @functools.wraps(funktion)
            def huelle(*args, **kwargs):     # wird bei jedem Aufruf ausgeführt
                for _ in range(anzahl):
                    ergebnis = funktion(*args, **kwargs)
                return ergebnis
            return huelle
        return dekorator

Eine falsche Einstellung prüft man in der äußersten Funktion, dann fällt
der Fehler schon beim Dekorieren auf und nicht erst beim ersten Aufruf.
Jeder Aufruf von budget(…) erzeugt einen neuen Dekorator mit seiner
eigenen Grenze, darum können zwei Funktionen verschiedene Budgets haben.
Stehen mehrere Dekoratoren übereinander, wird der unterste zuerst
angewendet: Im Beispiel rundet runde(2) das Ergebnis, und budget
prüft die gerundete Zahl. Ein Attribut setzt man an der Hüllfunktion
wie an jedem Objekt: huelle.budget = grenze. Ob etwas eine ganze Zahl
ist, prüft isinstance(stellen, int); weil True und False auch als int
gelten, schließt man sie mit isinstance(stellen, bool) aus.
"""

import functools


def runde(stellen):
    """Gibt einen Dekorator zurück, der das Ergebnis auf stellen Nachkommastellen rundet."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def budget(grenze):
    """Gibt einen Dekorator zurück, der Ergebnisse über grenze mit ValueError ablehnt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


@budget(25000)
@runde(2)
def kauf(anzahl, preis, betrieb_pro_jahr, jahre=5):
    """Gesamtkosten beim Kauf: Anschaffung plus Betrieb über die Jahre."""
    return anzahl * preis + jahre * betrieb_pro_jahr


try:
    kauf(30, 649.99, 1200)
except ValueError as fehler:
    print(fehler)
print(kauf(28, 649.99, 1200), kauf.budget, kauf.__name__)
