# Automatisch erzeugt aus lehrkraft/muster/5_010_formularfelder.py - nicht von Hand ändern.
# vorlage-hash: 3893baaaf948aaba
# text-hash: ec543f864af63113
# thema: klassen
# inhalt: `__init_subclass__`, Unterklassen registrieren

def ausnahme_bei(aktion):
    """Führt aktion() aus und gibt den Namen der ausgelösten Ausnahme zurück, sonst None."""
    try:
        aktion()
    except Exception as fehler:
        return type(fehler).__name__
    return None


# Textfeld und Zahlfeld haben sich angemeldet
ergebnis = dict(Feld.typen)
assert ergebnis == {"text": Textfeld, "zahl": Zahlfeld} and Textfeld.typ == "text" and Zahlfeld.typ == "zahl", (
    f"Feld.typen ist {ergebnis!r}, erwartet war {{'text': Textfeld, 'zahl': Zahlfeld}}, und Textfeld.typ und "
    "Zahlfeld.typ sollen 'text' und 'zahl' sein.\n"
    "Tipp: Tragen Sie in __init_subclass__ die Klasse cls unter typ ein und setzen Sie cls.typ = typ."
)

# Das Verzeichnis gehört zu Feld, nicht zu den Unterklassen
assert "typen" not in vars(Textfeld) and "typen" not in vars(Zahlfeld), (
    "Textfeld oder Zahlfeld haben ein eigenes Attribut typen; erwartet war, dass nur Feld.typen geändert wird.\n"
    "Tipp: Schreiben Sie Feld.typen[typ] = cls statt cls.typen = …."
)

# erzeuge aus dem Beispiel
feld = erzeuge({"typ": "zahl", "name": "alter", "maximum": 150})
ergebnis = (type(feld).__name__, feld.name, feld.minimum, feld.maximum, feld.pruefe("200"), feld.pruefe("36"))
erwartet = ("Zahlfeld", "alter", 0, 150, "alter: höchstens 150", None)
assert ergebnis == erwartet, (
    f"erzeuge({{'typ': 'zahl', 'name': 'alter', 'maximum': 150}}) ergibt ein Feld mit {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Alle Einträge außer typ werden Schlüsselwortargumente: Feld.typen[typ](**angaben)."
)

# erzeuge mit Standardwerten und für Text
feld = erzeuge({"name": "kommentar", "typ": "text"})
ergebnis = (type(feld).__name__, feld.name, feld.laenge, feld.pruefe("x" * 101), feld.pruefe(""))
erwartet = ("Textfeld", "kommentar", 100, "kommentar: höchstens 100 Zeichen", None)
assert ergebnis == erwartet, f"erzeuge({{'name': 'kommentar', 'typ': 'text'}}) ergibt ein Feld mit {ergebnis!r}, erwartet war {erwartet!r}."

# erzeuge ändert die Beschreibung nicht
beschreibung = {"typ": "text", "name": "ort", "laenge": 30}
erzeuge(beschreibung)
assert beschreibung == {"typ": "text", "name": "ort", "laenge": 30}, (
    f"Nach erzeuge(...) ist die Beschreibung {beschreibung!r}; sie soll unverändert bleiben.\n"
    "Tipp: Arbeiten Sie mit einer Kopie, dict(beschreibung), bevor Sie typ herausnehmen."
)

# Unbekannte Kürzel ergeben ValueError
art = ausnahme_bei(lambda: erzeuge({"typ": "datum", "name": "geburtstag"}))
assert art == "ValueError", f"erzeuge({{'typ': 'datum', 'name': 'geburtstag'}}) soll einen ValueError auslösen; ausgelöst wurde {art}."


# Eine neue Feldart meldet sich an, auch als Unterklasse einer Unterklasse
class Prozentfeld(Zahlfeld, typ="prozent_test"):
    """Ein Zahlfeld von 0 bis 100 mit eigener Kennung."""


feld = erzeuge({"typ": "prozent_test", "name": "rabatt"})
assert Feld.typen.get("prozent_test") is Prozentfeld and Prozentfeld.typ == "prozent_test" and Zahlfeld.typ == "zahl" and type(feld) is Prozentfeld, (
    f"Nach class Prozentfeld(Zahlfeld, typ='prozent_test') ist Feld.typen.get('prozent_test') {Feld.typen.get('prozent_test')!r}, "
    f"Prozentfeld.typ {getattr(Prozentfeld, 'typ', None)!r} und Zahlfeld.typ {getattr(Zahlfeld, 'typ', None)!r}; "
    "erwartet waren Prozentfeld, 'prozent_test' und weiterhin 'zahl'."
)


def lege_an(name, typ, mit_pruefe=True, **weitere):
    """Legt eine Unterklasse von Feld mit class an und gibt sie zurück."""
    if mit_pruefe:

        class Neu(Feld, typ=typ, **weitere):
            """Eine Testklasse mit pruefe."""

            def pruefe(self, text):
                """Alles ist in Ordnung."""
                return None

    else:

        class Neu(Feld, typ=typ, **weitere):
            """Eine Testklasse ohne pruefe."""

    Neu.__name__ = name
    return Neu


# Ein schon vergebenes Kürzel ergibt ValueError und ändert nichts
art = ausnahme_bei(lambda: lege_an("Doppelt", "text"))
assert art == "ValueError" and Feld.typen["text"] is Textfeld, (
    f"class Doppelt(Feld, typ='text') löst {art} aus, und Feld.typen['text'] ist danach {Feld.typen['text']!r}; "
    "erwartet waren ein ValueError und weiterhin Textfeld.\n"
    "Tipp: Prüfen Sie zuerst, ob typ schon in Feld.typen steht, und tragen Sie erst danach ein."
)

