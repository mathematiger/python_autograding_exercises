# Automatisch erzeugt aus lehrkraft/muster/4_053_linkpruefung.py - nicht von Hand ändern.
# vorlage-hash: 507faf6cd81633de
# text-hash: 1f73aeed84cf1e15
# thema: nebenlaeufigkeit
# inhalt: ThreadPoolExecutor.map

import threading
import time


class Gegenstelle:
    """Eine gespielte Webseite: wartet je Abruf kurz und zählt, wie viele Abrufe gleichzeitig laufen."""

    def __init__(self, antworten, wartezeit=0.02):
        """antworten: URL → Statuscode oder Ausnahme, die beim Abruf ausgelöst wird."""
        self.antworten = antworten
        self.wartezeit = wartezeit
        self.sperre = threading.Lock()
        self.gleichzeitig = 0
        self.hoechstens = 0
        self.abrufe = []

    def __call__(self, url):
        """Ruft die URL ab: merkt sich die Zahl der gleichzeitigen Abrufe, wartet, antwortet."""
        with self.sperre:
            self.gleichzeitig += 1
            self.hoechstens = max(self.hoechstens, self.gleichzeitig)
            self.abrufe.append(url)
        try:
            time.sleep(self.wartezeit)
            antwort = self.antworten[url]
            if isinstance(antwort, Exception):
                raise antwort
            return antwort
        finally:
            with self.sperre:
                self.gleichzeitig -= 1


