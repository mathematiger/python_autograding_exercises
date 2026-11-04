# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_026_formulartest.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_026_formulartest

"""Aufgabe 1_026 – Formulartest                                 Stufe 1 ★☆☆☆☆

Eine Firma hat ihr Anmeldeformular für Kundinnen und Kunden neu
gestaltet. In einem Usability-Test (einem Test, wie gut sich etwas
bedienen lässt) füllen mehrere Testpersonen das Formular aus, und
jemand misst mit der Stoppuhr, wie viele Sekunden jede braucht. Als
leicht bedienbar gilt das Formular für eine Person, wenn sie höchstens
90 Sekunden braucht. Das Programm fragt schon nach der Anzahl der
Testpersonen, legt zwei Variablen an und gibt am Ende das Ergebnis aus.
Ergänzen Sie dazwischen eine for-Schleife, die für jede Person nach
ihrer Zeit fragt, mit input("Sekunden von Person 1: ") und so weiter,
und eine Zeile ausgibt, ob sie in der Zeit war. Dabei zählt
in_der_zeit die Personen mit höchstens 90 Sekunden, und gesamt addiert
alle Zeiten. Bei den Eingaben 4, 75, 120, 90 und 61:

    Person 1: 75 Sekunden, in der Zeit
    Person 2: 120 Sekunden, zu langsam
    Person 3: 90 Sekunden, in der Zeit
    Person 4: 61 Sekunden, in der Zeit
    3 von 4 Personen waren in der Zeit.
    Durchschnitt: 86.5 Sekunden

Grenzen: Die Anzahl der Testpersonen ist eine ganze Zahl von 1 bis 30,
jede Zeit eine ganze Zahl von 1 bis 600.

Hintergrund: Diese Übung verbindet die letzten Aufgaben. for nummer in
range(1, anzahl + 1) zählt die Personen ab 1 (Aufgabe 1_023). Ein input
in der Schleife fragt bei jedem Durchlauf neu. Mit if/else (Aufgabe
1_018) entscheiden Sie in der Schleife für jede Person, welche Zeile
ausgegeben wird. Eine Zählvariable wächst nur, wenn die Bedingung
stimmt: in_der_zeit = in_der_zeit + 1 steht deshalb eingerückt unter
dem if. Die Summe aller Zeiten bilden Sie wie in Aufgabe 1_025 mit
gesamt = gesamt + sekunden, und zwar bei jeder Person.
"""

anzahl = int(input("Anzahl der Testpersonen: "))
in_der_zeit = 0
gesamt = 0

for nummer in range(1, anzahl + 1):
    sekunden = int(input(f"Sekunden von Person {nummer}: "))
    gesamt = gesamt + sekunden
    if sekunden <= 90:
        print(f"Person {nummer}: {sekunden} Sekunden, in der Zeit")
        in_der_zeit = in_der_zeit + 1
    else:
        print(f"Person {nummer}: {sekunden} Sekunden, zu langsam")

print(f"{in_der_zeit} von {anzahl} Personen waren in der Zeit.")
print(f"Durchschnitt: {gesamt / anzahl:.1f} Sekunden")


# Idee: Die Schleife läuft mit nummer von 1 bis anzahl. In jedem Durchlauf wird die Zeit eingelesen und
# zu gesamt addiert. Dann entscheidet if sekunden <= 90, welche Zeile ausgegeben wird; nur in diesem Zweig
# wächst in_der_zeit um 1. Nach der Schleife gibt der vorgegebene Code Zähler und Durchschnitt aus.
# Anderer Weg: Erst nur zählen und den Text in einer Variablen merken, etwa urteil = "zu langsam" und im if
# urteil = "in der Zeit", dann eine einzige print-Zeile mit f"…, {urteil}". Statt in_der_zeit könnte man
# auch die Langsamen zählen und am Ende anzahl - langsame ausgeben.
# Typische Fehler: < 90 statt <= 90 (90 Sekunden sind noch in der Zeit), range(anzahl) und dann „Person 0“,
# in_der_zeit = in_der_zeit + 1 nicht unter das if einrücken (dann zählt jede Person), gesamt nur im if
# erhöhen (dann fehlen die langsamen Zeiten im Durchschnitt) oder input vor die Schleife schreiben.
