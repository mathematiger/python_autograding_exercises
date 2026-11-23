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
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def pfad(abhaengigkeiten, start, ziel):
    """Gibt einen Weg von start zu ziel zurück oder None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def begruendung(abhaengigkeiten, produkt, verdaechtig):
    """Gibt für jedes verdächtige Paket in produkt einen Weg dorthin zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


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
