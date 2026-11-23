"""Aufgabe 4_053 – Linkprüfung                                   Stufe 4 ★★★★☆

Ein Entwicklungsteam dokumentiert seine Schnittstelle (API) auf einer
Webseite mit vielen Links: auf Beispielanfragen, Schemata und ältere
Versionen. Vor jeder Veröffentlichung soll ein Skript alle Links
abrufen und melden, welche kaputt sind. Jeder Abruf wartet eine Weile
auf den Server; nacheinander dauern 200 Links mit je einer halben
Sekunde fast zwei Minuten. Während ein Abruf wartet, kann aber längst
der nächste beginnen. Schreiben Sie:

- `status_oder_fehler(abfrage, url)` ruft abfrage(url) auf und gibt den
  HTTP-Statuscode zurück, den abfrage liefert (200 heißt in Ordnung, 404
  „nicht gefunden“). Löst abfrage einen TimeoutError oder einen
  ConnectionError aus, gibt die Funktion stattdessen den Namen der
  Ausnahme als Text zurück ("TimeoutError" bzw. "ConnectionError").
  Unterarten zählen mit: Bei einem ConnectionRefusedError (einer
  Unterart von ConnectionError) ist das Ergebnis "ConnectionRefusedError",
  also immer der Name der tatsächlich ausgelösten Ausnahme.
  Andere Ausnahmen fliegen weiter, denn sie zeigen einen Fehler im
  Skript selbst.
- `pruefe_links(urls, abfrage, parallel=8)` ruft status_oder_fehler für
  alle URLs mit einem ThreadPoolExecutor und dessen map auf, mit
  höchstens parallel Abrufen zugleich. Sie gibt ein Dictionary zurück:
  URL → Ergebnis, in der Reihenfolge von urls.
- `kaputte_links(ergebnisse)` bekommt so ein Dictionary und gibt die
  Liste der URLs zurück, deren Ergebnis ein Text oder ein Statuscode ab
  400 ist, in derselben Reihenfolge.

abfrage ist eine Funktion, die eine URL bekommt; in den Tests und im
Beispiel unten wartet sie mit time.sleep, statt ins Netz zu gehen.

    statuscodes = {"/start": 200, "/alt": 404, "/schema": 200}
    def abfrage(url):
        time.sleep(0.05)
        if url == "/langsam":
            raise TimeoutError(url)
        return statuscodes[url]

    pruefe_links(["/start", "/alt", "/langsam"], abfrage)
        →  {"/start": 200, "/alt": 404, "/langsam": "TimeoutError"}
    kaputte_links({"/start": 200, "/alt": 404, "/langsam": "TimeoutError"})
        →  ["/alt", "/langsam"]

Grenzen: urls enthält 0 bis 200 verschiedene Texte, 1 ≤ parallel ≤ 32.
abfrage liefert ganze Zahlen von 100 bis 599 oder löst eine Ausnahme
aus, ein Aufruf dauert bis zu 0,05 Sekunden.

Hintergrund: Ein Thread ist ein eigener Ablauf innerhalb eines
Programms. Mehrere Threads teilen sich dieselben Variablen, und während
einer wartet (auf das Netz, eine Datei, time.sleep), arbeitet ein
anderer weiter. Threads von Hand zu verwalten ist mühsam; das Modul
concurrent.futures bietet dafür einen Pool von Arbeitern an:

    from concurrent.futures import ThreadPoolExecutor

    def quadrat_langsam(x):
        time.sleep(0.1)                 # wartet, wie ein Netzaufruf
        return x * x

    with ThreadPoolExecutor(max_workers=4) as pool:
        ergebnisse = list(pool.map(quadrat_langsam, [1, 2, 3, 4]))
    ergebnisse                          →  [1, 4, 9, 16], nach etwa 0,1 s statt 0,4 s

pool.map(funktion, werte) verteilt die Aufrufe auf die max_workers
Threads und liefert die Ergebnisse in der Reihenfolge der Werte, auch
wenn ein späterer Aufruf zuerst fertig ist. Das Ergebnis ist ein
Iterator (Aufgabe 3_020); erst beim Durchlaufen wartet man auf die
einzelnen Ergebnisse. Löst ein Aufruf eine Ausnahme aus, fliegt sie
genau dann, wenn man sein Ergebnis abholt, und die übrigen Ergebnisse
sind verloren. Darum fängt man erwartbare Fehler in der Funktion selbst
ab, die man an map gibt. Braucht die Funktion ein festes zusätzliches
Argument, hilft functools.partial (Aufgabe 4_028) oder ein lambda. Der
with-Block wartet am Ende, bis alle Threads fertig sind, und gibt sie
frei (Kontextmanager, Aufgabe 4_051).

Threads lohnen sich nur, wenn viel gewartet wird. Reine Rechenarbeit
wird in Python durch Threads nicht schneller, weil immer nur ein Thread
zugleich Python-Code ausführt.
"""

import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial


def status_oder_fehler(abfrage, url):
    """Gibt den Statuscode von abfrage(url) zurück oder den Namen eines Netzfehlers."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def pruefe_links(urls, abfrage, parallel=8):
    """Fragt alle URLs mit höchstens parallel Threads zugleich ab; gibt URL → Ergebnis zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def kaputte_links(ergebnisse):
    """Gibt die URLs zurück, deren Ergebnis ein Fehlertext oder ein Statuscode ab 400 ist."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


statuscodes = {"/start": 200, "/alt": 404, "/schema": 200}


def abfrage(url):
    """Tut so, als riefe sie die URL ab: wartet kurz und liefert den Statuscode."""
    time.sleep(0.05)
    if url == "/langsam":
        raise TimeoutError(url)
    return statuscodes[url]


ergebnisse = pruefe_links(["/start", "/alt", "/langsam"], abfrage)
print(ergebnisse)
print(kaputte_links(ergebnisse))
