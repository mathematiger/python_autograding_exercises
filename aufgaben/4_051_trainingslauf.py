"""Aufgabe 4_051 – Trainingslauf                                 Stufe 4 ★★★★☆

Ein Team trainiert Modelle für maschinelles Lernen in einer Pipeline
aus mehreren Schritten: Daten laden, Daten bereinigen, trainieren,
bewerten. Für die Prozessanalyse soll jeder Schritt seine Laufzeit ins
Protokoll schreiben, auch wenn er mit einem Fehler abbricht. Außerdem
probiert das Team oft für einen Lauf andere Einstellungen aus, etwa
eine kleinere Lernrate; danach müssen wieder die alten gelten, auch
wenn der Probelauf abstürzt. Beides soll mit with gehen. Schreiben Sie
zwei Kontextmanager-Klassen:

- `Schrittzeit(protokoll, schritt, uhr=time.perf_counter)`: protokoll
  ist eine Liste, schritt der Name des Schritts, uhr eine Funktion, die
  die aktuelle Zeit in Sekunden liefert. Beim Betreten des with-Blocks
  merkt sich das Objekt die Zeit und gibt sich selbst zurück. Beim
  Verlassen setzt es das Attribut dauer (Zeit jetzt minus Zeit beim
  Betreten) und hängt das Tupel (schritt, dauer, status) an protokoll an;
  status ist "ok", wenn der Block normal endete, sonst "fehler". Eine
  Ausnahme aus dem Block wird nicht verschluckt.
- `Probeeinstellung(einstellungen, **probewerte)`: einstellungen ist
  ein Dictionary. Beim Betreten trägt das Objekt die probewerte darin
  ein und gibt einstellungen zurück. Beim Verlassen stellt es den
  Zustand von vorher wieder her: geänderte Schlüssel bekommen ihren
  alten Wert, Schlüssel, die es vorher nicht gab, werden entfernt. Das
  gilt auch nach einer Ausnahme, die ebenfalls nicht verschluckt wird.
  Es bleibt dasselbe Dictionary-Objekt.

    protokoll = []
    with Schrittzeit(protokoll, "laden", uhr=iter([10.0, 12.5]).__next__):
        pass
    protokoll                      →  [("laden", 2.5, "ok")]

    einstellungen = {"lernrate": 0.1, "epochen": 20}
    with Probeeinstellung(einstellungen, lernrate=0.01, seed=7) as e:
        e                          →  {"lernrate": 0.01, "epochen": 20, "seed": 7}
    einstellungen                  →  {"lernrate": 0.1, "epochen": 20}

Im ersten Beispiel ist uhr eine Funktion, die beim ersten Aufruf 10.0
und beim zweiten 12.5 liefert; so prüfen auch die Tests, ohne echte
Zeit zu messen.

Grenzen: protokoll ist eine Liste, schritt ein nicht leerer Text, uhr
liefert nicht fallende Zahlen. einstellungen hat 0 bis 10 000 Einträge
mit Texten als Schlüsseln, probewerte 0 bis 1000. Die Objekte können
verschachtelt benutzt werden, jedes Objekt aber nur für einen
with-Block.

Hintergrund: Sie kennen with von Dateien (Aufgabe 3_046): with open(...) as
datei: schließt die Datei am Ende des Blocks, auch wenn darin ein Fehler
passiert. Das funktioniert mit jedem Objekt, das zwei Methoden hat,
__enter__ und __exit__; so ein Objekt heißt Kontextmanager. Python
übersetzt

    with Ausdruck as name:
        Block

ungefähr in

    manager = Ausdruck
    name = manager.__enter__()
    try:
        Block
    except BaseException as fehler:
        if not manager.__exit__(type(fehler), fehler, fehler.__traceback__):
            raise
    else:
        manager.__exit__(None, None, None)

Was __enter__ zurückgibt, landet hinter as (oft self, aber nicht
immer). __exit__ bekommt drei Argumente: den Typ der Ausnahme, die
Ausnahme selbst und den Verlauf (Traceback), oder dreimal None, wenn
der Block normal endete. Gibt __exit__ etwas Falsches zurück (False
oder None), fliegt die Ausnahme danach weiter; nur ein wahrer
Rückgabewert verschluckt sie. Ein Beispiel:

    class Einrueckung:
        def __init__(self, zeilen):
            self.zeilen = zeilen
        def __enter__(self):
            self.zeilen.append("Anfang")
            return self
        def __exit__(self, typ, wert, verlauf):
            self.zeilen.append("Ende" if typ is None else f"Abbruch: {wert}")
            return False

So gehören Vorbereiten und Aufräumen zusammen in eine Klasse, und wer
sie benutzt, kann das Aufräumen nicht vergessen. Zustand sichern heißt:
In __enter__ merkt man sich, was man gleich ändert, und in __exit__
stellt man es wieder her. Ob ein Schlüssel vorher fehlte, muss man sich
dabei eigens merken, denn None kann auch ein echter alter Wert sein.
"""

import time


class Schrittzeit:
    """Misst die Laufzeit eines with-Blocks und schreibt sie ins Protokoll."""

    def __init__(self, protokoll, schritt, uhr=time.perf_counter):
        """Merkt sich Protokoll, Schrittname und Uhr."""
        self.protokoll = protokoll
        self.schritt = schritt
        self.uhr = uhr
        self.dauer = None

    def __enter__(self):
        """Merkt sich die Startzeit und gibt das Objekt zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __exit__(self, typ, wert, verlauf):
        """Setzt dauer, schreibt (schritt, dauer, status) ins Protokoll und lässt Ausnahmen weiterfliegen."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Probeeinstellung:
    """Setzt für einen with-Block andere Einstellungen und stellt danach die alten wieder her."""

    def __init__(self, einstellungen, **probewerte):
        """Merkt sich das Dictionary und die Probewerte."""
        self.einstellungen = einstellungen
        self.probewerte = probewerte

    def __enter__(self):
        """Sichert die betroffenen Einträge, trägt die Probewerte ein und gibt das Dictionary zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __exit__(self, typ, wert, verlauf):
        """Stellt den Zustand von vorher wieder her und lässt Ausnahmen weiterfliegen."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


protokoll = []
with Schrittzeit(protokoll, "laden", uhr=iter([10.0, 12.5]).__next__):
    pass
print(protokoll)

einstellungen = {"lernrate": 0.1, "epochen": 20}
with Probeeinstellung(einstellungen, lernrate=0.01, seed=7) as e:
    print(e)
print(einstellungen)
