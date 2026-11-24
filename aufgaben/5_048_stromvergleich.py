"""Aufgabe 5_048 – Stromvergleich                                Stufe 5 ★★★★★

Ein IT-Dienstleister schließt für seinen Serverraum einen neuen
Stromvertrag ab. Die Geschäftsführung will zwei Dinge: möglichst
geringe Jahreskosten und Strom mit wenig CO₂ je Kilowattstunde. Ein
kleines Vergleichswerkzeug fragt deshalb bei mehreren Stromanbietern
über deren Schnittstellen ein Angebot an. Jedes Angebot ist ein
Dictionary mit dem Grundpreis in Euro pro Jahr, dem Arbeitspreis in
Cent pro Kilowattstunde und dem CO₂-Wert in Gramm pro Kilowattstunde.
Manche Anbieter antworten schnell, manche gar nicht rechtzeitig, und
bei manchen kommt ein Fehler zurück. Weil ein Teil des Werkzeugs schon
mit asyncio arbeitet und ein anderer mit Threads, soll es die Abfrage
in beiden Fassungen geben, und beide sollen dasselbe Ergebnis liefern.

Vorgegeben sind zwei Fassungen derselben (hier nachgebildeten)
Schnittstelle: die Koroutine angebot_async(anbieter) und die blockierende
Funktion angebot_blockierend(anbieter). Beide warten DAUER[anbieter]
Sekunden und geben dann das Angebot aus ANGEBOTE zurück oder lösen die
Ausnahme aus, die dort steht. Dabei zählen sie unter einer Sperre in
LAST, wie viele Anfragen gerade gleichzeitig laufen, und tragen in
AUFRUFE ein, welche Fassung aus welchem Thread gefragt wurde. Die
Funktion als_text(ausnahme) macht aus einer Ausnahme den Text
"<Name der Ausnahme>: <Text der Ausnahme>". Schreiben Sie:

- `async def frage_mit_zeitlimit(anbieter, zeitlimit)` wartet mit dem
  Zeitlimit zeitlimit (Sekunden) auf angebot_async(anbieter) und gibt
  das Angebot zurück, bei Überschreiten des Zeitlimits den Text
  "Zeitlimit", bei jeder anderen Ausnahme als_text(ausnahme).
- `async def hole_async(anbieter, zeitlimit)` fragt alle Anbieter der
  Liste mit frage_mit_zeitlimit gleichzeitig ab und gibt ein Dictionary
  Anbieter → Antwort (Angebot oder Text) in der Reihenfolge der Liste
  zurück.
- `def hole_threads(anbieter, zeitlimit)` liefert dasselbe mit Threads:
  Sie reicht für jeden Anbieter einen Aufruf von angebot_blockierend in
  einen ThreadPoolExecutor ein, mit so vielen Arbeitern, dass alle
  Anbieter gleichzeitig gefragt werden, und sammelt die Antworten ein.
  Wer nicht innerhalb von zeitlimit Sekunden nach dem Einreichen fertig
  ist, bekommt "Zeitlimit", für alle Anbieter dieselbe Frist.
- `def bestes_angebot(antworten, verbrauch, co2_grenze)` bekommt so ein
  Dictionary, den Jahresverbrauch in Kilowattstunden und die
  CO₂-Obergrenze. Sie berechnet für jedes Angebot mit co2 ≤ co2_grenze
  die Jahreskosten grundpreis + arbeitspreis · verbrauch / 100 in Euro,
  auf zwei Nachkommastellen gerundet, und gibt das Paar (anbieter,
  kosten) mit den geringsten Kosten zurück. Texte (Fehler, Zeitlimit)
  zählen nicht. Bei gleichen Kosten gewinnt, wer im Dictionary zuerst
  steht; passt kein Angebot, ist das Ergebnis None.

    ANGEBOTE = {
        "Stadtwerk":      {"grundpreis": 180, "arbeitspreis": 28, "co2": 380},
        "Windkraft Nord": {"grundpreis": 240, "arbeitspreis": 29, "co2": 20},
        "Sonnenstrom":    {"grundpreis": 120, "arbeitspreis": 31, "co2": 40},
        "Graustrom24":    ConnectionError("Wartungsarbeiten"),
        "Flussstrom":     {"grundpreis": 90, "arbeitspreis": 27, "co2": 30},
    }
    DAUER = {"Stadtwerk": 0.02, "Windkraft Nord": 0.05, "Sonnenstrom": 0.01,
             "Graustrom24": 0.01, "Flussstrom": 0.2}
    antworten = asyncio.run(hole_async(list(ANGEBOTE), 0.1))
    →  {"Stadtwerk": {…}, "Windkraft Nord": {…}, "Sonnenstrom": {…},
        "Graustrom24": "ConnectionError: Wartungsarbeiten",
        "Flussstrom": "Zeitlimit"}
    hole_threads(list(ANGEBOTE), 0.1) == antworten   →  True
    bestes_angebot(antworten, 20000, 100)   →  ("Windkraft Nord", 6040.0)

Das Stadtwerk wäre mit 5780 Euro am günstigsten, liegt aber über der
CO₂-Grenze; Flussstrom hat zu spät geantwortet.

Grenzen: anbieter hat 0 bis 100 verschiedene Namen, die alle in
ANGEBOTE und DAUER stehen; zeitlimit ist eine Zahl von 0,01 bis 5. Ein
Anbieter antwortet entweder deutlich vor dem Zeitlimit oder deutlich
danach, aber nach höchstens einer Sekunde. Eine Ausnahme aus ANGEBOTE
ist irgendeine Unterart von Exception außer TimeoutError. Im Angebot
sind grundpreis und arbeitspreis Zahlen von 0 bis 10 000, co2 eine
ganze Zahl von 0 bis 1000; verbrauch ist eine ganze Zahl von 0 bis
10**7, co2_grenze eine von 0 bis 1000.

Hintergrund: Diese Übung verbindet beide Arten der Nebenläufigkeit, die
Sie kennengelernt haben. Beide lohnen sich, wenn ein Programm vor allem
wartet, hier auf die Schnittstellen der Anbieter.

Die asyncio-Fassung: Eine Koroutine (async def, Aufgabe 5_039) wartet
mit await; asyncio.run(koroutine) startet die Ereignisschleife.
asyncio.gather(*koroutinen) lässt viele Koroutinen gleichzeitig warten
und liefert die Ergebnisse in der Reihenfolge der Argumente (Aufgabe
5_040). asyncio.wait_for(koroutine, sekunden) bricht eine Koroutine ab,
die zu lange braucht, und löst dann TimeoutError aus; andere Ausnahmen
kommen unverändert heraus (Aufgabe 5_041):

    async def eine(name):
        try:
            return await asyncio.wait_for(frage(name), 0.5)
        except TimeoutError:
            return "zu spät"

    async def alle(namen):
        return await asyncio.gather(*[eine(name) for name in namen])

Die Thread-Fassung: Eine blockierende Funktion wie time.sleep hält die
ganze Ereignisschleife an; mit ihr hilft asyncio nicht, wohl aber
Threads. pool.submit(funktion, argument) reicht einen Aufruf in einen
ThreadPoolExecutor ein und gibt sofort ein Future zurück;
as_completed(futures) liefert die Futures, sobald sie fertig sind, und
future.result() gibt das Ergebnis oder löst die Ausnahme aus dem Thread
erneut aus (Aufgabe 5_046). max_workers begrenzt, wie viele Aufrufe
gleichzeitig laufen (Aufgabe 4_053), und muss mindestens 1 sein. Für
eine gemeinsame Frist bekommt as_completed das Argument timeout: Sind
nach so vielen Sekunden (gezählt ab dem Aufruf von as_completed) noch
Futures offen, löst der Iterator TimeoutError aus. Was bis dahin fertig
war, haben Sie schon in der Hand; der Rest hat das Zeitlimit verpasst:

    with ThreadPoolExecutor(max_workers=len(namen)) as pool:
        futures = {pool.submit(frage, name): name for name in namen}
        try:
            for future in as_completed(futures, timeout=0.5):
                ...
        except TimeoutError:
            ...   # alle noch offenen Futures sind zu spät

Anders als bei wait_for wird ein Thread dabei nicht abgebrochen; am Ende
des with-Blocks wartet der Pool, bis auch der langsame Aufruf fertig
ist. Gibt man jedem Future einzeln future.result(timeout=0.5), addieren
sich die Fristen: Wer auf den zweiten langsamen Anbieter wartet, hat
schon 0,5 Sekunden auf den ersten gewartet.

Schließlich der Zähler LAST: Mehrere Threads erhöhen ihn gleichzeitig,
darum steht das Lesen und Schreiben unter einem threading.Lock (Aufgabe
5_045). In der asyncio-Fassung schadet die Sperre nicht, weil zwischen
Nehmen und Freigeben kein await steht.
"""

