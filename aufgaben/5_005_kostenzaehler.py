"""Aufgabe 5_005 – Kostenzähler                                    Stufe 5 ★★★★★

Cloud-Anbieter rechnen viele Dienste nach Nutzung ab: Jeder Aufruf einer
Schnittstelle, etwa das Hochladen einer Datei, kostet einen kleinen
Betrag. Bevor eine Anwendung in Betrieb geht, will die IT-Abteilung
abschätzen, was sie im Monat kosten wird. Dazu soll ein Testlauf
mitzählen, welche kostenpflichtigen Aufrufe er macht, ohne dass man den
Code der Anwendung oder den Client des Anbieters ändern muss.

Das Mittel dafür ist ein Proxy, ein Stellvertreter-Objekt: Es sieht für
die Anwendung aus wie der echte Client, reicht alles an ihn weiter und
zählt dabei mit. Vervollständigen Sie die Klasse `Kostenzaehler`:

- `__init__(self, ziel, preise)` speichert das echte Objekt als
  Attribut `ziel` und das Dictionary preise (Methodenname → Preis pro
  Aufruf in Cent) als `preise`, setzt `kosten` auf 0 und `aufrufe`
  (Methodenname → Zahl der Aufrufe) auf ein leeres Dictionary.
- Jedes andere Attribut wird bei ziel nachgeschlagen und unverändert
  zurückgegeben, auch Methoden, die nichts kosten, und Datenattribute.
  Fehlt es auch dort, kommt wie gewohnt ein AttributeError.
- Steht der Name in preise, bekommt man stattdessen eine Funktion, die
  die Methode von ziel mit denselben Argumenten aufruft und deren
  Ergebnis zurückgibt; vorher addiert sie den Preis zu kosten und zählt
  den Aufruf in aufrufe. Auch ein Aufruf, der mit einer Ausnahme endet,
  wird berechnet und gezählt (der Anbieter berechnet ihn auch); die
  Ausnahme kommt unverändert beim Aufrufer an.
- Ein Kostenzaehler, dessen __init__ nicht gelaufen ist, muss bei jedem
  unbekannten Attribut einen AttributeError auslösen. So legen copy.copy
  und pickle Objekte an; copy.copy(zaehler) muss darum funktionieren.

    dienst = Kostenzaehler(Speicherdienst("eu-central"), PREISE)
    dienst.hochladen("bericht.pdf", b"PDF-Daten")   →  9
    dienst.herunterladen("bericht.pdf")             →  b"PDF-Daten"
    dienst.auflisten()                              →  ["bericht.pdf"]
    dienst.region                                   →  "eu-central"
    dienst.kosten                                   →  7
    dienst.aufrufe                                  →  {"hochladen": 1, "herunterladen": 1}
    dienst.loeschen                                 →  AttributeError

Grenzen: preise hat 0 bis 100 Einträge; die Namen sind Methoden von
ziel, die Preise ganze Zahlen von 0 bis 10**4. ziel ist ein beliebiges
Objekt ohne Attribute namens ziel, preise, kosten oder aufrufe. Die
Methoden von ziel können beliebige Positions- und Schlüsselwortargumente
haben und Ausnahmen auslösen. Ein Testlauf macht bis zu 100 000 Aufrufe.

Hintergrund: Bei obj.name sucht Python das Attribut über die Methode
type(obj).__getattribute__. Die Standardfassung von object schaut der
Reihe nach bei den Daten-Deskriptoren der Klasse (Aufgabe 5_001), im
__dict__ des Objekts und dann in der Klasse und ihren Basisklassen nach.
Findet sie nichts, löst sie einen AttributeError aus. Genau dann, und nur
dann, ruft Python noch __getattr__(self, name) auf, wenn die Klasse eine
solche Methode hat:

    class Standardwerte:
        def __init__(self):
            self.farbe = "blau"

        def __getattr__(self, name):
            return f"<{name} nicht gesetzt>"

    s = Standardwerte()
    s.farbe     →  "blau"                 normal gefunden, __getattr__ läuft nicht
    s.groesse   →  "<groesse nicht gesetzt>"

__getattr__ ist damit der Haken für alles, was fehlt; ideal für einen
Proxy, der seine eigenen Attribute ganz normal hat und alles Übrige
weiterreicht: return getattr(self.ziel, name). Soll es ein Attribut
wirklich nicht geben, löst __getattr__ selbst einen AttributeError aus.
Das ist wichtig, weil hasattr, getattr(obj, name, standard) und viele
Bibliotheken genau auf diesen Fehler achten.

Ganz anders __getattribute__(self, name): Wer es überschreibt, wird bei
jedem Attributzugriff gefragt, auch bei self.ziel und bei Methoden der
eigenen Klasse. Im Inneren darf man dann nicht self.irgendwas schreiben,
sonst ruft es sich endlos selbst auf; die eigenen Attribute holt man mit
object.__getattribute__(self, "ziel"). Das braucht man nur, wenn wirklich
jeder Zugriff abgefangen werden soll, etwa zum Protokollieren.

Auch __getattr__ hat eine Falle. copy.copy und pickle erzeugen das neue
Objekt mit cls.__new__(cls), ohne __init__, und fragen dann mit hasattr
nach Methoden wie __setstate__. Im neuen Objekt fehlt aber ziel, also
landet self.ziel in __getattr__, das wieder self.ziel braucht, und so
weiter bis zum RecursionError, den hasattr nicht abfängt. Abhilfe: das
eigene Attribut ohne Umweg lesen, etwa mit self.__dict__.get("ziel") oder
object.__getattribute__(self, "ziel"), und einen AttributeError auslösen,
wenn es fehlt.

Ein Ergebnis, das sich wie eine Methode aufrufen lässt, baut man mit einer
inneren Funktion, die sich die äußeren Variablen merkt (ein Closure):

    def mit_gruss(funktion):
        def aufruf(*args, **kwargs):
            print("Hallo!")
            return funktion(*args, **kwargs)
        return aufruf
"""


class Speicherdienst:
    """Nachbildung eines Cloud-Speichers mit derselben Schnittstelle wie der Client des Anbieters."""

    def __init__(self, region):
        self.region = region
        self._dateien = {}

    def hochladen(self, name, daten):
        """Speichert daten unter name und gibt die Zahl der Bytes zurück."""
        self._dateien[name] = daten
        return len(daten)

    def herunterladen(self, name):
        """Gibt die unter name gespeicherten Daten zurück; KeyError, wenn es name nicht gibt."""
        return self._dateien[name]

    def auflisten(self):
        """Gibt die Namen aller gespeicherten Dateien alphabetisch zurück."""
        return sorted(self._dateien)


# Preis pro Aufruf in Cent; auflisten kostet nichts
PREISE = {"hochladen": 5, "herunterladen": 2}


class Kostenzaehler:
    """Proxy, der alle Zugriffe an ziel weiterreicht und die Kosten der Aufrufe aus preise mitzählt."""

    def __init__(self, ziel, preise):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __getattr__(self, name):
        """Wird nur für Attribute aufgerufen, die der Kostenzaehler selbst nicht hat."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


dienst = Kostenzaehler(Speicherdienst("eu-central"), PREISE)
print(dienst.hochladen("bericht.pdf", b"PDF-Daten"))
print(dienst.herunterladen("bericht.pdf"))
print(dienst.auflisten(), dienst.region)
print(dienst.kosten, dienst.aufrufe)
