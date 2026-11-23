"""Aufgabe 5_040 – Datenknoten                                   Stufe 5 ★★★★★

Die Kundendatenbank eines Versandhändlers ist so groß, dass sie auf
mehrere Rechner verteilt ist, die Datenknoten. Jeder Knoten speichert
einen Teil der Kunden. Wer alle Kunden aus einem Ort sucht, muss also
jeden Knoten fragen und die Antworten zusammensetzen. Fragt man die
Knoten nacheinander, addieren sich ihre Antwortzeiten; fragt man alle
gleichzeitig, wartet man nur so lange wie auf den langsamsten.

Die Abfrage eines Knotens ist die vorgegebene Koroutine abfrage, hier
nachgebildet: Sie trägt Beginn und Ende in PROTOKOLL ein, wartet
DAUER[knoten] Runden der Ereignisschleife und gibt die Namen der Kunden
aus ort zurück, die auf diesem Knoten liegen. Ein Knoten in AUSGEFALLEN
antwortet nicht; dann löst abfrage einen ConnectionError aus.

Schreiben Sie drei Funktionen:

- `async def frage_alle(knoten, ort)` fragt alle Knoten der Liste
  gleichzeitig ab und gibt die Liste ihrer Ergebnisse zurück, in der
  Reihenfolge der Liste knoten, egal welcher zuerst antwortet. Fällt
  ein Knoten aus, darf der ConnectionError nach außen gehen.
- `async def frage_robust(knoten, ort)` fragt ebenfalls alle
  gleichzeitig ab, lässt sich aber von ausgefallenen Knoten nicht
  aufhalten. Sie gibt ein Paar (namen, ausgefallen) zurück: namen sind
  die Ergebnisse aller Knoten, die geantwortet haben, hintereinander in
  einer Liste, ausgefallen die Liste der Knoten mit ConnectionError,
  beides in der Reihenfolge der Liste knoten.
- `def kunden_in(knoten, ort)` führt frage_robust mit asyncio.run aus
  und gibt ihr Ergebnis zurück.

    DATEN = {"nord": [("Ada", "Kiel"), ("Bo", "Bonn")],
             "mitte": [("Cem", "Kiel")], "sued": [("Dana", "Kiel")]}
    DAUER = {"nord": 3, "mitte": 1, "sued": 2}
    asyncio.run(frage_alle(["nord", "mitte", "sued"], "Kiel"))
    →  [["Ada"], ["Cem"], ["Dana"]]
    AUSGEFALLEN = {"mitte"}
    kunden_in(["nord", "mitte", "sued"], "Kiel")
    →  (["Ada", "Dana"], ["mitte"])

Grenzen: knoten hat 0 bis 1000 verschiedene Einträge, alle stehen in
DATEN und DAUER. DAUER ist für jeden Knoten eine ganze Zahl von 1 bis 5,
jeder Knoten hat 0 bis 100 Kunden. Ein Knoten löst höchstens einen
ConnectionError aus, keine andere Ausnahme.

Hintergrund: In Aufgabe 5_039 liefen mehrere await nacheinander. Damit
Koroutinen gleichzeitig warten, übergibt man sie der Ereignisschleife
gemeinsam. asyncio.gather(k1, k2, …) nimmt beliebig viele Koroutinen,
startet alle, wartet, bis alle fertig sind, und liefert ihre Ergebnisse
als Liste, und zwar in der Reihenfolge der Argumente, nicht in der
Reihenfolge, in der sie fertig wurden:

    async def warte(name, sekunden):
        await asyncio.sleep(sekunden)
        return name

    await asyncio.gather(warte("a", 0.3), warte("b", 0.1))   →  ["a", "b"]

Das dauert etwa 0.3 Sekunden statt 0.4: Während warte("a", …) schläft,
läuft warte("b", …) weiter. Das ist Nebenläufigkeit, keine echte
Parallelität: Es rechnet immer nur eine Koroutine, aber das Warten
überlappt. Eine Liste von Koroutinen übergibt man mit dem Stern
(Aufgabe 4_018): await asyncio.gather(*[warte(n, 0.1) for n in namen]).

Löst eine der Koroutinen eine Ausnahme aus, gibt gather sie ohne weitere
Angaben an den Aufrufer weiter; die Ergebnisse der anderen sind dann
verloren. Mit return_exceptions=True steht die Ausnahme stattdessen als
Objekt an ihrem Platz in der Ergebnisliste, und man prüft selbst mit
isinstance (Aufgabe 4_056), was ein Ergebnis und was ein Fehler ist:

    ergebnisse = await asyncio.gather(*koroutinen, return_exceptions=True)
    for ergebnis in ergebnisse:
        if isinstance(ergebnis, ConnectionError):
            ...
"""

import asyncio

DATEN = {"nord": [("Ada", "Kiel"), ("Bo", "Bonn")], "mitte": [("Cem", "Kiel")], "sued": [("Dana", "Kiel")]}
DAUER = {"nord": 3, "mitte": 1, "sued": 2}
AUSGEFALLEN = set()
PROTOKOLL = []


async def abfrage(knoten, ort):
    """Gibt die Namen der Kunden aus ort zurück, die auf knoten gespeichert sind (hier nur nachgebildet)."""
    PROTOKOLL.append(f"beginn {knoten}")
    for _ in range(DAUER[knoten]):
        await asyncio.sleep(0)  # hier würde das Programm auf die Antwort des Knotens warten
    if knoten in AUSGEFALLEN:
        PROTOKOLL.append(f"ausfall {knoten}")
        raise ConnectionError(f"Datenknoten {knoten} antwortet nicht")
    PROTOKOLL.append(f"ende {knoten}")
    return [name for name, wohnort in DATEN[knoten] if wohnort == ort]


async def frage_alle(knoten, ort):
    """Fragt alle Knoten gleichzeitig ab und gibt ihre Ergebnisse in der Reihenfolge der Liste zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


async def frage_robust(knoten, ort):
    """Fragt alle Knoten gleichzeitig ab; gibt (namen, ausgefallen) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def kunden_in(knoten, ort):
    """Führt frage_robust mit asyncio.run aus und gibt (namen, ausgefallen) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(asyncio.run(frage_alle(["nord", "mitte", "sued"], "Kiel")))
AUSGEFALLEN.add("mitte")
print(kunden_in(["nord", "mitte", "sued"], "Kiel"))
AUSGEFALLEN.clear()
