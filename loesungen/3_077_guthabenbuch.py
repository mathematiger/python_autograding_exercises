# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_077_guthabenbuch.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_077_guthabenbuch

"""Aufgabe 3_077 – Guthabenbuch                                  Stufe 3 ★★★☆☆

Ein Rechenzentrum vermietet virtuelle Server an kleine Firmen und
rechnet über ein Prepaid-Guthaben ab: Der Kunde zahlt vorab Geld ein,
und am Ende jedes Monats wird der Serverbetrieb davon abgebucht. Ein
Minus gibt es nicht; reicht das Guthaben nicht, wird nicht abgebucht,
sondern der Kunde bekommt eine Zahlungserinnerung. Bisher führt die
Buchhaltung das in einer Tabellenkalkulation, jetzt soll ein kleines
Programm daraus werden, das jedes Guthabenbuch in einer Textdatei
ablegt. Vervollständigen Sie die Klassen und Funktionen:

- `Buchung(monat, art, betrag)` speichert die Attribute `monat` (ein
  Text wie "2026-01"), `art` und `betrag` (ganze Euro). art muss
  "einzahlung" oder "abbuchung" sein, betrag größer als 0; sonst löst
  __init__ einen ValueError aus.
  - `wert(self)` gibt den Betrag zurück, um den sich das Guthaben
    ändert: positiv bei einer Einzahlung, negativ bei einer Abbuchung.
  - `als_zeile(self)` gibt die Buchung als Zeile für die Datei zurück,
    etwa "2026-01;abbuchung;120" (ohne Zeilenumbruch).
- `buchung_aus_zeile(zeile)` macht aus einer solchen Zeile wieder eine
  Buchung, mit betrag als int. Hat die Zeile nicht genau drei Felder
  oder ist der Betrag keine ganze Zahl, kommt ein ValueError.
- `Guthabenbuch(kunde)` speichert `kunde` und eine leere Liste
  `buchungen`.
  - `guthaben(self)` gibt die Summe der Werte aller Buchungen zurück.
  - `buchen(self, buchung)` hängt die Buchung an buchungen an. Würde
    das Guthaben dadurch negativ, löst die Methode einen ValueError aus
    und bucht nichts.
  - `einzahlen(self, monat, betrag)` und `abbuchen(self, monat,
    betrag)` legen eine passende Buchung an und buchen sie.
  - `speichern(self, pfad)` schreibt das Buch in die Datei: in die
    erste Zeile den Kunden, dann jede Buchung als Zeile, in ihrer
    Reihenfolge. Jede Zeile endet mit einem Zeilenumbruch, ein alter
    Inhalt der Datei wird ersetzt.
- `lade_guthabenbuch(pfad)` liest eine solche Datei und gibt ein neues
  Guthabenbuch zurück. Jede Buchung der Datei geht dabei durch buchen,
  damit auch eine von Hand bearbeitete Datei die Regeln einhält; ist
  eine Zeile fehlerhaft, kommt ein ValueError. Fehlt die Datei, geht
  der FileNotFoundError an den Aufrufer weiter.

    buch = Guthabenbuch("Kanzlei Berg")
    buch.einzahlen("2026-01", 500)
    buch.abbuchen("2026-01", 120)
    buch.abbuchen("2026-02", 120)
    buch.guthaben()                    →  260
    buch.buchungen[1].als_zeile()      →  "2026-01;abbuchung;120"
    buch.abbuchen("2026-03", 300)      →  ValueError (nur 260 Euro da)
    buch.einzahlen("2026-03", 0)       →  ValueError
    buch.speichern(pfad)               # Datei: Kanzlei Berg / 2026-01;einzahlung;500 / …
    lade_guthabenbuch(pfad).guthaben() →  260

Die Tests legen einen leeren Ordner an und geben Ihnen Pfade darin.

Grenzen: kunde ist ein nicht leerer Text ohne Zeilenumbruch und ohne
Leerzeichen am Rand, Umlaute kommen vor. monat ist ein Text der Form
"JJJJ-MM", art ein beliebiger Text ohne Semikolon und Zeilenumbruch,
betrag eine ganze Zahl von -1 000 000 bis 1 000 000. Ein Buch hat bis
zu 1000 Buchungen. Eine Datei für lade_guthabenbuch ist in UTF-8
gespeichert, hat in der ersten Zeile den Kunden und danach keine leeren
Zeilen; jede Zeile endet mit einem Zeilenumbruch. Ihre Buchungszeilen
können aber alle Fehler enthalten, die oben stehen. Mehrere Bücher
nebeneinander sind unabhängig.

Hintergrund: Diese Aufgabe setzt zusammen, was Sie schon kennen:
Klassen mit __init__ und Methoden (Aufgaben 3_037 bis 3_043), Objekte
in Listen (Aufgabe 3_040), raise ValueError (Aufgabe 3_009) und
Textdateien mit with open(..., encoding="utf-8") lesen und mit "w"
schreiben (Aufgaben 3_046 und 3_048). Neu ist, ein kleines Projekt
sinnvoll aufzuteilen. Ein paar Regeln helfen dabei:

- Eine Klasse für jedes Ding, über das man redet: Eine Buchung kennt
  ihre Daten, prüft sie selbst in __init__ und weiß, wie sie als Zeile
  aussieht. Das Guthabenbuch verwaltet die Liste der Buchungen und
  prüft die Regel, die das ganze Konto betrifft: kein Minus.
- Jede Regel steht an genau einer Stelle. einzahlen und abbuchen sind
  zwei Zeilen lang, weil sie buchen aufrufen, und lade_guthabenbuch
  benutzt buchen ebenfalls; so gilt „kein Minus“ überall, ohne dass
  man es dreimal hinschreibt. Das Guthaben wird aus den Buchungen
  berechnet statt in einem zweiten Attribut mitgezählt, dann können
  beide nicht auseinanderlaufen.
- Das Dateiformat steht an genau zwei Stellen, die zusammengehören:
  als_zeile schreibt eine Buchung, buchung_aus_zeile liest sie. Eine
  Methode ruft man auf einem Objekt auf, das es schon gibt; was eine
  Buchung erst baut, ist deshalb hier eine gewöhnliche Funktion
  außerhalb der Klasse.
- Fehler entstehen dort, wo man sie bemerkt, und wandern zum Aufrufer
  (Aufgabe 3_029). Manche löst Python schon selbst aus: Hat
  "2026-01;abbuchung".split(";") nur zwei Teile, scheitert
  monat, art, betrag = ... mit einem ValueError (Auspacken: Aufgabe
  1_044), ebenso int("zwölf").

Wer das Programm später benutzt, etwa ein Skript, das am Monatsende
alle Kunden abbucht, ruft nur noch einzahlen, abbuchen, speichern und
lade_guthabenbuch auf und muss vom Dateiformat nichts wissen.
"""


