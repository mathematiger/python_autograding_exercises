"""Aufgabe 4_017 – Backlogwerkzeuge                                Stufe 4 ★★★★☆

Ein Entwicklungsteam arbeitet agil: Alle Aufgaben stehen im Product
Backlog, einer nach Wichtigkeit geordneten Liste von User Stories, jede
mit einer Schätzung in Story Points. Für ihre Planungsskripte braucht das
Team ein paar kleine Werkzeuge, die nicht nur mit Stories funktionieren,
sondern ebenso mit Arbeitspaketen, Meilensteinen oder einfachen Texten.
Die Werkzeuge sollen typannotiert sein (Aufgabe 4_016), und zwar so, dass
ein Prüfwerkzeug wie mypy weiß: Wer eine Liste von Stories hineingibt,
bekommt Stories heraus, und wer Texte hineingibt, bekommt Texte heraus.

Vervollständigen Sie die drei Funktionen mit Annotationen. Legen Sie
dafür die Typvariablen T (für die Elemente) und K (für die Schlüssel) mit
TypeVar an.

- `erstes_passendes(elemente, bedingung)`: elemente ist eine Liste von T,
  bedingung eine Funktion, die ein T bekommt und True oder False
  liefert. Gibt das erste Element zurück, für das bedingung True ist,
  oder None, wenn es keins gibt. bedingung wird nur so oft aufgerufen wie
  nötig: nach dem ersten Treffer nicht mehr.
- `gruppiere(elemente, schluessel)`: schluessel ist eine Funktion, die
  ein T bekommt und ein K liefert. Gibt ein Dictionary von K auf Listen
  von T zurück: zu jedem Schlüssel die Elemente mit diesem Schlüssel, in
  ihrer Reihenfolge. Die Schlüssel stehen in der Reihenfolge, in der sie
  zum ersten Mal vorkommen.
- `in_bloecke(elemente, groesse)`: groesse ist eine ganze Zahl. Teilt die
  Liste der Reihe nach in Blöcke mit je groesse Elementen auf (der letzte
  darf kürzer sein) und gibt die Liste der Blöcke zurück. Ist groesse
  kleiner als 1, löst sie einen ValueError aus.

    backlog = [("Login", 5), ("Suche", 8), ("Export", 3), ("Hilfe", 1)]
    erstes_passendes(backlog, lambda story: story[1] >= 8)   →  ("Suche", 8)
    erstes_passendes(backlog, lambda story: story[1] > 13)   →  None
    gruppiere(["Analyse", "Entwurf", "Abnahme", "Einführung"], lambda text: text[0])
        →  {"A": ["Analyse", "Abnahme"], "E": ["Entwurf", "Einführung"]}
    in_bloecke(backlog, 3)
        →  [[("Login", 5), ("Suche", 8), ("Export", 3)], [("Hilfe", 1)]]

Grenzen: elemente hat 0 bis 100 000 Einträge beliebigen Typs (in einem
Aufruf alle vom selben Typ). bedingung und schluessel lösen keine
Ausnahme aus, die Schlüssel sind hashbar. groesse ist eine ganze Zahl von
-10 bis 10**6.

Hintergrund: Eine Annotation wie list[str] -> str legt den Typ fest. Für
eine Funktion, die mit jedem Typ arbeitet, wäre list[Any] -> Any (Any aus
typing heißt „irgendein Typ“) zu ungenau: mypy wüsste dann nicht mehr,
dass bei einer Liste von Texten ein Text herauskommt, und könnte keinen
Fehler mehr melden. Dafür gibt es Typvariablen:

    from typing import TypeVar

    T = TypeVar("T")

    def letztes(elemente: list[T]) -> T:
        return elemente[-1]

T steht für einen Typ, der erst beim Aufruf feststeht. Kommt T in einer
Signatur mehrmals vor, ist es überall derselbe Typ: Bei letztes(["a",
"b"]) ist T gleich str, also ist das Ergebnis ein str; bei letztes([1, 2])
ist es ein int. Der Text in TypeVar("T") muss so heißen wie die Variable.
Mehrere unabhängige Typen bekommen mehrere Typvariablen, etwa T und K in
dict[K, list[T]].

Funktionen als Parameter annotiert man mit Callable aus collections.abc:
Callable[[T], bool] ist eine Funktion, die ein T bekommt und ein bool
liefert; Callable[[int, int], str] bekommt zwei ganze Zahlen und liefert
einen Text. Kann ein Ergebnis fehlen, schreibt man wie in Aufgabe 4_016
T | None.

Seit Python 3.12 gibt es eine kürzere Schreibweise ohne TypeVar, def
letztes[T](elemente: list[T]) -> T; dieser Kurs bleibt bei 3.11 und
schreibt TypeVar. Wie alle Annotationen prüft Python Typvariablen zur
Laufzeit nicht; sie sind für mypy und für die Leser des Codes.
"""

from collections.abc import Callable
from typing import TypeVar

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


backlog = [("Login", 5), ("Suche", 8), ("Export", 3), ("Hilfe", 1)]
print(erstes_passendes(backlog, lambda story: story[1] >= 8))
print(gruppiere(["Analyse", "Entwurf", "Abnahme", "Einführung"], lambda text: text[0]))
print(in_bloecke(backlog, 3))
