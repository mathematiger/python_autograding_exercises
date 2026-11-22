# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_053_planabweichung.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_053_planabweichung

"""Aufgabe 2_053 – Planabweichung                                Stufe 2 ★★☆☆☆

Ein agiles Team plant vor jedem Sprint, wie viele Story Points es
schaffen will, und trägt nach dem Sprint ein, wie viele es wirklich
geschafft hat. Für die Retrospektive, das Treffen, in dem das Team auf
den Sprint zurückblickt, speichert die Scrum Masterin je Sprint die
Abweichung: geschaffte minus geplante Punkte. Eine positive Zahl heißt,
das Team war besser als geplant, eine negative, es hat weniger
geschafft. Der erste Sprint hat die Nummer 1:

    abweichungen = [-3, 4, -8, 4, 0]     # Sprint 1 bis 5

Schreiben Sie zwei Funktionen, die je ein Tupel (Abweichung,
Sprintnummer) zurückgeben:

- `bester_sprint(abweichungen)` liefert die größte Abweichung und die
  Nummer des Sprints dazu. Gibt es sie mehrmals, zählt der letzte dieser
  Sprints, denn der jüngste sagt am meisten über das Team von heute.
- `schlechtester_sprint(abweichungen)` liefert die kleinste Abweichung
  und die Nummer dazu; bei Gleichstand zählt hier der erste Sprint.

    bester_sprint([-3, 4, -8, 4, 0])          →  (4, 4)
    schlechtester_sprint([-3, 4, -8, 4, 0])   →  (-8, 3)
    bester_sprint([-5, -2, -7])               →  (-2, 2)

Benutzen Sie weder max() noch min(), sorted(), sort() oder
liste.index(...).

Grenzen: abweichungen hat 1 bis 100 000 Einträge, alle ganze Zahlen von
-1000 bis 1000. Es kann vorkommen, dass alle Abweichungen negativ sind.

Hintergrund: In Aufgabe 2_021 haben Sie mit enumerate die Nummer des
längsten Schritts gesucht: Man merkt sich den bisher größten Wert und
seine Nummer und ersetzt beide nur, wenn ein Wert echt größer ist. Zwei
Dinge entscheiden, ob das stimmt:

- Der Startwert. Beginnt man mit groesster = 0, findet man bei lauter
  negativen Zahlen keinen größeren Wert und gibt 0 zurück, obwohl 0 gar
  nicht in der Liste steht. Sicher ist nur, mit dem ersten Eintrag zu
  beginnen: groesster = werte[0], nummer = 1.
- Der Vergleich bei Gleichstand. Mit > bleibt der erste der gleich großen
  Werte stehen, mit >= ersetzt jeder spätere gleich große ihn, am Ende
  steht also der letzte.

Für das Minimum dreht man nur den Vergleich um. Zwei Werte gibt eine
Funktion als Tupel zurück: return (groesster, nummer) (Aufgabe 2_010).
"""


def bester_sprint(abweichungen):
    """Gibt (größte Abweichung, Nummer des letzten Sprints mit diesem Wert) zurück."""
    groesste = abweichungen[0]
    beste_nummer = 1
    for nummer, abweichung in enumerate(abweichungen, start=1):
        if abweichung >= groesste:
            groesste = abweichung
            beste_nummer = nummer
    return (groesste, beste_nummer)


def schlechtester_sprint(abweichungen):
    """Gibt (kleinste Abweichung, Nummer des ersten Sprints mit diesem Wert) zurück."""
    kleinste = abweichungen[0]
    schlechteste_nummer = 1
    for nummer, abweichung in enumerate(abweichungen, start=1):
        if abweichung < kleinste:
            kleinste = abweichung
            schlechteste_nummer = nummer
    return (kleinste, schlechteste_nummer)


print(bester_sprint([-3, 4, -8, 4, 0]))
print(schlechtester_sprint([-3, 4, -8, 4, 0]))
print(bester_sprint([-5, -2, -7]))


# Idee: Man beginnt mit dem ersten Eintrag und der Nummer 1 und geht mit enumerate(..., start=1)
# alle Sprints durch. In bester_sprint ersetzt jeder Wert mit >= den gemerkten, so bleibt bei
# Gleichstand der letzte stehen; in schlechtester_sprint nur ein echt kleinerer Wert (<), so bleibt
# der erste stehen. Am Ende gibt man (Wert, Nummer) als Tupel zurück.
# Anderer Weg: for stelle in range(len(abweichungen)) mit abweichungen[stelle] und der Nummer
# stelle + 1; oder für den letzten Gleichstand die Liste rückwärts durchgehen und dort > benutzen.
# Mit max(), min() und index() ginge es kürzer, aber die Aufgabe übt gerade den Weg dahinter.
# Typische Fehler: Startwert 0 (falsch, wenn alle Werte negativ bzw. alle positiv sind), > statt >=
# beim besten Sprint (dann der erste statt des letzten), den Index ab 0 statt der Nummer ab 1
# zurückgeben, oder Wert und Nummer im Tupel vertauschen.
