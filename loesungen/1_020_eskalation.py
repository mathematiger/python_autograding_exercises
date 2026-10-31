# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_020_eskalation.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_020_eskalation

"""Aufgabe 1_020 – Eskalation                                    Stufe 1 ★☆☆☆☆

Beim IT-Support einer Firma kommen täglich viele Tickets an, also
Meldungen über Störungen oder Wünsche. Bleibt ein Ticket zu lange liegen,
wird es eskaliert: Es geht an die nächste Supportstufe mit erfahreneren
Leuten. Die Regel des Teams:

- Ein Ticket mit Priorität "hoch" wird eskaliert, sobald es seit
  mindestens 2 Stunden offen ist.
- Jedes andere Ticket wird eskaliert, sobald es seit mindestens 24
  Stunden offen ist.
- Wartet das Ticket aber auf eine Rückmeldung des Kunden, wird es nie
  eskaliert, denn dann kann der Support gerade nichts tun.

Das Programm fragt schon nach der Priorität, den Stunden und ob das
Ticket auf den Kunden wartet, und gibt die Entscheidung aus. Ergänzen
Sie die eine Zeile, die eskalieren auf True oder False setzt. Bei den
Eingaben hoch, 3 und nein:

    Priorität hoch, seit 3 Stunden offen
    Eskalieren: ja

Bei den Eingaben niedrig, 3 und nein steht dort „Eskalieren: nein“.

Grenzen: Die Priorität ist "hoch", "mittel" oder "niedrig", die Stunden
sind eine ganze Zahl von 0 bis 1000, die letzte Antwort ist "ja" oder
"nein".

Hintergrund: Bedingungen lassen sich verknüpfen. a and b ist nur True,
wenn beide True sind; a or b ist True, wenn mindestens eine True ist;
not a dreht True und False um. Wie bei Punkt- vor Strichrechnung bindet
not am stärksten, dann and, dann or. Klammern machen die Absicht
deutlich:

    frei = not krank and (tag == "Samstag" or tag == "Sonntag")

Das Ergebnis ist wieder True oder False und kann in einer Variablen
stehen wie jede andere Zahl oder jeder Text.
"""

prioritaet = input("Priorität (hoch, mittel, niedrig): ")
stunden = int(input("Seit wie vielen Stunden offen? "))
wartet = input("Wartet das Ticket auf den Kunden (ja/nein)? ") == "ja"
print(f"Priorität {prioritaet}, seit {stunden} Stunden offen")

eskalieren = not wartet and ((prioritaet == "hoch" and stunden >= 2) or stunden >= 24)

if eskalieren:
    print("Eskalieren: ja")
else:
    print("Eskalieren: nein")


# Idee: Die Regel Wort für Wort übersetzen: Das Ticket wartet nicht (not wartet), und es ist entweder
# hoch und mindestens 2 Stunden offen oder mindestens 24 Stunden offen. Die Klammer um den or-Teil ist
# nötig, sonst würde not wartet nur zum ersten Teil gehören.
# Anderer Weg: mit if und elif nacheinander prüfen und eskalieren in jedem Fall zuweisen, etwa zuerst
# if wartet: eskalieren = False. Das sind aber mehr Zeilen. Auch wartet == False statt not wartet geht.
# Typische Fehler: die Klammer um den or-Teil vergessen (dann wird ein Ticket, das auf den Kunden
# wartet, nach 24 Stunden doch eskaliert), > statt >= oder prioritaet == hoch ohne Anführungszeichen
# (dann sucht Python eine Variable namens hoch).