class Buchung:
    """Eine Einzahlung oder Abbuchung auf einem Guthabenkonto."""

    def __init__(self, monat, art, betrag):
        if art != "einzahlung" and art != "abbuchung":
            raise ValueError(f"Unbekannte Buchungsart: {art}")
        if betrag <= 0:
            raise ValueError(f"Der Betrag muss größer als 0 sein, nicht {betrag}")
        self.monat = monat
        self.art = art
        self.betrag = betrag

    def wert(self):
        """Gibt die Änderung des Guthabens zurück: positiv bei Einzahlung, negativ bei Abbuchung."""
        if self.art == "einzahlung":
            return self.betrag
        return -self.betrag

    def als_zeile(self):
        """Gibt die Buchung als Zeile "monat;art;betrag" ohne Zeilenumbruch zurück."""
        return f"{self.monat};{self.art};{self.betrag}"


def buchung_aus_zeile(zeile):
    """Macht aus einer Zeile "monat;art;betrag" eine Buchung."""
    monat, art, betrag = zeile.split(";")
    return Buchung(monat, art, int(betrag))


class Guthabenbuch:
    """Das Prepaid-Guthaben eines Kunden mit allen Buchungen."""

    def __init__(self, kunde):
        self.kunde = kunde
        self.buchungen = []

    def guthaben(self):
        """Gibt die Summe der Werte aller Buchungen zurück."""
        summe = 0
        for buchung in self.buchungen:
            summe += buchung.wert()
        return summe

    def buchen(self, buchung):
        """Hängt die Buchung an; würde das Guthaben negativ, kommt ein ValueError."""
        if self.guthaben() + buchung.wert() < 0:
            raise ValueError(f"Nicht genug Guthaben: {self.guthaben()} Euro, abgebucht werden sollen {buchung.betrag} Euro")
        self.buchungen.append(buchung)

    def einzahlen(self, monat, betrag):
        """Bucht eine Einzahlung."""
        self.buchen(Buchung(monat, "einzahlung", betrag))

    def abbuchen(self, monat, betrag):
        """Bucht eine Abbuchung."""
        self.buchen(Buchung(monat, "abbuchung", betrag))

    def speichern(self, pfad):
        """Schreibt den Kunden und alle Buchungen zeilenweise in die Datei."""
        with open(pfad, "w", encoding="utf-8") as datei:
            datei.write(f"{self.kunde}\n")
            for buchung in self.buchungen:
                datei.write(f"{buchung.als_zeile()}\n")


