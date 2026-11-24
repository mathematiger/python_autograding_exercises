# Automatisch erzeugt aus lehrkraft/muster/5_047_anfragekennung.py - nicht von Hand ändern.
# vorlage-hash: 24b355564a837efb
# text-hash: e1d6ff88d15f512c
# thema: nebenlaeufigkeit
# inhalt: contextvars: Kontext ohne globale Variable

import time

BEISPIEL = [
    "[A1] Anfrage beginnt", "[A1] lade Kunde Kaya",
    "[B2] Anfrage beginnt", "[B2] lade Kunde Berg",
    "[B2] Kunde Berg geladen", "[B2] Anfrage fertig",
    "[A1] Kunde Kaya geladen", "[A1] Anfrage fertig",
]


def wert_von(aufruf):
    """Führt den Aufruf aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def frisch(aufruf):
    """Führt den Aufruf in einem frischen Kontext mit leerem PROTOKOLL aus; liefert (Ergebnis, PROTOKOLL)."""
    PROTOKOLL.clear()
    ergebnis = contextvars.Context().run(wert_von, aufruf)
    return ergebnis, list(PROTOKOLL)


def kennung_im_block(kennung):
    """Gibt zurück, welchen Wert ANFRAGE im with-Block hat."""
    with mit_kennung(kennung):
        return ANFRAGE.get()


def mit_ausnahme():
    """Löst im with-Block einen Fehler aus und gibt danach den Wert von ANFRAGE zurück."""
    try:
        with mit_kennung("X9"):
            raise KeyError("Kunde fehlt")
    except KeyError:
        pass
    return ANFRAGE.get()


def ineinander():
    """Gibt die Werte von ANFRAGE in zwei ineinander stehenden with-Blöcken und danach zurück."""
    werte = []
    with mit_kennung("A1"):
        werte.append(ANFRAGE.get())
        with mit_kennung("B2"):
            werte.append(ANFRAGE.get())
        werte.append(ANFRAGE.get())
    werte.append(ANFRAGE.get())
    return werte


def zeilen_passen(protokoll, anfragen):
    """Prüft, ob jede Anfrage genau ihre vier Zeilen unter ihrer Kennung hat; liefert die erste Abweichung oder None."""
    for kennung, kunde, wartezeit in anfragen:
        eigene = [zeile for zeile in protokoll if zeile.startswith(f"[{kennung}] ")]
        erwartet = [
            f"[{kennung}] Anfrage beginnt", f"[{kennung}] lade Kunde {kunde}",
            f"[{kennung}] Kunde {kunde} geladen", f"[{kennung}] Anfrage fertig",
        ]
        if eigene != erwartet:
            return f"Unter [{kennung}] stehen {eigene}, erwartet waren {erwartet}."
    if len(protokoll) != 4 * len(anfragen):
        return f"Das Protokoll hat {len(protokoll)} Zeilen, erwartet waren {4 * len(anfragen)}."
    return None


# protokolliere: ohne Anfrage steht "-" vorn
ergebnis, protokoll = frisch(lambda: protokolliere("Dienst gestartet"))
assert protokoll == ["[-] Dienst gestartet"], (
    f"protokolliere('Dienst gestartet') ohne Anfrage schreibt {protokoll}, erwartet war ['[-] Dienst gestartet'].\n"
    "Tipp: PROTOKOLL.append(f\"[{ANFRAGE.get()}] {text}\")."
)

# protokolliere: mit gesetzter Kennung
def mit_gesetzter_kennung():
    """Setzt ANFRAGE von Hand und protokolliert."""
    ANFRAGE.set("Z7")
    protokolliere("Test")


ergebnis, protokoll = frisch(mit_gesetzter_kennung)
assert protokoll == ["[Z7] Test"], f"Nach ANFRAGE.set('Z7') schreibt protokolliere('Test') {protokoll}, erwartet war ['[Z7] Test']."

# mit_kennung: im with-Block gilt die Kennung
ergebnis, protokoll = frisch(lambda: kennung_im_block("A1"))
assert ergebnis == "A1", (
    f"Im Block with mit_kennung('A1'): hat ANFRAGE den Wert {ergebnis!r}, erwartet war 'A1'.\n"
    "Tipp: token = ANFRAGE.set(kennung) vor dem yield."
)

# mit_kennung: danach gilt wieder der alte Wert
ergebnis, protokoll = frisch(lambda: (kennung_im_block("A1"), ANFRAGE.get())[1])
assert ergebnis == "-", (
    f"Nach dem Block with mit_kennung('A1'): hat ANFRAGE den Wert {ergebnis!r}, erwartet war wieder '-'.\n"
    "Tipp: ANFRAGE.reset(token) nach dem yield."
)

# mit_kennung: ineinander stehende Blöcke
ergebnis, protokoll = frisch(ineinander)
assert ergebnis == ["A1", "B2", "A1", "-"], (
    f"In zwei ineinander stehenden with-Blöcken (A1 außen, B2 innen) hat ANFRAGE nacheinander {ergebnis!r}, "
    "erwartet war ['A1', 'B2', 'A1', '-'].\nTipp: reset(token) stellt den Wert von vor diesem set wieder her; "
    "ANFRAGE.set('-') würde das äußere A1 vergessen."
)

# mit_kennung: auch nach einer Ausnahme
ergebnis, protokoll = frisch(mit_ausnahme)
assert ergebnis == "-", (
    f"Nach einem KeyError im with-Block hat ANFRAGE den Wert {ergebnis!r}, erwartet war wieder '-'.\n"
    "Tipp: try: yield  finally: ANFRAGE.reset(token)."
)

# mit_kennung: die Ausnahme geht weiter an den Aufrufer
def ausnahme_durchreichen():
    """Gibt den Namen der Ausnahme zurück, die aus dem with-Block herauskommt."""
    try:
        with mit_kennung("X9"):
            raise KeyError("Kunde fehlt")
    except KeyError:
        return "KeyError"
    return "keine Ausnahme"


ergebnis, protokoll = frisch(ausnahme_durchreichen)
assert ergebnis == "KeyError", f"Ein KeyError im with-Block kommt als {ergebnis!r} heraus, erwartet war, dass er weiterfliegt."

# bearbeite: eine einzelne Anfrage
ergebnis, protokoll = frisch(lambda: asyncio.run(bearbeite("A1", "Kaya", 0.01)))
erwartet = ["[A1] Anfrage beginnt", "[A1] lade Kunde Kaya", "[A1] Kunde Kaya geladen", "[A1] Anfrage fertig"]
assert protokoll == erwartet, (
    f"asyncio.run(bearbeite('A1', 'Kaya', 0.01)) protokolliert\n{protokoll}\nerwartet war\n{erwartet}\n"
    "Tipp: with mit_kennung(kennung): um alles, auch um das await lade_kunde(...)."
)

# bearbeite: gibt zurück, was lade_kunde liefert
assert ergebnis == "Kunde Kaya", f"bearbeite('A1', 'Kaya', 0.01) ergibt {ergebnis!r}, erwartet war 'Kunde Kaya'."

# bearbeite_alle: das Beispiel, Ergebnisse
ergebnis, protokoll = frisch(lambda: asyncio.run(bearbeite_alle([("A1", "Kaya", 0.2), ("B2", "Berg", 0.1)])))
assert ergebnis == ["Kunde Kaya", "Kunde Berg"], (
    f"bearbeite_alle([('A1', 'Kaya', 0.2), ('B2', 'Berg', 0.1)]) ergibt {ergebnis!r}, erwartet war ['Kunde Kaya', 'Kunde Berg'].\n"
    "Tipp: return list(await asyncio.gather(*koroutinen))."
)

# bearbeite_alle: die Anfragen laufen gleichzeitig
assert protokoll[:4] == BEISPIEL[:4], (
    f"Die ersten vier Zeilen sind {protokoll[:4]}, erwartet war {BEISPIEL[:4]}: B2 beginnt, während A1 noch wartet.\n"
    "Tipp: Mit asyncio.gather laufen die Anfragen gleichzeitig, nicht nacheinander mit await in einer Schleife."
)

# bearbeite_alle: jede Zeile trägt die Kennung ihrer Anfrage
abweichung = zeilen_passen(protokoll, [("A1", "Kaya", 0.2), ("B2", "Berg", 0.1)])
assert abweichung is None, (
    f"bearbeite_alle protokolliert\n{protokoll}\n{abweichung}\n"
    "Tipp: Jede Anfrage braucht ihren eigenen Wert; eine ContextVar hat in jedem Task von gather ihren eigenen."
)

# bearbeite_alle: der Aufrufer behält seine eigene Kennung
async def aufrufer():
    """Bearbeitet zwei Anfragen unter einer eigenen Kennung und protokolliert danach."""
    with mit_kennung("HAUPT"):
        await bearbeite_alle([("A1", "Kaya", 0.02), ("B2", "Berg", 0.01)])
        protokolliere("alle fertig")


ergebnis, protokoll = frisch(lambda: asyncio.run(aufrufer()))
assert protokoll[-1:] == ["[HAUPT] alle fertig"], (
    f"Nach bearbeite_alle unter der Kennung HAUPT schreibt protokolliere {protokoll[-1:]}, erwartet war ['[HAUPT] alle fertig']."
)

# bearbeite_alle: keine Anfragen
ergebnis, protokoll = frisch(lambda: asyncio.run(bearbeite_alle([])))
assert ergebnis == [] and protokoll == [], f"bearbeite_alle([]) ergibt {ergebnis!r} und protokolliert {protokoll}; erwartet war [] ohne Zeilen."

# im_thread: der Thread kennt die Kennung
def im_thread_mit_kennung():
    """Ruft protokolliere unter der Kennung C3 in einem Thread auf und gibt den Thread zurück, in dem es lief."""
    threads = []

    def schreibe(text):
        """Merkt sich den Thread und protokolliert."""
        threads.append(threading.current_thread())
        protokolliere(text)
        return len(text)

    with mit_kennung("C3"):
        laenge = im_thread(schreibe, "Bericht erstellt")
    return laenge, threads


ergebnis, protokoll = frisch(im_thread_mit_kennung)
assert protokoll == ["[C3] Bericht erstellt"], (
    f"im_thread(protokolliere, 'Bericht erstellt') unter der Kennung C3 schreibt {protokoll}, "
    "erwartet war ['[C3] Bericht erstellt'].\nTipp: kontext = contextvars.copy_context() und im Thread kontext.run(funktion, *argumente)."
)

# im_thread: läuft in einem eigenen Thread
threads = ergebnis[1] if isinstance(ergebnis, tuple) else []
assert len(threads) == 1 and threads[0] is not threading.main_thread() and threads[0] is not threading.current_thread(), (
    f"Die Funktion lief in {threads}; erwartet war genau ein neuer Thread.\nTipp: threading.Thread(...), start() und join()."
)

# im_thread: gibt das Ergebnis der Funktion zurück
assert isinstance(ergebnis, tuple) and ergebnis[0] == 16, (
    f"im_thread gibt {ergebnis[0] if isinstance(ergebnis, tuple) else ergebnis!r} zurück, erwartet war 16, das Ergebnis der Funktion.\n"
    "Tipp: Legen Sie das Ergebnis im Thread in einer Liste ab und geben Sie es nach join() zurück."
)

# im_thread: wartet, bis der Thread fertig ist
def langsam():
    """Wartet kurz und gibt dann 7 zurück."""
    time.sleep(0.05)
    return 7


ergebnis = wert_von(lambda: im_thread(langsam))
assert ergebnis == 7, (
    f"im_thread mit einer Funktion, die 0.05 s wartet und 7 zurückgibt, ergibt {ergebnis!r}, erwartet war 7.\n"
    "Tipp: thread.join() wartet, bis der Thread fertig ist; erst danach steht das Ergebnis in der Liste."
)

# im_thread: ändert die Kennung des Aufrufers nicht
def thread_setzt_kennung():
    """Lässt den Thread die Kennung ändern und gibt die Kennung des Aufrufers danach zurück."""
    with mit_kennung("C3"):
        im_thread(ANFRAGE.set, "FREMD")
        return ANFRAGE.get()


ergebnis, protokoll = frisch(thread_setzt_kennung)
assert ergebnis == "C3", (
    f"Setzt der Thread ANFRAGE auf 'FREMD', hat der Aufrufer danach {ergebnis!r}, erwartet war weiter 'C3': "
    "Der Thread arbeitet in einer Kopie des Kontexts."
)

# Die Ausgabe des Programms
erwartet = "['Kunde Kaya', 'Kunde Berg']\n" + "\n".join(BEISPIEL) + "\n[C3] Bericht erstellt"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Anfragen
zufall = Zufall(5047)
for _ in range(20):
    anfragen = [(f"R{nummer}", f"K{zufall.randint(1, 99)}", zufall.randint(0, 20) / 1000) for nummer in range(zufall.randint(0, 12))]
    ergebnis, protokoll = frisch(lambda: asyncio.run(bearbeite_alle(anfragen)))
    erwartet = [f"Kunde {kunde}" for kennung, kunde, wartezeit in anfragen]
    assert ergebnis == erwartet, f"bearbeite_alle({anfragen})\nergibt   {ergebnis!r}\nerwartet {erwartet}"
    abweichung = zeilen_passen(protokoll, anfragen)
    assert abweichung is None, f"bearbeite_alle({anfragen}): {abweichung}"

# Obere Grenze: 1000 Anfragen gleichzeitig
anfragen = [(f"R{nummer:04d}", f"K{nummer}", zufall.randint(0, 50) / 1000) for nummer in range(1000)]
ergebnis, protokoll = frisch(lambda: asyncio.run(bearbeite_alle(anfragen)))
abweichung = zeilen_passen(protokoll, anfragen) if isinstance(ergebnis, list) and len(ergebnis) == 1000 else f"Ergebnis {str(ergebnis)[:100]}"
assert abweichung is None, f"Bei 1000 gleichzeitigen Anfragen: {abweichung}"
