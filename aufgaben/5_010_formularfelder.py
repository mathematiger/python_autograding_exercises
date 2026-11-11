"""Aufgabe 5_010 – Formularfelder                                Stufe 5 ★★★★★

Ein Team baut einen Formulargenerator für interne Webanwendungen: Statt
jede Eingabemaske von Hand zu programmieren, beschreibt man ein
Formular als Liste von Feldern, etwa [("name", "text"), ("alter",
"zahl"), ("kontakt", "email")]. Das zweite Element jedes Paars ist das
Kürzel eines Feldtyps. Zu jedem Kürzel gehört eine Klasse, die weiß, wie
das Feld beschriftet ist und wie eine Eingabe geprüft wird. Neue
Feldtypen sollen andere Teams später einfach als Unterklasse von `Feld`
schreiben können, ohne eine zentrale Liste anzupassen:

    class Datumsfeld(Feld, kuerzel="datum"):
        beschriftung = "Datum"

        def pruefe(self, text):
            ...

Schon das Schreiben dieser Klasse soll den Typ unter "datum"
registrieren. Fehler im Feldtyp sollen sofort beim Definieren der Klasse
auffallen, nicht erst, wenn ein Formular ihn benutzt. Vervollständigen
Sie `Feld`:

- `__init_subclass__(cls, kuerzel=None, **kwargs)` läuft für jede neue
  Unterklasse. Es ruft zuerst super().__init_subclass__(**kwargs) auf,
  damit auch andere Basisklassen ihren Teil erledigen. Ist kuerzel
  None, ist die Klasse nur eine Zwischenstufe: nichts weiter tun.
  Sonst prüft es, in dieser Reihenfolge:
  1. Die Klasse hat ein Attribut beschriftung, das ein nicht leerer Text
     ist (es darf auch geerbt sein). Sonst TypeError mit dem
     Klassennamen in der Meldung.
  2. Die Klasse hat eine eigene oder geerbte Methode pruefe, die nicht
     die von Feld ist. Sonst TypeError mit dem Klassennamen.
  3. Das Kürzel ist noch nicht vergeben. Sonst ValueError mit dem
     Kürzel in der Meldung.
  Erst wenn alles stimmt, setzt es cls.kuerzel = kuerzel und trägt die
  Klasse in das Dictionary Feld.typen ein. Scheitert eine Prüfung, wird
  nichts eingetragen.
- `Feld.erzeuge(kuerzel)` (eine classmethod) gibt ein neues Objekt der
  Klasse zum Kürzel zurück, bei einem unbekannten Kürzel einen
  ValueError mit dem Kürzel in der Meldung.

Schreiben Sie außerdem `pruefe_formular(felder, eingaben)`: felder ist
eine Liste von Paaren (name, kuerzel), eingaben ein Dictionary von
Feldnamen auf eingegebene Texte; ein fehlender Eintrag zählt als "".
Die Funktion erzeugt für jedes Feld mit Feld.erzeuge ein Objekt und gibt
die Liste der Paare (name, meldung) für alle Felder zurück, deren pruefe
nicht None liefert, in der Reihenfolge von felder. Die Feldtypen
Textfeld, Zahlfeld und Emailfeld sind schon vorgegeben.

    Feld.typen                            →  {"text": Textfeld, "zahl": Zahlfeld, "email": Emailfeld}
    Feld.erzeuge("zahl").beschriftung     →  "Zahl"
    pruefe_formular([("name", "text"), ("alter", "zahl"), ("kontakt", "email")],
                    {"name": "Ada", "alter": "zwölf"})
        →  [("alter", "Bitte geben Sie eine ganze Zahl ein."),
            ("kontakt", "Bitte füllen Sie dieses Feld aus.")]
    class Ohne(Feld, kuerzel="ohne"): pass             →  TypeError
    class Doppelt(Textfeld, kuerzel="text"): pass      →  ValueError

Grenzen: kuerzel ist None oder ein nicht leerer Text aus höchstens 20
Kleinbuchstaben. beschriftung kann fehlen oder ein beliebiger Wert sein
(Text, Zahl, None). felder hat 0 bis 1000 Einträge mit verschiedenen
Namen; Namen und eingegebene Texte haben höchstens 100 Zeichen. Ein
Kürzel in felder kann auch unbekannt sein; dann kommt der ValueError
aus Feld.erzeuge bei pruefe_formular an.

Hintergrund: Eine class-Anweisung ist in Python ein ausgeführter Befehl.
Python führt den Klassenkörper aus, sammelt die dort entstandenen Namen
und baut daraus das Klassenobjekt. Ganz am Ende ruft es auf der
Basisklasse die Methode __init_subclass__ auf und übergibt die neue
Klasse. Damit kann eine Basisklasse auf jede ihrer Unterklassen
reagieren, auch auf solche, die erst viel später in einem anderen Modul
geschrieben werden. __init_subclass__ ist automatisch eine classmethod;
cls ist die neue Unterklasse, nicht die Basisklasse.

    class Plugin:
        alle = []

        def __init_subclass__(cls, **kwargs):
            super().__init_subclass__(**kwargs)
            Plugin.alle.append(cls.__name__)

    class Export(Plugin):
        pass

    Plugin.alle   →  ["Export"]

Schlüsselwörter in der Klammer der class-Zeile, außer metaclass, landen
als Argumente bei __init_subclass__: class Export(Plugin, format="csv")
ruft Plugin.__init_subclass__ mit format="csv" auf. Weil der Körper
schon gelaufen ist, kann die Methode auch die Attribute der neuen Klasse
prüfen, etwa mit getattr(cls, "beschriftung", None). Ob eine Methode
überschrieben wurde, verrät ein Vergleich der Funktionsobjekte:
cls.pruefe is Feld.pruefe ist genau dann True, wenn weder die Klasse
noch eine Zwischenklasse pruefe neu definiert. Löst __init_subclass__
eine Ausnahme aus, scheitert die class-Anweisung, und der Name der
Klasse wird gar nicht erst angelegt.

Der Aufruf super().__init_subclass__(**kwargs) reicht die übrigen
Schlüsselwörter an die Klasse weiter, die in der MRO der neuen Klasse
nach Feld kommt (Aufgabe 4_010). Ganz am Ende steht
object.__init_subclass__, das keine Schlüsselwörter annimmt; ein
Tippfehler wie kuerzl="x" fällt so als TypeError auf. Lässt man den
Aufruf weg, bekommen weitere Basisklassen (etwa ein Mixin, das ebenfalls
__init_subclass__ hat) die neue Klasse nie zu sehen.

Vor Python 3.6 brauchte man für solche Registrierungen eine eigene
Metaklasse (sie kommt in Aufgabe 5_013). __init_subclass__ deckt die
häufigsten Fälle ab, ist einfacher zu lesen und verträgt sich mit
anderen Basisklassen, während zwei Klassen mit verschiedenen
Metaklassen oft gar nicht zusammen vererbt werden können.
"""


