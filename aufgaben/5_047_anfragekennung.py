"""Aufgabe 5_047 – Anfragekennung                                Stufe 5 ★★★★★

Ein Webdienst für Kundendaten bearbeitet viele Anfragen gleichzeitig
mit asyncio. Wenn etwas schiefgeht, sucht das Monitoring-Team im
Protokoll nach der Ursache, aber die Zeilen verschiedener Anfragen
stehen bunt durcheinander: Während eine Anfrage auf die Datenbank
wartet, schreibt schon die nächste. Deshalb bekommt jede Anfrage beim
Eingang eine Kennung (eine Korrelations-ID), und jede Protokollzeile
soll mit dieser Kennung beginnen. Sie als Parameter durch jede Funktion
zu reichen, wäre mühsam und fehleranfällig; eine globale Variable geht
nicht, weil sich die Anfragen gegenseitig überschreiben würden.

Vorgegeben sind die Kontextvariable ANFRAGE (Standardwert "-"), die
Liste PROTOKOLL und die Koroutine lade_kunde, die selbst protokolliert
und auf die Datenbank wartet (hier mit asyncio.sleep). Schreiben Sie:

- `protokolliere(text)` hängt an PROTOKOLL die Zeile "[<kennung>] <text>"
  an, mit der Kennung der aktuellen Anfrage aus ANFRAGE.
- `mit_kennung(kennung)` ist ein Kontextmanager (mit
  contextlib.contextmanager): Im with-Block hat ANFRAGE den Wert
  kennung, danach wieder den Wert von vorher, auch nach einer Ausnahme
  und auch, wenn with-Blöcke ineinander stehen.
- `bearbeite(kennung, kunde, wartezeit)` ist eine Koroutine: Unter der
  Kennung protokolliert sie "Anfrage beginnt", wartet auf
  lade_kunde(kunde, wartezeit), protokolliert "Anfrage fertig" und gibt
  zurück, was lade_kunde liefert.
- `bearbeite_alle(anfragen)` ist eine Koroutine, die alle Anfragen,
  Tripel (kennung, kunde, wartezeit), mit asyncio.gather gleichzeitig
  bearbeitet und die Liste der Ergebnisse in derselben Reihenfolge
  zurückgibt.
- `im_thread(funktion, *argumente)` führt funktion(*argumente) in einem
  neuen Thread aus, und zwar in einer Kopie des aktuellen Kontexts,
  damit der Thread die Kennung kennt; sie wartet auf den Thread und gibt
  das Ergebnis zurück.

    asyncio.run(bearbeite_alle([("A1", "Kaya", 0.2), ("B2", "Berg", 0.1)]))
    →  ["Kunde Kaya", "Kunde Berg"]
    PROTOKOLL
    →  ["[A1] Anfrage beginnt", "[A1] lade Kunde Kaya",
        "[B2] Anfrage beginnt", "[B2] lade Kunde Berg",
        "[B2] Kunde Berg geladen", "[B2] Anfrage fertig",
        "[A1] Kunde Kaya geladen", "[A1] Anfrage fertig"]

    with mit_kennung("C3"):
        im_thread(protokolliere, "Bericht erstellt")   # schreibt "[C3] Bericht erstellt"

Grenzen: anfragen hat 0 bis 1000 Tripel mit verschiedenen, nicht leeren
Kennungen; kunde ist ein nicht leerer Text, wartezeit eine Zahl von 0
bis 0,2 Sekunden.

Hintergrund: Seit Aufgabe 5_040 laufen bei Ihnen mehrere Koroutinen
gleichzeitig, seit Aufgabe 5_044 auch Threads. Eine globale Variable
gibt es aber nur einmal: Setzt Anfrage A sie auf "A1" und wartet, setzt
Anfrage B sie in der Zwischenzeit auf "B2", und wenn A weiterläuft,
protokolliert sie unter der falschen Kennung. Das Modul contextvars
löst das. Eine ContextVar ist eine Variable, deren Wert vom Kontext
abhängt, in dem der Code gerade läuft:

    import contextvars

    BENUTZER = contextvars.ContextVar("benutzer", default="anonym")

    BENUTZER.get()                  →  "anonym"
    token = BENUTZER.set("kim")     # setzt den Wert im aktuellen Kontext
    BENUTZER.get()                  →  "kim"
    BENUTZER.reset(token)           # stellt den Wert von vor diesem set wieder her
    BENUTZER.get()                  →  "anonym"

set gibt ein Token zurück, und reset(token) stellt genau den Wert von
vorher wieder her; deshalb funktioniert das auch ineinander, anders als
ein set("-") am Ende. Zusammen mit try/finally in einem Kontextmanager
aus Aufgabe 4_052 bleibt das auch nach Ausnahmen sauber.

Ein Kontext ist eine Zuordnung Kontextvariable → Wert. Jeder Task von
asyncio (asyncio.gather macht aus jeder Koroutine einen, Aufgabe 5_041)
bekommt beim Anlegen eine Kopie des Kontexts, in dem er angelegt wurde,
und arbeitet in dieser Kopie. Was ein Task mit set ändert, sieht nur er
selbst: Die Anfragen kommen sich nicht in die Quere, und der Aufrufer
von gather sieht hinterher seinen eigenen Wert unverändert. Ein neuer
Thread dagegen beginnt normalerweise mit einem frischen Kontext, in dem
jede Variable ihren Standardwert hat. Ihm gibt man die Kennung mit,
indem man den aktuellen Kontext kopiert und die Funktion darin laufen
lässt:

    kontext = contextvars.copy_context()      # Momentaufnahme aller Werte
    kontext.run(funktion, 1, 2)               # ruft funktion(1, 2) in dieser Kopie auf
    threading.Thread(target=kontext.run, args=(funktion, 1, 2))

Einen Rückgabewert liefert ein Thread nicht; man legt ihn wie in
Aufgabe 5_044 irgendwo ab, wo man ihn nach join() findet, etwa in einer
Liste. So arbeiten auch Webframeworks und Protokollbibliotheken: Die
Kennung der Anfrage, der angemeldete Benutzer oder die Sprache stehen
in Kontextvariablen statt in globalen Variablen.
"""

