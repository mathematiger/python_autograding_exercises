"""Aufgabe 4_028 – Tastenfeld                                    Stufe 4 ★★★★☆

Für das Bedienteil einer Zutrittskontrolle entsteht eine Oberfläche
mit einem Tastenfeld auf dem Touchscreen: zehn Zifferntasten, eine
Taste „C“ zum Löschen und eine Taste „←“, die das letzte Zeichen
entfernt. Wie in fast allen Oberflächen-Bibliotheken bekommt jede
Taste eine Rückruffunktion (Callback), die beim Antippen ohne
Argumente aufgerufen wird: taste() statt taste(anzeige, "7"). Die
eigentliche Arbeit erledigen die vorgegebenen Funktionen tippe,
loesche und zurueck, die aber Argumente brauchen. Außerdem gehört zur
Eingabemaske eine Prüfung der Feldlängen. Schreiben Sie mit
functools.partial zwei Funktionen:

- `baue_tastenfeld(anzeige)` gibt ein Dictionary zurück, das jeder
  Beschriftung "0" bis "9", "C" und "←" ein partial-Objekt ohne
  offene Parameter zuordnet: Die Ziffern rufen tippe(anzeige, ziffer)
  auf, "C" ruft loesche(anzeige) und "←" ruft zurueck(anzeige) auf.
- `pruefer_fuer(laengen)` bekommt ein Dictionary feldname →
  (minimum, maximum) und gibt ein Dictionary feldname → partial-Objekt
  zurück, das wie pruefe_laenge(text, minimum=…, maximum=…) mit den
  Grenzen des Felds arbeitet und nur noch den Text braucht.

    anzeige = []
    tasten = baue_tastenfeld(anzeige)
    tasten["4"](); tasten["2"](); tasten["7"](); tasten["←"](); tasten["9"]()
    "".join(anzeige)                         →  "429"
    pruefer = pruefer_fuer({"pin": (4, 6), "raum": (1, 3)})
    pruefer["pin"]("429")                    →  False   (zu kurz)
    pruefer["raum"]("B12")                   →  True

Grenzen: anzeige ist eine Liste mit 0 bis 6 Zeichen, die nur über die
Tasten verändert wird. laengen hat 0 bis 50 Einträge mit nicht leeren
Feldnamen, und es gilt 0 ≤ minimum ≤ maximum ≤ 1000. Die Texte für die
Prüfer haben 0 bis 1000 Zeichen.

Hintergrund: functools.partial(funktion, *args, **kwargs) baut aus
einer Funktion eine neue, bei der einige Argumente schon festgelegt
(vorbelegt) sind. Ruft man das Ergebnis auf, hängt partial die neuen
Argumente hinter die vorbelegten und ruft damit funktion auf:

    from functools import partial

    def potenz(basis, exponent):
        return basis ** exponent

    quadrat = partial(potenz, exponent=2)
    quadrat(7)                 →  49     (wie potenz(7, exponent=2))
    zweier = partial(potenz, 2)
    zweier(10)                 →  1024   (wie potenz(2, 10))
    quadrat.func, quadrat.keywords   →  potenz, {"exponent": 2}

Das Ergebnis ist ein partial-Objekt, keine mit def geschriebene
Funktion, aber man kann es aufrufen wie eine. Über die Attribute func,
args und keywords sieht man, was vorbelegt ist; das hilft beim
Debuggen.

Dasselbe ginge mit lambda: lambda: tippe(anzeige, "7"). In einer
Schleife steckt darin aber eine Falle: Ein lambda merkt sich nicht den
Wert einer Variablen, sondern die Variable selbst, und liest sie erst
beim Aufruf. Nach der Schleife hat sie ihren letzten Wert:

    tasten = {}
    for ziffer in "0123456789":
        tasten[ziffer] = lambda: tippe(anzeige, ziffer)
    tasten["4"]()              # tippt "9", den letzten Wert von ziffer

partial dagegen wertet seine Argumente sofort beim Bauen aus und
speichert die Werte; partial(tippe, anzeige, ziffer) behält die Ziffer
des jeweiligen Durchlaufs. Die Liste anzeige wird dabei nicht kopiert:
Alle Tasten verändern dieselbe Liste, und genau das ist hier gewollt.
"""

from functools import partial

STELLEN = 6


def tippe(anzeige, zeichen):
    """Hängt zeichen an die Anzeige an, solange sie weniger als STELLEN Zeichen hat."""
    if len(anzeige) < STELLEN:
        anzeige.append(zeichen)


def loesche(anzeige):
    """Leert die Anzeige."""
    anzeige.clear()


def zurueck(anzeige):
    """Entfernt das letzte Zeichen der Anzeige, falls es eines gibt."""
    if anzeige:
        anzeige.pop()


def pruefe_laenge(text, minimum, maximum):
    """Prüft, ob text mindestens minimum und höchstens maximum Zeichen hat."""
    return minimum <= len(text) <= maximum


def baue_tastenfeld(anzeige):
    """Gibt zu jeder Beschriftung eine Rückruffunktion ohne Argumente zurück, gebaut mit partial."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def pruefer_fuer(laengen):
    """Gibt zu jedem Feld eine Prüffunktion zurück, die nur noch den Text braucht."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


anzeige = []
tasten = baue_tastenfeld(anzeige)
for beschriftung in ["4", "2", "7", "←", "9"]:
    tasten[beschriftung]()
print("".join(anzeige))
pruefer = pruefer_fuer({"pin": (4, 6), "raum": (1, 3)})
print(pruefer["pin"]("429"), pruefer["raum"]("B12"))
