# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_023_firewallprotokoll.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_023_firewallprotokoll

"""Aufgabe 3_023 – Firewallprotokoll                            Stufe 3 ★★★☆☆

Die Firewall eines Firmennetzes schreibt jede Verbindung, die sie
durchlässt, als Tupel (quelle, port, bytes) in ihr Protokoll: die
IPv4-Adresse des Rechners, der die Verbindung aufgebaut hat, den
Zielport (die Nummer des Dienstes, etwa 443 für HTTPS) und die Anzahl
übertragener Bytes. Das Protokoll eines Tages ist riesig und kommt
Zeile für Zeile aus einem Iterator, der sich nur einmal durchlaufen
lässt. Die Netzwerkadministration braucht daraus drei schnelle
Antworten. Schreiben Sie drei Funktionen, jede mit einem einzigen
Generator-Ausdruck:

- `bytes_zu_port(verbindungen, port)` gibt die Summe der Bytes aller
  Verbindungen zu diesem Port zurück.
- `gesperrter_port_benutzt(verbindungen, gesperrt)` gibt True zurück,
  wenn mindestens eine Verbindung zu einem Port aus der Menge gesperrt
  ging, sonst False.
- `nur_intern(verbindungen, netz)` gibt True zurück, wenn jede
  Verbindung von einer Adresse kam, die mit dem Text netz beginnt
  (etwa "10.20."), sonst False.

gesperrter_port_benutzt und nur_intern sollen aufhören, die
Verbindungen durchzugehen, sobald ihr Ergebnis feststeht.

    protokoll = [("10.20.1.5", 443, 5200), ("10.20.1.7", 22, 800),
                 ("10.20.3.9", 443, 12000), ("172.16.0.4", 3389, 600)]
    bytes_zu_port(protokoll, 443)                     →  17200
    gesperrter_port_benutzt(protokoll, {23, 3389})    →  True
    nur_intern(protokoll, "10.20.")                   →  False

Grenzen: verbindungen ist eine Liste oder ein Iterator mit 0 bis
1 000 000 Tupeln. Adressen sind Texte wie "10.20.1.5", Ports ganze
Zahlen von 0 bis 65 535, bytes ganze Zahlen von 0 bis 10**9. port ist
eine ganze Zahl von 0 bis 65 535, gesperrt eine Menge mit 0 bis 1000
Ports, netz ein Text aus 1 bis 15 Ziffern und Punkten. Ihre Lösung
soll O(n) Schritte brauchen und keine Liste aller Verbindungen
anlegen.

Hintergrund: Ein Generator-Ausdruck sieht aus wie eine List
Comprehension (Aufgabe 3_017), steht aber in runden statt eckigen
Klammern: (b for q, p, b in verbindungen if p == 443). Er baut keine
Liste, sondern einen Generator (Aufgabe 3_022), der jeden Wert erst
berechnet, wenn er abgeholt wird. Steht er als einziges Argument in
einem Aufruf, darf man die eigenen Klammern weglassen:

    summe = sum(b for q, p, b in verbindungen if p == 443)

sum, max, min, any und all nehmen alles, was sich durchlaufen lässt,
also auch einen Generator, und holen sich die Werte einzeln. So
braucht die Rechnung auch bei einer Million Zeilen kaum Speicher.
any(...) gibt True zurück, sobald ein Wert wahr ist, all(...) gibt
False zurück, sobald ein Wert falsch ist; die übrigen Werte werden dann
gar nicht mehr berechnet. Bei einer Liste in eckigen Klammern,
any([…]), wären sie dagegen alle schon berechnet. Für leere Eingaben
gilt: sum ergibt 0, any ergibt False, all ergibt True (keiner der
Werte ist falsch). Ob ein Text mit einem anderen beginnt, prüft
adresse.startswith(netz).
"""


def bytes_zu_port(verbindungen, port):
    """Gibt die Summe der Bytes aller Verbindungen zu port zurück."""
    return sum(menge for _, ziel, menge in verbindungen if ziel == port)


def gesperrter_port_benutzt(verbindungen, gesperrt):
    """Gibt zurück, ob mindestens eine Verbindung zu einem gesperrten Port ging."""
    return any(ziel in gesperrt for _, ziel, _ in verbindungen)


def nur_intern(verbindungen, netz):
    """Gibt zurück, ob alle Verbindungen von Adressen kamen, die mit netz beginnen."""
    return all(quelle.startswith(netz) for quelle, _, _ in verbindungen)


protokoll = [("10.20.1.5", 443, 5200), ("10.20.1.7", 22, 800), ("10.20.3.9", 443, 12000), ("172.16.0.4", 3389, 600)]
print(bytes_zu_port(protokoll, 443))
print(gesperrter_port_benutzt(protokoll, {23, 3389}))
print(nur_intern(protokoll, "10.20."))


# Idee: Jede Funktion ist ein einziger Aufruf von sum, any oder all mit einem Generator-Ausdruck. Das
# Auspacken quelle, ziel, menge geschieht direkt im for des Ausdrucks; was nicht gebraucht wird, heißt _.
# sum addiert nur die Bytes der passenden Zeilen, any fragt für jede Verbindung, ob ihr Port in der Menge
# gesperrt steht, all, ob ihre Adresse mit netz beginnt. any und all hören von selbst auf, sobald das
# Ergebnis feststeht, weil der Generator die restlichen Werte erst gar nicht berechnet.
#
# Anderer Weg: Eine for-Schleife mit einer Summenvariable bzw. mit return True beim ersten Treffer und
# return False nach der Schleife; das tut dasselbe, braucht aber vier bis fünf Zeilen pro Funktion.
#
# Typische Fehler: eckige statt runder Klammern, any([...]) (dann wird erst die ganze Liste gebaut, und
# any hört nicht früh auf), das Protokoll zweimal durchlaufen (ein Iterator ist danach leer), ziel in
# gesperrt mit einer Liste statt der Menge nachbauen, oder bei leerem Protokoll in nur_intern False
# zurückgeben.
#
# Laufzeit: Jede Funktion sieht jede Verbindung höchstens einmal an, O(n); in auf einer Menge braucht
# O(1). Der Speicherbedarf bleibt konstant, weil nie eine Liste entsteht.
