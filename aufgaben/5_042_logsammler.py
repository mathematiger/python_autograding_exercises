"""Aufgabe 5_042 – Logsammler                                    Stufe 5 ★★★★★

Ein Monitoring-Team sammelt die Logzeilen vieler Server an einer
Stelle. Jede Zeile beginnt mit ihrer Stufe, etwa "ERROR Platte voll"
oder "INFO Dienst gestartet". Die Server liefern ihre Zeilen
unterschiedlich schnell, und die Auswertung jeder Zeile dauert etwas.
Damit kein Server auf die Auswertung warten muss und die Auswertung nie
untätig ist, solange es Arbeit gibt, sollen Erzeuger (je einer pro
Server) die Zeilen in eine gemeinsame Warteschlange legen, aus der
mehrere Verbraucher sie holen und auswerten. Die Warteschlange hat nur
begrenzt Platz, damit ein gesprächiger Server nicht den Speicher füllt.

Die Auswertung einer Zeile ist die vorgegebene Koroutine auswerten: Sie
wartet kurz (hier nur nachgebildet) und gibt die Stufe der Zeile zurück.
Schreiben Sie drei Koroutinen:

- `async def erzeuger(server, zeilen, schlange)` legt jede Zeile der
  Liste zeilen als Paar (server, zeile) in die asyncio.Queue schlange,
  in ihrer Reihenfolge.
- `async def verbraucher(schlange, zaehler)` holt immer wieder einen
  Eintrag aus schlange. Ist er None, hört der Verbraucher auf. Sonst
  ermittelt er mit await auswerten(zeile) die Stufe und erhöht im
  Dictionary zaehler den Wert dieser Stufe um 1 (beim ersten Mal auf
  1). Nach jedem geholten Eintrag, auch nach None, ruft er
  schlange.task_done() auf.
- `async def sammle(quellen, verbraucherzahl, platz)` bekommt das
  Dictionary quellen (Server → Liste seiner Zeilen), legt eine
  asyncio.Queue mit platz Plätzen an, startet verbraucherzahl
  Verbraucher als Tasks und alle Erzeuger gleichzeitig, wartet, bis
  alle Zeilen ausgewertet sind und alle Verbraucher aufgehört haben, und
  gibt das Dictionary Stufe → Anzahl zurück.

    quellen = {
        "web1": ["INFO start", "ERROR Platte voll", "INFO ok"],
        "db1": ["WARN langsam", "ERROR Verbindung weg"],
    }
    asyncio.run(sammle(quellen, 2, 1))   →  {"INFO": 2, "ERROR": 2, "WARN": 1}

Die Reihenfolge der Schlüssel im Ergebnis ist egal.

Grenzen: quellen hat 0 bis 50 Server, zusammen 0 bis 5000 Zeilen; jede
Zeile ist ein Text, dessen erstes Wort die Stufe ist (Großbuchstaben),
danach ein Leerzeichen und beliebiger Text. verbraucherzahl ist eine
ganze Zahl von 1 bis 20, platz eine von 1 bis 1000.

Hintergrund: In Aufgabe 5_040 und 5_041 haben Koroutinen jede für sich
gearbeitet und erst am Ende ein Ergebnis abgegeben. Oft reicht aber eine
Koroutine einer anderen laufend Arbeit weiter. Dafür gibt es
asyncio.Queue, eine Warteschlange wie die deque aus Aufgabe 3_057, bei
der man auf das Holen und Ablegen warten kann:

    schlange = asyncio.Queue(maxsize=3)     # höchstens 3 Einträge
    await schlange.put(eintrag)             # wartet, solange sie voll ist
    eintrag = await schlange.get()          # wartet, solange sie leer ist
    schlange.qsize()                        # Zahl der wartenden Einträge

Das Warten ist der Witz: Ein Erzeuger, der eine volle Schlange vorfindet,
hält bei put an, und die Ereignisschleife lässt derweil die Verbraucher
laufen. Ein Verbraucher, der nichts vorfindet, hält bei get an, bis
etwas kommt. Ohne maxsize (oder mit 0) ist die Schlange unbegrenzt.

Wie hört ein Verbraucher auf, der in einer Endlosschleife auf get
wartet? Der übliche Weg ist eine Endmarke wie beim iter mit Sentinel
(Aufgabe 4_038): Wenn alle Erzeuger fertig sind, legt man für jeden
Verbraucher ein None in die Schlange; wer es holt, beendet seine
Schleife. Weil jeder Verbraucher nach seinem None nichts mehr holt,
bekommt jeder genau eines.

    verbraucher_tasks = [asyncio.create_task(verbraucher(…)) for _ in range(n)]
    await asyncio.gather(*(erzeuger(…) for … in …))
    for _ in range(n):
        await schlange.put(None)
    await asyncio.gather(*verbraucher_tasks)

Die Verbraucher müssen als Tasks (Aufgabe 5_041) schon laufen, bevor die
Erzeuger anfangen; sonst bleibt ein Erzeuger bei einer vollen Schlange
für immer stehen. task_done() meldet der Schlange, dass ein geholter
Eintrag erledigt ist; await schlange.join() wartet, bis zu jedem
abgelegten Eintrag ein task_done gemeldet wurde. Damit kann man die
Verbraucher auch ohne Endmarke beenden: join abwarten und die Tasks
dann mit cancel() abbrechen.

Mehrere Verbraucher dürfen hier ohne Sperre dasselbe Dictionary zaehler
ändern: Koroutinen wechseln sich nur an einem await ab, und zwischen dem
Lesen und dem Schreiben von zaehler[stufe] steht keins. Bei Threads
(kommen in Aufgabe 5_044, die Race Condition in Aufgabe 5_045) ist das anders.
"""

import asyncio

BEARBEITET = []


async def auswerten(zeile):
    """Wertet eine Logzeile aus (hier nur nachgebildet) und gibt ihre Stufe zurück."""
    BEARBEITET.append((asyncio.current_task(), zeile))
    await asyncio.sleep(0)  # die Auswertung dauert einen Moment
    return zeile.split(" ", 1)[0]


async def erzeuger(server, zeilen, schlange):
    """Legt jede Zeile als Paar (server, zeile) in die Schlange."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


async def verbraucher(schlange, zaehler):
    """Holt Einträge aus der Schlange und zählt ihre Stufen, bis None kommt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


async def sammle(quellen, verbraucherzahl, platz):
    """Wertet alle Zeilen mit Erzeugern, Verbrauchern und einer begrenzten Schlange aus."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


quellen = {
    "web1": ["INFO start", "ERROR Platte voll", "INFO ok"],
    "db1": ["WARN langsam", "ERROR Verbindung weg"],
}
try:
    print(asyncio.run(asyncio.wait_for(sammle(quellen, 2, 1), 2)))
except TimeoutError:
    print("sammle ist nach 2 Sekunden nicht fertig geworden; wartet ein Erzeuger oder Verbraucher für immer?")
