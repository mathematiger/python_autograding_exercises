"""Aufgabe 2_035 – Schrittdauer                                  Stufe 2 ★★☆☆☆

Eine Softwarefirma will wissen, welche Schritte bei der Bearbeitung von
Kundenaufträgen am meisten Zeit kosten. Die Mitarbeitenden tragen dafür
ihre Zeiten von Hand in eine Zeiterfassung ein, die jeden Eintrag als
Textzeile exportiert: den Namen des Schritts, ein Semikolon und die Dauer
in ganzen Minuten. Danach kann, wieder nach einem Semikolon, ein Kommentar
folgen.

    Angebot prüfen;45
    Freigabe;120;Rückfrage beim Kunden

Weil von Hand getippt wird, sind manche Zeilen kaputt: Mal fehlt das Feld
für die Dauer ganz ("Freigabe" ohne Semikolon oder eine leere Zeile), mal
steht statt der Zahl etwas anderes oder gar nichts darin ("Freigabe;zwei
Stunden" oder "Freigabe;").

Vervollständigen Sie die Funktion `dauer(zeile)`. Sie zerlegt die Zeile mit
split(";") und gibt die Dauer als ganze Zahl zurück: das zweite Feld, mit
int(...) umgewandelt. Fehlt das zweite Feld oder lässt es sich nicht
umwandeln (auch weil es leer ist), gibt sie -1 zurück, statt abzustürzen;
eine echte Dauer ist nie negativ. Fangen Sie dafür den IndexError und den
ValueError ab, am einfachsten beide in einem einzigen except.

    dauer("Angebot prüfen;45")                    →  45
    dauer("Freigabe;120;Rückfrage beim Kunden")   →  120
    dauer("Test; 30 ")                            →  30
    dauer("Freigabe")                             →  -1
    dauer("Freigabe;zwei Stunden")                →  -1
    dauer("")                                     →  -1

Grenzen: zeile ist ein Text mit höchstens 100 Zeichen. Lässt sich das zweite
Feld umwandeln, ist die Dauer eine ganze Zahl von 0 bis 10 000; das zweite
Feld besteht aus den Ziffern 0 bis 9, Buchstaben, Leerzeichen und den
Zeichen ".", "," und "-". Leerzeichen am Anfang und am Ende des Felds
stören int nicht.

Hintergrund: int("zwei Stunden") löst einen ValueError aus (Aufgabe 2_033).
Bei "Freigabe" passiert ein anderer Fehler: "Freigabe".split(";") ergibt
["Freigabe"] (split, Aufgabe 2_015), eine Liste mit nur einem Element. Wer
dann auf teile[1] zugreift, bekommt einen IndexError, weil es diesen Index
nicht gibt. Will man mehrere Arten von Ausnahmen gleich behandeln, schreibt
man sie als Tupel (Aufgabe 2_010) in Klammern hinter except. Ein Beispiel
mit zwei anderen Ausnahmen: Eine Division durch 0 löst einen
ZeroDivisionError aus.

    try:
        schnitt = int(summe) / int(anzahl)
    except (ValueError, ZeroDivisionError):
        schnitt = 0

Der except-Block läuft, wenn eine der genannten Ausnahmen auftritt; jede
andere wird weiterhin gemeldet. Ein return beendet die Funktion auch mitten
im try- oder except-Block.
"""


def dauer(zeile):
    """Gibt die Dauer aus einer Protokollzeile in Minuten zurück, -1 bei einer kaputten Zeile."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(dauer("Angebot prüfen;45"))
print(dauer("Freigabe"))
