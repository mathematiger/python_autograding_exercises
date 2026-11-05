"""Aufgabe 1_028 – Ortsangaben                                  Stufe 1 ★☆☆☆☆

In der Kundendatenbank eines Versandhändlers wurde der Wohnort jahrelang
von Hand eingetippt. Deshalb steht derselbe Ort in verschiedenen
Schreibweisen darin, mal "Paderborn", mal "paderborn", mal "PADERBORN".
Bevor die Datensätze bereinigt werden, will das Datenbankteam wissen,
welche Einträge zu einem Ort gehören. Die Wohnorte stehen schon in der
Liste orte, und das Programm fragt nach dem gesuchten Ort. Ergänzen
Sie eine for-Schleife über die Liste orte: Für jeden Eintrag, der ohne
Rücksicht auf Groß- und Kleinschreibung gleich dem gesuchten Ort ist,
gibt sie "Treffer: " und den Eintrag so aus, wie er in der Liste
steht, und erhöht treffer um 1. Bei Eingabe Paderborn:

    Treffer: Paderborn
    Treffer: paderborn
    Treffer: PADERBORN
    3 Einträge zu Paderborn

Grenzen: Der gesuchte Ort ist ein Wort aus 1 bis 30 Buchstaben ohne
Umlaute, in beliebiger Schreibweise.

Hintergrund: Eine for-Schleife kann nicht nur über range (Aufgabe
1_022), sondern direkt über eine Liste laufen: for ort in orte: nimmt
beim ersten Durchlauf den ersten Eintrag der Liste in die Variable
ort, beim zweiten den zweiten und so weiter, bis die Liste zu Ende
ist. Einen Index braucht man dafür nicht. Groß- und Kleinschreibung
gleichen Sie aus, indem Sie beide Texte mit lower() (Aufgabe 1_013)
in Kleinbuchstaben vergleichen.
"""

orte = ["Paderborn", "Bielefeld", "paderborn", "Detmold", "PADERBORN", "bielefeld", "Lemgo"]
gesucht = input("Gesuchter Ort: ")
treffer = 0

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

print(f"{treffer} Einträge zu {gesucht}")
