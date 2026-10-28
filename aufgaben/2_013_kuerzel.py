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
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


for schritt in ["Auftrag erfassen", "Ware kommissionieren", "Paket versenden"]:
    print(f"{schritt}: {kuerzel(schritt)}")
