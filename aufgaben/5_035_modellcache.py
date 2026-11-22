"""Aufgabe 5_035 – Modellcache                                   Stufe 5 ★★★★★

Ein Werk sagt für jede seiner Maschinen mit einem eigenen trainierten
Modell voraus, ob sie bald gewartet werden muss. Ein Prognosedienst
nimmt Anfragen an („Presse 3 mit diesen Messwerten?“), lädt das
passende Modell und gibt die Vorhersage zurück. Ein Modell zu laden
dauert lange und kostet viel Speicher. Laufen mehrere Anfragen für
dieselbe Maschine zugleich, sollen sie sich ein geladenes Modell
teilen; benutzt aber niemand ein Modell mehr, soll es aus dem Speicher
verschwinden. Ein gewöhnliches Dictionary als Cache würde jedes Modell
für immer festhalten.

Die Klasse Modell und eine Ladefunktion sind vorgegeben (siehe unten).
Schreiben Sie die Klasse `Modellcache(lader, behalten=0)`; lader ist
eine Funktion, die zu einem Namen ein neues Modell lädt.

- `hole(name)` gibt das Modell zurück. Ist eins mit diesem Namen noch
  im Speicher, weil irgendwer es benutzt, dasselbe Objekt, sonst ein
  neu mit lader geladenes. Der Cache selbst hält Modelle nur mit
  schwachen Referenzen (weakref.WeakValueDictionary).
- Damit häufig gebrauchte Modelle nicht nach jeder Anfrage verfallen,
  hält der Cache die behalten zuletzt mit hole geholten Modelle
  zusätzlich stark fest (jedes nur einmal; ein erneut geholtes rückt
  nach hinten, das am längsten nicht geholte fällt heraus).
- `geladen()` gibt die sortierte Liste der Namen der Modelle zurück, die
  gerade im Cache sind.
- Das Attribut `freigegeben` ist eine Liste, an die der Cache den Namen
  jedes von ihm geladenen Modells hängt, sobald das Modell aus dem
  Speicher verschwindet (weakref.finalize).
- `vorhersage(name, messwerte)` holt das Modell mit hole und gibt
  modell.vorhersage(messwerte) zurück.

    cache = Modellcache(lade)
    presse = cache.hole("presse")          # lädt das Modell
    cache.hole("presse") is presse         →  True (nicht neu geladen)
    cache.geladen()                        →  ["presse"]
    del presse
    cache.geladen(), cache.freigegeben     →  ([], ["presse"])
    cache.vorhersage("fraese", [2, 1])     →  True (lädt fraese und gibt es gleich wieder frei)

    warm = Modellcache(lade, behalten=1)
    warm.vorhersage("presse", [2, 2])      →  True (lädt presse)
    warm.vorhersage("presse", [0, 0])      →  False (ohne neu zu laden)

Grenzen: 0 ≤ behalten ≤ 100, bis zu 10 000 Aufrufe von hole, bis zu
1000 verschiedene Namen. lader liefert jedes Mal ein neues Modell.

Hintergrund: Python gibt ein Objekt frei, sobald keine Referenz mehr
darauf zeigt: keine Variable, kein Eintrag einer Liste, kein Attribut.
Ein Cache in einem Dictionary ist selbst so eine Referenz und hält
seine Werte darum für immer am Leben. Eine schwache Referenz zeigt auf
ein Objekt, ohne es festzuhalten:

    import weakref

    class Bericht:
        pass

    b = Bericht()
    r = weakref.ref(b)
    r() is b          →  True      # Aufruf liefert das Objekt …
    del b
    r()               →  None      # … oder None, wenn es weg ist

weakref.WeakValueDictionary() verhält sich wie ein Dictionary, dessen
Werte nur schwach gehalten werden: Verschwindet ein Wert, verschwindet
sein Eintrag von selbst. Lesen geht mit get(schluessel) (None, wenn der
Eintrag fehlt), Schreiben mit d[schluessel] = objekt. Weil Einträge
jederzeit verschwinden können, fragt man nicht erst mit in und liest
danach, sondern liest einmal mit get und prüft das Ergebnis auf None;
dabei hält die Variable das Objekt fest. Werte müssen schwache
Referenzen erlauben: Objekte eigener Klassen können das, int, str,
list und dict nicht (TypeError), und eine Klasse mit __slots__
(Aufgabe 5_004) nur, wenn "__weakref__" in den slots steht.

weakref.finalize(objekt, funktion, *argumente) ruft funktion(*argumente)
auf, sobald objekt freigegeben wird, höchstens einmal. Die Argumente
hält finalize stark fest; darum darf objekt selbst nicht darunter sein,
sonst wird es nie freigegeben:

    weakref.finalize(b, protokoll.append, "Bericht weg")   # richtig
    weakref.finalize(b, protokoll.append, b)               # hält b für immer fest

CPython gibt ein Objekt sofort frei, wenn die letzte Referenz
verschwindet. Nur Objekte, die sich im Kreis gegenseitig referenzieren,
räumt erst der Garbage Collector auf; die Tests rufen darum vor jeder
Prüfung gc.collect() auf.
"""

import weakref


class Modell:
    """Ein trainiertes Modell: eine lineare Regel mit Gewichten und einer Schwelle."""

    def __init__(self, name, gewichte, schwelle):
        """Legt das Modell an."""
        self.name = name
        self.gewichte = gewichte
        self.schwelle = schwelle

    def vorhersage(self, messwerte):
        """True, wenn die gewichtete Summe der Messwerte die Schwelle erreicht (Wartung nötig)."""
        summe = 0
        for gewicht, wert in zip(self.gewichte, messwerte):
            summe += gewicht * wert
        return summe >= self.schwelle


class Modellcache:
    """Teilt geladene Modelle, ohne sie über ihre Benutzung hinaus festzuhalten."""

    def __init__(self, lader, behalten=0):
        """Merkt sich die Ladefunktion und wie viele zuletzt geholte Modelle stark gehalten werden."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def hole(self, name):
        """Gibt das Modell mit diesem Namen zurück, aus dem Cache oder neu geladen."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def _merke(self, modell):
        """Hält modell als zuletzt geholtes stark fest und lässt das älteste über behalten los."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def geladen(self):
        """Gibt die sortierten Namen der Modelle zurück, die gerade im Cache sind."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def vorhersage(self, name, messwerte):
        """Holt das Modell und gibt seine Vorhersage für die Messwerte zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


MODELLE = {"presse": ([0.5, 1.0], 3.0), "fraese": ([2.0, -1.0], 1.0)}


def lade(name):
    """Lädt ein Modell (hier nur aus MODELLE) und meldet das."""
    print(f"lade {name}")
    gewichte, schwelle = MODELLE[name]
    return Modell(name, gewichte, schwelle)


cache = Modellcache(lade)
presse = cache.hole("presse")
print(cache.hole("presse") is presse)
print(cache.geladen())
del presse
print(cache.geladen(), cache.freigegeben)
print(cache.vorhersage("fraese", [2, 1]))
print(cache.freigegeben)

warm = Modellcache(lade, behalten=1)
print(warm.vorhersage("presse", [2, 2]))
print(warm.vorhersage("presse", [0, 0]))
