# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_076_meldungstexte.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_076_meldungstexte

"""Aufgabe 3_076 – Meldungstexte                                 Stufe 3 ★★★☆☆

Wer im Firmennetz ein Problem hat, meldet es über ein Webformular an
das Netzwerkteam, in eigenen Worten: „Das WLAN im Besprechungsraum ist
sehr langsam.“ Nach einem Monat liegen Hunderte solcher Freitexte vor.
Das Team will sie auswerten, bevor es Zeit in einzelne Fälle steckt:
Welche Wörter kommen am häufigsten vor (sie zeigen, welcher Ort, welches
Gerät oder welcher Dienst die meisten Störungen hat), und wie lang sind
die Sätze (lange, verschachtelte Sätze heißen oft, dass das Formular
die falschen Fragen stellt)? Im Programm unten sind SATZZEICHEN, die
Zeichen am Satzende SATZENDE und eine Menge FUELLWOERTER vorgegeben:
häufige Wörter wie "der", "ist" oder "nicht", die nichts über die
Störung verraten. Schreiben Sie vier Funktionen:

- `woerter(text)` gibt die Wörter des Texts als Liste zurück, in ihrer
  Reihenfolge und in Kleinbuchstaben. Wörter sind durch Leerzeichen
  oder Zeilenumbrüche getrennt; Satzzeichen am Anfang oder Ende eines
  Worts gehören nicht dazu. Was danach leer ist, ist kein Wort.
- `haeufigste_woerter(meldungen, anzahl)` zählt die Wörter aller
  Meldungen zusammen, ohne die Füllwörter, und gibt die anzahl
  häufigsten als Liste von Paaren (wort, wie_oft) zurück, das häufigste
  zuerst; bei gleich vielen alphabetisch nach dem Wort. Gibt es weniger
  verschiedene Wörter, kommen alle.
- `satzlaengen(text)` gibt für jeden Satz des Texts die Anzahl seiner
  Wörter zurück, Füllwörter mitgezählt. Ein Satz endet an einem der
  Zeichen aus SATZENDE; auch Wörter nach dem letzten Satzende bilden
  einen Satz. Sätze ohne Wörter (etwa zwischen "?" und "?" in "??")
  zählen nicht.
- `mittlere_satzlaenge(meldungen)` gibt zurück, wie viele Wörter ein
  Satz aller Meldungen im Mittel hat: die Summe aller Satzlängen geteilt
  durch die Anzahl aller Sätze. Ohne Sätze ist das 0.

    meldungen = [
        "Das WLAN im Besprechungsraum ist sehr langsam. Videokonferenzen brechen ab!",
        "Kein WLAN im Lager. Der Drucker ist auch nicht erreichbar.",
        "WLAN langsam, VPN bricht ab. Bitte prüfen!",
    ]
    woerter("Bitte prüfen: (VPN) bricht ab!")   →  ["bitte", "prüfen", "vpn", "bricht", "ab"]
    haeufigste_woerter(meldungen, 5)
        →  [("wlan", 3), ("ab", 2), ("langsam", 2), ("besprechungsraum", 1), ("brechen", 1)]
    satzlaengen(meldungen[0])          →  [7, 3]
    satzlaengen("Netz weg?? Seit 9 Uhr")   →  [2, 3]
    mittlere_satzlaenge(meldungen)     →  4.5

Grenzen: 0 ≤ len(meldungen) ≤ 10 000 mit zusammen höchstens 100 000
Wörtern, 0 ≤ anzahl ≤ 100 000. Ein Text besteht aus Buchstaben (auch
Umlaute und ß), Ziffern, Bindestrichen, Leerzeichen, Zeilenumbrüchen
und den Zeichen aus SATZZEICHEN. Bindestriche stehen nur innerhalb
eines Worts ("WLAN-Router" ist ein Wort). Punkt, Ausrufe- und
Fragezeichen stehen nur am Ende eines Satzes, dort aber auch mehrfach
("...", "?!"). Alphabetisch heißt: so, wie Python Texte vergleicht.

Hintergrund: Wie man Wörter mit einem Dictionary zählt, kennen Sie aus
Aufgabe 2_025, und wie sorted mit key nach mehreren Kriterien ordnet,
aus Aufgabe 3_027: Mit key=lambda paar: (-paar[1], paar[0]) kommen die
großen Anzahlen zuerst und bei Gleichstand die Wörter alphabetisch.
Neu ist, einen Freitext erst in saubere Wörter zu zerlegen. split()
trennt nur an Leerraum (Aufgabe 2_015), die Satzzeichen bleiben am Wort
hängen: "langsam," und "langsam" wären zwei verschiedene Schlüssel. strip ohne
Argument und lower kennen Sie aus Aufgabe 1_013. Bekommt
strip einen Text als Argument, entfernt es am Anfang und Ende alle
Zeichen, die darin vorkommen, in beliebiger Reihenfolge und Anzahl,
aber keine in der Mitte:

    "(VPN)!".strip(".,;:!?()")         →  "VPN"
    "WLAN-Router,".strip(".,;:!?()")   →  "WLAN-Router"
    "...".strip(".,;:!?()")            →  ""

Für Sätze trennt man den Text an den Satzenden. split kennt nur ein
Trennzeichen, also macht man aus "!" und "?" vorher mit replace (Aufgabe
1_014) Punkte und teilt dann mit split("."); an "??" oder am Textende
entstehen dabei leere Stücke, die man überspringt. Eine solche
Textstatistik ist der erste Schritt jeder Textauswertung: Erst wenn
klar ist, was ein Wort und was ein Satz ist, kann man zählen.

Tipp: Benutzen Sie woerter in den anderen drei Funktionen, auch für
jeden einzelnen Satz in satzlaengen.
"""

