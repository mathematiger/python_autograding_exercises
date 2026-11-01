"""Aufgabe 5_010 – Formularfelder                                  Stufe 5 ★★★★★

Eine Firma baut ihre Eingabemasken nicht mehr von Hand, sondern
beschreibt sie in einer Konfiguration: eine Liste von Dictionaries, eins
pro Feld, etwa {"typ": "zahl", "name": "alter", "maximum": 150}. Ein
kleines Rahmenwerk liest die Beschreibung, erzeugt daraus die passenden
Feldobjekte und prüft damit die Eingaben der Nutzerinnen und Nutzer.
Jede Feldart ist eine Unterklasse von Feld mit einer Methode pruefe(text),
die eine verständliche Fehlermeldung oder None (alles in Ordnung)
zurückgibt.

Neue Feldarten sollen andere Teams später hinzufügen können, ohne den
Code des Rahmenwerks anzufassen. Darum meldet sich jede Unterklasse beim
Anlegen selbst an, mit ihrem Kürzel als Schlüsselwortargument in der
class-Zeile:

    class Zahlfeld(Feld, typ="zahl"):
        ...

Vervollständigen Sie:

- `Feld.__init_subclass__(cls, typ, **kwargs)`: Wird beim Anlegen jeder
  Unterklasse aufgerufen (auch bei Unterklassen von Unterklassen). Gibt
  es das Kürzel schon in Feld.typen, löst es einen ValueError aus und
  ändert nichts. Hat die Klasse keine aufrufbare Methode pruefe (selbst
  definiert oder geerbt), löst es einen TypeError aus und ändert nichts.
  Sonst setzt es das Klassenattribut cls.typ auf das Kürzel und trägt
  die Klasse in Feld.typen ein. Weitere Schlüsselwortargumente reicht es
  an super().__init_subclass__ weiter (bei unbekannten löst das einen
  TypeError aus).
- `erzeuge(beschreibung)`: Nimmt den Wert zu "typ" aus der Beschreibung,
  sucht die Klasse in Feld.typen (ValueError, wenn es das Kürzel nicht
  gibt) und erzeugt das Feld; alle übrigen Einträge der Beschreibung
  werden zu Schlüsselwortargumenten. Die Beschreibung bleibt unverändert.

Textfeld und Zahlfeld stehen schon im Code; sie funktionieren, sobald
__init_subclass__ fertig ist.

    Feld.typen                    →  {"text": Textfeld, "zahl": Zahlfeld}
    Zahlfeld.typ                  →  "zahl"
    feld = erzeuge({"typ": "zahl", "name": "alter", "maximum": 150})
    type(feld), feld.name, feld.maximum   →  Zahlfeld, "alter", 150
    feld.pruefe("200")            →  "alter: höchstens 150"
    erzeuge({"typ": "datum", "name": "geburtstag"})   →  ValueError
    class Doppelt(Feld, typ="text"): ...              →  ValueError

Grenzen: Ein Kürzel ist ein nicht leerer Text. Eine Beschreibung ist ein
Dictionary mit den Schlüsseln "typ" und "name" und höchstens den
weiteren Schlüsseln, die die __init__ der Feldart als Parameter kennt.

Hintergrund: Wie __init__ ein neues Objekt einrichtet, kann eine Klasse
mit __init_subclass__ jede neue Unterklasse einrichten. Python ruft die
Methode auf, sobald der Körper einer class-Anweisung fertig ausgeführt
ist, und zwar die __init_subclass__ der Elternklasse, mit der neuen
Klasse als erstem Argument. Sie ist von selbst eine Klassenmethode; ein
@classmethod ist nicht nötig:

    class Plugin:
        alle = []

        def __init_subclass__(cls, **kwargs):
            super().__init_subclass__(**kwargs)
            Plugin.alle.append(cls)

    class Export(Plugin):
        pass

    Plugin.alle        →  [Export]

Schlüsselwortargumente in der class-Zeile, außer metaclass, landen als
Schlüsselwortargumente bei __init_subclass__. So lassen sich Unterklassen
konfigurieren, ohne dass man nach der Klasse noch etwas aufrufen muss:

    class Plugin:
        def __init_subclass__(cls, endung, **kwargs):
            super().__init_subclass__(**kwargs)
            cls.endung = endung

    class CsvExport(Plugin, endung=".csv"):
        pass

    CsvExport.endung   →  ".csv"

Fehlt ein Pflichtargument wie endung, scheitert schon die class-Anweisung
mit einem TypeError, ebenso, wenn __init_subclass__ selbst eine Ausnahme
auslöst: Die Klasse entsteht dann gar nicht. Darum ist __init_subclass__
der richtige Ort, um Regeln für Unterklassen durchzusetzen, etwa dass sie
eine bestimmte Methode haben. Weil die Methode beim Anlegen der Klasse
läuft, kann sie die Methoden der neuen Klasse schon sehen: getattr(cls,
"pruefe", None) findet auch eine geerbte.

Warum super().__init_subclass__(**kwargs)? Bei Mehrfachvererbung (Aufgabe
4_010) kann eine weitere Elternklasse eigene Schlüsselwörter erwarten;
jede nimmt sich ihre und reicht den Rest weiter. Am Ende der Kette steht
object.__init_subclass__, das gar keine Schlüsselwörter annimmt; ein
Tippfehler wie endnug=".csv" fällt so als TypeError auf, statt still
ignoriert zu werden.

Wo steht das Verzeichnis? cls.typen in __init_subclass__ findet das
Klassenattribut von Feld, weil die Unterklasse es erbt; eine Zuweisung
cls.typen = … würde aber ein neues Attribut in der Unterklasse anlegen.
Ändern Sie das Dictionary darum nur (Feld.typen[typ] = cls).
"""


