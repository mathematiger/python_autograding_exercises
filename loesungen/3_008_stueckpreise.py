# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_008_stueckpreise.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_008_stueckpreise

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
    try:
        preis = float(position["gesamt"]) / int(position["menge"])
    except ValueError:
        return "Formatfehler"
    except ZeroDivisionError:
        return "Menge ist 0"
    else:
        return round(preis, 2)
    finally:
        protokoll.append(position["artikel"])


export = [
    {"artikel": "Maus", "gesamt": "59.70", "menge": "3"},
    {"artikel": "Kabel", "gesamt": "12,50", "menge": "5"},
    {"artikel": "Dock", "gesamt": "149.00", "menge": "0"},
]
bearbeitet = []
for position in export:
    print(position["artikel"], stueckpreis(position, bearbeitet))
print("Bearbeitet:", bearbeitet)


# Idee: Im try-Block stehen nur Umwandlung und Division. Ein except ValueError liefert
# "Formatfehler", ein except ZeroDivisionError "Menge ist 0", der else-Block gibt bei Erfolg den
# gerundeten Preis zurück, und der finally-Block hängt den Artikel an das Protokoll, egal was
# vorher passiert ist, auch bei einem KeyError, der weiterläuft.
#
# Anderer Weg: das Protokoll ganz am Anfang der Funktion schreiben, noch vor dem try; das geht
# hier auch, solange "artikel" vorhanden ist. Statt auf den ZeroDivisionError zu warten, kann man
# vor der Division mit if menge == 0 prüfen. finally ist aber der sichere Ort für alles, was
# immer passieren muss, auch wenn später weitere return-Zeilen dazukommen.
#
# Typische Fehler: protokoll.append(...) hinter einem return (wird nie erreicht), ein nacktes
# except: oder except Exception (verschluckt den KeyError) und int(...) statt float(...) für den
# Gesamtpreis (dann ist schon "59.70" ein Formatfehler).
#
# Laufzeit: O(1) pro Position, es gibt keine Schleife.
