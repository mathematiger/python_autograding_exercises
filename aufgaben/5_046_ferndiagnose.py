"""Aufgabe 5_046 – Ferndiagnose                                  Stufe 5 ★★★★★

Beim Service-Desk geht ein Ticket ein: „Im Büro 3 ist seit heute früh
alles langsam.“ Bevor jemand hinfährt, holt das Diagnosewerkzeug von
jedem Arbeitsplatzrechner des Büros über das Netz ein paar Kennzahlen
(Prozessorlast, freier Speicher). Manche Rechner antworten schnell,
manche brauchen eine Weile, und ausgeschaltete oder abgestürzte
Rechner antworten gar nicht, dann kommt eine Ausnahme. Damit die
Kollegin am Telefon nicht warten muss, bis der langsamste Rechner fertig
ist, soll jedes Ergebnis sofort im Ticket erscheinen, sobald es da ist,
und ein Fehler bei einem Rechner darf die übrigen nicht verhindern.

Die Abfrage ist die vorgegebene Funktion hole_diagnose(rechner): Sie
wartet (hier nachgebildet mit time.sleep und dem Dictionary
ANTWORTZEIT) und gibt die Kennzahlen aus DIAGNOSEN zurück, oder sie
löst die Ausnahme aus, die in DIAGNOSEN steht. Ins Ticket schreibt die
vorgegebene Funktion melde(text). Schreiben Sie drei Funktionen:

- `starte_abfragen(pool, rechner)` reicht für jeden Rechner mit
  pool.submit einen Aufruf von hole_diagnose ein und gibt ein Dictionary
  zurück, das jedem Future den Namen seines Rechners zuordnet.
- `sammle(abfragen)` bekommt so ein Dictionary und holt die Ergebnisse
  mit as_completed in der Reihenfolge ab, in der sie fertig werden. Für
  jedes ruft sie sofort melde auf, mit "<rechner>: ok" oder bei einer
  Ausnahme "<rechner>: <Name der Ausnahme>: <Text der Ausnahme>". Sie
  gibt das Paar (berichte, fehler) zurück: berichte ordnet jedem
  erfolgreichen Rechner seine Kennzahlen zu, fehler jedem anderen den
  Text "<Name der Ausnahme>: <Text der Ausnahme>"; beide Dictionaries
  nach den Namen der Rechner sortiert.
- `diagnose(rechner, threads)` erledigt beides mit einem
  ThreadPoolExecutor mit threads Arbeitern und gibt zurück, was sammle
  liefert.

    ANTWORTZEIT = {"PC-01": 0.3, "PC-02": 0.1, "PC-03": 0.2}
    DIAGNOSEN = {"PC-01": {"cpu": 97, "ram_frei_mb": 210},
                 "PC-02": {"cpu": 12, "ram_frei_mb": 5400},
                 "PC-03": ConnectionError("keine Antwort")}
    diagnose(["PC-01", "PC-02", "PC-03"], 3)
    →  ({"PC-01": {"cpu": 97, "ram_frei_mb": 210},
         "PC-02": {"cpu": 12, "ram_frei_mb": 5400}},
        {"PC-03": "ConnectionError: keine Antwort"})
    PROTOKOLL   →  ["PC-02: ok", "PC-03: ConnectionError: keine Antwort", "PC-01: ok"]

Grenzen: rechner hat 0 bis 50 verschiedene Namen, die alle in DIAGNOSEN
stehen; threads ist eine ganze Zahl von 1 bis 16. Eine Abfrage dauert
höchstens 0,3 Sekunden und kann jede Unterart von Exception auslösen.

Hintergrund: In Aufgabe 4_053 hat pool.map die Ergebnisse in der
Reihenfolge der Eingaben geliefert, und eine Ausnahme hat alle
weiteren Ergebnisse verschluckt; deshalb mussten Sie die Fehler schon
in der Funktion abfangen. Mehr Kontrolle gibt pool.submit(funktion,
*argumente): Es reicht genau einen Aufruf ein, kehrt sofort zurück und
liefert ein Future (eine „Zukunft“), einen Platzhalter für das
Ergebnis, das noch kommt:

    from concurrent.futures import ThreadPoolExecutor, as_completed

    with ThreadPoolExecutor(max_workers=4) as pool:
        future = pool.submit(pow, 2, 10)
        future.done()       →  True oder False, je nachdem, ob er schon fertig ist
        future.result()     →  1024, wartet nötigenfalls, bis er fertig ist

Hat der Aufruf eine Ausnahme ausgelöst, löst future.result() genau
diese Ausnahme im aufrufenden Thread erneut aus; jedes Future trägt
seinen eigenen Erfolg oder Fehler. future.exception() gibt die Ausnahme
zurück, statt sie auszulösen (oder None). So fängt man Fehler aus
Threads dort ab, wo man das Ergebnis braucht:

    try:
        wert = future.result()
    except Exception as fehler:
        print(type(fehler).__name__, fehler)

as_completed(futures) nimmt viele Futures und liefert sie als Iterator
in der Reihenfolge, in der sie fertig werden, nicht in der, in der sie
eingereicht wurden. Weil ein Future selbst nicht weiß, wofür es steht,
merkt man sich die Zuordnung in einem Dictionary Future → Eingabe;
Futures lassen sich als Schlüssel benutzen:

    futures = {pool.submit(langsam, x): x for x in [3, 1, 2]}
    for future in as_completed(futures):
        print(futures[future], future.result())

Die Arbeiter des Pools sind gewöhnliche Threads (Aufgabe 5_044), die
Anzahl max_workers begrenzt, wie viele Aufrufe gleichzeitig laufen; die
übrigen warten in einer Warteschlange. Das Abholen gehört in den
with-Block: Am Ende des Blocks wartet der Pool auf alle Aufrufe und
schließt dann. Fertige Futures behalten zwar ihr Ergebnis, wer erst
danach abholt, bekommt die Meldungen aber alle auf einmal am Ende statt
sofort.
"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

ANTWORTZEIT = {}
DIAGNOSEN = {}
PROTOKOLL = []
LAST = {"gleichzeitig": 0, "hoechstens": 0}
LAST_SPERRE = threading.Lock()


def melde(text):
    """Schreibt eine Zeile ins Ticket (hier: in die Liste PROTOKOLL)."""
    PROTOKOLL.append(text)


def hole_diagnose(rechner):
    """Holt die Kennzahlen eines Rechners über das Netz (hier nur nachgebildet)."""
    with LAST_SPERRE:
        LAST["gleichzeitig"] += 1
        LAST["hoechstens"] = max(LAST["hoechstens"], LAST["gleichzeitig"])
    try:
        time.sleep(ANTWORTZEIT.get(rechner, 0.05))  # wartet auf die Antwort
        antwort = DIAGNOSEN[rechner]
        if isinstance(antwort, Exception):
            raise antwort
        return dict(antwort)
    finally:
        with LAST_SPERRE:
            LAST["gleichzeitig"] -= 1


def starte_abfragen(pool, rechner):
    """Reicht für jeden Rechner einen Aufruf von hole_diagnose ein; gibt Future → Rechner zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def sammle(abfragen):
    """Holt die Ergebnisse ab, sobald sie fertig sind, meldet jedes und gibt (berichte, fehler) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def diagnose(rechner, threads):
    """Fragt alle Rechner mit threads Arbeitern ab und gibt (berichte, fehler) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


ANTWORTZEIT.update({"PC-01": 0.3, "PC-02": 0.1, "PC-03": 0.2})
DIAGNOSEN.update(
    {
        "PC-01": {"cpu": 97, "ram_frei_mb": 210},
        "PC-02": {"cpu": 12, "ram_frei_mb": 5400},
        "PC-03": ConnectionError("keine Antwort"),
    }
)
print(diagnose(["PC-01", "PC-02", "PC-03"], 3))
print(PROTOKOLL)
