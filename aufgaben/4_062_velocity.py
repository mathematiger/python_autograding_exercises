"""Aufgabe 4_062 – Velocity                                      Stufe 4 ★★★★☆

Ein agiles Team schätzt seine Aufgaben in Story Points, einer Zahl für
den Aufwand. Am Ende jedes Sprints zählt es, wie viele Punkte es
geschafft hat; das ist die Velocity des Sprints. Für die Prognose, wie
viele Sprints der Rest des Projekts noch braucht, nimmt das Team den
Durchschnitt der letzten drei Sprints, denn ältere Sprints sagen wenig
über das heutige Team. Außerdem übernimmt nach jedem Release ein anderes
Team die Rufbereitschaft für Störungen in der Nacht. Wie weit die Reihe
weiterrückt, hängt davon ab, wie viele Teams am Release beteiligt
waren, und wird ein Release zurückgenommen, rückt sie wieder zurück.
Schreiben Sie mit collections.deque:

- Die Klasse `Velocity(fenster=3)`. Sie speichert die Punkte der
  letzten fenster Sprints im Attribut letzte, einer deque mit maxlen.
  `abschliessen(punkte)` nimmt die Punkte eines fertigen Sprints auf,
  `verlauf()` gibt die gespeicherten Punkte als Liste zurück, den
  ältesten Sprint vorn, und `durchschnitt()` gibt ihren Mittelwert
  zurück. `sprints_bis_fertig(restpunkte)` gibt zurück, wie viele
  Sprints die restlichen Punkte beim Durchschnitt noch brauchen,
  aufgerundet. Gibt es noch keinen Sprint, lösen durchschnitt und
  sprints_bis_fertig einen ValueError aus, ebenso sprints_bis_fertig,
  wenn noch Punkte offen sind, aber der Durchschnitt 0 ist. Rechnen Sie
  in sprints_bis_fertig mit ganzen Zahlen (siehe Hintergrund).
- Die Funktion `nach_release(teams, schritte)`. teams ist die Reihe der
  Teams, das erste hat gerade Rufbereitschaft. Sie gibt eine neue Liste
  zurück, in der die Reihe um schritte Plätze weitergerückt ist: Das
  Team, das schritte Plätze hinter dem ersten stand, ist jetzt vorn.
  Ein negativer Wert rückt zurück. Benutzen Sie dafür rotate.

    v = Velocity()
    for punkte in [21, 30, 18, 27]:
        v.abschliessen(punkte)
    v.verlauf()                  →  [30, 18, 27]
    v.durchschnitt()             →  25.0
    v.sprints_bis_fertig(60)     →  3

    teams = ["Web", "App", "Daten", "Netz"]
    nach_release(teams, 1)       →  ["App", "Daten", "Netz", "Web"]
    nach_release(teams, -1)      →  ["Netz", "Web", "App", "Daten"]
    nach_release(teams, 6)       →  ["Daten", "Netz", "Web", "App"]

Grenzen: fenster ist eine ganze Zahl von 1 bis 20, punkte eine von 0 bis
500, restpunkte eine von 0 bis 100 000; ein Objekt erlebt bis zu
100 000 Sprints. teams hat 1 bis 1000 verschiedene Namen und bleibt
unverändert, schritte ist eine ganze Zahl von -10**9 bis 10**9.

Hintergrund: Eine Liste ist schnell, wenn man hinten anhängt oder
wegnimmt. liste.pop(0) und liste.insert(0, x) müssen dagegen alle
übrigen Einträge um einen Platz verschieben, bei einer Million Einträgen
eine Million Schritte. collections.deque („double-ended queue“, sprich
„deck“) ist eine Folge, die an beiden Enden in einem Schritt anhängt
und wegnimmt:

    from collections import deque

    warteschlange = deque(["a", "b"])
    warteschlange.append("c")       # hinten anhängen:  deque(['a', 'b', 'c'])
    warteschlange.appendleft("z")   # vorn anhängen:    deque(['z', 'a', 'b', 'c'])
    warteschlange.popleft()         # vorn wegnehmen:   'z'
    warteschlange.pop()             # hinten wegnehmen: 'c'

Ansonsten verhält sich eine deque wie eine Liste: len, for, in,
list(warteschlange) und der Zugriff über [0] und [-1] gehen, Slicing
dagegen nicht. Zwei Dinge kann sie zusätzlich. Mit maxlen bekommt sie
eine feste Länge; ist sie voll, fällt beim Anhängen am anderen Ende ein
Eintrag heraus. So merkt man sich „die letzten n“ ohne eigene Prüfung:

    letzte = deque(maxlen=3)
    for wert in [1, 2, 3, 4, 5]:
        letzte.append(wert)
    letzte                          # deque([3, 4, 5], maxlen=3)
    letzte.maxlen                   # 3

Und rotate(n) dreht die deque an Ort und Stelle um n Plätze nach
rechts: Die letzten n Einträge kommen nach vorn. Ein negatives n dreht
nach links, und Drehungen um mehr als die Länge zählen nur mit ihrem
Rest:

    reihe = deque([1, 2, 3, 4])
    reihe.rotate(1)                 # deque([4, 1, 2, 3])
    reihe.rotate(-2)                # deque([2, 3, 4, 1])

In Aufgabe 4_040 lief die Moderation mit itertools.cycle immer nur
vorwärts; rotate dreht um beliebig viele Plätze in beide Richtungen.
Weil rotate die deque selbst ändert, legen Sie für ein neues Ergebnis
zuerst eine neue deque an.

Zum Aufrunden: Der Durchschnitt von 4, 4 und 5 ist 13 / 3, und das ist
als Kommazahl nicht genau 4.333…; 65 / (13 / 3) ergibt darum
15.000000000000002, und math.ceil macht daraus 16 statt 15. Rechnen Sie
lieber mit ganzen Zahlen: restpunkte / (summe / anzahl) ist dasselbe wie
restpunkte · anzahl / summe, und a / b aufgerundet ist -(-a // b).
"""

from collections import deque


class Velocity:
    """Merkt sich die Story Points der letzten Sprints und rechnet daraus eine Prognose."""

    def __init__(self, fenster=3):
        """Legt die leere deque letzte mit maxlen fenster an."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def abschliessen(self, punkte):
        """Nimmt die Punkte eines fertigen Sprints auf; der älteste fällt heraus, wenn das Fenster voll ist."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def verlauf(self):
        """Gibt die gespeicherten Punkte als Liste zurück, den ältesten Sprint vorn."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def durchschnitt(self):
        """Gibt den Mittelwert der gespeicherten Punkte zurück; ValueError, wenn es keine gibt."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def sprints_bis_fertig(self, restpunkte):
        """Gibt die aufgerundete Zahl der Sprints für restpunkte zurück; ValueError, wenn das nicht geht."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def nach_release(teams, schritte):
    """Gibt eine neue Liste zurück, in der die Reihe der Teams um schritte Plätze weitergerückt ist."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


v = Velocity()
for punkte in [21, 30, 18, 27]:
    v.abschliessen(punkte)
print(v.verlauf(), v.durchschnitt(), v.sprints_bis_fertig(60))
teams = ["Web", "App", "Daten", "Netz"]
print(nach_release(teams, 1), nach_release(teams, -1), nach_release(teams, 6))
