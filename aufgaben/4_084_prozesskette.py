"""Aufgabe 4_084 – Prozesskette                                  Stufe 4 ★★★★☆

Eine Werkstatt für Firmenlaptops beschreibt ihren Reparaturablauf als
Kette von Prozessschritten, jeder mit einer Bearbeitungsdauer in
Minuten: Annahme, Diagnose, Reparatur, Funktionstest, Rückgabe. Die
Kette ändert sich oft: Nach der Diagnose kommt bei manchen Geräten eine
„Datensicherung“ hinzu, ein Schritt fällt weg, neue Schritte kommen ans
Ende. Das Werkzeug, das die Abläufe verwaltet, speichert die Kette als
verkettete Liste (siehe Hintergrund): Jeder Schritt kennt nur seinen
Nachfolger, die Kette kennt ihren ersten und letzten Schritt.

Die Klasse `Schritt` und `__init__` von `Prozesskette` sind vorgegeben.
Vervollständigen Sie die Methoden von `Prozesskette`, ohne die Schritte
zusätzlich in einer Python-Liste oder einem Dictionary zu speichern:

- `anhaengen(name, dauer)` hängt einen neuen Schritt ans Ende, in O(1)
  Schritten, egal wie lang die Kette ist.
- `einfuegen_nach(vorgaenger, name, dauer)` fügt einen neuen Schritt
  direkt hinter dem Schritt mit dem Namen vorgaenger ein. Gibt es ihn
  nicht, löst sie KeyError aus und ändert nichts.
- `entfernen(name)` nimmt den Schritt mit diesem Namen aus der Kette
  und gibt seine Dauer zurück. Gibt es ihn nicht, löst sie KeyError aus.
- `__len__` gibt die Anzahl der Schritte zurück, in O(1).
- `__iter__` ist eine Generatormethode und liefert Paare (name, dauer)
  vom ersten bis zum letzten Schritt.
- `durchlaufzeit()` gibt die Summe aller Dauern zurück.

    kette = Prozesskette()
    kette.anhaengen("Annahme", 5)
    kette.anhaengen("Diagnose", 20)
    kette.anhaengen("Reparatur", 45)
    kette.einfuegen_nach("Diagnose", "Datensicherung", 30)
    list(kette)              →  [("Annahme", 5), ("Diagnose", 20),
                                 ("Datensicherung", 30), ("Reparatur", 45)]
    kette.entfernen("Annahme")   →  5
    len(kette)               →  3
    kette.durchlaufzeit()    →  95

Grenzen: Die Namen in einer Kette sind verschieden und nicht leer, jede
dauer ist eine ganze Zahl von 0 bis 10 000; neue Schritte haben einen
Namen, den es in der Kette noch nicht gibt. Eine Kette hat bis zu
100 000 Schritte und kann leer sein. Auch nach entfernen und
einfuegen_nach müssen erster, letzter und anzahl stimmen, denn
anhaengen und __len__ verlassen sich darauf.

Hintergrund: Eine Python-Liste legt ihre Elemente nebeneinander in den
Speicher. Darum ist liste[i] schnell, aber ein Element vorn oder in der
Mitte einzufügen oder zu löschen schiebt alle dahinter um einen Platz:
O(n). Eine verkettete Liste legt jedes Element in ein eigenes kleines
Objekt, den Knoten, der auf seinen Nachfolger zeigt; der letzte zeigt auf
None. Sie ist eine rekursive Datenstruktur wie der Baum aus Aufgabe 4_083,
nur mit einem Kind pro Knoten:

    class Knoten:
        def __init__(self, wert):
            self.wert = wert
            self.naechster = None

    a, b, c = Knoten("A"), Knoten("B"), Knoten("C")
    a.naechster = b                 # A → B
    b.naechster = c                 # A → B → C

    neu = Knoten("X")               # X zwischen A und B einfügen:
    neu.naechster = a.naechster     #   erst X → B
    a.naechster = neu               #   dann A → X → B → C

    a.naechster = a.naechster.naechster   # X wieder herausnehmen: A → B → C

Kennt man den Knoten davor, kostet Einfügen und Entfernen also nur zwei
Zuweisungen, egal wie lang die Liste ist. Dafür muss man zum i-ten
Element von vorn hinlaufen (O(n)), und wer entfernen will, braucht den
Vorgänger, also läuft man mit zwei Variablen (vorher, aktuell) durch die
Kette. Die Reihenfolge der Zuweisungen ist wichtig: Wer zuerst
a.naechster = neu schreibt, hat den Rest der Kette verloren.

Merkt sich die Kette außer dem ersten auch den letzten Knoten, geht
anhaengen in O(1): letzter.naechster = neu, dann letzter = neu. Ohne
diesen Zeiger müsste man jedes Mal bis zum Ende laufen, und n Schritte
anzuhängen kostete O(n²). Vorsicht bei den Rändern: Bei der leeren
Kette sind erster und letzter None; entfernt man den ersten Schritt,
wird sein Nachfolger der neue erste, entfernt man den letzten, wird sein
Vorgänger der neue letzte. Genau so arbeitet collections.deque
(Aufgabe 3_057) intern, nur mit Zeigern in beide Richtungen.

Wie in Aufgabe 4_035 schreiben Sie __iter__ als Generatormethode: eine
Variable beginnt bei self.erster und geht mit aktuell = aktuell.naechster
weiter, bis sie None ist. So liefert jedes for einen neuen Durchlauf, und
durchlaufzeit kann einfach über self laufen.
"""


class Schritt:
    """Ein Prozessschritt: Name, Dauer in Minuten und der nachfolgende Schritt (oder None)."""

    def __init__(self, name, dauer):
        """Legt einen Schritt ohne Nachfolger an."""
        self.name = name
        self.dauer = dauer
        self.naechster = None


class Prozesskette:
    """Eine Kette von Prozessschritten als verkettete Liste."""

    def __init__(self):
        """Legt eine leere Kette an."""
        self.erster = None
        self.letzter = None
        self.anzahl = 0

    def anhaengen(self, name, dauer):
        """Hängt einen neuen Schritt ans Ende der Kette, in O(1)."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def einfuegen_nach(self, vorgaenger, name, dauer):
        """Fügt einen neuen Schritt direkt hinter dem Schritt vorgaenger ein; KeyError, wenn es ihn nicht gibt."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def entfernen(self, name):
        """Nimmt den Schritt name aus der Kette und gibt seine Dauer zurück; KeyError, wenn es ihn nicht gibt."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __len__(self):
        """Gibt die Anzahl der Schritte zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __iter__(self):
        """Liefert (name, dauer) für jeden Schritt vom ersten bis zum letzten."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def durchlaufzeit(self):
        """Gibt die Summe aller Dauern zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


kette = Prozesskette()
kette.anhaengen("Annahme", 5)
kette.anhaengen("Diagnose", 20)
kette.anhaengen("Reparatur", 45)
kette.einfuegen_nach("Diagnose", "Datensicherung", 30)
print(list(kette))
print(kette.entfernen("Annahme"), len(kette), kette.durchlaufzeit())
