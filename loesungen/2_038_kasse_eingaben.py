# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_038_kasse_eingaben.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_038_kasse_eingaben

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
    positionsbetrag = einzelpreis * menge
    return positionsbetrag


def berechne_rabatt(gesamtbetrag):
    """Gibt den Rabatt in Euro zurück: 10 % ab 50 €, darunter 0."""
    if gesamtbetrag >= 50:
        rabattbetrag = gesamtbetrag * 0.1
    else:
        rabattbetrag = 0.0
    return rabattbetrag


def berechne_endbetrag(gesamtbetrag, rabattbetrag):
    """Gibt den Betrag nach Abzug des Rabatts zurück."""
    endbetrag = gesamtbetrag - rabattbetrag
    return endbetrag


def zeige_artikel(artikelname, einzelpreis, menge, positionsbetrag):
    """Gibt eine Artikelposition aus, Geldbeträge mit zwei Nachkommastellen."""
    print(f"{artikelname}: {menge} x {einzelpreis:.2f} € = {positionsbetrag:.2f} €")


def lies_einzelpreis(aufforderung):
    """Fragt so lange nach, bis eine Zahl größer als 0 eingegeben wird, und gibt sie als float zurück."""
    while True:
        text = input(aufforderung)
        try:
            preis = float(text)
        except ValueError:
            print(f"„{text}“ ist keine Zahl. Bitte geben Sie den Preis mit Punkt ein, z. B. 8.50.")
            continue
        if preis > 0:
            return preis
        print("Der Preis muss größer als 0 sein.")


def lies_anzahl(aufforderung):
    """Fragt so lange nach, bis eine ganze Zahl größer als 0 eingegeben wird, und gibt sie als int zurück."""
    while True:
        text = input(aufforderung)
        try:
            anzahl = int(text)
        except ValueError:
            print(f"„{text}“ ist keine ganze Zahl. Bitte geben Sie eine ganze Zahl ein.")
            continue
        if anzahl > 0:
            return anzahl
        print("Die Zahl muss größer als 0 sein.")


auswahl = ""
while auswahl != "0":
    print("=" * 30)
    print("TECH-SHOP".center(30))
    print("=" * 30)
    print("1 – Einkauf bearbeiten")
    print("2 – Preisanfrage berechnen")
    print("0 – Programm beenden")
    auswahl = input("Ihre Auswahl: ")
    if auswahl == "1":
        gesamtbetrag = 0.0
        anzahl = lies_anzahl("Anzahl der Artikelpositionen: ")
        for _ in range(anzahl):
            artikelname = input("Artikelname: ")
            einzelpreis = lies_einzelpreis("Einzelpreis in €: ")
            menge = lies_anzahl("Menge: ")
            positionsbetrag = berechne_positionsbetrag(einzelpreis, menge)
            zeige_artikel(artikelname, einzelpreis, menge, positionsbetrag)
            gesamtbetrag = gesamtbetrag + positionsbetrag
        rabattbetrag = berechne_rabatt(gesamtbetrag)
        endbetrag = berechne_endbetrag(gesamtbetrag, rabattbetrag)
        print(f"Gesamtbetrag: {gesamtbetrag:.2f} €")
        print(f"Rabatt: {rabattbetrag:.2f} €")
        print(f"Endbetrag: {endbetrag:.2f} €")
    elif auswahl == "2":
        artikelname = input("Artikelname: ")
        einzelpreis = lies_einzelpreis("Einzelpreis in €: ")
        menge = lies_anzahl("Menge: ")
        angebotsbetrag = berechne_positionsbetrag(einzelpreis, menge)
        rabattbetrag = berechne_rabatt(angebotsbetrag)
        angebotspreis = berechne_endbetrag(angebotsbetrag, rabattbetrag)
        print("Unverbindliches Preisangebot")
        zeige_artikel(artikelname, einzelpreis, menge, angebotsbetrag)
        print(f"Rabatt: {rabattbetrag:.2f} €")
        print(f"Angebotspreis: {angebotspreis:.2f} €")
    elif auswahl != "0":
        print("Ungültige Auswahl. Bitte geben Sie 1, 2 oder 0 ein.")


# Idee: lies_einzelpreis und lies_anzahl sind eine while-True-Schleife: input, im try umwandeln, bei
# ValueError eine Meldung und continue, danach mit if prüfen, ob die Zahl größer als 0 ist; nur dann
# return. Im Hauptprogramm aus 2_037 wird jedes float(input(...)) zu lies_einzelpreis(...) und jedes
# int(input(...)) zu lies_anzahl(...); alles andere bleibt, wie es war. Weil beide Abläufe dieselben
# Lesefunktionen benutzen, steht die Prüfung nur an einer Stelle.
#
# Anderer Weg: statt continue ein else-Block hinter dem except, in dem die Prüfung auf > 0 steht. Oder
# eine Schleife mit Merker gueltig = False, die läuft, bis gueltig wahr ist, und das return erst danach.
# Für ganze Zahlen ginge auch text.isdigit() statt try, aber dann muss man an "-3" und " 3" selbst denken.
#
# Typische Fehler: try um das ganze Hauptprogramm statt um die einzelne Umwandlung (dann bricht ein
# Fehler den Einkauf ab), die Prüfung auf > 0 vergessen (0 als Menge läuft durch), nach der Meldung
# nicht noch einmal fragen, int(float(text)) für die Menge (dann gilt „2.5“ als 2), except ohne
# ValueError (dann fängt man auch Fehler ab, die man nicht erwartet).
