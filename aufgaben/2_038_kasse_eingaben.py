"""Aufgabe 2_038 – Kasse mit Eingabeprüfung                       Stufe 2 ★★☆☆☆

Die Kasse des TECH-SHOPs aus Aufgabe 2_037 ist im Einsatz, und schon am
ersten Tag stürzt sie ab: Jemand hat beim Preis „acht“ getippt, jemand
anderes bei der Menge eine 0. Die Kasse soll solche Eingaben jetzt abfangen,
eine verständliche Meldung ausgeben und dieselbe Frage noch einmal stellen.

Haben Sie Aufgabe 2_037 gelöst, übernehmen Sie Ihre vier Funktionen und Ihr
Hauptprogramm in diese Datei und ersetzen nur die Umwandlungen der
Eingaben. Sonst schreiben Sie alles neu; die Regeln aus 2_037 stehen unten
noch einmal knapp.

1. Schreiben Sie zwei neue Funktionen. Beide fragen mit input(aufforderung)
   so lange nach, bis die Eingabe gültig ist, und geben bei jeder
   ungültigen Eingabe eine Meldung aus:

   - lies_einzelpreis(aufforderung) gibt den Preis als float zurück. Gültig
     ist eine Zahl größer als 0.
   - lies_anzahl(aufforderung) gibt die Zahl als int zurück. Gültig ist eine
     ganze Zahl größer als 0. Sie dient für die Menge und für die Anzahl der
     Artikelpositionen.

       lies_einzelpreis("Einzelpreis: ")   Eingaben acht, -3, 8.5   →  8.5
       lies_anzahl("Menge: ")              Eingaben 0, 2.5, 3       →  3

2. Das Hauptprogramm liest Einzelpreise, Mengen und die Anzahl der Positionen
   nur noch mit diesen beiden Funktionen ein. Eine falsche Eingabe darf das
   Programm nicht beenden. Mit den Eingaben 1, -2, 1, Maus, acht, 15, 0, 2
   und am Ende 0 rechnet es den Einkauf von 2 Mäusen zu je 15 € ab, mit drei
   Meldungen dazwischen.

Die Regeln aus 2_037: Die Funktionen berechne_positionsbetrag(einzelpreis,
menge), berechne_rabatt(gesamtbetrag) (10 % ab 50 € einschließlich, sonst 0)
und berechne_endbetrag(gesamtbetrag, rabattbetrag) rechnen nur und geben das
Ergebnis mit return zurück; zeige_artikel(artikelname, einzelpreis, menge,
positionsbetrag) gibt eine Position aus. Das Menü

    ==============================
              TECH-SHOP
    ==============================
    1 – Einkauf bearbeiten
    2 – Preisanfrage berechnen
    0 – Programm beenden

erscheint nach jeder Aktion wieder, bis jemand 0 wählt; andere Eingaben
bekommen einen Hinweis. Bei 1 fragt das Programm nach der Anzahl der
Positionen und dann je Position nach Artikelname, Einzelpreis und Menge,
gibt jede Position mit zeige_artikel aus und danach Zeilen, die mit
„Gesamtbetrag“, „Rabatt“ und „Endbetrag“ beginnen. Bei 2 fragt es nach
Artikelname, Einzelpreis und Menge und gibt „Unverbindliches Preisangebot“,
die Position und Zeilen mit „Rabatt“ und „Angebotspreis“ aus. Alle
Geldbeträge haben zwei Nachkommastellen.

Grenzen: Jede Eingabe kann ein beliebiger Text mit höchstens 30 Zeichen
sein. Gültige Eingaben liegen in den Grenzen von Aufgabe 2_037: Anzahl der
Positionen bis 100, Menge bis 1000, Einzelpreis mit Punkt, höchstens zwei
Nachkommastellen und bis 10 000.

Hintergrund: float(...) und int(...) lösen bei einem Text, der keine passende
Zahl ist, einen ValueError aus; den fangen Sie mit try/except ab (Aufgabe
2_033). Für int ist auch „2.5“ kein gültiger Text. Eine Zahl wie 0 oder -3
lässt sich dagegen umwandeln, sie ist nur nicht erlaubt; das prüfen Sie
danach mit if. Damit die Frage wiederholt wird, steht alles in einer
Schleife, die erst return verlässt:

    while True:
        text = input(aufforderung)
        try:
            zahl = int(text)
        except ValueError:
            print("Bitte geben Sie eine ganze Zahl ein.")
            continue
        if zahl > 0:
            return zahl
        print("Die Zahl muss größer als 0 sein.")

continue springt sofort zur nächsten Runde (Aufgabe 2_008). Ein return in
einer Schleife beendet Schleife und Funktion zugleich.
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


def lies_einzelpreis(aufforderung):
    """Fragt so lange nach, bis eine Zahl größer als 0 eingegeben wird, und gibt sie als float zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def lies_anzahl(aufforderung):
    """Fragt so lange nach, bis eine ganze Zahl größer als 0 eingegeben wird, und gibt sie als int zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
