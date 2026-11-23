"""Aufgabe 5_044 – Planungspoker                                 Stufe 5 ★★★★★

Ein verteiltes Scrum-Team schätzt den Aufwand seiner User Stories mit
Planungspoker (englisch Planning Poker): Jede Person legt verdeckt eine
Zahl von Story Points fest, erst wenn alle geschätzt haben, wird
aufgedeckt. Liegen die Schätzungen auseinander, erklären die Person mit
der niedrigsten und die mit der höchsten Zahl ihre Gründe, dann wird
neu geschätzt. Das Team arbeitet von zu Hause; ein kleines Programm
fragt jede Person über den Teamchat nach ihrer Karte und wartet auf die
Antwort. Bisher fragt es eine Person nach der anderen, und bei zwölf
Leuten dauert jede Runde ewig.

Die Abfrage ist die vorgegebene Funktion frage(person, story): Sie
wartet, bis die Person antwortet (hier nur nachgebildet mit time.sleep
und den Dictionaries ANTWORTZEIT und KARTEN), und gibt ihre Zahl zurück.
Dabei schreibt sie in PROTOKOLL, wann gefragt und wann geantwortet wurde,
und in FRAGENDE, aus welchem Thread gefragt wurde. Schreiben Sie:

- die Klasse `Abfrage`, eine Unterklasse von threading.Thread: Abfrage(
  person, story) merkt sich beides in den Attributen person und story;
  wenn der Thread läuft, ruft er frage(person, story) auf und speichert
  die Antwort im Attribut karte.
- `runde(personen, story)` fragt alle Personen gleichzeitig, mit je
  einem Abfrage-Thread, wartet, bis alle geantwortet haben, und gibt ein
  Dictionary Person → Karte in der Reihenfolge der Liste personen zurück.
- `aussprache(karten)` gibt None zurück, wenn alle Karten gleich sind
  (oder keine da ist), sonst das Paar (person_mit_niedrigster,
  person_mit_hoechster). Haben mehrere Personen dieselbe niedrigste oder
  höchste Karte, zählt die, die im Dictionary zuerst kommt.

    KARTEN = {"Aylin": 5, "Ben": 8, "Chiara": 3, "Dario": 8}
    runde(["Aylin", "Ben", "Chiara", "Dario"], "Login per Fingerabdruck")
    →  {"Aylin": 5, "Ben": 8, "Chiara": 3, "Dario": 8}
    aussprache({"Aylin": 5, "Ben": 8, "Chiara": 3, "Dario": 8})
    →  ("Chiara", "Ben")

Grenzen: personen hat 0 bis 30 verschiedene Namen, die alle in KARTEN
stehen; eine Karte ist eine der Zahlen 0, 1, 2, 3, 5, 8, 13, 20, 40, 100.
Jede Person antwortet nach höchstens einer halben Sekunde. karten hat 0
bis 30 Einträge.

Hintergrund: In Aufgabe 4_053 hat ein ThreadPoolExecutor Threads für
Sie gestartet und die Ergebnisse eingesammelt. Darunter liegt das Modul
threading. Ein Thread ist ein eigener Ablauf im selben Programm: Er
teilt sich alle Variablen mit dem Hauptprogramm, läuft aber
gleichzeitig weiter, während das Hauptprogramm etwas anderes tut. Am
einfachsten gibt man ihm eine Funktion mit, die er ausführen soll:

    import threading

    def melden(name):
        print("hallo", name)

    t = threading.Thread(target=melden, args=("Ada",))
    t.start()       # der Thread läuft los, start() kehrt sofort zurück
    t.join()        # wartet, bis der Thread fertig ist

start() kehrt sofort zurück; erst join() wartet. Wer gleichzeitig
warten will, startet deshalb erst alle Threads in einer Schleife und
ruft danach in einer zweiten Schleife join() für jeden auf. Steht
join() in derselben Schleife wie start(), wartet das Programm auf jeden
Thread, bevor es den nächsten startet, und alles läuft wieder
nacheinander.

Einen Rückgabewert von target gibt es nicht: Was ein Thread ausrechnet,
muss er irgendwo ablegen, wo das Hauptprogramm es nach join() findet.
Eine saubere Art ist eine Unterklasse von threading.Thread, die ihr
Ergebnis in einem Attribut speichert. Die Arbeit gehört in die Methode
run(); start() legt den neuen Ablauf an und ruft darin run() auf:

    class Quadrat(threading.Thread):
        def __init__(self, zahl):
            super().__init__()       # Thread muss sich selbst einrichten
            self.zahl = zahl

        def run(self):
            self.ergebnis = self.zahl ** 2

    q = Quadrat(7)
    q.start()
    q.join()
    q.ergebnis      →  49

Ruft man q.run() selbst auf statt q.start(), läuft es ganz normal im
Hauptprogramm, ohne neuen Thread. Und nennen Sie kein eigenes Attribut
name: Das benutzt Thread schon für den Namen des Threads.

Threads lohnen sich in Python vor allem beim Warten, auf das Netz, eine
Datei oder wie hier einen Menschen. Reine Rechenarbeit wird nicht
schneller, weil immer nur ein Thread gleichzeitig Python-Code ausführt
(die globale Sperre GIL). Dafür kann jeder Thread jederzeit unterbrochen
werden, nicht nur an einem await wie bei asyncio (Aufgabe 5_042); was
das für gemeinsame Variablen bedeutet, zeigt eine spätere Aufgabe.
"""

import threading
import time

ANTWORTZEIT = {}
KARTEN = {}
PROTOKOLL = []
FRAGENDE = []


def frage(person, story):
    """Fragt person nach ihrer Karte für story und wartet auf die Antwort (hier nur nachgebildet)."""
    FRAGENDE.append(threading.current_thread())
    PROTOKOLL.append(f"gefragt {person}")
    time.sleep(ANTWORTZEIT.get(person, 0.05))  # wartet, bis die Person antwortet
    PROTOKOLL.append(f"geantwortet {person}")
    return KARTEN[person]


class Abfrage(threading.Thread):
    """Ein Thread, der eine Person nach ihrer Karte fragt und die Antwort in karte speichert."""

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def runde(personen, story):
    """Fragt alle Personen gleichzeitig und gibt Person → Karte zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def aussprache(karten):
    """Gibt (niedrigste, höchste) Person zurück oder None, wenn alle Karten gleich sind."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


KARTEN.update({"Aylin": 5, "Ben": 8, "Chiara": 3, "Dario": 8})
karten = runde(["Aylin", "Ben", "Chiara", "Dario"], "Login per Fingerabdruck")
print(karten)
print(aussprache(karten))
