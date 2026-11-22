"""Aufgabe 4_040 – Moderationsplan                               Stufe 4 ★★★★☆

Ein agiles Entwicklungsteam arbeitet in Sprints, kurzen Abschnitten von
einigen Arbeitstagen mit fortlaufender Nummer. Jeden Morgen gibt es ein
kurzes Treffen, das Daily, und das moderiert reihum immer jemand anderes
aus dem Team: erst Ada, dann Ben, dann Cem, dann wieder Ada. Die Reihe
läuft über das Ende eines Sprints hinaus einfach weiter. Die Teamleitung
möchte dafür einen Plan, und weil neue Sprints, Tickets und Tage nie
aufhören, soll der Code mit unendlichen Folgen arbeiten statt mit
Listen fester Länge. Schreiben Sie mit dem Modul itertools:

- `rotation(team)` gibt einen unendlichen Iterator zurück, der die Namen
  aus der Liste team reihum liefert (itertools.cycle).
- `sprintplan(team, erster_sprint, anzahl, tage)` gibt eine Liste von
  anzahl Tupeln (sprintnummer, moderationen) zurück. Die Sprintnummern
  zählen ab erster_sprint hoch (itertools.count), moderationen ist die
  Liste der tage Namen für die Dailys dieses Sprints. Die Rotation läuft
  über alle Sprints durch und beginnt nicht in jedem Sprint neu
  (itertools.islice auf einem gemeinsamen Iterator).
- `kapazitaeten(team, stunden)` gibt ein Dictionary zurück, das jedem
  Namen dieselbe Stundenzahl zuordnet, als Startwert für die Planung
  (itertools.repeat).
- `naechste_freie_nummer(belegt, start)` gibt die kleinste ganze Zahl
  ab start zurück, die nicht in der Menge belegt vorkommt, etwa für die
  Nummer des nächsten Tickets (itertools.count).

    team = ["Ada", "Ben", "Cem"]
    r = rotation(team)
    [next(r) for _ in range(4)]       →  ["Ada", "Ben", "Cem", "Ada"]
    sprintplan(team, 41, 2, 2)        →  [(41, ["Ada", "Ben"]),
                                          (42, ["Cem", "Ada"])]
    kapazitaeten(team, 30)            →  {"Ada": 30, "Ben": 30, "Cem": 30}
    naechste_freie_nummer({7, 8, 10}, 7)  →  9

Grenzen: team hat 1 bis 20 verschiedene Namen. 1 ≤ erster_sprint ≤
10**6, 0 ≤ anzahl ≤ 1000, 1 ≤ tage ≤ 20, 0 ≤ stunden ≤ 40. belegt ist
eine Menge mit bis zu 100 000 ganzen Zahlen, 0 ≤ start ≤ 10**9. Ihre
Lösung soll für einen Sprint nur tage Namen aus der Rotation holen.

Hintergrund: Generatoren können unendlich sein (Aufgabe 4_034), und das
Modul itertools hat fertige unendliche Iteratoren, die man nicht selbst
schreiben muss:

    from itertools import count, cycle, repeat, islice

    count(41)          →  41, 42, 43, …             (ohne Ende)
    count(0, 5)        →  0, 5, 10, 15, …           (Schrittweite 5)
    cycle("AB")        →  "A", "B", "A", "B", …     (immer wieder von vorn)
    repeat(30)         →  30, 30, 30, …             (ohne Ende)
    repeat(30, 3)      →  30, 30, 30                (genau dreimal)

Weil sie nie enden, darf man sie nicht an list(...) übergeben. Man nimmt
sich mit islice einen endlichen Teil heraus, so wie mit Slicing bei
einer Liste: islice(iterator, 5) liefert die ersten 5 Werte,
islice(iterator, 2, 8, 3) die Werte an den Stellen 2 und 5. islice ist
selbst lazy und holt nur so viele Werte, wie es abgibt. Wichtig: Ein
Iterator merkt sich, wo er steht. Ruft man islice zweimal auf demselben
Iterator auf, macht das zweite dort weiter, wo das erste aufgehört hat:

    zahlen = count(1)
    list(islice(zahlen, 3))   →  [1, 2, 3]
    list(islice(zahlen, 3))   →  [4, 5, 6]

Mit zip kann man einen unendlichen Iterator neben einen endlichen
legen; zip hört auf, sobald der kürzere zu Ende ist:
list(zip("xyz", count(1))) ist [("x", 1), ("y", 2), ("z", 3)], und
dict(zip(namen, repeat(0))) ordnet jedem Namen 0 zu. Ein Generator-
Ausdruck über count mit next findet den ersten passenden Wert:
next(n for n in count(10) if n % 7 == 0) ist 14.
"""

from itertools import count, cycle, islice, repeat


def rotation(team):
    """Gibt einen unendlichen Iterator über die Namen reihum zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def sprintplan(team, erster_sprint, anzahl, tage):
    """Gibt eine Liste von (sprintnummer, moderationen) für anzahl Sprints zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def kapazitaeten(team, stunden):
    """Gibt ein Dictionary zurück, das jedem Namen die Stundenzahl zuordnet."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def naechste_freie_nummer(belegt, start):
    """Gibt die kleinste Zahl ab start zurück, die nicht in belegt ist."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


team = ["Ada", "Ben", "Cem"]
reihe = rotation(team)
print([next(reihe) for _ in range(4)])
print(sprintplan(team, 41, 2, 2))
print(kapazitaeten(team, 30))
print(naechste_freie_nummer({7, 8, 10}, 7))
