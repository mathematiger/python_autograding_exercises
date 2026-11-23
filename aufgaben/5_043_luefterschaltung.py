"""Aufgabe 5_043 – Lüfterschaltung                               Stufe 5 ★★★★★

In einem kleinen Technikraum schickt ein Temperatursensor über das
Netz laufend Messwerte in °C. Ein Steuerprogramm soll daraus Befehle
für einen Lüfter machen: Wird es zu warm, schaltet es ihn ein, ist es
wieder kühl genug, schaltet es ihn aus. Damit der Lüfter nicht bei
jedem Zehntelgrad um eine Grenze herum klackt, gibt es zwei Grenzen
(eine Hysterese): Der Lüfter geht an, sobald ein Wert mindestens ein
ist, und erst wieder aus, sobald ein Wert höchstens aus ist. Am Anfang
ist er aus.

Der Sensor ist der vorgegebene asynchrone Generator sensor: Er baut eine
Verbindung auf, liefert die Werte einzeln, wartet vor jedem auf die
nächste Nachricht und trennt am Ende die Verbindung (im finally, also
auch, wenn er vorher geschlossen wird). Beides trägt er in PROTOKOLL
ein. Schreiben Sie:

- `async def schaltbefehle(quelle, ein, aus)`, einen asynchronen
  Generator, der die Werte aus quelle mit async for liest und für jeden
  Schaltvorgang das Tupel (befehl, nummer, wert) liefert: befehl ist
  "ein" oder "aus", nummer die Stelle des Werts in quelle (ab 0). Er
  liest nur so viele Werte, wie er für den nächsten Befehl braucht.
- `async def erste(quelle, anzahl)` gibt die ersten anzahl Elemente aus
  der asynchronen Quelle quelle als Liste zurück (alle, wenn es weniger
  sind) und schließt die Quelle, bevor sie zurückkehrt.
- `async def schaltplan(werte, ein, aus)` gibt alle Schaltbefehle für
  die Liste werte als Liste zurück. Benutzen Sie dafür
  schaltbefehle(sensor(werte), ein, aus), am kürzesten mit einer
  asynchronen Comprehension.

    werte = [24.0, 27.5, 28.0, 26.0, 25.0, 24.5, 29.0]
    asyncio.run(schaltplan(werte, 28, 25))
    →  [("ein", 2, 28.0), ("aus", 4, 25.0), ("ein", 6, 29.0)]
    asyncio.run(erste(sensor(werte), 3))   →  [24.0, 27.5, 28.0]
    PROTOKOLL                              →  [..., "verbunden", "getrennt"]

Grenzen: werte hat 0 bis 10 000 Zahlen von -50 bis 150; aus und ein sind
Zahlen von -50 bis 150 mit aus < ein. quelle ist ein asynchroner
Generator, der auch endlos sein kann; anzahl ist eine ganze Zahl von 0
bis 10 000.

Hintergrund: Eine for-Schleife holt mit next() Element für Element
(Aufgabe 3_020). Kommen die Elemente aus dem Netz, muss man auf jedes
warten, und dafür braucht es ein await. Das asynchrone Gegenstück heißt
async for: Es ruft __anext__() auf und wartet mit await auf das Ergebnis.
Ein Objekt, das das kann, ist asynchron iterierbar; am Ende löst
__anext__ statt StopIteration ein StopAsyncIteration aus. async for
darf, wie await, nur in einer Koroutine stehen.

Am einfachsten schreibt man so etwas als asynchronen Generator: eine
Funktion mit async def, in der yield vorkommt. Sie darf beides, mit
await warten und mit yield liefern:

    async def zaehler(bis):
        for zahl in range(bis):
            await asyncio.sleep(0)       # wartet auf etwas
            yield zahl

    async def main():
        async for zahl in zaehler(3):
            print(zahl)                  # 0, 1, 2

Wie gewöhnliche Generatoren (Aufgabe 4_034) laufen asynchrone erst
weiter, wenn man das nächste Element verlangt. Liest ein asynchroner
Generator aus einem anderen, entsteht eine Pipeline wie in Aufgabe 4_036,
die nie mehr Werte holt als nötig, auch nicht bei einer endlosen Quelle.
Comprehensions gibt es auch asynchron, und sie dürfen ebenfalls nur in
einer Koroutine stehen:

    zahlen = [zahl async for zahl in zaehler(3)]     # [0, 1, 2]

Bricht man ein async for mit break ab, ist der Generator noch nicht zu
Ende: Sein finally läuft erst, wenn er geschlossen wird. Ein gewöhnlicher
Generator wird sofort geschlossen, sobald ihn niemand mehr braucht
(Aufgabe 5_028); einen asynchronen schließt Python dagegen erst irgendwann
später, weil close dort selbst ein await braucht: await gen.aclose().
Damit das nicht vergessen wird, gibt es contextlib.aclosing, einen
asynchronen Kontextmanager für async with (das asynchrone with):

    from contextlib import aclosing

    async with aclosing(zaehler(100)) as quelle:
        async for zahl in quelle:
            if zahl == 2:
                break
    # hier ist zaehler(100) schon geschlossen, sein finally ist gelaufen

So wird eine Netzverbindung getrennt, sobald man genug Werte hat.
"""

import asyncio
from contextlib import aclosing

PROTOKOLL = []


async def sensor(werte):
    """Liefert die Messwerte einzeln, wie sie über das Netz kommen (hier nur nachgebildet)."""
    PROTOKOLL.append("verbunden")
    try:
        for wert in werte:
            await asyncio.sleep(0)  # wartet auf die nächste Nachricht
            yield wert
    finally:
        PROTOKOLL.append("getrennt")


async def schaltbefehle(quelle, ein, aus):
    """Liefert (befehl, nummer, wert) für jedes Ein- und Ausschalten des Lüfters."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


async def erste(quelle, anzahl):
    """Gibt die ersten anzahl Elemente von quelle zurück und schließt die Quelle."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


async def schaltplan(werte, ein, aus):
    """Gibt alle Schaltbefehle für die Messwerte werte als Liste zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


werte = [24.0, 27.5, 28.0, 26.0, 25.0, 24.5, 29.0]
print(asyncio.run(schaltplan(werte, 28, 25)))
print(asyncio.run(erste(sensor(werte), 3)))
PROTOKOLL.clear()
