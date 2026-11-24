"""Aufgabe 2_049 – Cäsar                                         Stufe 2 ★★☆☆☆

In der Schulung zur IT-Sicherheit sollen die neuen Auszubildenden sehen,
warum alte Verschlüsselungen heute nicht mehr reichen. Den Anfang macht
die Cäsar-Verschlüsselung, die schon im alten Rom benutzt wurde: Jeder
Buchstabe wird im Alphabet um eine feste Zahl von Stellen verschoben,
den Schlüssel. Mit Schlüssel 3 wird aus A ein D, aus B ein E und aus
Y ein B, denn nach Z geht es wieder bei A los. Entschlüsselt wird mit
dem negativen Schlüssel: Schlüssel -3 macht aus D wieder ein A.

Schreiben Sie die Funktion `verschluesseln(text, schluessel)`, die den
verschlüsselten Text zurückgibt:

- Großbuchstaben A bis Z werden verschoben und bleiben groß,
  Kleinbuchstaben a bis z werden verschoben und bleiben klein.
- Alle anderen Zeichen (Leerzeichen, Ziffern, Satzzeichen, auch die
  Umlaute ä, ö, ü und ß) bleiben, wie sie sind.

    verschluesseln("Angriff um 9 Uhr!", 3)    →  "Dqjulii xp 9 Xku!"
    verschluesseln("Dqjulii xp 9 Xku!", -3)   →  "Angriff um 9 Uhr!"
    verschluesseln("xyz", 3)                  →  "abc"
    verschluesseln("Grüße", 1)                →  "Hsüßf"

Grenzen: text hat 0 bis 100 000 Zeichen. schluessel ist eine ganze
Zahl von -1000 bis 1000; 26 und jedes Vielfache davon lassen den Text
also unverändert.

Hintergrund: Der Rechner speichert jedes Zeichen als Zahl. ord(zeichen)
liefert diese Zahl, chr(zahl) das Zeichen dazu:

    ord("A")  →  65      ord("B")  →  66      ord("Z")  →  90
    ord("a")  →  97      chr(68)   →  "D"

Die Großbuchstaben liegen also hintereinander bei 65 bis 90, die
Kleinbuchstaben bei 97 bis 122. ord(zeichen) - ord("A") ist die
Position eines Großbuchstabens im Alphabet, von 0 für A bis 25 für Z.
Verschiebt man diese Position und nimmt das Ergebnis % 26 (Aufgabe
1_009), bleibt sie im Bereich 0 bis 25, auch bei negativen Zahlen:
(1 - 3) % 26 ist 24. chr(position + ord("A")) macht daraus wieder einen
Buchstaben. Ob ein Zeichen ein Großbuchstabe ist, prüft "A" <= zeichen
<= "Z" (Kurzform für "A" <= zeichen and zeichen <= "Z", Aufgabe 1_020);
Texte vergleicht Python Zeichen für Zeichen nach diesen Zahlen.
Den neuen Text bauen Sie wie in Aufgabe 2_014 Zeichen für Zeichen auf.

Tipp: zeichen.isalpha() hilft hier nicht, denn es ist auch für ä und ß
wahr.
"""


def verschluesseln(text, schluessel):
    """Gibt den Text mit allen Buchstaben A–Z und a–z um schluessel Stellen verschoben zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(verschluesseln("Angriff um 9 Uhr!", 3))
print(verschluesseln("Dqjulii xp 9 Xku!", -3))
