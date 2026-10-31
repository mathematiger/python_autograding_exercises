"""Aufgabe 2_019 – Messreihe bereinigen                          Stufe 2 ★★☆☆☆

Ein Monitoring-Werkzeug misst jede Minute die CPU-Auslastung eines
Servers in Prozent und sammelt die Werte in einer Liste. Bevor daraus
ein Diagramm wird, muss die Messreihe bereinigt werden. Die Liste ist
lang und wird an vielen Stellen im Programm benutzt; darum sollen die
Funktionen nicht eine neue Liste liefern, sondern die vorhandene Liste
selbst ändern, sodass jeder, der sie benutzt, die bereinigten Werte
sieht.

Schreiben Sie zwei Funktionen:

- `entferne_ausfaelle(messwerte)`: Konnte der Sensor nicht messen, steht
  in der Liste -1. Die Funktion entfernt alle -1 aus der Liste
  messwerte selbst; die Reihenfolge der übrigen Werte bleibt gleich. Sie
  gibt nichts zurück.
- `kappe(messwerte, obergrenze)`: Manche Werte sind durch einen
  Messfehler zu groß. Die Funktion ersetzt in der Liste selbst jeden
  Wert über obergrenze durch obergrenze und gibt zurück, wie viele Werte
  sie ersetzt hat.

    cpu = [12, -1, 47, 130, -1, 99]
    entferne_ausfaelle(cpu)
    cpu                →  [12, 47, 130, 99]
    kappe(cpu, 100)    →  1
    cpu                →  [12, 47, 100, 99]

Grenzen: messwerte ist eine Liste ganzer Zahlen von -1 bis 1000 mit
0 ≤ len(messwerte) ≤ 10 000; bei kappe kommt -1 nicht mehr vor.
0 ≤ obergrenze ≤ 1000.

Hintergrund: Eine Funktion bekommt keine Kopie, sondern das Objekt
selbst (Aufgabe 2_018). Ob sie es ändern kann, hängt vom Typ ab. Listen
sind veränderlich: liste[i] = wert, liste.append(wert) oder
liste.remove(wert) ändern das Objekt, und der Aufrufer sieht die
Änderung. Zahlen, Texte und Tupel sind unveränderlich: Es gibt keine
Anweisung, die die Zahl 5 in eine 6 verwandelt. zahl = zahl + 1 legt eine
neue Zahl an und gibt ihr den Namen zahl, nur innerhalb der Funktion.

Genau so wirkt eine Zuweisung an den Parameter auch bei Listen: Schreibt
die Funktion werte = [1, 2], zeigt nur ihr lokaler Name auf eine neue
Liste; die Liste des Aufrufers bleibt, wie sie war. Den ganzen Inhalt
der Liste selbst ersetzt man dagegen mit einer Zuweisung an ein Slice:

    def leere(werte):
        werte = []          # wirkt nur lokal
    def leere_wirklich(werte):
        werte[:] = []       # ändert die Liste des Aufrufers

Darum gibt kappe die Anzahl mit return zurück: Eine Zahl, die man ihr
übergibt, könnte sie nicht für den Aufrufer ändern.
"""


def entferne_ausfaelle(messwerte):
    """Entfernt alle -1 aus der Liste messwerte selbst."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def kappe(messwerte, obergrenze):
    """Ersetzt in messwerte jeden Wert über obergrenze durch obergrenze; gibt die Zahl der Ersetzungen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


cpu = [12, -1, 47, 130, -1, 99]
entferne_ausfaelle(cpu)
print(cpu)
print(kappe(cpu, 100))
print(cpu)
