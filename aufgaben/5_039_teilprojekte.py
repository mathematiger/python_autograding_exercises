"""Aufgabe 5_039 – Teilprojekte                                  Stufe 5 ★★★★★

Ein großes Softwareprojekt ist in Teilprojekte aufgeteilt, die bei
verschiedenen Partnerfirmen laufen. Jede Firma meldet über eine
Webschnittstelle, wie weit ihr Teilprojekt ist, als Fertigstellungsgrad
in Prozent. Die Projektleitung möchte jeden Morgen einen kurzen Bericht,
welche Teilprojekte noch nicht fertig sind. Eine Abfrage dauert, weil
das Programm auf die Antwort über das Netz warten muss; deshalb ist die
vorgegebene Funktion hole_stand eine Koroutine (async def). Hier ist sie
nur nachgebildet: Sie trägt Frage und Antwort in PROTOKOLL ein und liest
den Stand aus STAENDE.

Schreiben Sie drei Funktionen:

- `async def fortschritt(teilprojekte)` fragt die Teilprojekte mit
  hole_stand nacheinander in der Reihenfolge der Liste ab, jedes erst,
  wenn die Antwort auf das vorige da ist, und gibt ein Dictionary
  Teilprojekt → Prozent zurück.
- `async def offene(teilprojekte)` gibt mit fortschritt die Liste der
  Teilprojekte zurück, die unter 100 Prozent stehen, in der Reihenfolge
  der Liste.
- `def morgenbericht(teilprojekte)` ist eine gewöhnliche Funktion, die
  offene mit asyncio.run ausführt und ihr Ergebnis zurückgibt.

    STAENDE = {"Webshop": 100, "Lager": 80, "Zahlung": 35, "App": 0}
    morgenbericht(["Webshop", "Lager", "Zahlung", "App"])
    →  ["Lager", "Zahlung", "App"]
    asyncio.run(fortschritt(["Lager", "Webshop"]))
    →  {"Lager": 80, "Webshop": 100}

Grenzen: 0 bis 1000 verschiedene Teilprojekte, alle stehen in STAENDE,
die Stände sind ganze Zahlen von 0 bis 100.

Hintergrund: Viele Programme verbringen die meiste Zeit mit Warten: auf
einen Server, eine Datenbank, eine Datei. Python bietet dafür
Koroutinen. Eine Funktion mit async def ist eine Koroutinenfunktion;
ruft man sie auf, läuft noch nichts, man bekommt nur ein
Koroutinen-Objekt, eine Art angehaltene Funktion:

    import asyncio

    async def begruessung(name):
        await asyncio.sleep(0.1)      # warten, ohne das Programm zu blockieren
        return f"Hallo {name}"

    begruessung("Ada")                →  <coroutine object begruessung at 0x…>

Ausgeführt wird eine Koroutine erst von einer Ereignisschleife (event
loop), dem Teil von asyncio, der entscheidet, welche Koroutine gerade
weiterläuft. asyncio.run(koroutine) startet eine neue Schleife, lässt
die Koroutine bis zum Ende laufen und gibt ihr Ergebnis zurück. Das ist
die Brücke von gewöhnlichem zu asynchronem Code und steht meist genau
einmal ganz außen im Programm:

    asyncio.run(begruessung("Ada"))   →  "Hallo Ada"

Innerhalb einer Koroutine wartet await auf eine andere Koroutine und
liefert deren Ergebnis: text = await begruessung("Bo"). await darf nur
in einer async-Funktion stehen. Vergisst man es, bekommt man das
Koroutinen-Objekt statt des Ergebnisses, und Python warnt später
„coroutine … was never awaited“. Umgekehrt darf man asyncio.run nicht
innerhalb einer laufenden Schleife aufrufen, also nicht in einer
Koroutine; dort heißt es immer await.

Mehrere await nacheinander laufen nacheinander: Die zweite Abfrage
beginnt erst, wenn die erste fertig ist, die Wartezeiten addieren sich.
Wie man mehrere Abfragen gleichzeitig warten lässt, zeigt die nächste
Aufgabe. Koroutinen erinnern an die Generatoren mit send aus Aufgabe
5_027: Auch sie halten an einer Stelle an und machen später dort
weiter; await ist die Stelle, an der die Ereignisschleife eine andere
Koroutine weiterlaufen lassen darf.
"""

import asyncio

STAENDE = {"Webshop": 100, "Lager": 80, "Zahlung": 35, "App": 0}
PROTOKOLL = []


async def hole_stand(teilprojekt):
    """Fragt den Fertigstellungsgrad eines Teilprojekts in Prozent ab (hier nur nachgebildet)."""
    PROTOKOLL.append(f"frage {teilprojekt}")
    await asyncio.sleep(0)  # hier würde das Programm auf die Antwort der Partnerfirma warten
    PROTOKOLL.append(f"antwort {teilprojekt}")
    return STAENDE[teilprojekt]


async def fortschritt(teilprojekte):
    """Fragt die Teilprojekte nacheinander ab und gibt ein Dictionary Teilprojekt → Prozent zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


async def offene(teilprojekte):
    """Gibt die Teilprojekte zurück, die noch unter 100 Prozent stehen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def morgenbericht(teilprojekte):
    """Führt offene mit asyncio.run aus und gibt die offenen Teilprojekte zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(morgenbericht(["Webshop", "Lager", "Zahlung", "App"]))
