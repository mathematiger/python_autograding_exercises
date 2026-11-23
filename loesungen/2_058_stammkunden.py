# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_058_stammkunden.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_058_stammkunden

"""Aufgabe 2_058 – Stammkunden                                   Stufe 2 ★★☆☆☆

Ein Onlineshop will seine Stammkunden mit einem Gutschein belohnen. Aus
der Datenbank kommt dafür ein Export aller Bestellungen des letzten
Jahres, von dem hier nur die Kundennummern gebraucht werden. Die Abfrage
hat sie aufsteigend sortiert; wer mehrmals bestellt hat, steht deshalb
mehrmals direkt hintereinander:

    nummern = [104, 104, 117, 120, 120, 120, 131, 131]

Gesucht ist, wie viele Bestellungen der fleißigste Kunde hatte und wer
das ist. Bevor Sie programmieren, füllen Sie eine Wertetabelle aus.

1. Tragen Sie in die Liste `TABELLE` für das Beispiel oben nach jedem
   Durchlauf der Schleife ein Tupel (wert, aktuell, laengste) ein: den
   gerade gelesenen Wert, die Länge der Serie gleicher Nummern, die mit
   diesem Wert endet, und die längste Serie unter allen bisher gelesenen
   Werten. Die ersten drei Zeilen sind (104, 1, 1), (104, 2, 2) und
   (117, 1, 2); es sind acht Zeilen, eine je Wert.
2. Schreiben Sie `laengste_serie(nummern)`: die Länge der längsten Serie
   gleicher Nummern, also die meisten Bestellungen eines Kunden; 0 bei
   einer leeren Liste. Die Schleife soll genau so arbeiten wie Ihre
   Tabelle.
3. Schreiben Sie `stammkunde(nummern)`: die Kundennummer mit den meisten
   Bestellungen. Haben mehrere Kunden gleich viele, gilt die kleinste
   Nummer; bei einer leeren Liste ist das Ergebnis None.

    laengste_serie([104, 104, 117, 120, 120, 120, 131, 131])   →  3
    stammkunde([104, 104, 117, 120, 120, 120, 131, 131])       →  120
    stammkunde([3, 3, 8, 8])                                   →  3

Gehen Sie die Liste dabei nur einmal von vorn nach hinten durch.

Grenzen: nummern hat 0 bis 100 000 Einträge, ganze Zahlen von 1 bis
1 000 000, aufsteigend sortiert; gleiche Nummern stehen also direkt
hintereinander. Jede Funktion soll höchstens etwa zwei Zugriffe auf
nummern je Eintrag brauchen.

Hintergrund: Eine Schleife, die etwas Schwieriges ausrechnet, versteht
man am besten über eine Aussage, die nach jedem Durchlauf stimmt. So
eine Aussage heißt Schleifen-Invariante. Bei der Summe in Aufgabe 1_025
lautet sie: „Nach jedem Durchlauf ist summe die Summe aller bisher
gelesenen Werte.“ Beim Maximum von Hand in Aufgabe 2_053: „groesste ist
der größte bisher gelesene Wert.“ Stimmt die Aussage vor der Schleife
(für null gelesene Werte), und bleibt sie bei jedem Durchlauf wahr,
dann stimmt sie auch am Ende, für die ganze Liste, und das Ergebnis ist
richtig.

Ob eine Schleife ihre Invariante einhält, sieht man in einer
Wertetabelle: eine Zeile je Durchlauf, eine Spalte je Variable, und
zwar mit den Werten am Ende des Durchlaufs. Für die Summe von
[4, 1, 5]:

    wert   summe
      4      4
      1      5
      5     10

Hier braucht es zwei Variablen. aktuell zählt die Serie, die gerade
läuft: Ist der neue Wert gleich dem vorigen, wird sie um 1 länger,
sonst beginnt eine neue Serie der Länge 1. laengste merkt sich das
Beste bisher, so wie groesste in 2_053. Damit man den vorigen Wert
vergleichen kann, merkt man ihn sich am Ende jedes Durchlaufs in einer
dritten Variable. Wer die Tabelle von Hand ausgefüllt hat, sieht sofort,
in welcher Zeile die eigene Schleife etwas anderes tut.
"""

TABELLE = []  # (wert, aktuell, laengste) nach jedem Durchlauf, für das Beispiel
TABELLE = [
    (104, 1, 1),
    (104, 2, 2),
    (117, 1, 2),
    (120, 1, 2),
    (120, 2, 2),
    (120, 3, 3),
    (131, 1, 3),
    (131, 2, 3),
]


def laengste_serie(nummern):
    """Gibt die Länge der längsten Serie gleicher Nummern zurück (0 bei leerer Liste)."""
    aktuell = 0
    laengste = 0
    vorige = None
    for wert in nummern:
        if wert == vorige:
            aktuell = aktuell + 1
        else:
            aktuell = 1
        if aktuell > laengste:
            laengste = aktuell
        vorige = wert
    return laengste


def stammkunde(nummern):
    """Gibt die Nummer mit den meisten Einträgen zurück, bei Gleichstand die kleinste; None bei leerer Liste."""
    aktuell = 0
    laengste = 0
    bester = None
    vorige = None
    for wert in nummern:
        if wert == vorige:
            aktuell = aktuell + 1
        else:
            aktuell = 1
        if aktuell > laengste:
            laengste = aktuell
            bester = wert
        vorige = wert
    return bester


nummern = [104, 104, 117, 120, 120, 120, 131, 131]
print(laengste_serie(nummern))
print(stammkunde(nummern))


# Idee: Die Schleife hält zwei Aussagen wahr (die Invarianten): aktuell ist die Länge der Serie, die
# mit dem gerade gelesenen Wert endet, und laengste die längste Serie unter allen gelesenen Werten.
# Ist der Wert gleich dem vorigen, wächst aktuell um 1, sonst ist aktuell = 1; danach wird laengste
# erhöht, wenn aktuell größer ist. Am Ende jedes Durchlaufs merkt sich vorige den Wert. stammkunde
# merkt sich zusätzlich den Wert, bei dem laengste zuletzt größer wurde; weil nur bei > (nicht >=)
# übernommen wird, gewinnt bei Gleichstand die zuerst gelesene, also kleinste Nummer.
# Anderer Weg: Mit einem Index i ab 1 nummern[i] mit nummern[i - 1] vergleichen, dann ist der erste
# Wert ein Sonderfall. Oder die Nummern in einem Dictionary zählen (Aufgabe 2_025); das braucht die
# Sortierung gar nicht, aber zusätzlichen Speicher. Naiv wäre nummern.count(wert) für jeden Wert:
# Das liest die ganze Liste für jeden Eintrag, bei 100 000 Einträgen also zehn Milliarden Zugriffe.
# Typische Fehler: laengste nur aktualisieren, wenn eine neue Serie beginnt (dann fehlt die letzte
# Serie), aktuell beim Wechsel auf 0 statt 1 setzen, >= statt > bei stammkunde (dann gewinnt bei
# Gleichstand die größte Nummer), eine leere Liste nicht bedenken.
