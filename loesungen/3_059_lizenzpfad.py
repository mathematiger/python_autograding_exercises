# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_059_lizenzpfad.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_059_lizenzpfad

"""Aufgabe 3_059 – Lizenzpfad                                    Stufe 3 ★★★☆☆

Ein Softwarehaus verkauft ein Kassensystem. Es benutzt fremde
Programmbibliotheken (Pakete), die wiederum andere Pakete benutzen. Vor
jeder Auslieferung prüft die Rechtsabteilung die Lizenzen, denn manche
Lizenzen verlangen etwas, das bei der Preisgestaltung zählt: etwa dass
der eigene Quelltext offengelegt wird oder dass pro Installation
Gebühren anfallen. Taucht ein solches Paket irgendwo auf, will die
Abteilung wissen, über welche Kette von Paketen es hineinkommt, um zu
entscheiden, welches direkte Paket ersetzt werden müsste.

Die Abhängigkeiten stehen in einem Dictionary: Jedem Paket ist die
Liste der Pakete zugeordnet, die es direkt benutzt. Pakete, die nichts
benutzen, fehlen als Schlüssel.

    abhaengigkeiten = {
        "kassensystem": ["oberflaeche", "datenbanktreiber"],
        "oberflaeche": ["grafik", "schriften"],
        "datenbanktreiber": ["verschluesselung"],
        "grafik": ["bildformate"],
        "verschluesselung": ["zufallszahlen"],
        "bildformate": ["kompression"],
    }

Schreiben Sie drei Funktionen:

- `suche(abhaengigkeiten, paket, ziel, besucht)` sucht rekursiv, also
  indem sie sich selbst aufruft, einen Weg von paket zu ziel und gibt
  ihn als Liste der Pakete von paket bis ziel zurück, oder None, wenn es
  keinen gibt. besucht ist eine Menge der Pakete, die die Suche schon
  angesehen hat; suche trägt jedes Paket ein, das sie ansieht, und geht
  in keins hinein, das schon darin steht.
- `pfad(abhaengigkeiten, start, ziel)` gibt einen Weg von start zu ziel
  zurück oder None. Benutzen Sie dafür suche mit einer leeren Menge.
- `begruendung(abhaengigkeiten, produkt, verdaechtig)` gibt ein
  Dictionary zurück, das jedem Paket aus der Liste verdaechtig, das in
  produkt steckt, einen Weg von produkt zu ihm zuordnet. Pakete, die
  nicht darin stecken, fehlen. Benutzen Sie dafür pfad.

Gibt es mehrere Wege, ist jeder richtig, der den Abhängigkeiten folgt
und kein Paket zweimal enthält.

    pfad(abhaengigkeiten, "kassensystem", "kompression")
    →  ["kassensystem", "oberflaeche", "grafik", "bildformate", "kompression"]
    pfad(abhaengigkeiten, "datenbanktreiber", "schriften")   →  None
    pfad(abhaengigkeiten, "grafik", "grafik")                →  ["grafik"]
    begruendung(abhaengigkeiten, "kassensystem", ["zufallszahlen", "druckertreiber"])
    →  {"zufallszahlen": ["kassensystem", "datenbanktreiber",
                          "verschluesselung", "zufallszahlen"]}

Grenzen: abhaengigkeiten hat 0 bis 500 Pakete als Schlüssel, zusammen 0
bis 5000 Einträge in den Listen, ohne Doppelte in einer Liste. Die Namen
sind nicht leere Texte; ein Paket kann über Umwege wieder sich selbst
benutzen (ein Kreis). start, ziel und produkt sind beliebige Namen,
verdaechtig hat 0 bis 50 verschiedene. pfad soll O(Pakete +
Abhängigkeiten) Schritte brauchen.

Hintergrund: Die Abhängigkeiten sind ein Graph wie der Kabelplan in
Aufgabe 3_058, nur dass jede Kante eine Richtung hat: Das Kassensystem
benutzt die Oberfläche, nicht umgekehrt. Die Breitensuche aus 3_058
geht in Wellen vor. Die Tiefensuche (englisch depth-first search) geht
dagegen erst einen Weg so weit wie möglich und kehrt erst um, wenn es
nicht weitergeht, so wie man einen Irrgarten mit der Hand an der Wand
erkundet. Rekursiv (Aufgabe 2_044) lässt sie sich sehr kurz schreiben,
denn „gibt es einen Weg von hier zum Ziel?“ zerfällt in „gibt es einen
Weg von einem meiner Nachbarn zum Ziel?“:

    def erreichbar(graph, knoten, ziel, besucht):
        if knoten == ziel:
            return True
        besucht.add(knoten)
        for nachbar in graph.get(knoten, []):
            if nachbar not in besucht and erreichbar(graph, nachbar, ziel, besucht):
                return True
        return False

Für den Weg selbst gibt die Funktion statt True die Liste zurück: Am
Ziel ist das [ziel]; liefert der Aufruf für einen Nachbarn einen Weg,
setzt man den eigenen Knoten davor ([knoten] + weg). Statt False kommt
None, und mit if weg is not None: prüft man, ob der Nachbar Erfolg hatte.

Die Menge besucht (Aufgabe 2_028) wird bei allen Aufrufen gemeinsam
benutzt; jeder Aufruf sieht, was die anderen schon eingetragen haben.
Ohne sie liefe die Suche in einem Kreis endlos, und bei vielen Wegen zum
selben Paket würde sie dieses Paket immer wieder durchsuchen, was bei
einigen Dutzend Paketen schon Milliarden Schritte werden können. Ein
Paket, das schon einmal erfolglos durchsucht wurde, führt auch beim
zweiten Mal nicht zum Ziel. Den kürzesten Weg findet die Tiefensuche
nicht unbedingt; dafür ist die Breitensuche da.
"""


