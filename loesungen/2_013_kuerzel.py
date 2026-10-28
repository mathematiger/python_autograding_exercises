# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_013_kuerzel.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_013_kuerzel

"""Aufgabe 2_013 – Kürzel für Prozessschritte                     Stufe 2 ★★☆☆☆

Eine Firma lässt ihren Versandprozess analysieren: Jede Bestellung läuft
durch Schritte wie "Auftrag erfassen", "Ware kommissionieren" oder
"Paket versenden", und für jeden Schritt wird gemessen, wie lange er
dauert. Im Auswertungsprogramm stehen die Schritte als Spalten einer
Tabelle nebeneinander, und dort sind die langen Namen zu breit. Deshalb
bekommt jeder Schritt ein Kürzel: Man entfernt alle Vokale (a, e, i, o, u,
ä, ö, ü, groß und klein) und alle Leerzeichen. Nur der erste Buchstabe
bleibt immer stehen, auch wenn er ein Vokal ist, damit man den Schritt
noch erkennt.

Schreiben Sie die Funktion `kuerzel(schritt)`, die das Kürzel zurückgibt.
Ein leerer Name ergibt ein leeres Kürzel.

    kuerzel("Ware prüfen")         →  "Wrprfn"
    kuerzel("Auftrag erfassen")    →  "Aftrgrfssn"
    kuerzel("Übergabe")            →  "Übrgb"
    kuerzel("")                    →  ""

Benutzen Sie dafür eine for-Schleife über die Zeichen des Namens und nicht
replace.

Grenzen: 0 ≤ len(schritt) ≤ 100. schritt besteht nur aus Buchstaben (auch
Umlauten und ß) und Leerzeichen. Ist schritt nicht leer, ist das erste
Zeichen ein Buchstabe.

Hintergrund: Ein Text lässt sich wie eine Liste Zeichen für Zeichen
durchlaufen: for zeichen in "Ware" liefert nacheinander "W", "a", "r" und
"e". Texte kann man nicht verändern, aber man kann einen neuen Text Stück
für Stück aufbauen. Man beginnt mit dem leeren Text "" und hängt in der
Schleife mit + jedes Zeichen an, das man behalten will:

    ergebnis = ""
    for zeichen in text:
        if zeichen != "-":
            ergebnis = ergebnis + zeichen

Ob ein Zeichen zu einer Gruppe gehört, prüft zeichen in "aeiou" kurz und
übersichtlich, statt jedes Zeichen einzeln mit == zu vergleichen.

Tipp: schritt[0] ist der erste Buchstabe, schritt[1:] der ganze Rest.
"""

VOKALE = "aeiouäöüAEIOUÄÖÜ"


def kuerzel(schritt):
    """Gibt das Kürzel eines Prozessschritts zurück: erster Buchstabe, dann alles außer Vokalen und Leerzeichen."""
    if schritt == "":
        return ""
    ergebnis = schritt[0]
    for zeichen in schritt[1:]:
        if zeichen not in VOKALE and zeichen != " ":
            ergebnis = ergebnis + zeichen
    return ergebnis


for schritt in ["Auftrag erfassen", "Ware kommissionieren", "Paket versenden"]:
    print(f"{schritt}: {kuerzel(schritt)}")


# Idee: Der erste Buchstabe kommt immer ins Ergebnis. Danach läuft die Schleife
# über schritt[1:] und hängt jedes Zeichen an, das weder in VOKALE steht noch
# ein Leerzeichen ist. Den leeren Namen fängt ein if vorher ab, weil es dort
# kein schritt[0] gibt.
#
# Anderer Weg: eine Schleife über alle Zeichen mit enumerate oder einem Zähler;
# das Zeichen an Position 0 wird immer behalten, alle anderen nur, wenn sie
# keine Vokale und keine Leerzeichen sind. Ohne Schleife ginge es mit replace für
# jeden Vokal, das ist hier aber nicht verlangt.
#
# Typische Fehler: nur kleine Vokale entfernen, die Leerzeichen vergessen, auch
# den ersten Buchstaben streichen, wenn er ein Vokal ist, oder bei "" auf
# schritt[0] zugreifen (IndexError).
