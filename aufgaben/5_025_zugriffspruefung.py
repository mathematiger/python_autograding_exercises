"""Aufgabe 5_025 – Zugriffsprüfung                               Stufe 5 ★★★★★

Bei einer Sicherheitsprüfung versucht ein Skript, Hunderte von Dateien
und Diensten mit dem Konto eines normalen Mitarbeiters zu öffnen. Jeder
verweigerte Zugriff ist ein gutes Zeichen: Das Berechtigungskonzept
funktioniert. Er soll im Prüfbericht landen, den Lauf aber nicht
abbrechen. Alle anderen Ausnahmen (etwa ein Tippfehler im Skript, der
einen NameError auslöst) sollen dagegen wie gewohnt durchschlagen,
damit niemand einen kaputten Prüflauf für einen bestandenen hält.

Vervollständigen Sie den Kontextmanager `Abwehr`:

- `Abwehr(bericht, *arten)` merkt sich die Liste bericht und die
  Ausnahmeklassen arten, die abgefangen werden sollen.
- `__enter__(self)` setzt das Attribut `abgefangen` auf None und gibt
  das Objekt selbst zurück.
- `__exit__(self, typ, wert, traceback)` entscheidet, was mit einer
  Ausnahme aus dem with-Block passiert. Ist sie eine Instanz einer der
  arten (Unterklassen zählen mit), hängt es das Paar
  (Klassenname, str(ausnahme)) an bericht an, speichert die Ausnahme in
  `abgefangen` und unterdrückt sie. Jede andere Ausnahme lässt es
  unverändert weiterlaufen, ohne Eintrag im Bericht. Ohne Ausnahme
  passiert nichts.

Dasselbe Abwehr-Objekt darf für viele with-Blöcke benutzt werden.

    bericht = []
    abwehr = Abwehr(bericht, PermissionError, TimeoutError)
    with abwehr:
        raise PermissionError("kein Zugriff auf /etc/shadow")
    print("läuft weiter")                       # wird ausgegeben
    bericht  →  [("PermissionError", "kein Zugriff auf /etc/shadow")]
    with abwehr as a:
        pass
    a.abgefangen  →  None
    with abwehr:
        raise KeyError("Tippfehler")            # KeyError schlägt durch

Grenzen: arten sind 1 bis 10 Unterklassen von Exception. Der Block darf
jede Unterklasse von Exception auslösen oder gar keine. Ein Abwehr-Objekt
wird für bis zu 10 000 with-Blöcke nacheinander benutzt.

Hintergrund: Ein with-Block ruft beim Betreten __enter__ auf; was es
zurückgibt, landet hinter as. Beim Verlassen ruft Python immer
__exit__(typ, wert, traceback) auf, egal ob der Block normal endet oder
mit einer Ausnahme. Die drei Argumente beschreiben die Ausnahme: typ ist
ihre Klasse, wert das Ausnahme-Objekt selbst und traceback die Stelle,
an der sie entstand. Endet der Block ohne Ausnahme, sind alle drei None.

Wichtig ist der Rückgabewert von __exit__. Ist er wahr (True), gilt die
Ausnahme als erledigt: Python verwirft sie und macht hinter dem
with-Block weiter. Ist er falsch (False oder None, also auch, wenn
__exit__ gar nichts zurückgibt), läuft die Ausnahme weiter zum Aufrufer.
__exit__ selbst soll die Ausnahme nicht noch einmal mit raise auslösen;
es reicht, False zurückzugeben.

    class Leise:
        def __enter__(self):
            return self

        def __exit__(self, typ, wert, traceback):
            return typ is not None and issubclass(typ, ZeroDivisionError)

    with Leise():
        1 / 0                 # wird verschluckt
    with Leise():
        int("x")              # ValueError läuft weiter

issubclass(typ, klassen) und isinstance(wert, klassen) nehmen auch ein
Tupel von Klassen und zählen Unterklassen mit: isinstance(
FileNotFoundError(), OSError) ist True. Einen Klassennamen liefert
type(wert).__name__. Fertig gibt es so etwas als
contextlib.suppress(*arten); es führt aber keinen Bericht. Vorsicht:
Ein Kontextmanager, der zu viel verschluckt, versteckt echte Fehler.
Darum fängt man nur die Arten ab, mit denen man rechnet, und nie
pauschal Exception.
"""


class Abwehr:
    """Kontextmanager, der erwartete Ausnahmen protokolliert und unterdrückt."""

    def __init__(self, bericht, *arten):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __enter__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __exit__(self, typ, wert, traceback):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


bericht = []
abwehr = Abwehr(bericht, PermissionError, TimeoutError)
with abwehr:
    raise PermissionError("kein Zugriff auf /etc/shadow")
print("läuft weiter")
print(bericht)