import asyncio
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

ANGEBOTE = {}
DAUER = {}
LAST = {"gleichzeitig": 0, "hoechstens": 0}
LAST_SPERRE = threading.Lock()
AUFRUFE = []


def beginne_anfrage(art):
    """Trägt den Aufruf in AUFRUFE ein und zählt die gleichzeitig laufenden Anfragen hoch."""
    AUFRUFE.append((art, threading.get_ident()))
    with LAST_SPERRE:
        LAST["gleichzeitig"] += 1
        LAST["hoechstens"] = max(LAST["hoechstens"], LAST["gleichzeitig"])


def beende_anfrage():
    """Zählt die gleichzeitig laufenden Anfragen wieder herunter."""
    with LAST_SPERRE:
        LAST["gleichzeitig"] -= 1


def antwort(anbieter):
    """Gibt eine Kopie des Angebots zurück oder löst die hinterlegte Ausnahme aus."""
    angebot = ANGEBOTE[anbieter]
    if isinstance(angebot, Exception):
        raise angebot
    return dict(angebot)


async def angebot_async(anbieter):
    """Fragt einen Anbieter über seine Schnittstelle nach dem Angebot (asyncio-Fassung, nachgebildet)."""
    beginne_anfrage("async")
    try:
        await asyncio.sleep(DAUER[anbieter])  # wartet auf die Antwort der Schnittstelle
        return antwort(anbieter)
    finally:
        beende_anfrage()