# Ohne Methode pruefe: TypeError, nichts eingetragen
art = ausnahme_bei(lambda: lege_an("OhnePruefe", "ohne_pruefe_test", mit_pruefe=False))
assert art == "TypeError" and "ohne_pruefe_test" not in Feld.typen, (
    f"Eine Unterklasse ohne Methode pruefe löst {art} aus, und 'ohne_pruefe_test' in Feld.typen ist "
    f"{'ohne_pruefe_test' in Feld.typen}; erwartet waren ein TypeError und kein Eintrag.\n"
    "Tipp: getattr(cls, 'pruefe', None) findet die Methode, auch wenn sie geerbt ist; callable(...) prüft, ob man sie aufrufen kann."
)

# Ein Attribut pruefe, das keine Methode ist, reicht nicht
art = ausnahme_bei(lambda: type("Kaputt", (Feld,), {"pruefe": "keine Methode"}, typ="kaputt_test"))
assert art == "TypeError" and "kaputt_test" not in Feld.typen, (
    f"Eine Unterklasse mit pruefe = 'keine Methode' löst {art} aus; erwartet war ein TypeError ohne Eintrag."
)

# Ohne Kürzel scheitert die class-Anweisung
def ohne_kuerzel():
    """Legt eine Unterklasse ohne typ an."""

    class OhneKuerzel(Feld):
        """Hat kein Kürzel."""

        def pruefe(self, text):
            """Alles ist in Ordnung."""
            return None


art = ausnahme_bei(ohne_kuerzel)
assert art == "TypeError", f"class OhneKuerzel(Feld) ohne typ soll einen TypeError auslösen; ausgelöst wurde {art}."

# Unbekannte Schlüsselwörter werden an super() weitergereicht und dort abgelehnt
art = ausnahme_bei(lambda: lege_an("MitFarbe", "farbe_test", farbe="rot"))
assert art == "TypeError" and "farbe_test" not in Feld.typen, (
    f"class MitFarbe(Feld, typ='farbe_test', farbe='rot') löst {art} aus, und 'farbe_test' in Feld.typen ist "
    f"{'farbe_test' in Feld.typen}; erwartet waren ein TypeError und kein Eintrag.\n"
    "Tipp: Rufen Sie zuerst super().__init_subclass__(**kwargs) auf; object lehnt unbekannte Schlüsselwörter ab."
)


class Kennzeichen:
    """Eine zweite Elternklasse, die ein eigenes Schlüsselwort verarbeitet."""

    def __init_subclass__(cls, kennzeichen="", **kwargs):
        """Merkt sich das Kennzeichen und reicht den Rest weiter."""
        super().__init_subclass__(**kwargs)
        cls.kennzeichen = kennzeichen


# Mehrfachvererbung: die zweite Elternklasse bekommt ihr Schlüsselwort
def mit_kennzeichen():
    """Legt eine Klasse mit Feld und Kennzeichen als Eltern an."""

    class Markiert(Feld, Kennzeichen, typ="markiert_test", kennzeichen="★"):
        """Ein Feld mit Kennzeichen."""

        def pruefe(self, text):
            """Alles ist in Ordnung."""
            return None

    return Markiert


try:
    klasse = mit_kennzeichen()
    ergebnis = (klasse.typ, klasse.kennzeichen, Feld.typen.get("markiert_test") is klasse)
except Exception as fehler:
    ergebnis = f"{type(fehler).__name__}: {fehler}"
assert ergebnis == ("markiert_test", "★", True), (
    f"class Markiert(Feld, Kennzeichen, typ='markiert_test', kennzeichen='★') ergibt {ergebnis!r}, "
    "erwartet war ('markiert_test', '★', True).\n"
    "Tipp: super().__init_subclass__(**kwargs) reicht kennzeichen an Kennzeichen weiter."
)

# 300 zufällige Beschreibungen
zufall = Zufall(5010)
for nummer in range(300):
    if zufall.random() < 0.5:
        beschreibung = {"typ": "text", "name": f"feld{nummer}"}
        if zufall.random() < 0.5:
            beschreibung["laenge"] = zufall.randint(0, 50)
        text = "x" * zufall.randint(0, 60)
        grenze = beschreibung.get("laenge", 100)
        erwartet = (Textfeld, f"feld{nummer}: höchstens {grenze} Zeichen" if len(text) > grenze else None)
    else:
        beschreibung = {"typ": "zahl", "name": f"feld{nummer}", "minimum": zufall.randint(-50, 50)}
        if zufall.random() < 0.5:
            beschreibung["maximum"] = zufall.randint(50, 200)
        zahl = zufall.randint(-100, 250)
        text = str(zahl)
        unten, oben = beschreibung["minimum"], beschreibung.get("maximum", 100)
        meldung = None
        if zahl < unten:
            meldung = f"feld{nummer}: mindestens {unten}"
        elif zahl > oben:
            meldung = f"feld{nummer}: höchstens {oben}"
        erwartet = (Zahlfeld, meldung)
    kopie = dict(beschreibung)
    feld = erzeuge(beschreibung)
    ergebnis = (type(feld), feld.pruefe(text))
    assert ergebnis == erwartet and beschreibung == kopie, (
        f"erzeuge({kopie}) und pruefe({text!r}) ergeben {ergebnis!r}, erwartet war {erwartet!r}."
    )

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "['text', 'zahl'] zahl\nZahlfeld alter 150 alter: höchstens 150 None"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
