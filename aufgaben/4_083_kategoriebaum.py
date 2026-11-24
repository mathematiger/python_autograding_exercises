"""Aufgabe 4_083 – Kategoriebaum                                 Stufe 4 ★★★★☆

Ein Onlineshop für IT-Zubehör speichert seine Produktkategorien in einer
Datenbanktabelle mit Selbstbezug: Jede Zeile hat eine id, den Namen und
die eltern_id, die auf die id der übergeordneten Kategorie zeigt. Nur die
oberste Kategorie hat keine Eltern (eltern_id ist None). Aus der Tabelle
wird ein Baum: Die oberste Kategorie ist die Wurzel, jede Kategorie hat
eine Liste von Unterkategorien (Kindern), und eine Kategorie ohne Kinder
heißt Blatt. In den Blättern liegen später die Produkte.

    id  eltern_id  name               IT-Zubehör
     1  None       IT-Zubehör         ├── Eingabegeräte
     2  1          Eingabegeräte      │   ├── Tastaturen
     3  1          Kabel              │   └── Mäuse
     4  2          Tastaturen         └── Kabel
     5  2          Mäuse                  └── Netzwerkkabel
     6  3          Netzwerkkabel              ├── Cat 6
     7  6          Cat 6                      └── Cat 7
     8  6          Cat 7

Die Klasse `Kategorie` mit `__init__` und `hinzufuegen` ist vorgegeben.
Vervollständigen Sie:

- `durchlauf(self, tiefe=0)` ist eine Generatormethode. Sie liefert für
  die Kategorie selbst und alle Kategorien darunter Paare (tiefe, name),
  wie im Bild von oben nach unten: erst die Kategorie mit der
  übergebenen tiefe, dann nacheinander jedes Kind mit allem, was darunter
  liegt, eine Ebene tiefer. Sie arbeitet lazy: Wer nur das erste Paar
  will, wartet nicht, bis der ganze Baum durchlaufen ist.
- `blaetter(self)` ist eine Generatormethode, die die Namen aller Blätter
  unter der Kategorie (oder sie selbst, wenn sie ein Blatt ist) in
  derselben Reihenfolge liefert.
- `pfad_zu(self, name)` gibt die Liste der Namen von der Kategorie bis zur
  Kategorie name zurück (beide eingeschlossen), oder None, wenn es name
  darunter nicht gibt.
- `baue_baum(zeilen)` bekommt die Zeilen der Tabelle als Tupel
  (id, eltern_id, name) in beliebiger Reihenfolge und gibt die Wurzel
  zurück. Die Kinder jeder Kategorie stehen nach aufsteigender id.

    baum = baue_baum(zeilen)
    next(baum.durchlauf())          →  (0, "IT-Zubehör")
    list(baum.durchlauf())          →  [(0, "IT-Zubehör"), (1, "Eingabegeräte"),
                                        (2, "Tastaturen"), (2, "Mäuse"),
                                        (1, "Kabel"), (2, "Netzwerkkabel"),
                                        (3, "Cat 6"), (3, "Cat 7")]
    list(baum.blaetter())           →  ["Tastaturen", "Mäuse", "Cat 6", "Cat 7"]
    baum.pfad_zu("Cat 7")           →  ["IT-Zubehör", "Kabel", "Netzwerkkabel", "Cat 7"]
    baum.pfad_zu("Drucker")         →  None

Grenzen: zeilen hat 1 bis 10 000 Einträge mit verschiedenen ids (ganze
Zahlen von 1 bis 10**6) und verschiedenen, nicht leeren Namen. Genau eine
Zeile hat eltern_id None, jede andere eltern_id ist die id einer Zeile,
und es gibt keine Kreise. Der Baum ist höchstens 100 Ebenen tief.
baue_baum soll O(n log n) Schritte brauchen; durchlauf soll für das erste
Paar nur wenige Schritte brauchen, egal wie groß der Baum ist.

Hintergrund: Eine rekursive Datenstruktur enthält Objekte ihrer eigenen
Art. Eine Kategorie hat in self.kinder eine Liste von Kategorien, die
selbst wieder Kinder haben. Wie bei den verschachtelten Listen in Aufgabe
3_034 behandelt man so etwas mit einer Methode, die sich für jedes Kind
selbst aufruft; die Rekursion endet an den Blättern, deren Liste leer
ist:

    def anzahl(self):
        summe = 1                       # die Kategorie selbst
        for kind in self.kinder:
            summe += kind.anzahl()      # alles unter dem Kind
        return summe

Die Reihenfolge „erst der Knoten, dann jedes Kind mit allem darunter“
heißt Tiefensuche (Aufgabe 3_059) in Preorder. Soll eine solche Methode
viele Werte liefern, ist ein Generator (Aufgabe 3_022, als Methode in
Aufgabe 4_035) meist besser als eine Liste: Er erzeugt einen Wert erst,
wenn jemand ihn anfordert, braucht keinen Speicher für alle Werte auf
einmal und kann mittendrin aufhören (any, next, break). Ruft ein
Generator rekursiv einen anderen Generator auf, muss er dessen Werte
weiterreichen. Das tut yield from:

    def namen(self):
        yield self.name
        for kind in self.kinder:
            yield from kind.namen()     # wie: for n in kind.namen(): yield n

Ohne yield from bekäme man mit kind.namen() nur ein Generatorobjekt,
keinen einzigen Namen. Jede Ebene des Baums hält dabei einen eigenen
Generator offen, darum geht das nur bis zum Rekursionslimit von Python
(etwa 1000 Ebenen; Bäume aus Datenbanken sind fast immer viel flacher).

Um aus Tabellenzeilen einen Baum zu bauen, braucht man zu jeder
eltern_id schnell das Objekt der Eltern. Suchen Sie es nicht jedes Mal in
der Liste der Zeilen (das wären O(n²) Schritte), sondern legen Sie
zuerst für jede Zeile ein Objekt an und merken Sie sich alle in einem
Dictionary id → Kategorie. Danach hängt ein zweiter Durchgang jedes
Objekt an seine Eltern. Wer die Zeilen vorher nach id sortiert, bekommt
die Kinder automatisch in der richtigen Reihenfolge.
"""


class Kategorie:
    """Eine Produktkategorie mit Namen und einer Liste von Unterkategorien."""

    def __init__(self, name):
        """Legt eine Kategorie ohne Unterkategorien an."""
        self.name = name
        self.kinder = []

    def hinzufuegen(self, kind):
        """Hängt kind als letzte Unterkategorie an und gibt es zurück."""
        self.kinder.append(kind)
        return kind

    def durchlauf(self, tiefe=0):
        """Liefert (tiefe, name) für diese Kategorie und alle darunter, von oben nach unten."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def blaetter(self):
        """Liefert die Namen aller Blätter unter dieser Kategorie."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def pfad_zu(self, name):
        """Gibt die Namen von dieser Kategorie bis zur Kategorie name zurück, oder None."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def baue_baum(zeilen):
    """Baut aus den Zeilen (id, eltern_id, name) den Baum und gibt die Wurzel zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


zeilen = [
    (1, None, "IT-Zubehör"),
    (2, 1, "Eingabegeräte"),
    (3, 1, "Kabel"),
    (4, 2, "Tastaturen"),
    (5, 2, "Mäuse"),
    (6, 3, "Netzwerkkabel"),
    (7, 6, "Cat 6"),
    (8, 6, "Cat 7"),
]
baum = baue_baum(zeilen)
for tiefe, name in baum.durchlauf():
    print("  " * tiefe + name)
print(list(baum.blaetter()))
print(baum.pfad_zu("Cat 7"))