def suche(abhaengigkeiten, paket, ziel, besucht):
    """Sucht rekursiv einen Weg von paket zu ziel; gibt die Liste der Pakete oder None zurück."""
    if paket == ziel:
        return [paket]
    besucht.add(paket)
    for naechstes in abhaengigkeiten.get(paket, []):
        if naechstes not in besucht:
            weg = suche(abhaengigkeiten, naechstes, ziel, besucht)
            if weg is not None:
                return [paket] + weg
    return None


def pfad(abhaengigkeiten, start, ziel):
    """Gibt einen Weg von start zu ziel zurück oder None."""
    return suche(abhaengigkeiten, start, ziel, set())


def begruendung(abhaengigkeiten, produkt, verdaechtig):
    """Gibt für jedes verdächtige Paket in produkt einen Weg dorthin zurück."""
    wege = {}
    for paket in verdaechtig:
        weg = pfad(abhaengigkeiten, produkt, paket)
        if weg is not None:
            wege[paket] = weg
    return wege


abhaengigkeiten = {
    "kassensystem": ["oberflaeche", "datenbanktreiber"],
    "oberflaeche": ["grafik", "schriften"],
    "datenbanktreiber": ["verschluesselung"],
    "grafik": ["bildformate"],
    "verschluesselung": ["zufallszahlen"],
    "bildformate": ["kompression"],
}
print(pfad(abhaengigkeiten, "kassensystem", "kompression"))
print(begruendung(abhaengigkeiten, "kassensystem", ["zufallszahlen", "druckertreiber"]))


# Idee: suche ist eine rekursive Tiefensuche. Ist paket das Ziel, ist der Weg [paket]. Sonst trägt sie
# paket in besucht ein und probiert jedes direkt benutzte Paket, das noch nicht besucht ist: Liefert der
# rekursive Aufruf einen Weg, setzt sie paket davor und gibt [paket] + weg zurück. Hat keins Erfolg, gibt
# sie None zurück. pfad ruft suche mit set() auf, begruendung ruft pfad für jedes verdächtige Paket auf
# und nimmt nur die Wege auf, die nicht None sind.
# Anderer Weg: ohne Rekursion mit einer Liste als Stapel, auf der man Paare (paket, weg_bis_hierher)
# ablegt; oder eine Breitensuche wie in Aufgabe 3_058, die sich für jedes Paket den Vorgänger merkt und
# den Weg am Ende rückwärts zusammensetzt (die findet sogar den kürzesten). Naiv wäre eine Tiefensuche,
# die nur den aktuellen Weg prüft statt aller besuchten Pakete; sie hält Kreise auf, braucht bei vielen
# Wegen zum selben Paket aber exponentiell viele Schritte.
# Typische Fehler: besucht vergessen (RecursionError bei Kreisen), den Weg des Nachbarn nicht prüfen und
# sofort zurückgeben (dann bricht die Suche nach dem ersten erfolglosen Nachbarn ab), abhaengigkeiten[paket]
# statt get (KeyError bei Paketen ohne Abhängigkeiten), in begruendung eine gemeinsame Menge für alle
# Suchen benutzen.
# Laufzeit: O(Pakete + Abhängigkeiten) für pfad, denn jedes Paket wird höchstens einmal betreten und jede
# Liste einmal durchlaufen ([paket] + weg kommt nur auf dem gefundenen Weg vor und kostet zusammen
# O(Länge²), höchstens 500²). begruendung ruft pfad für jedes verdächtige Paket einmal auf.