class Feld:
    """Ein Eingabefeld; Unterklassen melden sich mit typ="…" in der class-Zeile an."""

    typen = {}

    def __init__(self, name):
        """Merkt sich den Namen des Felds."""
        self.name = name

    def __init_subclass__(cls, typ, **kwargs):
        """Prüft die neue Unterklasse und trägt sie unter dem Kürzel typ in Feld.typen ein."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def erzeuge(beschreibung):
    """Erzeugt aus einer Beschreibung wie {"typ": "zahl", "name": "alter"} das passende Feld."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Textfeld(Feld, typ="text"):
    """Ein Feld für Text mit einer Höchstlänge."""

    def __init__(self, name, laenge=100):
        """Merkt sich Name und Höchstlänge."""
        super().__init__(name)
        self.laenge = laenge

    def pruefe(self, text):
        """Meldet einen zu langen Text."""
        if len(text) > self.laenge:
            return f"{self.name}: höchstens {self.laenge} Zeichen"
        return None


class Zahlfeld(Feld, typ="zahl"):
    """Ein Feld für eine ganze Zahl zwischen minimum und maximum."""

    def __init__(self, name, minimum=0, maximum=100):
        """Merkt sich Name und Bereich."""
        super().__init__(name)
        self.minimum = minimum
        self.maximum = maximum

    def pruefe(self, text):
        """Meldet einen Text, der keine ganze Zahl im Bereich ist."""
        if not text.strip().lstrip("-").isdigit():
            return f"{self.name}: keine ganze Zahl"
        if int(text) < self.minimum:
            return f"{self.name}: mindestens {self.minimum}"
        if int(text) > self.maximum:
            return f"{self.name}: höchstens {self.maximum}"
        return None


feld = erzeuge({"typ": "zahl", "name": "alter", "maximum": 150})
print(sorted(Feld.typen), Zahlfeld.typ)
print(type(feld).__name__, feld.name, feld.maximum, feld.pruefe("200"), feld.pruefe("36"))
