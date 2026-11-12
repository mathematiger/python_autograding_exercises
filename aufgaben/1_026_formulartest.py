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
in der Schleife fragt bei jedem Durchlauf neu; wie in Aufgabe 1_004
wandeln Sie die Eingabe mit int(...) in eine Zahl um, und die Frage
setzen Sie wie in Aufgabe 1_010 mit einem f-String zusammen. Mit
if/else (Aufgabe 1_018) entscheiden Sie in der Schleife für jede
Person, welche Zeile ausgegeben wird. Eine Zählvariable wächst nur,
wenn die Bedingung stimmt: in_der_zeit = in_der_zeit + 1 steht deshalb eingerückt unter
dem if. Die Summe aller Zeiten bilden Sie wie in Aufgabe 1_025 mit
gesamt = gesamt + sekunden, und zwar bei jeder Person.
"""

anzahl = int(input("Anzahl der Testpersonen: "))
in_der_zeit = 0
gesamt = 0

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

print(f"{in_der_zeit} von {anzahl} Personen waren in der Zeit.")
print(f"Durchschnitt: {gesamt / anzahl:.1f} Sekunden")
