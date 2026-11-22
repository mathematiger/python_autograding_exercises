"""Aufgabe 2_050 – Häufigkeitsanalyse                            Stufe 2 ★★☆☆☆

Für eine Prozessanalyse werden die Kommentare aus der Webschnittstelle
eines alten Auftragssystems ausgewertet. Das Altsystem hat alle
Kommentare mit der Cäsar-Verschlüsselung aus Aufgabe 2_049 verschleiert,
aber niemand weiß mehr, mit welchem Schlüssel. Zum Glück verrät sich der
Schlüssel durch die Statistik: In deutschen Texten ist e mit großem
Abstand der häufigste Buchstabe. Ist im verschlüsselten Text h am
häufigsten, wurde vermutlich e um 3 Stellen auf h verschoben.

Die Funktion `verschiebe(text, schluessel)` ist vorgegeben; sie
verschiebt alle Buchstaben A–Z und a–z wie in Aufgabe 2_049. Schreiben
Sie drei Funktionen:

- `haeufigkeiten(text)` gibt eine Liste mit 26 ganzen Zahlen zurück: an
  Stelle 0, wie oft a im Text vorkommt, an Stelle 1 wie oft b, … bis
  Stelle 25 für z. Groß- und Kleinbuchstaben zählen zusammen (A wie a),
  alle anderen Zeichen zählen nicht.
- `schluessel_schaetzen(text)` sucht den häufigsten Buchstaben und gibt
  den Schlüssel zurück, der e auf ihn verschiebt, als Zahl von 0 bis 25.
  Sind mehrere Buchstaben gleich häufig, zählt der, der im Alphabet
  zuerst kommt. Ein Text ganz ohne Buchstaben hat den Schlüssel 0.
- `knacken(text)` gibt den entschlüsselten Text zurück, also den Text
  mit dem geschätzten Schlüssel zurückverschoben.

    haeufigkeiten("Abba!")[:3]               →  [2, 2, 0]
    schluessel_schaetzen("Hlq Ohhuhu Whvw")  →  3
    knacken("Hlq Ohhuhu Whvw")               →  "Ein Leerer Test"
    schluessel_schaetzen("a b")              →  22

Im letzten Beispiel sind a und b gleich häufig, also zählt a; von e
nach a sind es 22 Stellen vorwärts (oder 4 rückwärts).

Grenzen: text hat 0 bis 100 000 Zeichen, beliebige Zeichen auch außer
Buchstaben. Ihre Lösung soll den Text nur wenige Male durchgehen, nicht
für jeden der 26 Buchstaben einmal.

Hintergrund: Mit ord und chr (Aufgabe 2_049) rechnet man einen
Buchstaben in seine Position im Alphabet um und zurück: ord("c") -
ord("a") ist 2. Damit lässt sich eine Liste aus 26 Zählern direkt mit
der Position als Index erhöhen (zaehler[position] += 1), statt für jeden
Buchstaben eine eigene Variable zu haben; zeichen.lower() macht vorher
aus A ein a. Den Index des größten Werts in einer Liste liefert
werte.index(max(werte)); index findet dabei das erste Vorkommen. Diese
Art, eine Verschlüsselung über die Häufigkeit der Zeichen zu brechen,
heißt Häufigkeitsanalyse. Sie funktioniert umso besser, je länger der
Text ist; bei sehr kurzen Texten kann sie sich irren. Darum gilt die
Cäsar-Verschlüsselung längst als unsicher.
"""


def verschiebe(text, schluessel):
    """Verschiebt alle Buchstaben A–Z und a–z um schluessel Stellen (vorgegeben, wie Aufgabe 2_049)."""
    teile = []
    for zeichen in text:
        if "A" <= zeichen <= "Z":
            teile.append(chr((ord(zeichen) - ord("A") + schluessel) % 26 + ord("A")))
        elif "a" <= zeichen <= "z":
            teile.append(chr((ord(zeichen) - ord("a") + schluessel) % 26 + ord("a")))
        else:
            teile.append(zeichen)
    return "".join(teile)


def haeufigkeiten(text):
    """Gibt eine Liste mit 26 Zählern für a bis z zurück, Groß- und Kleinbuchstaben zusammen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def schluessel_schaetzen(text):
    """Gibt den Schlüssel zurück, der e auf den häufigsten Buchstaben verschiebt (0 bis 25)."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def knacken(text):
    """Gibt den mit dem geschätzten Schlüssel entschlüsselten Text zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


geheim = "Hlq Ohhuhu Whvw"
print(schluessel_schaetzen(geheim))
print(knacken(geheim))