class Feld:
    """Basisklasse aller Feldtypen; registriert jede Unterklasse mit Kürzel in Feld.typen."""

    typen = {}

    def __init_subclass__(cls, kuerzel=None, **kwargs):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    @classmethod
    def erzeuge(cls, kuerzel):
        """Gibt ein neues Objekt des Feldtyps mit diesem Kürzel zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def pruefe(self, text):
        """Gibt None zurück, wenn text gültig ist, sonst eine Meldung; jeder Feldtyp definiert das selbst."""
        raise NotImplementedError


class Textfeld(Feld, kuerzel="text"):
    """Ein Pflichtfeld für beliebigen Text."""

    beschriftung = "Text"

    def pruefe(self, text):
        """Verlangt mindestens ein Zeichen außer Leerzeichen."""
        if text.strip() == "":
            return "Bitte füllen Sie dieses Feld aus."
        return None


class Zahlfeld(Feld, kuerzel="zahl"):
    """Ein Feld für eine ganze Zahl ohne Vorzeichen."""

    beschriftung = "Zahl"

    def pruefe(self, text):
        """Verlangt nur Ziffern (Leerzeichen am Rand sind erlaubt)."""
        if not text.strip().isdecimal():
            return "Bitte geben Sie eine ganze Zahl ein."
        return None


class Emailfeld(Textfeld, kuerzel="email"):
    """Ein Pflichtfeld für eine E-Mail-Adresse."""

    beschriftung = "E-Mail"

    def pruefe(self, text):
        """Verlangt einen Text mit genau einem @, vor und hinter dem etwas steht."""
        meldung = super().pruefe(text)
        if meldung is not None:
            return meldung
        vorne, _, hinten = text.strip().partition("@")
        if vorne == "" or hinten == "" or "@" in hinten:
            return "Bitte geben Sie eine gültige E-Mail-Adresse an."
        return None


def pruefe_formular(felder, eingaben):
    """Gibt (name, meldung) für jedes Feld zurück, dessen Eingabe nicht gültig ist."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(sorted(Feld.typen))
print(Feld.erzeuge("zahl").beschriftung)
print(pruefe_formular([("name", "text"), ("alter", "zahl"), ("kontakt", "email")], {"name": "Ada", "alter": "zwölf"}))