def lade_guthabenbuch(pfad):
    """Liest ein Guthabenbuch aus der Datei; jede Buchung geht durch buchen."""
    with open(pfad, encoding="utf-8") as datei:
        zeilen = datei.read().splitlines()
    buch = Guthabenbuch(zeilen[0])
    for zeile in zeilen[1:]:
        buch.buchen(buchung_aus_zeile(zeile))
    return buch


buch = Guthabenbuch("Kanzlei Berg")
buch.einzahlen("2026-01", 500)
buch.abbuchen("2026-01", 120)
buch.abbuchen("2026-02", 120)
print(buch.guthaben())
print(buch.buchungen[1].als_zeile())


# Idee: Buchung prüft in __init__ zuerst art und betrag und legt erst dann die Attribute an; wert gibt
# den Betrag mit Vorzeichen zurück, als_zeile baut "monat;art;betrag". buchung_aus_zeile zerlegt mit
# split(";") in genau drei Teile und baut mit Buchung(monat, art, int(betrag)), so prüft __init__ auch
# die Zeilen aus der Datei. Guthabenbuch.guthaben summiert die Werte; buchen prüft, ob das Guthaben
# negativ würde, und hängt sonst an. einzahlen und abbuchen rufen nur buchen auf. speichern schreibt
# den Kunden und alle Zeilen mit "\n", lade_guthabenbuch liest die erste Zeile als Kunden und bucht
# jede weitere mit buchen(buchung_aus_zeile(zeile)).
# Anderer Weg: Das Guthaben zusätzlich in einem Attribut self.stand mitführen, das buchen anpasst;
# dann kostet guthaben() nur O(1), aber Liste und Stand müssen immer zusammen geändert werden.
# Beim Lesen geht auch for zeile in datei: mit zeile.rstrip("\n") wie in Aufgabe 3_046.
# Typische Fehler: in lade_guthabenbuch direkt an buch.buchungen anhängen (dann ist ein Minus aus
# der Datei möglich), int vergessen ("120" als Text speichert sich gleich, rechnet aber falsch), erst
# anhängen und dann prüfen, die Prüfung „kein Minus“ in einzahlen und abbuchen doppelt schreiben
# und eine davon vergessen, den Zeilenumbruch an der Kundenzeile lassen und den FileNotFoundError
# abfangen.
# Laufzeit: guthaben braucht O(n) für n Buchungen, also buchen auch; ein Buch mit n Buchungen zu
# laden kostet damit O(n²) (mit self.stand O(n)). speichern ist O(n).
