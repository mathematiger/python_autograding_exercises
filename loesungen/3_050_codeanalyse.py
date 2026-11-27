# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_050_codeanalyse.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_050_codeanalyse

r"""Aufgabe 3_050 – Codeanalyse                                   Stufe 3 ★★★☆☆

Ein Entwicklungsteam lässt jede Nacht ein Werkzeug zur statischen
Codeanalyse über sein Projekt laufen. Es liest den Quelltext, ohne ihn
auszuführen, und meldet Auffälligkeiten in Kategorien: stil (etwa zu
lange Zeilen), fehler (etwa eine Variable, die nie belegt wird) und
sicherheit (etwa ein Passwort im Code). Das Ergebnis kommt als CSV-Text:
Die erste Zeile nennt die Spalten, jede weitere gehört zu einem Modul
(einer Python-Datei), die Werte sind durch Kommas getrennt:

    modul,stil,fehler,sicherheit
    login.py,12,0,1
    kasse.py,3,2,0
    bericht.py,0,0,0

Für die Teambesprechung sollen Summen und Auffälligkeiten her. Schreiben
Sie drei Funktionen, die alle den CSV-Text bekommen:

- `spaltensummen(text)` gibt ein Dictionary zurück: für jede Spalte außer
  der ersten der Name → die Summe der Werte, in der Reihenfolge der
  Kopfzeile.
- `mit_summenzeile(text)` gibt einen neuen CSV-Text zurück: alle nicht
  leeren Zeilen des alten unverändert, dahinter eine Zeile, die in der
  ersten Spalte gesamt und dann die Summen enthält. Jede Zeile endet mit
  einem Zeilenumbruch.
- `auffaellige_module(text, spalte, grenze)` gibt die Namen der Module
  zurück, deren Wert in der Spalte spalte mindestens grenze ist, in der
  Reihenfolge des Textes.

    spaltensummen(text)                       →  {"stil": 15, "fehler": 2, "sicherheit": 1}
    mit_summenzeile(text)                     →  "modul,stil,fehler,sicherheit\nlogin.py,12,0,1\n…\ngesamt,15,2,1\n"
    auffaellige_module(text, "stil", 3)       →  ["login.py", "kasse.py"]

Die Kategorien und ihre Zahl hängen davon ab, wie das Werkzeug
eingestellt ist; verlassen Sie sich also nur auf die Kopfzeile.

Grenzen: Der Text beginnt mit der Kopfzeile; sie hat 2 bis 20 Spalten
mit verschiedenen Namen ohne Leerzeichen. Danach kommen 0 bis 10 000
Zeilen mit genau so vielen Feldern, dazwischen und am Ende können leere
Zeilen stehen (auch solche nur aus Leerzeichen; sie zählen als leer).
Die Zeilen sind durch "\n" getrennt, die letzte kann mit oder ohne
"\n" enden. Die erste Spalte ist ein Name ohne Komma, alle anderen
sind ganze Zahlen von 0 bis 100 000, um die auch Leerzeichen stehen
können. spalte ist der Name einer Spalte außer der ersten, grenze eine
ganze Zahl von 0 bis 100 000.

Hintergrund: CSV („comma-separated values“) ist das einfachste
Tabellenformat: eine Zeile je Datensatz, die Felder durch Kommas
getrennt, die erste Zeile mit den Spaltennamen. In Aufgabe 3_046 haben
Sie Zeilen schon mit split zerlegt. Hier kommt es auf die Kopfzeile an:
Erst sie sagt, welches Feld welche Bedeutung hat. Zerlegt man sie auch,
gehören Name und Wert über ihre Stelle zusammen, und zip (Aufgabe 2_022)
liefert die Paare:

    kopf = "artikel,montag,dienstag".split(",")      # ["artikel", "montag", "dienstag"]
    werte = "Maus, 4 ,7".split(",")                   # ["Maus", " 4 ", "7"]
    for name, wert in zip(kopf[1:], werte[1:]):
        print(name, int(wert))                         # int übergeht Leerzeichen am Rand

kopf.index("dienstag") ist 2, die Stelle der Spalte in jeder Zeile (index:
Aufgabe 3_049). Umgekehrt setzt ",".join(...) Felder wieder zu einer Zeile
zusammen; die Felder müssen dafür Texte sein (Aufgabe 2_015). So einfach geht
es nur, solange kein Feld selbst ein Komma enthält; für Felder wie "Meier,
Ada" in Anführungszeichen gibt es das Modul csv (nächste Aufgabe).
"""


def spaltensummen(text):
    """Gibt ein Dictionary Spaltenname → Summe für alle Spalten außer der ersten zurück."""
    zeilen = text.splitlines()
    kopf = zeilen[0].split(",")
    summen = {}
    for name in kopf[1:]:
        summen[name] = 0
    for zeile in zeilen[1:]:
        if zeile.strip() == "":
            continue
        felder = zeile.split(",")
        for name, wert in zip(kopf[1:], felder[1:]):
            summen[name] += int(wert)
    return summen


def mit_summenzeile(text):
    """Gibt den CSV-Text ohne leere Zeilen und mit einer Summenzeile gesamt am Ende zurück."""
    ergebnis = ""
    for zeile in text.splitlines():
        if zeile.strip() != "":
            ergebnis += zeile + "\n"
    felder = ["gesamt"]
    for summe in spaltensummen(text).values():
        felder.append(str(summe))
    return ergebnis + ",".join(felder) + "\n"


def auffaellige_module(text, spalte, grenze):
    """Gibt die Module zurück, deren Wert in der Spalte mindestens grenze ist."""
    zeilen = text.splitlines()
    stelle = zeilen[0].split(",").index(spalte)
    module = []
    for zeile in zeilen[1:]:
        if zeile.strip() == "":
            continue
        felder = zeile.split(",")
        if int(felder[stelle]) >= grenze:
            module.append(felder[0])
    return module


text = "modul,stil,fehler,sicherheit\nlogin.py,12,0,1\nkasse.py,3,2,0\nbericht.py,0,0,0\n"
print(spaltensummen(text))
print(mit_summenzeile(text))
print(auffaellige_module(text, "stil", 3))


# Idee: text.splitlines() liefert die Zeilen, die erste mit split(",") die Spaltennamen. spaltensummen
# legt für jeden Namen ab der zweiten Stelle eine Summe 0 an, zerlegt jede nicht leere Zeile und
# addiert mit zip(kopf[1:], felder[1:]) jeden Wert als int zur passenden Summe. mit_summenzeile
# sammelt die nicht leeren Zeilen mit "\n" und hängt ",".join(["gesamt"] + Summen als Text) an.
# auffaellige_module sucht mit kopf.index(spalte) die Stelle und vergleicht dort mit >= grenze.
# Anderer Weg: statt zip mit for stelle in range(1, len(kopf)) und felder[stelle]; die Summenzeile
# geht auch mit "\n".join(...) über die nicht leeren Zeilen + "\n"; die Module ließen sich mit einer Comprehension sammeln.
# Typische Fehler: die Kopfzeile mitsummieren (ValueError bei int("stil")), Spalten fest mit Namen
# oder Stellen hinschreiben, leere Zeilen nicht überspringen, als Text vergleichen ("10" < "9"),
# int-Werte in join (TypeError) oder den Zeilenumbruch nach der Summenzeile vergessen.
# Laufzeit: O(z · s) für z Zeilen mit s Spalten; jedes Feld wird einmal zerlegt und addiert.