import asyncio
import contextlib
import contextvars
import threading

ANFRAGE = contextvars.ContextVar("anfrage", default="-")
PROTOKOLL = []


async def lade_kunde(kunde, wartezeit):
    """Lädt einen Kunden aus der Datenbank (hier nur nachgebildet) und protokolliert dabei."""
    protokolliere(f"lade Kunde {kunde}")
    await asyncio.sleep(wartezeit)  # wartet auf die Datenbank
    protokolliere(f"Kunde {kunde} geladen")
    return f"Kunde {kunde}"


def protokolliere(text):
    """Hängt eine Zeile mit der Kennung der aktuellen Anfrage an PROTOKOLL an."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


@contextlib.contextmanager
def mit_kennung(kennung):
    """Setzt ANFRAGE im with-Block auf kennung und stellt danach den alten Wert wieder her."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


async def bearbeite(kennung, kunde, wartezeit):
    """Bearbeitet eine Anfrage unter ihrer Kennung und gibt den geladenen Kunden zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


async def bearbeite_alle(anfragen):
    """Bearbeitet alle Anfragen gleichzeitig und gibt ihre Ergebnisse in derselben Reihenfolge zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def im_thread(funktion, *argumente):
    """Führt funktion(*argumente) in einem Thread mit einer Kopie des aktuellen Kontexts aus und gibt das Ergebnis zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(asyncio.run(bearbeite_alle([("A1", "Kaya", 0.2), ("B2", "Berg", 0.1)])))
with mit_kennung("C3"):
    im_thread(protokolliere, "Bericht erstellt")
for zeile in PROTOKOLL:
    print(zeile)
