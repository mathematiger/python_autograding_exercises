"""Aufgabe 5_027 – Platzierer                                    Stufe 5 ★★★★★

In einem Rechenzentrum kommen Anfragen für neue virtuelle Maschinen (VMs)
nacheinander herein, jede mit dem Arbeitsspeicher, den sie braucht, in
GB. Ein Platzierer entscheidet sofort für jede Anfrage, auf welchem Host
(physischen Server) die VM läuft: auf dem ersten Host in der festen
Reihenfolge der Liste, der noch genug freien Speicher hat (First Fit).
Passt die VM nirgends, wird sie abgelehnt. Der Platzierer muss sich also
zwischen den Anfragen merken, wie viel auf jedem Host noch frei ist.

Dafür soll ein Generator als Koroutine dienen, dem man jede Anfrage mit
send schickt und der die Entscheidung zurückliefert. Vervollständigen
Sie:

- `gestartet(generatorfunktion)` ist ein Dekorator. Die dekorierte
  Funktion erzeugt beim Aufruf den Generator, ruft einmal next() auf und
  gibt den so gestarteten Generator zurück. Name und Docstring der
  Funktion bleiben erhalten (functools.wraps).
- `platzierer(kapazitaeten)` ist eine mit @gestartet dekorierte
  Generatorfunktion. kapazitaeten ist ein Dictionary Host → freier
  Speicher in GB, seine Reihenfolge ist die Reihenfolge der Hosts; es
  wird nicht verändert. Jedes send(ram) liefert den Namen des Hosts, auf
  den die VM kommt, und zieht ram von dessen freiem Speicher ab, oder
  None, wenn kein Host genug frei hat (dann ändert sich nichts).
- `verteile(kapazitaeten, anfragen)` benutzt platzierer und gibt die
  Liste der Entscheidungen für alle Anfragen zurück.

    p = platzierer({"host1": 64, "host2": 32})
    p.send(48)   →  "host1"    (host1 hat noch 16 frei)
    p.send(20)   →  "host2"    (host2 hat noch 12 frei)
    p.send(16)   →  "host1"    (passt genau, host1 hat noch 0 frei)
    p.send(20)   →  None
    p.send(12)   →  "host2"
    verteile({"a": 8, "b": 8}, [4, 6, 4, 6])  →  ["a", "b", "a", None]

Grenzen: 0 ≤ len(kapazitaeten) ≤ 50, freier Speicher von 0 bis 10**4 GB
je Host, Hostnamen sind verschiedene Texte. Jede Anfrage ist eine ganze
Zahl von 1 bis 10**4; anfragen hat 0 bis 20 000 Einträge. Mehrere
Platzierer können gleichzeitig unabhängig voneinander laufen.

Hintergrund: Bisher lieferte ein Generator nur Werte nach außen (Aufgabe
4_034). Ein yield ist aber auch ein Ausdruck, der einen Wert von außen
empfangen kann. Mit generator.send(wert) setzt man den Generator fort;
das yield, an dem er wartet, ergibt dann wert, und send liefert den
Wert des nächsten yield zurück. So wird aus dem Generator eine
Koroutine: ein Stück Code, das zwischen den Aufrufen seinen Zustand in
lokalen Variablen behält und Daten empfängt.

    def mittelwert():
        summe, anzahl, schnitt = 0, 0, None
        while True:
            wert = yield schnitt        # liefert schnitt, wartet auf send
            summe += wert
            anzahl += 1
            schnitt = summe / anzahl

    m = mittelwert()
    next(m)          →  None  (läuft bis zum ersten yield)
    m.send(10)       →  10.0
    m.send(20)       →  15.0

Der erste Schritt ist besonders: Ein frischer Generator steht noch vor
seiner ersten Zeile, an keinem yield, das etwas empfangen könnte.
m.send(10) würde einen TypeError auslösen („can't send non-None value
to a just-started generator“). Man muss ihn erst mit next(m) (gleich
bedeutend: m.send(None)) bis zum ersten yield laufen lassen; das nennt
man Starten oder Vorbereiten (englisch priming). Weil man das leicht
vergisst, übernimmt es gern ein Dekorator (Aufgabe 4_022):

    import functools

    def vorbereitet(funktion):
        @functools.wraps(funktion)
        def huelle(*args, **kwargs):
            generator = funktion(*args, **kwargs)
            next(generator)
            return generator
        return huelle

Gegenüber einer Klasse mit Attributen und einer Methode hat die
Koroutine den Vorteil, dass ihr Zustand einfach aus lokalen Variablen
besteht und der Ablauf von oben nach unten lesbar bleibt. Was der
Generator beim ersten yield nach außen gibt, holt der Dekorator mit
next ab; bei platzierer ist das None.
"""

import functools


def gestartet(generatorfunktion):
    """Dekorator: erzeugt den Generator, startet ihn mit next() und gibt ihn zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


@gestartet
def platzierer(kapazitaeten):
    """Empfängt mit send den Speicherbedarf einer VM und liefert den gewählten Host oder None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def verteile(kapazitaeten, anfragen):
    """Gibt für jede Anfrage den gewählten Host oder None zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


p = platzierer({"host1": 64, "host2": 32})
print(p.send(48), p.send(20), p.send(16), p.send(20), p.send(12))
print(verteile({"a": 8, "b": 8}, [4, 6, 4, 6]))
