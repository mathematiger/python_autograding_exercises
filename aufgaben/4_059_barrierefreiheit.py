"""Aufgabe 4_059 – Barrierefreiheit                              Stufe 4 ★★★★☆

Eine Stadtverwaltung lässt ihr Bürgerportal jede Nacht automatisch auf
Barrierefreiheit prüfen: Kann man es auch mit einem Bildschirmleser,
nur mit der Tastatur oder bei schwachem Sehvermögen benutzen? Das
Prüfwerkzeug geht alle Seiten durch und meldet jeden Verstoß als Paar
(Seite, Regel), etwa ("/antrag", "label") für ein Eingabefeld ohne
Beschriftung oder ("/start", "alt-text") für ein Bild ohne
Alternativtext, den ein Bildschirmleser vorlesen könnte:

    befunde = [("/start", "alt-text"), ("/antrag", "label"), ("/antrag", "kontrast"),
               ("/termine", "label"), ("/start", "kontrast"), ("/antrag", "label")]

Das Team will wissen, welche Regeln am häufigsten verletzt werden und
ob die Umbauten etwas gebracht haben. Schreiben Sie mit
collections.Counter vier Funktionen:

- `je_regel(befunde)` gibt einen Counter Regel → Anzahl der Verstöße
  zurück.
- `dringendste(befunde, n)` gibt die n Regeln mit den meisten Verstößen
  als Liste von Paaren (Regel, Anzahl) zurück, die häufigste zuerst. Bei
  gleicher Anzahl kommt die Regel zuerst, die früher in befunde
  auftaucht. Gibt es weniger als n Regeln, kommen alle.
- `veraenderung(vorher, nachher)` bekommt zwei Counter Regel → Anzahl
  und gibt ein Paar von Countern (besser, schlechter) zurück: besser
  enthält für jede Regel, die nachher seltener verletzt wird, um wie
  viel; schlechter für jede, die häufiger verletzt wird, um wie viel.
  Regeln ohne Veränderung kommen in keinem der beiden vor.
- `gesamt(zaehlungen)` bekommt eine Liste von Countern (einen je
  Teilportal) und gibt einen Counter mit den Summen zurück.

    je_regel(befunde)        →  Counter({"label": 3, "kontrast": 2, "alt-text": 1})
    dringendste(befunde, 2)  →  [("label", 3), ("kontrast", 2)]
    veraenderung(Counter({"label": 3, "kontrast": 2}), Counter({"label": 1, "kontrast": 2, "alt-text": 4}))
                             →  (Counter({"label": 2}), Counter({"alt-text": 4}))
    gesamt([Counter({"label": 2}), Counter({"label": 1, "kontrast": 5})])
                             →  Counter({"kontrast": 5, "label": 3})

Die übergebenen Counter bleiben unverändert.

Grenzen: befunde hat 0 bis 100 000 Paare aus nicht leeren Texten,
0 ≤ n ≤ 100. Die Counter in vorher, nachher und zaehlungen enthalten
nur Anzahlen von 1 bis 100 000; zaehlungen hat 0 bis 1000 Einträge.

Hintergrund: In Aufgabe 2_025 haben Sie Häufigkeiten von Hand in einem
Dictionary gezählt. collections.Counter ist ein Dictionary, das genau
dafür gebaut ist. Man gibt ihm etwas Iterierbares, und es zählt, wie oft
jedes Element vorkommt; ein Schlüssel, den es nicht gibt, hat die Anzahl
0 statt eines KeyError:

    from collections import Counter

    farben = Counter(["rot", "blau", "rot", "grün", "rot", "blau"])
    farben["rot"]              →  3
    farben["gelb"]             →  0     (kein KeyError, kein neuer Eintrag)
    farben.update(["gelb"])    # zählt weiter
    farben.most_common(2)      →  [("rot", 3), ("blau", 2)]
    farben.total()             →  7

most_common(n) liefert die n häufigsten Elemente als Paare (Element,
Anzahl), ohne n alle; bei gleicher Anzahl bleibt die Reihenfolge, in der
die Elemente zum ersten Mal gezählt wurden. Counter kann man rechnen wie
Mengen mit Vielfachheit:

    a = Counter(rot=3, blau=1)
    b = Counter(rot=1, blau=4)
    a + b    →  Counter({"blau": 5, "rot": 4})     Summe
    a - b    →  Counter({"rot": 2})                nur was positiv bleibt
    a & b    →  Counter({"rot": 1, "blau": 1})     Minimum je Element
    a | b    →  Counter({"blau": 4, "rot": 3})     Maximum je Element

Alle vier geben einen neuen Counter zurück und lassen a und b
unverändert. a.subtract(b) dagegen ändert a selbst und behält auch
negative Anzahlen. Die Summe einer Liste von Countern geht mit sum und
einem leeren Counter als Startwert: sum(liste, Counter()); ohne
Startwert beginnt sum bei der Zahl 0, und 0 + Counter() ist ein
TypeError.
"""

from collections import Counter


def je_regel(befunde):
    """Gibt einen Counter Regel → Anzahl der Verstöße zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def dringendste(befunde, n):
    """Gibt die n meistverletzten Regeln als Paare (Regel, Anzahl) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def veraenderung(vorher, nachher):
    """Gibt (besser, schlechter) als zwei Counter mit den positiven Differenzen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def gesamt(zaehlungen):
    """Gibt die Summe aller Counter der Liste zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


befunde = [
    ("/start", "alt-text"),
    ("/antrag", "label"),
    ("/antrag", "kontrast"),
    ("/termine", "label"),
    ("/start", "kontrast"),
    ("/antrag", "label"),
]
print(je_regel(befunde))
print(dringendste(befunde, 2))
print(veraenderung(Counter({"label": 3, "kontrast": 2}), Counter({"label": 1, "kontrast": 2, "alt-text": 4})))
print(gesamt([Counter({"label": 2}), Counter({"label": 1, "kontrast": 5})]))
