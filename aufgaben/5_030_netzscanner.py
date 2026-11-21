"""Aufgabe 5_030 – Netzscanner                                   Stufe 5 ★★★★★

Die IT-Abteilung prüft regelmäßig, welche Geräte im eigenen Firmennetz
antworten. Ein kleines Werkzeug erzeugt dafür die Adressen eines
Netzes, fragt jede an und wertet die gemessenen Antwortzeiten (Latenzen)
aus. Das Werkzeug soll in ein Projekt übernommen werden, das mit mypy
--strict geprüft wird; jede Funktion braucht deshalb genaue
Annotationen, die beschreiben, was hineingeht und was herauskommt.

Schreiben Sie die vier Funktionen vollständig, mit genau diesen
Annotationen (aus collections.abc, oben schon importiert):

- `hostadressen(praefix: str, erster: int, letzter: int) -> Iterator[str]`
  ist eine Generatorfunktion und liefert der Reihe nach die Adressen
  f"{praefix}.{nummer}" für nummer von erster bis einschließlich letzter.
- `erreichbare(adressen: Iterable[str], antwortet: Callable[[str], bool])
  -> Iterator[str]` ist eine Generatorfunktion und liefert die Adressen,
  für die antwortet(adresse) True ergibt, in ihrer Reihenfolge. Sie ruft
  antwortet erst auf, wenn die nächste Adresse gebraucht wird.
- `latenzstatistik() -> Generator[int, float | None, float]` ist eine
  Generatorfunktion, die Messwerte mit send annimmt. Das erste next()
  liefert 0, jedes send(wert) danach die Zahl der bisher empfangenen
  Werte. send(None) beendet sie; sie gibt dann den Mittelwert der Werte
  zurück, ohne Werte 0.0.
- `mittlere_latenz(messwerte: Iterable[float]) -> float` schickt alle
  Messwerte an eine neue latenzstatistik(), beendet sie mit send(None)
  und gibt deren Rückgabewert zurück.

    list(hostadressen("192.168.1", 1, 3))
        →  ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
    list(erreichbare(hostadressen("10.0.0", 1, 6), lambda a: a.endswith(("2", "5"))))
        →  ["10.0.0.2", "10.0.0.5"]
    s = latenzstatistik()
    next(s)  →  0      s.send(12.5)  →  1      s.send(7.5)  →  2
    s.send(None)  →  StopIteration mit dem Wert 10.0
    mittlere_latenz([12.5, 7.5, 4.0])  →  8.0

Grenzen: 0 ≤ erster, letzter ≤ 10**9; ist letzter < erster, liefert
hostadressen nichts. adressen kann jedes Iterable von Texten sein, auch
ein unendlicher Iterator. Messwerte sind Zahlen von 0 bis 10**4, es gibt
0 bis 100 000 davon.

Hintergrund: Annotationen wie list[str] kennen Sie aus Aufgabe 4_017.
Für alles, worüber man mit for laufen kann, gibt es im Modul
collections.abc feinere Typen, und die Wahl zwischen ihnen ist eine
Aussage über die Schnittstelle:

- Iterable[T]: Man kann einmal oder mehrmals mit for darüber laufen
  (Listen, Tupel, Mengen, range, Generatoren …). Mehr verspricht der Typ
  nicht: kein len(), kein Index. Als Typ eines Parameters ist er die
  großzügigste Wahl, denn die Funktion nimmt dann jede Art von Folge an.
- Iterator[T]: ein Iterable, das zusätzlich next() kennt und sich beim
  Durchlaufen verbraucht (Aufgabe 4_033). Generatorfunktionen geben
  einen Iterator zurück; wer nur Werte liefert, annotiert die Rückgabe
  darum meist mit Iterator[T].
- Generator[Y, S, R]: ein Iterator, dessen drei Typen man genau angibt:
  Y für das, was yield liefert, S für das, was send hineinschickt, und R
  für den Wert von return (Aufgabe 5_029). Iterator[T] ist dasselbe wie
  Generator[T, None, None] aus Sicht dessen, der nur liest.
- Callable[[A, B], R]: eine Funktion mit Argumenten der Typen A und B,
  die R zurückgibt; Callable[[str], bool] also eine Prüfung für Texte.

    from collections.abc import Callable, Generator, Iterable, Iterator

    def quadrate(zahlen: Iterable[int]) -> Iterator[int]:
        for zahl in zahlen:
            yield zahl * zahl

    def summierer() -> Generator[int, int, str]:
        summe = 0
        while summe < 100:
            summe += yield summe
        return f"fertig bei {summe}"

Ein Parameter vom Typ list[int] würde dagegen einen Generator ablehnen,
obwohl die Funktion ihn genauso gut verarbeiten könnte. Annotationen
prüft Python beim Ausführen nicht; das übernimmt mypy vor dem Start.
Lesen kann man sie aber zur Laufzeit, mit typing.get_type_hints(funktion);
so prüfen auch die Tests dieser Aufgabe. float | None heißt „ein float
oder None“ (gleichbedeutend mit Optional[float] aus typing).
"""

from collections.abc import Callable, Generator, Iterable, Iterator


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(list(hostadressen("192.168.1", 1, 3)))
print(list(erreichbare(hostadressen("10.0.0", 1, 6), lambda adresse: adresse.endswith(("2", "5")))))
print(mittlere_latenz([12.5, 7.5, 4.0]))
