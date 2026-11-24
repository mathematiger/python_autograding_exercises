"""Aufgabe 4_086 – Alarmzuständigkeit                            Stufe 4 ★★★★☆

Das Monitoring einer Firma überwacht mehrere tausend Server. Ihre Namen
sind nach einem Schema aufgebaut, etwa "web-fra-03" oder
"db-muc-prod-12". Schlägt ein Alarm an, muss sofort klar sein, welches
Team zuständig ist. Dafür gibt es Regeln für Namensanfänge: "web" gehört
dem Team Web, "db" dem Team Datenbank, "db-muc-prod" aber dem
Bereitschaftsdienst München. Es gilt immer die Regel mit dem längsten
passenden Anfang; für "db-muc-prod-12" also der Bereitschaftsdienst.
Außerdem soll das Suchfeld der Oberfläche beim Tippen alle Servernamen
vorschlagen, die mit dem bisher Getippten beginnen. Beides erledigt ein
Trie (siehe Hintergrund).

Die Klasse `Knoten` und `__init__` von `Trie` sind vorgegeben.
Vervollständigen Sie die Methoden von `Trie`:

- `einfuegen(schluessel, wert)` speichert wert unter schluessel. Gibt es
  den Schlüssel schon, wird nur sein Wert ersetzt.
- `_knoten_zu(text)` ist eine Hilfsmethode für die beiden nächsten: Sie
  gibt den Knoten am Ende des Weges text zurück, oder None, wenn es den
  Weg nicht gibt.
- `nachschlagen(schluessel)` gibt den Wert zu genau diesem Schlüssel
  zurück, oder None, wenn es ihn nicht gibt.
- `mit_praefix(praefix)` gibt die alphabetisch sortierte Liste aller
  Schlüssel zurück, die mit praefix beginnen (auch praefix selbst, wenn
  er ein Schlüssel ist).
- `laengstes_praefix(text)` gibt das Paar (schluessel, wert) für den
  längsten Schlüssel zurück, mit dem text beginnt, oder None, wenn keiner
  passt.
- `__len__` gibt die Anzahl der Schlüssel zurück.

    regeln = Trie()
    regeln.einfuegen("web", "Team Web")
    regeln.einfuegen("db", "Team Datenbank")
    regeln.einfuegen("db-muc-prod", "Bereitschaft München")
    regeln.laengstes_praefix("db-muc-prod-12")  →  ("db-muc-prod", "Bereitschaft München")
    regeln.laengstes_praefix("db-muc-test-01")  →  ("db", "Team Datenbank")
    regeln.laengstes_praefix("mail-01")         →  None
    regeln.nachschlagen("db")                   →  "Team Datenbank"
    regeln.nachschlagen("db-muc")               →  None
    regeln.mit_praefix("d")                     →  ["db", "db-muc-prod"]
    len(regeln)                                 →  3

Grenzen: Schlüssel und text sind nicht leer und bestehen aus bis zu 60
Kleinbuchstaben, Ziffern, "-" und "."; praefix besteht aus denselben
Zeichen und darf leer sein (dann passen alle Schlüssel). Jeder wert ist
ein nicht leerer Text. Ein Trie hat bis zu 100 000 Schlüssel.
nachschlagen und laengstes_praefix sollen O(L) Schritte brauchen, L die
Länge des Textes, egal wie viele Schlüssel es gibt; mit_praefix
O(L + Länge aller gefundenen Schlüssel), dazu das Sortieren.

Hintergrund: Mit einem Dictionary (Aufgabe 2_025) findet man einen
ganzen Schlüssel schnell, aber für „alle Schlüssel, die mit d beginnen“
oder „der längste Schlüssel, mit dem der Text beginnt“ müsste man alle
Schlüssel durchgehen. Ein Trie (von „retrieval“, gesprochen wie „try“)
ist ein Baum, dessen Kanten Zeichen sind: Jeder Knoten hat ein
Dictionary kinder von Zeichen zu Kindknoten, und der Weg von der Wurzel
zu einem Knoten buchstabiert einen Anfang. Schlüssel mit gleichem
Anfang teilen sich den Weg:

    Schlüssel: "db", "db-muc-prod", "web"

    (Wurzel) ─d─ ● ─b─ ●* ─-─ ● ─m─ ● ─u─ … ─d─ ●*
             └w─ ● ─e─ ● ─b─ ●*

Ein Stern markiert einen Knoten, an dem ein Schlüssel endet; dort steht
auch sein Wert. Der Knoten nach "d", "b" ist markiert, der nach "d",
"b", "-" nicht. Alle Methoden laufen Zeichen für Zeichen von der Wurzel
nach unten, etwa diese, die prüft, ob irgendein Schlüssel mit text
beginnt:

    def hat_anfang(self, text):
        knoten = self.wurzel
        for zeichen in text:
            if zeichen not in knoten.kinder:
                return False            # hier geht kein Weg weiter
            knoten = knoten.kinder[zeichen]
        return True

Das kostet O(L) Schritte, egal ob der Trie zehn oder hunderttausend
Schlüssel hat. Beim Einfügen legt man fehlende Kinder an, statt
aufzuhören, und setzt am Ende den Wert (der Stern; ein Wert ist nie
None, darum bedeutet wert None „kein Schlüssel“). Für das längste Präfix läuft man genauso den Text
entlang und merkt sich unterwegs den letzten markierten Knoten, bis es
kein passendes Kind mehr gibt. Für alle Schlüssel mit einem Präfix
läuft man erst bis zum Knoten des Präfixes und sammelt dann alle
markierten Knoten darunter, mit Tiefensuche wie in Aufgabe 4_083; den
bisherigen Weg trägt man als Text mit. Router benutzen dieselbe Idee mit
Bits statt Zeichen, um für eine IP-Adresse den Eintrag mit dem längsten
passenden Präfix in der Routingtabelle zu finden.
"""


class Knoten:
    """Ein Knoten im Trie: Kinder je Zeichen und der Wert, falls hier ein Schlüssel endet."""

    def __init__(self):
        """Legt einen Knoten ohne Kinder und ohne Wert an."""
        self.kinder = {}
        self.wert = None


class Trie:
    """Schlüssel (Texte) mit Werten, sortiert nach ihren Anfängen."""

    def __init__(self):
        """Legt einen leeren Trie an."""
        self.wurzel = Knoten()
        self.anzahl = 0

    def einfuegen(self, schluessel, wert):
        """Speichert wert unter schluessel; ein vorhandener Wert wird ersetzt."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def _knoten_zu(self, text):
        """Gibt den Knoten am Ende des Weges text zurück, oder None, wenn es den Weg nicht gibt."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def nachschlagen(self, schluessel):
        """Gibt den Wert zu schluessel zurück, oder None."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def mit_praefix(self, praefix):
        """Gibt alle Schlüssel, die mit praefix beginnen, alphabetisch sortiert zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def laengstes_praefix(self, text):
        """Gibt (schluessel, wert) für den längsten Schlüssel zurück, mit dem text beginnt, oder None."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __len__(self):
        """Gibt die Anzahl der Schlüssel zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


regeln = Trie()
regeln.einfuegen("web", "Team Web")
regeln.einfuegen("db", "Team Datenbank")
regeln.einfuegen("db-muc-prod", "Bereitschaft München")
print(regeln.laengstes_praefix("db-muc-prod-12"), regeln.laengstes_praefix("db-muc-test-01"))
print(regeln.laengstes_praefix("mail-01"), regeln.nachschlagen("db"), regeln.nachschlagen("db-muc"))
print(regeln.mit_praefix("d"), len(regeln))
