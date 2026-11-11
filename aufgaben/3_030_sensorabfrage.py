"""Aufgabe 3_030 – Sensorabfrage                                 Stufe 3 ★★★☆☆

In einer Fertigungshalle fragt ein kleiner Rechner, das Gateway, jede
Minute alle Sensoren ab und schickt die Werte an die Leitwarte, von der
aus das Personal die Halle überwacht. Für jeden Sensor gibt es eine
Lesefunktion, die man ohne Argumente aufruft und die den Messwert
zurückgibt. Manchmal geht dabei etwas schief: Ein Sensor antwortet nicht
(TimeoutError), die Netzwerkverbindung zu ihm bricht ab
(ConnectionError), ein Sensor ist abgesteckt (FileNotFoundError, denn
unter Linux erscheint ein angeschlossenes Gerät als Datei wie
/dev/ttyUSB0), die Adresse eines Sensors fehlt in der Konfiguration
(KeyError), eine Lesefunktion teilt versehentlich durch 0
(ZeroDivisionError) oder hat einen anderen Programmierfehler. Ein
einziger gestörter Sensor darf aber nicht die ganze Abfrage anhalten. Die
Leitwarte will außerdem wissen, welcher Art die Störung ist, damit man
gleich weiß, wo man suchen muss:

    Ausnahme (und jede Unterart, siehe unten)    Störung
    TimeoutError                                 "Sensor antwortet nicht"
    jeder andere OSError                         "Gerät nicht erreichbar"
    LookupError                                  "Konfiguration prüfen"
    ArithmeticError                              "Rechenfehler"
    jede andere Exception                        "Softwarefehler: <Meldung>"

Bei "Softwarefehler: <Meldung>" steht hinter dem Doppelpunkt die Meldung
der Ausnahme, also str(...) von ihr (Aufgabe 3_029).

Schreiben Sie die Funktion `frage_ab(sensoren)`. sensoren ist eine Liste
von Paaren (name, lesefunktion); die Lesefunktionen sind Funktionen als
Werte wie in Aufgabe 3_028. frage_ab ruft jede Lesefunktion genau einmal
auf, in der Reihenfolge der Liste, und gibt ein Tupel (werte, stoerungen)
aus zwei Dictionaries zurück: werte ordnet jedem Sensor, der geantwortet
hat, seinen Messwert zu, stoerungen jedem anderen Sensor seine Störung aus
der Tabelle. In beiden stehen die Sensoren in der Reihenfolge der Liste.
Bricht jemand das Gateway mit Strg+C ab (KeyboardInterrupt), soll es
wirklich anhalten; diese Ausnahme fängt frage_ab also nicht ab.

    frage_ab([("temperatur", halle_temperatur), ("tor", tor_sensor),
              ("kran", kran_last), ("feuchte", feuchte_sensor)])
        →  ({"temperatur": 21.5},
            {"tor": "Sensor antwortet nicht", "kran": "Rechenfehler",
             "feuchte": "Konfiguration prüfen"})

Die vier Lesefunktionen stehen unten im Code.

Grenzen: 0 ≤ len(sensoren) ≤ 1000, alle Namen sind verschieden. Jede
Lesefunktion gibt eine Zahl zurück oder löst eine Ausnahme aus.

Hintergrund: Die Arten von Ausnahmen bilden einen Stammbaum. Ein
except-Block fängt nicht nur die Art, die hinter except steht, sondern
auch jede, die im Stammbaum darunter steht. Ein Ausschnitt:

    BaseException
    ├── KeyboardInterrupt          Abbruch mit Strg+C
    └── Exception                  alle gewöhnlichen Fehler
        ├── ArithmeticError        Rechenfehler
        │   ├── ZeroDivisionError
        │   └── OverflowError
        ├── LookupError            Nachschlagen ging schief
        │   ├── IndexError
        │   └── KeyError
        ├── OSError                Ein- und Ausgabe, Geräte, Netz
        │   ├── ConnectionError    mit ConnectionRefusedError, ConnectionResetError, …
        │   ├── TimeoutError
        │   ├── FileNotFoundError
        │   └── PermissionError
        ├── TypeError
        └── ValueError

except LookupError fängt also einen KeyError ebenso wie einen IndexError,
und except Exception fängt alle gewöhnlichen Fehler, aber nicht
KeyboardInterrupt. (In Python heißen die Arten Klassen; mehr dazu bei den
Klassen.) Gehören mehrere except-Blöcke zu einem try, prüft Python sie von
oben nach unten und nimmt den ersten, der passt (Aufgabe 3_008). Die
speziellere Art gehört deshalb über die allgemeinere: Stünde except
OSError über except TimeoutError, käme jeder TimeoutError schon beim
OSError an, und stünde except Exception ganz oben, landete jeder Fehler
dort. Die Blöcke darunter kämen nie zum Zug.

Bisher galt: Fangen Sie nur ab, womit Sie rechnen (Aufgabe 3_007). An
genau einer Stelle weicht man davon ab: Dort, wo ein Programm auf jeden
Fall weiterlaufen muss (hier die Schleife über alle Sensoren), fängt man
mit except Exception alle übrigen gewöhnlichen Fehler ab, aber nie
stillschweigend, sondern mit der Meldung der Ausnahme. Echte Programme
schreiben dabei zusätzlich den ganzen Traceback in ein Protokoll, damit
jemand den Programmierfehler finden kann. Ein nacktes except: ohne Art
fängt dagegen sogar KeyboardInterrupt; solange ein Programm in einem
solchen try-Block steckt, lässt es sich mit Strg+C nicht anhalten.
Schreiben Sie das nie.
"""

ADRESSEN = {"temperatur": 3, "tor": 7, "kran": 12}
# Was die Sensoren an ihren Adressen gerade melden; der Sensor am Tor (7) antwortet nicht
ANTWORTEN = {3: 21.5, 12: 2400, 20: 55.0}


def halle_temperatur():
    """Liest den Temperatursensor der Halle und gibt °C zurück."""
    return ANTWORTEN[ADRESSEN["temperatur"]]


def tor_sensor():
    """Fragt den Sensor am Hallentor ab, der gerade nicht antwortet."""
    raise TimeoutError("keine Antwort von Adresse " + str(ADRESSEN["tor"]))


def kran_last():
    """Gibt die mittlere Last der Kranwaage in Kilogramm zurück; teilt dabei versehentlich durch 0."""
    summe = ANTWORTEN[ADRESSEN["kran"]]
    anzahl_messungen = 0
    return summe / anzahl_messungen


def feuchte_sensor():
    """Liest die Luftfeuchte in Prozent; die Adresse des Sensors fehlt in ADRESSEN."""
    return ANTWORTEN[ADRESSEN["feuchte"]]


def frage_ab(sensoren):
    """Fragt alle Sensoren ab und gibt das Tupel (werte, stoerungen) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


werte, stoerungen = frage_ab(
    [("temperatur", halle_temperatur), ("tor", tor_sensor), ("kran", kran_last), ("feuchte", feuchte_sensor)]
)
print("Werte:", werte)
print("Störungen:", stoerungen)
