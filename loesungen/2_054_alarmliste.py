# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_054_alarmliste.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_054_alarmliste

"""Aufgabe 2_054 – Alarmliste                                    Stufe 2 ★★☆☆☆

Die Monitoring-Zentrale einer Firma zeigt alle offenen Alarme in einer
Liste an, den ältesten vorn. Von jedem Alarm steht dort nur der Name
des Servers, der ihn ausgelöst hat; derselbe Server kann mehrere offene
Alarme haben:

    alarme = ["web01", "db01", "web01", "mail01", "web01"]

Zwei Dinge sollen gehen, beide ohne die angezeigte Liste selbst zu
verändern, denn an ihr hängt noch die Anzeige der Kollegen. Schreiben
Sie zwei Funktionen, die je eine neue Liste zurückgeben:

- `ohne_ersten(alarme, server)`: Die Bereitschaft quittiert einen Alarm
  von server, also bestätigt, dass sie sich darum kümmert. Er
  verschwindet aus der Liste, und zwar der älteste dieses Servers, also
  der erste, der in der Liste steht. Die übrigen bleiben in ihrer
  Reihenfolge.
- `ohne_alle(alarme, server)`: Der Server geht in die Wartung; alle seine
  Alarme verschwinden.

Hat server keinen Alarm in der Liste, ist die neue Liste eine Kopie der
alten.

    ohne_ersten(alarme, "web01")   →  ["db01", "web01", "mail01", "web01"]
    ohne_alle(alarme, "web01")     →  ["db01", "mail01"]
    ohne_alle(alarme, "fs01")      →  ["web01", "db01", "web01", "mail01", "web01"]

Benutzen Sie dafür weder remove() noch pop() oder index().

Grenzen: alarme hat 0 bis 100 000 Einträge, alle nicht leere Texte;
server ist ein nicht leerer Text.

Hintergrund: Aus Aufgabe 1_030 kennen Sie liste.remove(wert). Es
entfernt nur das erste Vorkommen, löst einen ValueError aus, wenn der
Wert fehlt, und verändert die Liste selbst, also auch die Anzeige der
Kollegen (Aufgabe 2_019). Wer in einer for-Schleife aus derselben Liste
entfernt, über die die Schleife läuft, überspringt Einträge:

    werte = ["a", "a", "b"]
    for wert in werte:
        if wert == "a":
            werte.remove(wert)
    print(werte)              # ["a", "b"] – das zweite "a" ist noch da

Nach dem Entfernen rückt alles eine Stelle nach vorn, die Schleife geht
aber zur nächsten Stelle weiter. Sicherer ist, eine neue Liste
aufzubauen und mit append nur die Einträge hineinzulegen, die bleiben
sollen. Soll nur das erste Vorkommen wegfallen, merkt man sich wie in
Aufgabe 2_053 etwas während der Schleife, hier in einer Variablen mit
True oder False, ob man schon eines übersprungen hat.
"""


def ohne_ersten(alarme, server):
    """Gibt eine neue Liste ohne den ersten Alarm von server zurück."""
    ergebnis = []
    schon_entfernt = False
    for alarm in alarme:
        if alarm == server and not schon_entfernt:
            schon_entfernt = True
        else:
            ergebnis.append(alarm)
    return ergebnis


def ohne_alle(alarme, server):
    """Gibt eine neue Liste ohne alle Alarme von server zurück."""
    ergebnis = []
    for alarm in alarme:
        if alarm != server:
            ergebnis.append(alarm)
    return ergebnis


alarme = ["web01", "db01", "web01", "mail01", "web01"]
print(ohne_ersten(alarme, "web01"))
print(ohne_alle(alarme, "web01"))
print(ohne_alle(alarme, "fs01"))


# Idee: Beide Funktionen legen eine neue leere Liste an und gehen die alte einmal mit for durch.
# ohne_alle hängt jeden Alarm an, der nicht von server stammt. ohne_ersten merkt sich in
# schon_entfernt, ob es den ersten passenden Alarm schon übersprungen hat: Der erste Treffer wird
# übersprungen und setzt den Merker auf True, alle anderen Einträge kommen in die neue Liste.
# Anderer Weg: Für ohne_ersten die Stelle des ersten Treffers in einer Schleife mit enumerate suchen
# und die Liste mit Slicing aus alarme[:stelle] + alarme[stelle + 1:] zusammensetzen (Aufgabe 2_018).
# Für ohne_alle geht später auch eine Comprehension [alarm for alarm in alarme if alarm != server]
# (Aufgabe 3_017).
# Typische Fehler: aus alarme selbst entfernen (verändert die Anzeige; in der for-Schleife werden
# außerdem Einträge übersprungen), in ohne_ersten jeden Treffer überspringen statt nur den ersten,
# vergessen, die Liste mit return zurückzugeben, oder bei einem fehlenden Server nichts zurückgeben.
