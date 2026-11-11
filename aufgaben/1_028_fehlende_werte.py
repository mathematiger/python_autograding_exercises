"""Aufgabe 1_028 – Fehlende Werte                                Stufe 1 ★☆☆☆☆

Eine Firma will die Telefonnummern ihrer Lieferanten in ein neues
System übernehmen. Vorher prüft sie die Datenqualität: Wie viele
Datensätze haben überhaupt eine Telefonnummer? Die Spalte telefon wurde
aus der Datenbank exportiert, die Werte stehen durch Kommas getrennt
hintereinander. Wo in der Datenbank kein Wert steht (dort heißt das
NULL), hat der Export das Wort NULL hineingeschrieben. Der vorgegebene Code macht daraus eine Liste, legt den Zähler
fehlend an und gibt am Ende das Ergebnis aus. Ergänzen Sie dazwischen
eine for-Schleife über die Liste nummern, die mit fehlend zählt, wie
viele Werte NULL sind. Bei der Eingabe
0211 4711,NULL,030 1234,NULL,NULL,089 555:

    3 von 6 Telefonnummern fehlen.
    Vollständigkeit: 50.0 %

Grenzen: Die Spalte hat 1 bis 50 Werte. Jeder Wert ist NULL oder eine
Telefonnummer aus Ziffern und Leerzeichen.

Hintergrund: Eine for-Schleife kann nicht nur über range laufen,
sondern über jede Liste (Aufgabe 1_027): for wert in werte: nimmt bei
jedem Durchlauf das nächste Element der Liste und speichert es unter
dem Namen wert, vom ersten bis zum letzten. Bei werte = ["a", "b"]
läuft die Schleife zweimal, erst mit wert = "a", dann mit wert = "b".
Einen Index braucht man dafür nicht. Gezählt wird wie in Aufgabe 1_026
mit einem if und fehlend = fehlend + 1 darunter.
"""

eingabe = input("Spalte telefon, durch Kommas getrennt: ")
nummern = eingabe.split(",")
fehlend = 0

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

vollstaendig = (len(nummern) - fehlend) / len(nummern) * 100
print(f"{fehlend} von {len(nummern)} Telefonnummern fehlen.")
print(f"Vollständigkeit: {vollstaendig:.1f} %")
