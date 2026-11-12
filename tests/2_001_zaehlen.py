# Automatisch erzeugt aus lehrkraft/muster/2_001_zaehlen.py - nicht von Hand ändern.
# vorlage-hash: ed45b13e0519d95e
# text-hash: 1c60b4ec6b853878
# thema: kontrollfluss
# inhalt: for-Schleife

# Ausgabe sind die Zahlen 1 bis 5
if AUSGABE.startswith("0"):
    hinweis = "\nTipp: range(5) liefert 0 bis 4, range(1, 6) liefert 1 bis 5."
elif AUSGABE == "1\n2\n3\n4":
    hinweis = "\nTipp: range(1, 5) endet bei 4; die obere Grenze gehört nicht dazu."
else:
    hinweis = ""
assert AUSGABE == "1\n2\n3\n4\n5", f"Erwartet:\n1\n2\n3\n4\n5\nIhr Programm gibt aus:\n{AUSGABE}{hinweis}"

# Eine for-Schleife wird benutzt
assert verwendet("for"), "Benutzen Sie eine for-Schleife, statt fünfmal print zu schreiben."

import ast


def prints_im_programm():
    """Gibt die Zahl aller print-Aufrufe zurück und ob einer davon in einer for-Schleife keinen festen Wert ausgibt."""
    with open(__file__, encoding="utf-8-sig") as datei:
        baum = ast.parse(datei.read())
    anzahl = 0
    variabel_in_for = False
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Call) and isinstance(knoten.func, ast.Name) and knoten.func.id == "print":
            anzahl = anzahl + 1
        if isinstance(knoten, ast.For):
            for innen in ast.walk(knoten):
                if (
                    isinstance(innen, ast.Call)
                    and isinstance(innen.func, ast.Name)
                    and innen.func.id == "print"
                    and not all(isinstance(argument, ast.Constant) for argument in innen.args)
                ):
                    variabel_in_for = True
    return anzahl, variabel_in_for


# Die Zahlen kommen aus der Schleife, nicht fest hingeschrieben
anzahl_print, variabel_in_for = prints_im_programm()
assert anzahl_print == 1 and variabel_in_for, (
    f"Ihr Programm enthält {anzahl_print}-mal print; erwartet war genau ein print in der for-Schleife, "
    "das die Schleifenvariable ausgibt.\n"
    "Tipp: print(zahl) im eingerückten Block gibt bei jedem Durchlauf die aktuelle Zahl aus. "
    'Fest hingeschriebene Zahlen wie print("1\\n2\\n3\\n4\\n5") gelten nicht.'
)
