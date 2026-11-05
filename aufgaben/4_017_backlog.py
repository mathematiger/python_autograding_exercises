"""Aufgabe 4_017 – Backlog-Helfer                                Stufe 4 ★★★★☆

Ein Entwicklungsteam arbeitet agil: Alle offenen Anforderungen stehen im
Product Backlog, einer nach Wichtigkeit geordneten Liste. Je nach
Werkzeug sind die Einträge unterschiedlich gespeichert: im Planungstool
als Ticketnummern wie "PRJ-17", in der Aufwandsschätzung als Story
Points (ganze Zahlen), im Export als Tupel (titel, punkte). Das Team
möchte ein kleines Hilfsmodul, dessen Funktionen mit jeder dieser Listen
funktionieren und trotzdem genau annotiert sind, damit mypy bei jedem
Aufruf weiß, welcher Typ herauskommt.

Schreiben Sie die drei Funktionen vollständig, mit Annotationen für jeden
Parameter und den Rückgabewert. Legen Sie dafür oben selbst die
Typvariablen mit TypeVar an und verwenden Sie die eingebauten Typen
list, dict und tuple.

- `erstes_oder(eintraege, standard)`: eintraege ist eine Liste von
  Werten eines beliebigen, aber festen Typs, standard ein Wert desselben
  Typs. Gibt den ersten Eintrag zurück (das, was das Team als Nächstes
  bearbeitet), bei leerer Liste standard. Rückgabe: derselbe Typ.
- `in_sprints(eintraege, groesse)`: eintraege wie oben, groesse eine
  ganze Zahl. Teilt das Backlog der Reihe nach in Sprints zu je groesse
  Einträgen auf; der letzte Sprint darf kürzer sein. Gibt eine Liste von
  Listen mit Einträgen desselben Typs zurück. Ist groesse kleiner als 1,
  löst die Funktion einen ValueError aus.
- `gruppiere(paare)`: paare ist eine Liste von Tupeln (schluessel, wert),
  wobei alle Schlüssel denselben Typ haben und alle Werte einen zweiten
  Typ, der derselbe oder ein anderer sein kann. Gibt ein Dictionary zurück, das jedem
  Schlüssel die Liste seiner Werte in der ursprünglichen Reihenfolge
  zuordnet; die Schlüssel stehen in der Reihenfolge ihres ersten
  Auftretens.

    erstes_oder(["PRJ-17", "PRJ-4"], "leer")         →  "PRJ-17"
    erstes_oder([], 0)                                →  0
    in_sprints([5, 3, 8, 2, 1], 2)                    →  [[5, 3], [8, 2], [1]]
    gruppiere([("Ada", "PRJ-17"), ("Bo", "PRJ-4"), ("Ada", "PRJ-9")])
        →  {"Ada": ["PRJ-17", "PRJ-9"], "Bo": ["PRJ-4"]}

Grenzen: eintraege und paare haben 0 bis 100 000 Elemente; die Einträge
können Texte, ganze Zahlen, Tupel oder beliebige andere Objekte sein,
auch 0, "" oder None. groesse ist eine ganze Zahl von -10**9 bis 10**9;
jede groesse kleiner als 1 muss einen ValueError auslösen. Die
Schlüssel in paare sind hashbar. Die Eingaben bleiben unverändert.

Hintergrund: In Aufgabe 4_016 hatten alle Annotationen feste Typen wie
list[str]. Eine Funktion wie „gib den ersten Eintrag zurück“ funktioniert
aber mit Listen jedes Typs. Schreibt man list[Any] und -> Any, geht die
Information verloren: mypy weiß dann nicht mehr, dass aus einer Liste
von Texten ein Text herauskommt, und prüft danach nichts mehr. Mit object
statt Any wäre es noch schlimmer, denn mit einem object darf man fast
nichts tun.

Die Lösung ist eine Typvariable. Sie steht für „irgendein Typ, aber bei
jedem Aufruf überall derselbe“:

    from typing import TypeVar

    T = TypeVar("T")

    def letztes(werte: list[T]) -> T:
        return werte[-1]

    letztes([3, 1, 4])        # mypy weiß: das Ergebnis ist ein int
    letztes(["a", "b"])       # hier ist es ein str

Bei jedem Aufruf setzt mypy für T den passenden Typ ein, wie bei einer
Gleichung. Eine Funktion mit Typvariablen heißt generisch. Der Text in
TypeVar("T") muss mit dem Variablennamen übereinstimmen. Kommen zwei
voneinander unabhängige Typen vor, braucht man zwei Typvariablen:

    K = TypeVar("K")
    V = TypeVar("V")

    def tausche(paar: tuple[K, V]) -> tuple[V, K]:
        return paar[1], paar[0]

Würde man hier zweimal T schreiben, müsste mypy für beide Teile einen
gemeinsamen Typ finden: Bei ("a", 1) wird T zu object, und das Ergebnis
verrät nicht mehr, welcher Teil ein Text und welcher eine Zahl ist. Typvariablen lassen sich auch
schachteln: list[list[T]] ist eine Liste von Listen, deren Einträge alle
den Typ T haben, dict[K, list[V]] ordnet Schlüsseln Listen zu.

Zur Laufzeit ändert sich nichts: Python prüft auch Typvariablen nicht,
typing.get_type_hints(letztes) zeigt sie nur als ~T an. Ab Python 3.12
gibt es dafür die kürzere Schreibweise def letztes[T](werte: list[T]) ->
T; dieser Kurs läuft aber auch auf Python 3.11, darum bleibt es hier bei
TypeVar.
"""

from typing import TypeVar

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(erstes_oder(["PRJ-17", "PRJ-4"], "leer"), erstes_oder([], 0))
print(in_sprints([5, 3, 8, 2, 1], 2))
print(gruppiere([("Ada", "PRJ-17"), ("Bo", "PRJ-4"), ("Ada", "PRJ-9")]))
