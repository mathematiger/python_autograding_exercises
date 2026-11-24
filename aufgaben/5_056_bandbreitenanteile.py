"""Aufgabe 5_056 – Bandbreitenanteile                            Stufe 5 ★★★★★

Der Router am Internetanschluss einer Firma teilt die Bandbreite im
Engpass auf Verkehrsklassen auf, damit Telefonate nicht ruckeln, wenn
jemand ein großes Backup hochlädt (Quality of Service, QoS). Jede
Klasse bekommt ein ganzzahliges Gewicht; ihr Anteil an der Bandbreite
ist ihr Gewicht geteilt durch die Summe aller Gewichte. Das Team, das
die Router einrichtet, schreibt ein Werkzeug, das die Anteile anzeigt,
Anteile aus einem Planungsdokument in Gewichte zurückrechnet und die
Bandbreite in ganzen kbit/s verteilt. Damit die verteilten kbit/s immer
genau die Bandbreite ergeben, rechnet es exakt mit fractions.Fraction.
Schreiben Sie drei Funktionen:

- `anteile(gewichte)` bekommt ein Dictionary Klasse → Gewicht und gibt
  ein Dictionary Klasse → Anteil zurück, jeder Anteil ein gekürzter
  Bruch (Fraction), in derselben Reihenfolge der Klassen.
- `gewichte_aus(anteile)` macht es umgekehrt: Sie bekommt ein
  Dictionary Klasse → Fraction und gibt die kleinsten ganzen Gewichte
  (int) zurück, die genau dieselben Verhältnisse haben. Die Anteile
  müssen sich dabei nicht zu 1 addieren.
- `zuteilung(gewichte, bandbreite)` verteilt bandbreite kbit/s in
  ganzen kbit/s auf die Klassen und gibt ein Dictionary Klasse → int
  zurück. Jede Klasse bekommt zuerst ihren genauen Anteil abgerundet.
  Was dann noch fehlt, bekommen einzeln die Klassen mit dem größten
  Rest (genauer Anteil minus abgerundeter Anteil), je eine kbit/s; bei
  gleichem Rest zuerst die Klasse, die in gewichte weiter vorn steht.
  Die Summe ist so immer genau bandbreite.

    gewichte = {"sprache": 5, "video": 3, "geschaeft": 2, "standard": 2}
    anteile(gewichte)
        →  {"sprache": Fraction(5, 12), "video": Fraction(1, 4),
            "geschaeft": Fraction(1, 6), "standard": Fraction(1, 6)}
    gewichte_aus({"sprache": Fraction(1, 2), "video": Fraction(1, 3), "standard": Fraction(1, 6)})
        →  {"sprache": 3, "video": 2, "standard": 1}
    zuteilung(gewichte, 1000)
        →  {"sprache": 417, "video": 250, "geschaeft": 167, "standard": 166}

Genau wären es 416 2/3, 250, 166 2/3 und 166 2/3 kbit/s. Abgerundet sind
das 998; die zwei fehlenden bekommen sprache und geschaeft, deren Rest
2/3 ist; standard hat denselben Rest, steht aber weiter hinten.

Grenzen: gewichte hat 1 bis 50 Klassen mit verschiedenen, nicht leeren
Namen; jedes Gewicht ist eine ganze Zahl von 0 bis 10**6, mindestens
eines ist größer als 0. In gewichte_aus hat anteile 1 bis 50 Klassen,
jeder Anteil ist eine Fraction von 0 bis 1 mit einem Nenner bis 10**6,
mindestens einer ist größer als 0. bandbreite ist eine ganze Zahl von
0 bis 10**9.

Hintergrund: float kann die meisten Brüche nur ungefähr speichern
(Aufgabe 2_043), und Decimal hilft nur bei Zehnteln, Hundertsteln und
so weiter (Aufgabe 5_055): 1/3 ist auch als Dezimalzahl unendlich lang.
Bei der Zuteilung kommt es aber genau auf solche Reste an. Mit float
hat 10 / 18 * 1000 den Rest 0.5555555555555429 und 1 / 18 * 1000 den
Rest 0.55555555555555, obwohl beide genau 5/9 sind; welche Klasse die
zusätzliche kbit/s bekommt, entscheidet dann ein Rundungsfehler.

Das Modul fractions rechnet mit Brüchen aus zwei ganzen Zahlen, Zähler
und Nenner, und damit ganz ohne Rundung. Ein Bruch wird beim Erzeugen
immer gekürzt, der Nenner ist positiv:

    from fractions import Fraction

    Fraction(10, 12)                  # Fraction(5, 6)
    Fraction(5, 12) * 1000            # Fraction(1250, 3), also 416 2/3
    Fraction(1, 3) + Fraction(1, 6)   # Fraction(1, 2)
    sum([Fraction(1, 3)] * 3) == 1    # True
    x = Fraction(1250, 3)
    x.numerator, x.denominator        # (1250, 3)
    math.floor(x), x - math.floor(x)  # (416, Fraction(2, 3))
    Fraction("0.25"), Fraction(7)     # Fraction(1, 4), Fraction(7, 1)

Brüche lassen sich mit int mischen und genau vergleichen (<, ==, als
key für sorted und max). Mit float gemischt kommt wieder ein float
heraus, und die Genauigkeit ist weg: Fraction(1, 3) + 0.5 ist
0.8333333333333333. Auch Fraction(0.1) ist nicht 1/10, sondern der
Bruch, der wirklich im float steckt, 3602879701896397/36028797018963968;
limit_denominator(1000) findet daraus den nächsten Bruch mit Nenner bis
1000, Fraction(1, 10). Brüche sind langsamer als float, weil Zähler und
Nenner bei langen Rechnungen wachsen; für ein paar Dutzend Werte spielt
das keine Rolle.

Zum Kürzen braucht Fraction den größten gemeinsamen Teiler (ggT) von
Zähler und Nenner: die größte Zahl, die beide ohne Rest teilt (von Hand
in Aufgabe 3_071). Den gibt es auch direkt: math.gcd(10, 12) ist 2, und math.gcd nimmt beliebig
viele Zahlen, math.gcd(12, 18, 30) ist 6. Das Gegenstück ist das
kleinste gemeinsame Vielfache (kgV), die kleinste Zahl, die alle
Zahlen teilen: math.lcm(4, 6) ist 12. Will man Brüche zu ganzen Zahlen
im selben Verhältnis machen, multipliziert man alle mit dem kgV ihrer
Nenner und teilt sie danach durch den ggT der Ergebnisse:

    werte = [Fraction(1, 4), Fraction(1, 6)]
    nenner = math.lcm(*[w.denominator for w in werte])   # 12
    ganze = [w * nenner for w in werte]                   # [3, 2] als Fraction
    math.gcd(*[int(g) for g in ganze])                    # 1, also schon am kleinsten

Für die Reihenfolge der Reste hilft, dass sorted stabil ist (Aufgabe
3_027): Bei gleichem Schlüssel bleibt die ursprüngliche Reihenfolge
erhalten, und ein Dictionary behält die Reihenfolge, in der seine
Schlüssel eingetragen wurden.
"""

import math
from fractions import Fraction


def anteile(gewichte):
    """Gibt zu jeder Klasse ihren Anteil Gewicht / Summe aller Gewichte als Fraction zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def gewichte_aus(anteile):
    """Gibt die kleinsten ganzen Gewichte mit denselben Verhältnissen wie die Brüche in anteile zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def zuteilung(gewichte, bandbreite):
    """Verteilt bandbreite ganze kbit/s nach den Gewichten, die Reste an die Klassen mit dem größten Rest."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


GEWICHTE = {"sprache": 5, "video": 3, "geschaeft": 2, "standard": 2}
print(anteile(GEWICHTE))
print(gewichte_aus({"sprache": Fraction(1, 2), "video": Fraction(1, 3), "standard": Fraction(1, 6)}))
print(zuteilung(GEWICHTE, 1000))
