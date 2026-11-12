"""Aufgabe 2_037 – Kasse                                         Stufe 2 ★★☆☆☆

Der TECH-SHOP, ein kleiner Laden für Computerzubehör, braucht ein
Konsolenprogramm für die Kasse. Es soll zwei Dinge können: einen Einkauf
abrechnen und einem Kunden ein unverbindliches Preisangebot machen. Für beide
gilt dieselbe Rabattregel: Ab 50 € (einschließlich) gibt es 10 % Rabatt,
darunter keinen. Damit die Regel nur an einer Stelle steht, benutzen beide
Abläufe dieselben Funktionen.

1. Schreiben Sie die vier Funktionen:

   - berechne_positionsbetrag(einzelpreis, menge) gibt Einzelpreis mal Menge
     zurück.
   - berechne_rabatt(gesamtbetrag) gibt den Rabatt in Euro zurück: 10 % des
     Gesamtbetrags ab 50 €, sonst 0.
   - berechne_endbetrag(gesamtbetrag, rabattbetrag) gibt den Gesamtbetrag
     abzüglich des Rabatts zurück.
   - zeige_artikel(artikelname, einzelpreis, menge, positionsbetrag) gibt
     eine Artikelposition übersichtlich aus, Einzelpreis und Positionsbetrag
     mit zwei Nachkommastellen, zum Beispiel:

         Maus: 2 x 15.00 € = 30.00 €

   Die drei berechne-Funktionen rechnen nur: kein input, kein print, alle
   Werte kommen über die Parameter. zeige_artikel gibt nur aus und braucht
   kein return.

       berechne_positionsbetrag(15.0, 2)  →  30.0
       berechne_rabatt(54.0)              →  5.4
       berechne_rabatt(49.0)              →  0
       berechne_endbetrag(54.0, 5.4)      →  48.6

2. Schreiben Sie darunter das Hauptprogramm. Es zeigt dieses Menü:

       ==============================
                 TECH-SHOP
       ==============================
       1 – Einkauf bearbeiten
       2 – Preisanfrage berechnen
       0 – Programm beenden

   Dann liest es die Auswahl mit input ein. Nach jeder Aktion erscheint das
   Menü wieder, bis jemand 0 wählt; dann endet das Programm. Bei jeder
   anderen Eingabe als 1, 2 oder 0 gibt es einen Hinweis aus und zeigt das
   Menü erneut.

3. Bei 1 (Einkauf) fragt das Programm nach der Anzahl der Artikelpositionen
   und dann für jede Position nach Artikelname, Einzelpreis und Menge, in
   dieser Reihenfolge. Jede Position gibt es gleich mit zeige_artikel aus.
   Nach der letzten Position gibt es drei Zeilen aus, die mit „Gesamtbetrag“,
   „Rabatt“ und „Endbetrag“ beginnen, gefolgt vom Betrag. Der Rabatt gilt für
   den ganzen Einkauf, nicht für jede Position einzeln. Mit den Eingaben 1,
   2, USB-Kabel, 8, 3, Maus, 15, 2 und am Ende 0:

       USB-Kabel: 3 x 8.00 € = 24.00 €
       Maus: 2 x 15.00 € = 30.00 €
       Gesamtbetrag: 54.00 €
       Rabatt: 5.40 €
       Endbetrag: 48.60 €

   Jeder Einkauf beginnt wieder bei 0 €.

4. Bei 2 (Preisanfrage) fragt das Programm nach Artikelname, Einzelpreis und
   Menge. Es gibt die Überschrift „Unverbindliches Preisangebot“ aus, dann
   die Position mit zeige_artikel und zwei Zeilen, die mit „Rabatt“ und
   „Angebotspreis“ beginnen. Mit den Eingaben 2, USB-Kabel, 8, 10 und 0:

       Unverbindliches Preisangebot
       USB-Kabel: 10 x 8.00 € = 80.00 €
       Rabatt: 8.00 €
       Angebotspreis: 72.00 €

Alle Geldbeträge haben zwei Nachkommastellen. Wie die Zeile von zeige_artikel
genau aussieht und was im Hinweis steht, entscheiden Sie.

Ungültige Eingaben wie „acht“ als Preis oder 0 als Menge müssen Sie hier noch
nicht abfangen; das ist die Erweiterung in Aufgabe 2_038.

Grenzen: Die Eingaben sind gültig. Anzahl der Positionen und Menge sind ganze
Zahlen mit 1 ≤ anzahl ≤ 100 und 1 ≤ menge ≤ 1000, der Einzelpreis ist eine
Zahl mit Punkt und höchstens zwei Nachkommastellen, 0.01 ≤ einzelpreis ≤
10 000. Ein Artikelname ist ein nicht leerer Text mit höchstens 30 Zeichen.
Die Menüauswahl kann ein beliebiger Text sein.

Hintergrund: Ein großes Programm wird übersichtlich, wenn jede Funktion genau
eine Aufgabe hat. Die berechne-Funktionen bekommen ihre Werte als Parameter
und liefern das Ergebnis mit return (Aufgabe 2_002); was sie intern anlegen,
sind lokale Variablen (Aufgabe 2_013). Weil sie weder fragen noch ausgeben,
kann man sie überall wiederverwenden: im Einkauf genauso wie in der
Preisanfrage. Ändert sich die Rabattregel, ändert man sie nur in
berechne_rabatt. Eine Funktion testen Sie für sich, bevor Sie sie einbauen:

    print(berechne_positionsbetrag(15.0, 2))   # erwartet: 30.0

Ein Menü ist eine while-Schleife (Aufgabe 2_004), die bei jedem Durchlauf
eine Eingabe liest und mit if/elif/else (Aufgabe 1_019) entscheidet, was zu
tun ist. Sie läuft, bis die Eingabe "0" ist:

    auswahl = ""
    while auswahl != "0":
        auswahl = input("Ihre Auswahl: ")
        if auswahl == "1":
            ...

Lesen Sie die Auswahl als Text ein und vergleichen Sie mit "1", "2" und
"0"; so stürzt das Programm bei „abc“ nicht ab. Die Positionen eines
Einkaufs gehen Sie mit for und range durch (Aufgabe 2_001) und summieren sie
wie in Aufgabe 1_025. Zwei Nachkommastellen bekommen Sie mit
f"{betrag:.2f}" (Aufgabe 1_010).
"""


def berechne_positionsbetrag(einzelpreis, menge):
    """Gibt den Betrag einer Artikelposition zurück: Einzelpreis mal Menge."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def berechne_rabatt(gesamtbetrag):
    """Gibt den Rabatt in Euro zurück: 10 % ab 50 €, darunter 0."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def berechne_endbetrag(gesamtbetrag, rabattbetrag):
    """Gibt den Betrag nach Abzug des Rabatts zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def zeige_artikel(artikelname, einzelpreis, menge, positionsbetrag):
    """Gibt eine Artikelposition aus, Geldbeträge mit zwei Nachkommastellen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
