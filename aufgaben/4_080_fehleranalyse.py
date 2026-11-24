"""Aufgabe 4_080 – Fehleranalyse                                 Stufe 4 ★★★★☆

Bevor ein neues Monitoring-System in Betrieb geht, macht das Team eine
FMEA (Fehlermöglichkeits- und Einflussanalyse): Für jede denkbare
Fehlerart schätzt es drei Zahlen von 1 bis 10, die Bedeutung (wie schlimm
ist der Fehler), das Auftreten (wie oft kommt er vor) und die Entdeckung
(wie schwer fällt er auf; 10 heißt: fast unentdeckbar). Ihr Produkt ist
die Risikoprioritätszahl RPZ; die Fehlerart mit der höchsten RPZ wird
zuerst angegangen.

Ein Kollege hat das Werkzeug dafür angefangen, aber es verhält sich
seltsam:

    def erfasse(fehlerart, bedeutung, auftreten, entdeckung, tabelle=[]):
        tabelle.append((fehlerart, bedeutung * auftreten * entdeckung))
        return tabelle

    erfasse("Sensor liefert keine Werte", 8, 3, 6)
                      →  [("Sensor liefert keine Werte", 144)]
    erfasse("Zeitstempel falsch", 4, 5, 7)
                      →  [("Sensor liefert keine Werte", 144),
                          ("Zeitstempel falsch", 140)]

Der zweite Aufruf sollte eine neue Analyse beginnen, enthält aber die
Fehlerart des ersten. Schreiben Sie die drei Funktionen richtig; die
Funktionsköpfe sind vorgegeben:

- `erfasse(fehlerart, bedeutung, auftreten, entdeckung, tabelle=None)`
  hängt das Tupel (fehlerart, RPZ) an die Liste tabelle an und gibt
  tabelle zurück. Ohne tabelle beginnt jeder Aufruf eine neue Liste;
  eine übergebene Liste (auch eine leere) wird selbst ergänzt.
- `neue_analyse(system, beteiligte=("Betrieb",))` gibt ein neues
  Dictionary {"system": system, "beteiligte": [...], "eintraege": []}
  zurück. "beteiligte" ist eine Liste mit den Namen aus beteiligte,
  "eintraege" eine leere Liste. Jede Analyse hat ihre eigenen Listen:
  Was man an einer ändert, ändert weder eine andere Analyse noch die
  übergebene Folge beteiligte noch spätere Analysen.
- `hoechste_rpz(tabelle, standard=FEHLT)` gibt das Tupel mit der
  höchsten RPZ zurück, bei Gleichstand das vordere. Ist tabelle leer,
  gibt sie standard zurück, auch wenn das None ist; wurde kein standard
  übergeben, löst sie einen ValueError aus.

    tabelle = erfasse("Sensor liefert keine Werte", 8, 3, 6)
    erfasse("Zeitstempel falsch", 4, 5, 7, tabelle)
    erfasse("Alarm-Mail landet im Spam", 9, 4, 5, tabelle)
    hoechste_rpz(tabelle)       →  ("Alarm-Mail landet im Spam", 180)
    erfasse("Zeitstempel falsch", 4, 5, 7)
                                →  [("Zeitstempel falsch", 140)]
    neue_analyse("Monitoring")  →  {"system": "Monitoring",
                                    "beteiligte": ["Betrieb"],
                                    "eintraege": []}
    hoechste_rpz([], None)      →  None
    hoechste_rpz([])            →  ValueError

Grenzen: fehlerart und system sind nicht leere Texte; bedeutung,
auftreten und entdeckung sind ganze Zahlen von 1 bis 10. tabelle ist
None oder eine Liste mit 0 bis 100 000 Tupeln (fehlerart, rpz).
beteiligte ist ein Tupel oder eine Liste mit 0 bis 20 Namen. standard
darf jeder Wert sein, auch None.

Hintergrund: Standardwerte für Parameter kennen Sie aus Aufgabe 2_011.
Neu ist, wann sie entstehen: Python wertet den Ausdruck hinter dem =
genau einmal aus, wenn die def-Zeile ausgeführt wird, also beim Laden
des Programms, nicht bei jedem Aufruf. Das Ergebnis hängt an der
Funktion, in funktion.__defaults__:

    def merke(eintrag, liste=[]):
        liste.append(eintrag)
        return liste

    merke.__defaults__         →  ([],)
    merke("a")                 →  ["a"]
    merke("b")                 →  ["a", "b"]    (dieselbe Liste!)
    merke.__defaults__         →  (["a", "b"],)

Jeder Aufruf ohne liste bekommt also dasselbe Listenobjekt, und
append verändert es für alle späteren Aufrufe (eine Zuweisung kopiert
nichts, Aufgabe 2_018). Bei Zahlen, Texten und Tupeln passiert das
nicht, weil sie unveränderlich sind (Aufgabe 2_019). Die Falle lauert
nur bei veränderlichen Standardwerten: Listen, Dictionaries, Mengen
und eigenen Objekten. Darum nimmt man None als Standardwert und legt
das neue Objekt erst im Rumpf an, bei jedem Aufruf neu (so schon in
Aufgabe 3_033):

    def merke(eintrag, liste=None):
        if liste is None:
            liste = []
        liste.append(eintrag)
        return liste

Verlockend kürzer ist liste = liste or [], aber falsch: Auch eine
übergebene leere Liste ist „falsch“ im Sinne von or, und der Aufrufer
wundert sich, dass seine Liste leer bleibt. Prüfen Sie mit is None.
Dieselbe Falle verhindert @dataclass mit field(default_factory=list)
(Aufgabe 4_012).

Ein unveränderlicher Standardwert wie das Tupel ("Betrieb",) ist
dagegen sicher. Soll das Ergebnis eine veränderliche Liste enthalten,
macht man daraus im Rumpf mit list(beteiligte) eine neue; das kopiert
zugleich eine übergebene Liste, sodass Ergebnis und Aufrufer sich
nichts teilen.

Und wenn None selbst ein sinnvoller Wert ist, wie bei standard? Dann
braucht man ein eigenes Zeichen für „nicht übergeben“, ein Objekt, das
niemand sonst hat. object() liefert bei jedem Aufruf ein neues, mit
nichts anderem identisches Objekt; man vergleicht mit is:

    FEHLT = object()

    def erster(werte, standard=FEHLT):
        if werte:
            return werte[0]
        if standard is FEHLT:
            raise ValueError("leer und kein Standardwert")
        return standard

So arbeitet auch next(iterator, standard) aus Aufgabe 4_034.
"""

FEHLT = object()


def erfasse(fehlerart, bedeutung, auftreten, entdeckung, tabelle=None):
    """Hängt (fehlerart, RPZ) an tabelle an (ohne tabelle an eine neue Liste) und gibt die Liste zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def neue_analyse(system, beteiligte=("Betrieb",)):
    """Gibt ein neues Analyse-Dictionary mit eigenen Listen beteiligte und eintraege zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def hoechste_rpz(tabelle, standard=FEHLT):
    """Gibt den Eintrag mit der höchsten RPZ zurück; bei leerer tabelle standard oder ValueError."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


tabelle = erfasse("Sensor liefert keine Werte", 8, 3, 6)
erfasse("Zeitstempel falsch", 4, 5, 7, tabelle)
erfasse("Alarm-Mail landet im Spam", 9, 4, 5, tabelle)
print(hoechste_rpz(tabelle))
print(erfasse("Zeitstempel falsch", 4, 5, 7))
print(neue_analyse("Monitoring"))
