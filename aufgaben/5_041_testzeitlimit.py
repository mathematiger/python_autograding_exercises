"""Aufgabe 5_041 – Testzeitlimit                                 Stufe 5 ★★★★★

Ein Entwicklungsteam lässt vor jeder Auslieferung alle Testsammlungen
laufen: die Tests für die Oberfläche, die Datenbank, die Schnittstellen
und so weiter. Manche Sammlung hängt gelegentlich, weil ein Test auf
einen Dienst wartet, der nie antwortet. Damit die Auslieferung nicht
ewig wartet, bekommt jede Sammlung ein Zeitlimit; wer es überschreitet,
wird abgebrochen. Außerdem sollen alle Sammlungen gleichzeitig laufen,
damit das Warten nicht so lange dauert.

Eine Testsammlung ist die vorgegebene Koroutine testlauf, hier
nachgebildet: Sie trägt Beginn, Ende und Aufräumen in PROTOKOLL ein.
Steht die Sammlung in HAENGT, wartet sie eine Stunde; steht sie in
KAPUTT, schlägt ein Test fehl, und sie löst einen AssertionError aus. Am
Ende räumt sie immer auf (finally), auch wenn sie abgebrochen wird.

Schreiben Sie zwei Koroutinen:

- `async def mit_zeitlimit(name, sekunden)` führt testlauf(name) mit dem
  Zeitlimit sekunden aus und gibt "bestanden", "fehlgeschlagen" (bei
  einem AssertionError) oder "abgebrochen" (Zeitlimit überschritten)
  zurück. Eine abgebrochene Sammlung muss aufgeräumt haben, bevor
  mit_zeitlimit zurückkehrt.
- `async def alle(namen, sekunden)` startet für jede Sammlung zuerst mit
  asyncio.create_task eine Task mit mit_zeitlimit, sodass alle
  gleichzeitig laufen, wartet dann auf alle und gibt ein Dictionary
  Name → Ergebnis zurück, in der Reihenfolge der Liste namen.

    HAENGT = {"schnittstellen"}
    KAPUTT = {"datenbank"}
    asyncio.run(alle(["oberflaeche", "datenbank", "schnittstellen"], 0.1))
    →  {"oberflaeche": "bestanden", "datenbank": "fehlgeschlagen",
        "schnittstellen": "abgebrochen"}

Grenzen: namen hat 0 bis 1000 verschiedene Einträge, sekunden ist eine
Zahl von 0.01 bis 10. Eine Sammlung, die nicht hängt, ist nach wenigen
Runden der Ereignisschleife fertig; testlauf löst keine andere Ausnahme
als AssertionError aus.

Hintergrund: asyncio.gather (Aufgabe 5_040) startet Koroutinen und
wartet sofort auf alle. Mehr Kontrolle gibt eine Task: asyncio.
create_task(koroutine) meldet die Koroutine bei der Ereignisschleife an
und gibt ein Task-Objekt zurück. Die Koroutine läuft los, sobald die
aufrufende Koroutine das nächste Mal wartet, und man kann später mit
await task auf ihr Ergebnis warten. Wer erst alle Tasks anlegt und dann
auf sie wartet, lässt sie gleichzeitig laufen:

    tasks = [asyncio.create_task(warte(name)) for name in namen]
    ergebnisse = [await task for task in tasks]

Würde man stattdessen in der Schleife await warte(name) schreiben,
liefen sie wieder nacheinander wie in Aufgabe 5_039.

Eine Task kann man abbrechen: task.cancel() wirft beim nächsten await in
der Koroutine einen asyncio.CancelledError. Er läuft wie jede Ausnahme
durch try/finally, sodass die Koroutine aufräumen kann, und kommt am Ende
beim await task an. asyncio.wait_for(koroutine, sekunden) erledigt
Zeitlimit und Abbruch in einem: Ist die Koroutine nicht rechtzeitig
fertig, bricht wait_for sie ab, wartet, bis sie aufgeräumt hat, und löst
dann einen TimeoutError aus. Andere Ausnahmen der Koroutine kommen
unverändert heraus:

    try:
        ergebnis = await asyncio.wait_for(langsam(), 0.5)
    except TimeoutError:
        ergebnis = None

(Seit Python 3.11 ist asyncio.TimeoutError dasselbe wie das eingebaute
TimeoutError.) Den CancelledError fängt man in der Regel nicht selbst ab
und verschluckt ihn nie, sonst lässt sich die Koroutine nicht mehr
abbrechen; er ist deshalb auch keine Unterklasse von Exception.
"""

import asyncio

HAENGT = set()
KAPUTT = set()
PROTOKOLL = []


async def testlauf(name):
    """Führt die Testsammlung name aus (hier nur nachgebildet)."""
    PROTOKOLL.append(f"beginn {name}")
    try:
        await asyncio.sleep(0)
        if name in HAENGT:
            await asyncio.sleep(3600)  # wartet auf einen Dienst, der nie antwortet
        if name in KAPUTT:
            raise AssertionError(f"{name}: ein Test ist fehlgeschlagen")
        PROTOKOLL.append(f"ende {name}")
    finally:
        PROTOKOLL.append(f"aufgeraeumt {name}")


async def mit_zeitlimit(name, sekunden):
    """Führt testlauf(name) mit Zeitlimit aus und gibt "bestanden", "fehlgeschlagen" oder "abgebrochen" zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


async def alle(namen, sekunden):
    """Lässt alle Testsammlungen als Tasks gleichzeitig laufen und gibt Name → Ergebnis zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


HAENGT.add("schnittstellen")
KAPUTT.add("datenbank")
print(asyncio.run(alle(["oberflaeche", "datenbank", "schnittstellen"], 0.1)))
HAENGT.clear()
KAPUTT.clear()
