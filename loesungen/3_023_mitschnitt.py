# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_023_mitschnitt.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_023_mitschnitt

"""Aufgabe 3_023 – Mitschnitt                                    Stufe 3 ★★★☆☆

Die Netzwerkabteilung schneidet am Übergang zum Internet den Verkehr
eines Servers mit: Ein Werkzeug zeichnet jedes Paket auf, das dort
vorbeikommt, und liefert es als Paar (zielport, laenge). Der Zielport
sagt, für welchen Dienst das Paket bestimmt ist (443 für HTTPS, 53 für
DNS, 22 für SSH), die Länge ist die Größe des Pakets in Byte. Der
Mitschnitt kann eine Liste sein oder ein Iterator, der die Pakete live
nacheinander liefert. Schreiben Sie drei Funktionen:

- `datenmenge(pakete, port)` gibt zurück, wie viele Byte die Pakete an
  den Zielport port zusammen haben.
- `zu_gross(pakete, mtu)` gibt True zurück, wenn mindestens ein Paket
  länger als mtu ist, sonst False. Die MTU ist die größte Paketlänge,
  die das Netz ohne Zerlegen weiterleitet, im Ethernet meist 1500 Byte.
- `nur_freigegeben(pakete, freigaben)` gibt True zurück, wenn jedes
  Paket an einen Port aus der Menge freigaben geht, sonst False. So
  prüft die Abteilung, ob die Firewall nur die freigegebenen Dienste
  durchlässt.

    mitschnitt = [(443, 1500), (53, 80), (443, 900), (22, 120)]
    datenmenge(mitschnitt, 443)                  →  2400
    datenmenge(mitschnitt, 80)                   →  0
    zu_gross(mitschnitt, 1500)                   →  False
    zu_gross(mitschnitt, 1400)                   →  True
    nur_freigegeben(mitschnitt, {53, 443})       →  False
    nur_freigegeben(mitschnitt, {22, 53, 443})   →  True

Schreiben Sie jede Funktion mit einem Generator-Ausdruck in sum, any
oder all, ohne for-Schleife als eigene Anweisung und ohne
Zwischenliste.

Grenzen: pakete liefert 0 bis 100 000 Paare aus ganzen Zahlen, der
Zielport von 0 bis 65 535, die Länge von 1 bis 65 535. pakete kann eine
Liste oder ein Iterator sein und wird deshalb nur einmal durchlaufen.
port ist eine ganze Zahl von 0 bis 65 535, mtu eine von 68 bis 65 535,
freigaben eine Menge mit 0 bis 65 536 Ports. zu_gross und
nur_freigegeben sollen kein Paket mehr abholen, sobald das Ergebnis
feststeht. Ihre Lösung soll O(n) Schritte für n Pakete brauchen.

Hintergrund: Ein Generator-Ausdruck sieht aus wie eine List
Comprehension (Aufgabe 3_017), steht aber in runden statt in eckigen
Klammern. Er baut keine Liste, sondern einen Generator (Aufgabe 3_022),
der jeden Wert erst berechnet, wenn er abgeholt wird:

    quadrate = (zahl * zahl for zahl in zahlen)
    print(next(quadrate))           # das erste Quadrat

Ist der Generator-Ausdruck das einzige Argument einer Funktion, darf
man die eigenen Klammern weglassen:

    summe = sum(netto for artikel, netto in preise if netto > 100)

sum holt die Werte einzeln ab und addiert sie; eine Liste mit allen
Werten entsteht nie, das spart bei großen Datenmengen Speicher. any(…)
ist True, wenn mindestens ein Wert wahr ist, all(…) ist True, wenn
alle Werte wahr sind. Beide hören auf, sobald das Ergebnis feststeht:
any beim ersten wahren Wert, all beim ersten falschen. Mit einem
Generator-Ausdruck werden die übrigen Werte dann gar nicht mehr
berechnet; any([…]) mit eckigen Klammern dagegen baut erst die ganze
Liste. Ohne Werte ist sum(…) gleich 0, any(…) gleich False und
all(…) gleich True („es gibt keinen Wert, der falsch ist“).
"""


def datenmenge(pakete, port):
    """Gibt die Summe der Längen aller Pakete an den Zielport port zurück."""
    return sum(laenge for ziel, laenge in pakete if ziel == port)


def zu_gross(pakete, mtu):
    """Gibt zurück, ob mindestens ein Paket länger als mtu ist."""
    return any(laenge > mtu for _, laenge in pakete)


def nur_freigegeben(pakete, freigaben):
    """Gibt zurück, ob jedes Paket an einen Port aus freigaben geht."""
    return all(ziel in freigaben for ziel, _ in pakete)


mitschnitt = [(443, 1500), (53, 80), (443, 900), (22, 120)]
print(datenmenge(mitschnitt, 443))
print(zu_gross(mitschnitt, 1500), zu_gross(mitschnitt, 1400))
print(nur_freigegeben(mitschnitt, {53, 443}), nur_freigegeben(mitschnitt, {22, 53, 443}))


# Idee: Jede Funktion ist eine einzige Zeile: ein Generator-Ausdruck, der die Paare gleich in ziel, laenge
# auspackt, direkt in sum, any oder all. datenmenge filtert mit if ziel == port und summiert die Längen.
# zu_gross fragt any(laenge > mtu …), nur_freigegeben fragt all(ziel in freigaben …). Weil keine Liste
# entsteht, holen any und all nur so viele Pakete ab, bis das Ergebnis feststeht.
#
# Anderer Weg: zu_gross als not all(laenge <= mtu …) und nur_freigegeben als not any(ziel not in freigaben …);
# datenmenge als sum(laenge if ziel == port else 0 for …). Eine for-Schleife mit return True beim ersten
# Treffer rechnet ebenfalls richtig und hört früh auf, ist aber länger und war hier nicht verlangt.
#
# Typische Fehler: any([…]) oder sum([…]) mit eckigen Klammern (die ganze Liste entsteht, any hört nicht
# früh auf), >= statt > bei der MTU, freigaben als Liste prüfen (dann kostet jedes in O(k)), oder bei
# leerem Mitschnitt nur_freigegeben False zurückgeben (all ohne Werte ist True).
#
# Laufzeit: Jedes Paket wird höchstens einmal abgeholt, ziel in freigaben kostet bei einer Menge im Mittel
# O(1); zusammen O(n) für n Pakete, bei any und all oft weniger.