def angebot_blockierend(anbieter):
    """Fragt einen Anbieter über seine Schnittstelle nach dem Angebot (blockierende Fassung, nachgebildet)."""
    beginne_anfrage("blockierend")
    try:
        time.sleep(DAUER[anbieter])  # wartet auf die Antwort der Schnittstelle
        return antwort(anbieter)
    finally:
        beende_anfrage()


def als_text(ausnahme):
    """Macht aus einer Ausnahme den Text "<Name>: <Text>"."""
    return f"{type(ausnahme).__name__}: {ausnahme}"


async def frage_mit_zeitlimit(anbieter, zeitlimit):
    """Gibt das Angebot eines Anbieters zurück, "Zeitlimit" oder den Fehlertext."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


async def hole_async(anbieter, zeitlimit):
    """Fragt alle Anbieter gleichzeitig mit asyncio ab und gibt Anbieter → Antwort zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def hole_threads(anbieter, zeitlimit):
    """Fragt alle Anbieter gleichzeitig mit Threads ab und gibt Anbieter → Antwort zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def bestes_angebot(antworten, verbrauch, co2_grenze):
    """Gibt (anbieter, jahreskosten) des günstigsten Angebots unter der CO₂-Grenze zurück oder None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


ANGEBOTE.update(
    {
        "Stadtwerk": {"grundpreis": 180, "arbeitspreis": 28, "co2": 380},
        "Windkraft Nord": {"grundpreis": 240, "arbeitspreis": 29, "co2": 20},
        "Sonnenstrom": {"grundpreis": 120, "arbeitspreis": 31, "co2": 40},
        "Graustrom24": ConnectionError("Wartungsarbeiten"),
        "Flussstrom": {"grundpreis": 90, "arbeitspreis": 27, "co2": 30},
    }
)
DAUER.update({"Stadtwerk": 0.02, "Windkraft Nord": 0.05, "Sonnenstrom": 0.01, "Graustrom24": 0.01, "Flussstrom": 0.2})
antworten = asyncio.run(hole_async(list(ANGEBOTE), 0.1))
for name, antwort_des_anbieters in antworten.items():
    print(name, antwort_des_anbieters)
print(hole_threads(list(ANGEBOTE), 0.1) == antworten)
print(bestes_angebot(antworten, 20000, 100))
