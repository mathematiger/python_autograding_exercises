"""Aufgabe 3_008 – Stückpreise                                   Stufe 3 ★★★☆☆

Ein Großhändler stellt sein Warenwirtschaftssystem um. Die alten
Bestellungen sollen in die neue Datenbank übernommen werden, und dabei
wird für jede Bestellposition der Stückpreis berechnet: der Gesamtpreis
geteilt durch die Menge. Der Export aus dem alten System liefert jede
Position als Dictionary, alle Werte als Texte:

    {"artikel": "Maus", "gesamt": "59.70", "menge": "3"}

Die Daten sind nicht sauber. Manchmal steht im Gesamtpreis ein Komma statt
eines Punkts oder ein Wort statt einer Zahl, manchmal ist die Menge 0.
Solche Positionen sollen nicht übernommen, sondern mit dem Grund
gemeldet werden, damit jemand sie von Hand nachbessert.

Schreiben Sie die Funktion `stueckpreis(position, protokoll)`:

- Sie wandelt den Gesamtpreis mit float(...) und die Menge mit int(...)
  um und gibt den Stückpreis auf zwei Nachkommastellen gerundet zurück.
- Lässt sich ein Wert nicht umwandeln, gibt sie den Text "Formatfehler"
  zurück, ist die Menge 0, den Text "Menge ist 0".
- In jedem Fall, auch bei einem Fehler, hängt sie den Artikelnamen an die
  Liste protokoll an. So sieht man hinterher, welche Positionen schon
  bearbeitet wurden.
- Fehlt im Dictionary ein Feld, ist der Export selbst kaputt. Diesen
  Fehler (KeyError) fängt die Funktion nicht ab; er soll das Programm
  anhalten.

    protokoll = []
    stueckpreis({"artikel": "Maus", "gesamt": "59.70", "menge": "3"}, protokoll)
        →  19.9
    stueckpreis({"artikel": "Kabel", "gesamt": "12,50", "menge": "5"}, protokoll)
        →  "Formatfehler"
    stueckpreis({"artikel": "Dock", "gesamt": "149.00", "menge": "0"}, protokoll)
        →  "Menge ist 0"
    protokoll  →  ["Maus", "Kabel", "Dock"]

Grenzen: Alle Texte haben höchstens 20 Zeichen. Lässt sich der
Gesamtpreis umwandeln, liegt er zwischen 0 und 100 000 und hat höchstens
zwei Nachkommastellen; lässt sich die Menge umwandeln, liegt sie zwischen 0
und 10 000. Ist der Gesamtpreis unbrauchbar, ist die Menge nicht 0.

Hintergrund: Zu einem try können mehrere except-Blöcke gehören, einer pro
Art von Ausnahme. Python nimmt den ersten, der passt. So kann man jeden
Fehler anders behandeln: float("12,50") löst einen ValueError aus, eine
Division durch 0 einen ZeroDivisionError. Zwei weitere Blöcke sind
möglich:

    try:
        anteil = teil / gesamt
    except ZeroDivisionError:
        print("Gesamt ist 0")
    else:
        print("Anteil:", anteil)
    finally:
        print("Berechnung beendet")

Der else-Block läuft nur, wenn im try-Block keine Ausnahme aufgetreten ist.
Dorthin gehört, was nur bei Erfolg passieren soll. Der try-Block bleibt so
kurz und enthält nur die Zeilen, deren Fehler man abfangen will; ein Fehler
im else-Block wird nicht versehentlich mit abgefangen. Der finally-Block
läuft immer: nach Erfolg, nach einem abgefangenen Fehler, nach einem nicht
abgefangenen Fehler und sogar dann, wenn im try- oder except-Block ein
return steht. Man benutzt ihn für Aufräumarbeiten, die auf keinen Fall
vergessen werden dürfen, etwa eine Datei schließen oder einen Eintrag ins
Protokoll schreiben. Ausnahmen, mit denen man nicht rechnet, fängt man
nicht ab (siehe Aufgabe 3_007): Sie zeigen einen Fehler, den man nicht
überspielen soll.

Tipp: Ein return in jedem except-Block und im else-Block, das Protokoll im
finally-Block. round(zahl, 2) rundet auf zwei Nachkommastellen.
"""


def stueckpreis(position, protokoll):
    """Gibt den Stückpreis einer Bestellposition zurück oder den Fehlergrund als Text."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


export = [
    {"artikel": "Maus", "gesamt": "59.70", "menge": "3"},
    {"artikel": "Kabel", "gesamt": "12,50", "menge": "5"},
    {"artikel": "Dock", "gesamt": "149.00", "menge": "0"},
]
bearbeitet = []
for position in export:
    print(position["artikel"], stueckpreis(position, bearbeitet))
print("Bearbeitet:", bearbeitet)