SATZZEICHEN = '.,;:!?()"'
SATZENDE = ".!?"
FUELLWOERTER = {
    "auch", "bei", "bitte", "das", "dem", "den", "der", "die", "ein", "eine",
    "es", "geht", "hier", "ich", "im", "in", "ist", "kein", "keine", "mit",
    "nicht", "schon", "sehr", "seit", "und", "uns", "von", "wieder", "wir", "zu",
}


def woerter(text):
    """Gibt die Wörter des Texts in Kleinbuchstaben und ohne Satzzeichen am Rand zurück."""
    liste = []
    for stueck in text.lower().split():
        wort = stueck.strip(SATZZEICHEN)
        if wort != "":
            liste.append(wort)
    return liste


def haeufigste_woerter(meldungen, anzahl):
    """Gibt die anzahl häufigsten Wörter ohne Füllwörter als Paare (wort, wie_oft) zurück."""
    zaehler = {}
    for meldung in meldungen:
        for wort in woerter(meldung):
            if wort not in FUELLWOERTER:
                zaehler[wort] = zaehler.get(wort, 0) + 1
    paare = sorted(zaehler.items(), key=lambda paar: (-paar[1], paar[0]))
    return paare[:anzahl]


def satzlaengen(text):
    """Gibt für jeden Satz des Texts die Anzahl seiner Wörter zurück."""
    einheitlich = text.replace("!", ".").replace("?", ".")
    laengen = []
    for satz in einheitlich.split("."):
        laenge = len(woerter(satz))
        if laenge > 0:
            laengen.append(laenge)
    return laengen


def mittlere_satzlaenge(meldungen):
    """Gibt die mittlere Anzahl Wörter je Satz über alle Meldungen zurück, ohne Sätze 0."""
    alle = []
    for meldung in meldungen:
        alle.extend(satzlaengen(meldung))
    if len(alle) == 0:
        return 0
    return sum(alle) / len(alle)


meldungen = [
    "Das WLAN im Besprechungsraum ist sehr langsam. Videokonferenzen brechen ab!",
    "Kein WLAN im Lager. Der Drucker ist auch nicht erreichbar.",
    "WLAN langsam, VPN bricht ab. Bitte prüfen!",
]
print(woerter("Bitte prüfen: (VPN) bricht ab!"))
print(haeufigste_woerter(meldungen, 5))
print(satzlaengen(meldungen[0]), satzlaengen("Netz weg?? Seit 9 Uhr"))
print(mittlere_satzlaenge(meldungen))


# Idee: woerter zerlegt den kleingeschriebenen Text mit split() und schneidet von jedem Stück mit
# strip(SATZZEICHEN) die Satzzeichen am Rand ab; leere Reste fallen weg. haeufigste_woerter zählt wie
# in Aufgabe 2_025 mit einem Dictionary, überspringt die Füllwörter, sortiert die Paare aus items()
# mit key=lambda paar: (-paar[1], paar[0]) und schneidet mit [:anzahl] ab. satzlaengen macht aus
# "!" und "?" Punkte, teilt mit split(".") und nimmt von jedem Stück len(woerter(stueck)), wenn sie
# größer als 0 ist. mittlere_satzlaenge sammelt alle Satzlängen und teilt ihre Summe durch ihre Anzahl.
# Anderer Weg: Die Sätze kann man auch Zeichen für Zeichen sammeln und an jedem Satzende abschließen.
# Statt des Dictionaries zählt in Stufe 4 collections.Counter, dessen most_common(anzahl) die
# häufigsten liefert (bei Gleichstand aber nicht alphabetisch). Naiv mit liste.count(wort) für jedes
# verschiedene Wort sieht man die Liste immer wieder durch: O(n · d) statt O(n).
# Typische Fehler: erst die Füllwörter prüfen und dann kleinschreiben ("Das" bleibt drin), mit
# reverse=True sortieren (dann stehen auch die Wörter bei Gleichstand rückwärts), leere Sätze aus
# "??" oder vom Textende mitzählen, das letzte Stück ohne Satzende vergessen, durch die Zahl der
# Meldungen statt der Sätze teilen und bei keinem Satz durch 0 teilen.
# Laufzeit: Für n Wörter brauchen woerter, satzlaengen und mittlere_satzlaenge O(n) Schritte,
# haeufigste_woerter O(n + d log d) für d verschiedene Wörter (zählen, dann sortieren).