def wert_von(aufruf):
    """Führt den Aufruf aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def erwartet_fuer(antworten, urls):
    """Das erwartete Ergebnis von pruefe_links."""
    erwartet = {}
    for url in urls:
        antwort = antworten[url]
        erwartet[url] = type(antwort).__name__ if isinstance(antwort, Exception) else antwort
    return erwartet


BEISPIEL = {"/start": 200, "/alt": 404, "/langsam": TimeoutError("/langsam")}

# status_oder_fehler liefert den Statuscode
ergebnis = wert_von(lambda: status_oder_fehler(Gegenstelle({"/start": 200}, 0), "/start"))
assert ergebnis == 200, f"status_oder_fehler(abfrage, '/start') ergibt {ergebnis!r}, erwartet war 200."

# status_oder_fehler mit einem anderen Statuscode (nicht fest hinschreiben!)
ergebnis = wert_von(lambda: status_oder_fehler(Gegenstelle({"/alt": 404}, 0), "/alt"))
assert ergebnis == 404, f"status_oder_fehler(abfrage, '/alt') ergibt {ergebnis!r}, erwartet war 404."

# status_oder_fehler: TimeoutError wird zum Text "TimeoutError"
ergebnis = wert_von(lambda: status_oder_fehler(Gegenstelle({"/x": TimeoutError("zu langsam")}, 0), "/x"))
assert ergebnis == "TimeoutError", (
    f"Löst abfrage einen TimeoutError aus, ergibt status_oder_fehler {ergebnis!r}, erwartet war 'TimeoutError'.\n"
    "Tipp: except (TimeoutError, ConnectionError) as fehler: return type(fehler).__name__"
)

# status_oder_fehler: ConnectionError wird zum Text "ConnectionError"
ergebnis = wert_von(lambda: status_oder_fehler(Gegenstelle({"/x": ConnectionError("abgelehnt")}, 0), "/x"))
assert ergebnis == "ConnectionError", (
    f"Löst abfrage einen ConnectionError aus, ergibt status_oder_fehler {ergebnis!r}, erwartet war 'ConnectionError'."
)

# status_oder_fehler: auch Unterarten wie ConnectionRefusedError gelten als Netzfehler, mit ihrem eigenen Namen
ergebnis = wert_von(lambda: status_oder_fehler(Gegenstelle({"/x": ConnectionRefusedError("Port zu")}, 0), "/x"))
assert ergebnis == "ConnectionRefusedError", (
    f"Löst abfrage einen ConnectionRefusedError aus, ergibt status_oder_fehler {ergebnis!r}, erwartet war 'ConnectionRefusedError'.\n"
    "Tipp: Fangen Sie ConnectionError mit except ab und geben Sie den Namen der tatsächlichen Ausnahme zurück."
)

# status_oder_fehler: andere Ausnahmen fliegen weiter
ergebnis = wert_von(lambda: status_oder_fehler(Gegenstelle({}, 0), "/fehlt"))
assert isinstance(ergebnis, str) and ergebnis.startswith("KeyError:"), (
    f"Löst abfrage einen KeyError aus, ergibt status_oder_fehler {ergebnis!r}; erwartet war, dass der KeyError weiterfliegt.\n"
    "Tipp: Fangen Sie nur TimeoutError und ConnectionError ab, nicht Exception."
)

# pruefe_links im Beispiel
gegenstelle = Gegenstelle(BEISPIEL)
ergebnis = wert_von(lambda: pruefe_links(["/start", "/alt", "/langsam"], gegenstelle))
erwartet = {"/start": 200, "/alt": 404, "/langsam": "TimeoutError"}
assert ergebnis == erwartet, (
    f"pruefe_links(['/start', '/alt', '/langsam'], abfrage) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
    "Tipp: Geben Sie pool.map eine Funktion, die nur die URL bekommt, z. B. partial(status_oder_fehler, abfrage)."
)

# pruefe_links mit anderen Links (nicht fest hinschreiben!)
antworten = {"/v1": 301, "/v2": 200, "/bild.png": 500, "/kontakt": ConnectionError("weg")}
urls = ["/v2", "/kontakt", "/v1", "/bild.png"]
ergebnis = wert_von(lambda: pruefe_links(urls, Gegenstelle(antworten)))
assert ergebnis == erwartet_fuer(antworten, urls), f"pruefe_links({urls}, abfrage) ergibt {ergebnis!r}, erwartet war {erwartet_fuer(antworten, urls)}."

# pruefe_links: die Reihenfolge ist die von urls, auch wenn ein späterer Abruf zuerst fertig ist
class Gestaffelt(Gegenstelle):
    """Eine Gegenstelle, bei der frühe URLs länger brauchen als späte."""

    def __call__(self, url):
        """Wartet umso länger, je weiter vorn die URL steht."""
        time.sleep(0.01 * (5 - int(url[-1])))
        return self.antworten[url]


antworten = {f"/seite{nummer}": 200 + nummer for nummer in range(5)}
ergebnis = wert_von(lambda: pruefe_links(list(antworten), Gestaffelt(antworten)))
reihenfolge = list(ergebnis) if isinstance(ergebnis, dict) else ergebnis
assert reihenfolge == list(antworten) and ergebnis == antworten, (
    f"pruefe_links ergibt {ergebnis!r}, erwartet war {antworten} in dieser Reihenfolge.\n"
    "Tipp: pool.map liefert die Ergebnisse in der Reihenfolge der Werte; zip(urls, ergebnisse) passt sie zusammen."
)

# pruefe_links: keine URLs, leeres Dictionary
ergebnis = wert_von(lambda: pruefe_links([], Gegenstelle({})))
assert ergebnis == {}, f"pruefe_links([], abfrage) ergibt {ergebnis!r}, erwartet war {{}}."

# pruefe_links fragt jede URL genau einmal ab
antworten = {f"/doku/{nummer}": 200 for nummer in range(10)}
gegenstelle = Gegenstelle(antworten, 0.01)
wert_von(lambda: pruefe_links(list(antworten), gegenstelle))
assert sorted(gegenstelle.abrufe) == sorted(antworten), (
    f"pruefe_links hat {len(gegenstelle.abrufe)} Abrufe gemacht ({sorted(gegenstelle.abrufe)[:5]} …), erwartet war jede der 10 URLs einmal."
)

# pruefe_links benutzt ThreadPoolExecutor und map
assert verwendet("ThreadPoolExecutor") and verwendet("map"), (
    "pruefe_links soll einen ThreadPoolExecutor anlegen und dessen map aufrufen."
)

# pruefe_links fragt mehrere URLs gleichzeitig ab
antworten = {f"/api/{nummer}": 200 for nummer in range(16)}
gegenstelle = Gegenstelle(antworten, 0.03)
wert_von(lambda: pruefe_links(list(antworten), gegenstelle))
assert gegenstelle.hoechstens >= 2, (
    f"Bei 16 Links liefen höchstens {gegenstelle.hoechstens} Abrufe gleichzeitig, erwartet waren mehrere.\n"
    "Tipp: Rufen Sie status_oder_fehler nicht selbst in einer Schleife auf, sondern über pool.map."
)

# pruefe_links: höchstens parallel Abrufe zugleich
gegenstelle = Gegenstelle(antworten, 0.03)
wert_von(lambda: pruefe_links(list(antworten), gegenstelle, parallel=3))
assert 2 <= gegenstelle.hoechstens <= 3, (
    f"Mit parallel=3 liefen höchstens {gegenstelle.hoechstens} Abrufe gleichzeitig, erwartet waren 3 (mindestens 2, höchstens 3).\n"
    "Tipp: ThreadPoolExecutor(max_workers=parallel) legt die Zahl der Threads fest."
)

# pruefe_links: parallel=1 heißt einer nach dem anderen
gegenstelle = Gegenstelle(antworten, 0.005)
wert_von(lambda: pruefe_links(list(antworten), gegenstelle, parallel=1))
assert gegenstelle.hoechstens == 1, f"Mit parallel=1 liefen {gegenstelle.hoechstens} Abrufe gleichzeitig, erwartet war 1."

# pruefe_links: ohne Angabe bis zu 8 Abrufe gleichzeitig
gegenstelle = Gegenstelle(antworten, 0.05)
wert_von(lambda: pruefe_links(list(antworten), gegenstelle))
assert 6 <= gegenstelle.hoechstens <= 8, (
    f"Ohne Angabe von parallel liefen höchstens {gegenstelle.hoechstens} Abrufe gleichzeitig, erwartet waren 8.\n"
    "Tipp: Der Standardwert von parallel ist 8."
)

# pruefe_links: ein Fehler im Skript (hier KeyError) fliegt weiter
ergebnis = wert_von(lambda: pruefe_links(["/da", "/fehlt"], Gegenstelle({"/da": 200}, 0.005)))
assert isinstance(ergebnis, str) and ergebnis.startswith("KeyError:"), (
    f"pruefe_links mit einer abfrage, die einen KeyError auslöst, ergibt {ergebnis!r}; erwartet war, dass der KeyError weiterfliegt."
)

# kaputte_links im Beispiel
ergebnis = wert_von(lambda: kaputte_links({"/start": 200, "/alt": 404, "/langsam": "TimeoutError"}))
assert ergebnis == ["/alt", "/langsam"], f"kaputte_links im Beispiel ergibt {ergebnis!r}, erwartet war ['/alt', '/langsam']."

# kaputte_links: 399 ist in Ordnung, 400 kaputt, Fehlertexte kaputt
ergebnisse = {"/a": 399, "/b": 400, "/c": 301, "/d": "ConnectionError", "/e": 599, "/f": 100}
ergebnis = wert_von(lambda: kaputte_links(ergebnisse))
assert ergebnis == ["/b", "/d", "/e"], (
    f"kaputte_links({ergebnisse}) ergibt {ergebnis!r}, erwartet war ['/b', '/d', '/e'].\n"
    "Tipp: Ein Text ist immer ein Fehler; eine Zahl nur ab 400. Prüfen Sie den Text mit isinstance zuerst."
)

# kaputte_links: alles in Ordnung oder leer
ergebnis = wert_von(lambda: [kaputte_links({"/a": 200, "/b": 204}), kaputte_links({})])
assert ergebnis == [[], []], f"kaputte_links ohne kaputte Links ergibt {ergebnis!r}, erwartet war jeweils []."

# Die Ausgabe des Programms
erwartet = "{'/start': 200, '/alt': 404, '/langsam': 'TimeoutError'}\n['/alt', '/langsam']"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Linklisten
zufall = Zufall(4053)
moeglich = [200, 201, 301, 302, 399, 400, 403, 404, 500, 503, TimeoutError("t"), ConnectionResetError("r")]
for _ in range(25):
    antworten = {f"/seite/{nummer}": zufall.choice(moeglich) for nummer in range(zufall.randint(0, 20))}
    urls = list(antworten)
    zufall.shuffle(urls)
    parallel = zufall.randint(1, 32)
    ergebnis = wert_von(lambda: pruefe_links(urls, Gegenstelle(antworten, 0.001), parallel))
    erwartet = erwartet_fuer(antworten, urls)
    assert ergebnis == erwartet and list(ergebnis) == urls, f"pruefe_links({urls}, abfrage, {parallel}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    kaputt = [url for url in urls if isinstance(erwartet[url], str) or erwartet[url] >= 400]
    assert wert_von(lambda: kaputte_links(erwartet)) == kaputt, f"kaputte_links({erwartet}) ergibt {wert_von(lambda: kaputte_links(erwartet))!r}, erwartet war {kaputt}."

# Obere Grenze: 200 Links mit je 0,05 Sekunden Wartezeit und 32 Threads
antworten = {f"/archiv/{nummer}": 200 if nummer % 7 else 404 for nummer in range(200)}
gegenstelle = Gegenstelle(antworten, 0.05)
ergebnis = wert_von(lambda: pruefe_links(list(antworten), gegenstelle, parallel=32))
assert ergebnis == antworten and gegenstelle.hoechstens >= 16, (
    f"Bei 200 Links mit parallel=32 stimmt das Ergebnis nicht oder es liefen nur {gegenstelle.hoechstens} Abrufe gleichzeitig."
)
