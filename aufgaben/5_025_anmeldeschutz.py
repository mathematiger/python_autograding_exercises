"""Aufgabe 5_025 – Anmeldeschutz                                 Stufe 5 ★★★★★

Ein Anmeldedienst soll sich gegen das Durchprobieren von Passwörtern
(Brute Force) wehren. Jeder Anmeldeversuch läuft in einem with-Block;
schlägt er fehl, löst die Prüfung eine Ausnahme `Zugriffsverweigert` (oder
eine Unterklasse davon) aus. Ein Kontextmanager `Anmeldeschutz` soll diese
Ausnahmen abfangen und protokollieren, damit der Dienst nach einem
falschen Passwort einfach weiterläuft. Ab einer Grenze ist aber Schluss:
Dann lässt der Schutz die Ausnahme durch, und der Aufrufer muss das Konto
sperren. Andere Fehler (ein Programmierfehler, ein Netzwerkausfall) gehen
den Schutz nichts an: Sie werden weder protokolliert noch unterdrückt.

Vervollständigen Sie `Anmeldeschutz`:

- `__init__(self, erlaubte_fehler)` merkt sich die Grenze und legt das
  Protokoll `fehlversuche` als leere Liste an.
- `__enter__(self)` gibt das Objekt selbst zurück.
- `__exit__(self, typ, wert, verlauf)`:
  - Ohne Ausnahme im Block passiert nichts.
  - Bei einer Ausnahme der Klasse Zugriffsverweigert oder einer ihrer
    Unterklassen hängt er str(wert) an fehlversuche an. Sind es danach
    höchstens erlaubte_fehler Einträge, unterdrückt er die Ausnahme;
    sonst lässt er sie durch.
  - Jede andere Ausnahme lässt er unverändert durch.
  - Der Rückgabewert ist True genau dann, wenn er unterdrückt, sonst
    False.

Dasselbe Anmeldeschutz-Objekt wird für viele with-Blöcke nacheinander
benutzt und zählt über alle hinweg.

    schutz = Anmeldeschutz(2)
    with schutz:
        anmelden("admin", "1234")        # falsch: unterdrückt, protokolliert
    with schutz:
        anmelden("admin", "passwort")    # falsch: unterdrückt, protokolliert
    with schutz:
        anmelden("admin", "geheim")      # falsch: Zugriffsverweigert kommt durch
    schutz.fehlversuche
        →  ["admin: falsches Passwort", "admin: falsches Passwort",
            "admin: falsches Passwort"]

Grenzen: erlaubte_fehler ist eine ganze Zahl mit 0 ≤ erlaubte_fehler ≤
1000. Ein Schutz-Objekt wird für bis zu 10 000 with-Blöcke benutzt. Im
Block kann jede Ausnahme auftreten, auch KeyboardInterrupt oder
SystemExit, die nicht von Exception abstammen; nur Zugriffsverweigert und
ihre Unterklassen werden unterdrückt.

Hintergrund: Ein with-Block ruft beim Betreten `__enter__` auf; was es
zurückgibt, landet hinter `as`. Beim Verlassen ruft er immer `__exit__`
auf, egal ob der Block normal endet, mit return verlassen wird oder eine
Ausnahme auslöst. `__exit__` bekommt drei Argumente, die die Ausnahme
beschreiben:

- `typ`: die Klasse der Ausnahme, etwa ValueError,
- `wert`: das Ausnahme-Objekt selbst (str(wert) ist die Meldung),
- `verlauf`: der Traceback, also wo es passiert ist.

Endet der Block ohne Ausnahme, sind alle drei None. Entscheidend ist der
Rückgabewert von `__exit__`: Ist er wahr, gilt die Ausnahme als erledigt,
und das Programm macht hinter dem with-Block weiter, als wäre nichts
gewesen. Ist er falsch (auch None, also ohne return), läuft die Ausnahme
weiter zum Aufrufer. Den Rest des Blocks nach der Ausnahme führt Python
in keinem Fall mehr aus.

    class Schlucke:
        def __init__(self, klasse):
            self.klasse = klasse
            self.anzahl = 0

        def __enter__(self):
            return self

        def __exit__(self, typ, wert, verlauf):
            if typ is not None and issubclass(typ, self.klasse):
                self.anzahl += 1
                return True        # Ausnahme ist erledigt
            return False           # durchlassen

    with Schlucke(ZeroDivisionError) as s:
        1 / 0
        print("nie")               # wird übersprungen
    print(s.anzahl)                # 1, das Programm läuft weiter
    with Schlucke(ZeroDivisionError):
        int("x")                   # ValueError kommt durch

issubclass(typ, Klasse) prüft, ob typ diese Klasse oder eine Unterklasse
davon ist, so wie except Klasse auch Unterklassen fängt. Weil typ ohne
Ausnahme None ist, prüft man das zuerst; issubclass(None, …) wäre ein
TypeError. Die Standardbibliothek hat diesen Kontextmanager schon fertig:
contextlib.suppress(ZeroDivisionError) schluckt genau diese Ausnahmen,
zählt aber nicht mit. Unterdrücken ist mächtig und gefährlich: Ein
Kontextmanager, der immer True zurückgibt, verschluckt auch Tippfehler
und Abbrüche mit Strg+C. Darum nur genau die Ausnahmen unterdrücken, für
die man zuständig ist, und `__exit__` sollte die Ausnahme nicht selbst
mit raise neu auslösen, sondern False zurückgeben; dann behält sie ihren
ursprünglichen Traceback.
"""


class Zugriffsverweigert(Exception):
    """Ein Anmeldeversuch ist fehlgeschlagen."""


class PasswortAbgelaufen(Zugriffsverweigert):
    """Das Passwort stimmt, ist aber abgelaufen; auch das ist ein Fehlversuch."""


PASSWOERTER = {"admin": "Sommer2026!", "gast": "gast123"}


def anmelden(name, passwort):
    """Prüft ein Passwort; löst Zugriffsverweigert aus, wenn es nicht stimmt."""
    if PASSWOERTER.get(name) != passwort:
        raise Zugriffsverweigert(f"{name}: falsches Passwort")
    return f"{name} ist angemeldet"


class Anmeldeschutz:
    """Kontextmanager, der fehlgeschlagene Anmeldungen protokolliert und bis zu einer Grenze unterdrückt."""

    def __init__(self, erlaubte_fehler):
        """Merkt sich, wie viele Fehlversuche unterdrückt werden; das Protokoll ist anfangs leer."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __enter__(self):
        """Gibt den Schutz selbst zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __exit__(self, typ, wert, verlauf):
        """Protokolliert einen Fehlversuch; gibt True zurück, wenn die Ausnahme unterdrückt wird."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


schutz = Anmeldeschutz(2)
for versuch in ["1234", "passwort", "geheim"]:
    try:
        with schutz:
            anmelden("admin", versuch)
    except Zugriffsverweigert:
        print("Konto gesperrt")
print(schutz.fehlversuche)
