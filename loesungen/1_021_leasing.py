# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_021_leasing.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_021_leasing

"""Aufgabe 1_021 – Kauf oder Leasing                             Stufe 1 ★☆☆☆☆

Eine Firma braucht neue Notebooks. Die IT-Abteilung kann sie kaufen
oder leasen. Beim Leasing mietet man die Geräte für eine feste Zeit
gegen eine monatliche Rate und gibt sie danach zurück; ein Kauf kostet
sofort viel Geld aus dem Investitionsbudget, also dem Geld, das in
diesem Jahr für Anschaffungen eingeplant ist. Die Leasingfirma vermietet
erst ab 5 Geräten. Das Team entscheidet nach diesen Regeln; es gilt die
erste Regel, die passt:

    1. Mindestens 5 Geräte und (Nutzung kürzer als 36 Monate
       oder kein Budget frei)                         Leasing
    2. Kein Budget frei                               Verschieben
    3. Mindestens 50 Geräte                           Kauf mit Mengenrabatt
    4. Sonst                                          Kauf

Das Programm fragt schon nach der Anzahl der Geräte, nach der geplanten
Nutzungsdauer in Monaten und ob Budget frei ist. Ergänzen Sie die
Entscheidung, die der Variablen empfehlung den passenden Text zuweist.
Bei den Eingaben 15, 24 und ja:

    15 Geräte für 24 Monate
    Empfehlung: Leasing

Bei den Eingaben 15, 48 und ja steht dort „Empfehlung: Kauf“, bei 3, 24
und nein „Empfehlung: Verschieben“.

Grenzen: Die Anzahl ist eine ganze Zahl von 1 bis 1000, die
Nutzungsdauer eine ganze Zahl von 1 bis 120, die letzte Antwort ist "ja"
oder "nein".

Hintergrund: Diese Übung verbindet alles über Bedingungen: Vergleiche wie
anzahl >= 5 liefern True oder False (Aufgabe 1_016), if, elif und else
wählen genau einen von mehreren Fällen, und zwar den ersten, dessen
Bedingung wahr ist (Aufgaben 1_017 bis 1_019), und and, or und not
verknüpfen Bedingungen (Aufgabe 1_020). Weil and stärker bindet als or,
braucht Regel 1 Klammern um den or-Teil:

    if alt >= 18 and (ticket == "ja" or gast == "ja"):

Die Reihenfolge der Regeln steckt in der Reihenfolge von if und elif:
Regel 2 muss nicht noch einmal „weniger als 5 Geräte“ prüfen, weil sie
nur drankommt, wenn Regel 1 nicht gepasst hat.
"""

anzahl = int(input("Wie viele Geräte? "))
monate = int(input("Nutzungsdauer in Monaten: "))
budget_frei = input("Ist Budget frei (ja/nein)? ") == "ja"
print(f"{anzahl} Geräte für {monate} Monate")

if anzahl >= 5 and (monate < 36 or not budget_frei):
    empfehlung = "Leasing"
elif not budget_frei:
    empfehlung = "Verschieben"
elif anzahl >= 50:
    empfehlung = "Kauf mit Mengenrabatt"
else:
    empfehlung = "Kauf"

print("Empfehlung:", empfehlung)


# Idee: Jede Regel wird zu einem Zweig, in derselben Reihenfolge: if für Regel 1 mit
# anzahl >= 5 and (monate < 36 or not budget_frei), elif not budget_frei für Regel 2,
# elif anzahl >= 50 für Regel 3 und else für Regel 4. Weil elif nur drankommt, wenn
# alles darüber falsch war, muss Regel 2 die Zahl der Geräte nicht noch einmal prüfen.
# Anderer Weg: jede Bedingung vollständig ausschreiben, etwa Regel 2 als
# elif anzahl < 5 and not budget_frei; das ist länger, aber jede Zeile für sich lesbar.
# Statt not budget_frei geht auch budget_frei == False.
# Typische Fehler: die Klammern in Regel 1 vergessen (dann wird bei 3 Geräten ohne
# Budget geleast), Regel 3 vor Regel 1 setzen (dann gibt es bei 80 Geräten und kurzer
# Nutzung Mengenrabatt statt Leasing) oder <= 36 statt < 36.
