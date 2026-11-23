r"""Aufgabe 3_052 – Alarmbericht                                  Stufe 3 ★★★☆☆

Ein Monitoring-System überwacht die Server einer Firma. Es misst
regelmäßig Kennzahlen wie die Auslastung des Prozessors (cpu) oder den
belegten Speicher (ram) und löst Alarme aus, wenn ein Wert eine Grenze
überschreitet. Die Leitung des Rechenzentrums will beides jeden Morgen
in ihrer Tabellenkalkulation öffnen, darum soll das System CSV-Dateien
schreiben. Schreiben Sie zwei Funktionen, die den Pfad der Datei als
Text bekommen und nichts zurückgeben:

- `schreibe_messwerte(pfad, messwerte)` bekommt eine Liste von Tupeln
  (server, metrik, wert) und schreibt eine Kopfzeile server,metrik,wert
  und darunter je Tupel eine Zeile.
- `schreibe_alarme(pfad, alarme)` bekommt eine Liste von Dictionaries
  mit den Schlüsseln zeit, server und meldung und schreibt eine
  Kopfzeile mit den Spalten aus SPALTEN und darunter je Alarm eine
  Zeile. Manche Alarme haben weitere Schlüssel, zum Beispiel notiz für
  interne Vermerke; die kommen nicht in die Datei.

Gibt es die Datei schon, wird ihr Inhalt ersetzt. Weil Meldungen Kommas
und Anführungszeichen enthalten, schreiben Sie die Dateien mit dem Modul
csv, nicht mit join. Zum Beispiel schreibt

    schreibe_alarme(pfad, [{"zeit": "03:12", "server": "db01",
                            "meldung": "RAM 97 %, Swap aktiv", "notiz": "Ada ruft an"}])

die Datei

    zeit,server,meldung
    03:12,db01,"RAM 97 %, Swap aktiv"

Die Tests legen einen leeren Ordner an, geben Ihnen Pfade darin und
lesen die Dateien mit csv.reader wieder ein.

Grenzen: 0 bis 10 000 Tupel oder Alarme. Server, Metrik, Zeit und
Meldung sind nicht leere Texte ohne Zeilenumbruch; in der Meldung kommen
Kommas, Anführungszeichen und Umlaute vor. wert ist eine ganze Zahl
oder Kommazahl von 0 bis 100 000. Jeder Alarm hat die drei Schlüssel aus
SPALTEN, dazu 0 bis 3 weitere. Der Ordner, in dem die Datei liegt,
existiert.

Hintergrund: Wie man mit csv.reader und csv.DictReader liest, steht in
Aufgabe 3_051, wie man eine Datei zum Schreiben öffnet, in Aufgabe
3_048. Das Modul csv schreibt auch: csv.writer(datei) liefert ein
Objekt, dessen Methode writerow(liste) eine Zeile schreibt und jedes
Feld in Anführungszeichen setzt, das es braucht; writerows(zeilen)
schreibt viele auf einmal. Zahlen wandelt es selbst in Text um:

    import csv

    with open("lager.csv", "w", encoding="utf-8", newline="") as datei:
        schreiber = csv.writer(datei)
        schreiber.writerow(["artikel", "anzahl"])
        schreiber.writerows([("Maus, kabellos", 4), ("Kabel", 12)])

Das Argument newline="" ist wichtig: csv beendet jede Zeile selbst mit
"\r\n", und ohne newline="" machte Windows daraus "\r\r\n", also eine
leere Zeile dazwischen. csv.DictWriter(datei, fieldnames=spalten)
schreibt Dictionaries; writeheader() schreibt die Kopfzeile, writerow
und writerows nehmen Dictionaries. Hat ein Dictionary einen Schlüssel,
der nicht in fieldnames steht, löst er einen ValueError aus, außer man
gibt ihm extrasaction="ignore" mit.
"""

import csv
import os
import tempfile

SPALTEN = ["zeit", "server", "meldung"]


def schreibe_messwerte(pfad, messwerte):
    """Schreibt die Messwerte (server, metrik, wert) mit Kopfzeile als CSV-Datei."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def schreibe_alarme(pfad, alarme):
    """Schreibt die Alarme mit den Spalten aus SPALTEN als CSV-Datei; weitere Schlüssel fallen weg."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


ordner = tempfile.mkdtemp()
pfad = os.path.join(ordner, "alarme.csv")
schreibe_alarme(pfad, [{"zeit": "03:12", "server": "db01", "meldung": "RAM 97 %, Swap aktiv", "notiz": "Ada ruft an"}])
with open(pfad, encoding="utf-8", newline="") as datei:
    print(datei.read())
