# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_071_serientickets.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_071_serientickets

"""Aufgabe 3_071 – Serientickets                                 Stufe 3 ★★★☆☆

Das Ticketsystem eines Service-Desks legt wiederkehrende Aufgaben
selbst an: Alle 12 Tage entsteht ein Ticket „Tonerstand der Drucker
prüfen“, alle 18 Tage „Freien Speicher der Dateiserver prüfen“, alle 30
Tage „Lizenzbericht erstellen“. Heute (Tag 0) wurden alle drei zugleich
angelegt. Die Teamleitung will wissen, an welchem Tag zum ersten Mal
wieder alle Serientickets zugleich anfallen, denn an diesem Tag braucht
sie mehr Leute. Außerdem will sie selbst in einem festen Rhythmus von d
Tagen auf die Serientickets schauen, und zwar so selten wie möglich,
aber an jedem Tag, an dem eines anfällt. Schreiben Sie vier Funktionen:

- `ggt(a, b)` gibt den größten gemeinsamen Teiler von a und b zurück,
  mit dem euklidischen Algorithmus (siehe Hintergrund).
- `kgv(a, b)` gibt das kleinste gemeinsame Vielfache von a und b zurück.
- `gemeinsam_faellig(intervalle)` gibt den ersten Tag nach Tag 0 zurück,
  an dem alle Serientickets zugleich anfallen, also das kgV aller
  Intervalle.
- `pruefrhythmus(intervalle)` gibt den größten Rhythmus d zurück, bei dem
  die Teamleitung an jedem Tag eines Serientickets nachschaut: d muss
  jedes Intervall teilen, also der ggT aller Intervalle.

    ggt(12, 18)                          →  6
    kgv(12, 18)                          →  36
    gemeinsam_faellig([12, 18, 30])      →  180
    pruefrhythmus([12, 18, 30])          →  6

Verwenden Sie dafür nicht math.gcd oder math.lcm, sondern schreiben Sie
den Algorithmus selbst.

Grenzen: Für ggt gilt 0 ≤ a, b ≤ 10**18, nicht beide 0; für kgv
1 ≤ a, b ≤ 10**18. intervalle hat 1 bis 1000 Einträge, ganze Zahlen von
1 bis 10**6, Doppelte möglich. ggt soll O(log(min(a, b))) Schritte
brauchen, also auch für Zahlen mit 18 Stellen nur etwa hundert.

Hintergrund: Der größte gemeinsame Teiler (ggT) zweier Zahlen ist die
größte Zahl, die beide ohne Rest teilt: ggT(12, 18) = 6. Man könnte alle
Zahlen von min(a, b) abwärts durchprobieren, aber bei 18-stelligen
Zahlen wären das bis zu 10**18 Versuche. Euklid hat um 300 v. Chr. einen
viel schnelleren Weg beschrieben. Er beruht auf einer Beobachtung: Jede
Zahl, die a und b teilt, teilt auch den Rest a % b (Aufgabe 1_005 zu %),
denn a % b ist a minus ein Vielfaches von b. Also gilt

    ggT(a, b) = ggT(b, a % b)       und      ggT(a, 0) = a,

und die Zahlen werden dabei schnell kleiner:

    ggT(30, 12) = ggT(12, 6) = ggT(6, 0) = 6

Spätestens nach zwei Schritten ist die größere Zahl halbiert; deshalb
braucht der euklidische Algorithmus nur O(log n) Schritte. Man kann
ihn mit einer while-Schleife schreiben, die (a, b) durch (b, a % b)
ersetzt, bis b 0 ist, oder rekursiv mit dem Rekursionsanfang b == 0
(Aufgabe 3_034). Ist a kleiner als b, tauscht der erste Schritt die
beiden von selbst: 12 % 30 ist 12.

Das kleinste gemeinsame Vielfache (kgV) bekommt man über den ggT:
a · b ist ein gemeinsames Vielfaches, aber darin steckt der gemeinsame
Teil doppelt. Also kgV(a, b) = a · b // ggT(a, b), mit // statt /, damit
eine ganze Zahl herauskommt und bei großen Zahlen nichts gerundet wird
(Aufgabe 2_043 zu float). Für mehrere Zahlen nimmt man sie nacheinander
dazu: kgV(12, 18, 30) = kgV(kgV(12, 18), 30) = kgV(36, 30) = 180, und
genauso beim ggT.
"""


def ggt(a, b):
    """Gibt den größten gemeinsamen Teiler von a und b zurück (euklidischer Algorithmus)."""
    while b != 0:
        a, b = b, a % b
    return a


def kgv(a, b):
    """Gibt das kleinste gemeinsame Vielfache von a und b zurück."""
    return a * b // ggt(a, b)


def gemeinsam_faellig(intervalle):
    """Gibt den ersten Tag nach Tag 0 zurück, an dem alle Intervalle zugleich fällig sind."""
    tag = 1
    for intervall in intervalle:
        tag = kgv(tag, intervall)
    return tag


def pruefrhythmus(intervalle):
    """Gibt den größten Rhythmus zurück, der jedes Intervall teilt."""
    rhythmus = 0
    for intervall in intervalle:
        rhythmus = ggt(rhythmus, intervall)
    return rhythmus


print(ggt(12, 18), kgv(12, 18))
print(gemeinsam_faellig([12, 18, 30]), pruefrhythmus([12, 18, 30]))


# Idee: ggt ersetzt in einer while-Schleife (a, b) durch (b, a % b), bis b 0 ist, und gibt a zurück.
# kgv rechnet a * b // ggt(a, b). Für die Listen beginnt man mit dem neutralen Wert (1 beim kgV,
# 0 beim ggT, denn kgV(1, x) = x und ggT(0, x) = x) und nimmt jedes Intervall dazu.
# Anderer Weg: ggt rekursiv: return a if b == 0 else ggt(b, a % b). Für die Listen geht auch
# functools.reduce(kgv, intervalle). Der naive Weg probiert alle Teiler von min(a, b) abwärts (O(n))
# oder zieht wie Euklid ursprünglich immer die kleinere von der größeren Zahl ab, was bei ggt(10**18, 1)
# 10**18 Schritte braucht.
# Typische Fehler: a * b / ggt(a, b) mit / (ein float, bei großen Zahlen gerundet), die Liste mit 0
# statt 1 beim kgV beginnen (dann bleibt alles 0), den ggT mit 1 statt 0 beginnen (dann kommt immer 1
# heraus; mit dem ersten Intervall zu beginnen ist dagegen richtig); ggt(a, 0) nicht abfangen, wenn man mit b % a rechnet.
# Laufzeit: ggt braucht O(log min(a, b)) Schritte, weil der Rest nach zwei Schritten höchstens halb so
# groß ist; die Listenfunktionen brauchen O(n log m) für n Intervalle bis m, dazu die Multiplikation
# großer Zahlen beim kgV.
