"""Aufgabe 1_049 – Ratedauer                                     Stufe 1 ★☆☆☆☆

Das Sicherheitsteam einer Firma will in einer Schulung zeigen, warum
lange Passwörter besser sind. Ein Angreifer, der ein Passwort durch
Ausprobieren errät, muss im schlimmsten Fall alle möglichen Passwörter
dieser Länge durchgehen. Bei 62 Zeichen (Groß- und Kleinbuchstaben und
Ziffern) und 10 Milliarden Versuchen pro Sekunde rechnet das Programm
unten aus, wie viele Jahre das dauert, und bewertet das Ergebnis.

Ein Kollege hat das Programm schon aufgeräumt: Alles steht in
Funktionen, der Ablauf in der Funktion main. Gestartet wird aber
nichts, denn main wird nirgends aufgerufen. Außerdem will das Team des
Passwortportals die Funktion bewertung aus dieser Datei mit import
übernehmen; dabei darf das Programm weder etwas fragen noch ausgeben.
Ergänzen Sie:

- In main eine Zeile, die die Bewertung ausgibt, zum Beispiel
  Bewertung: mittel. Benutzen Sie dafür die Funktion bewertung.
- Ganz unten zwei Zeilen, die main aufrufen, aber nur, wenn die Datei
  selbst gestartet wird, nicht beim import.

Bei Eingabe 10 gibt das Programm aus:

    Mögliche Passwörter: 839299365868340224
    Jahre zum Durchprobieren: 2.7
    Bewertung: mittel

Grenzen: Die Länge ist eine ganze Zahl von 1 bis 30.

Hintergrund: Startet man eine Datei mit python3 ratedauer.py, hat die
Variable __name__ den Wert "__main__"; holt eine andere Datei sie mit
import ratedauer, ist __name__ dagegen "ratedauer". Darum steht der
Aufruf des Hauptprogramms am Ende in einem if:

    def main():
        print("Hallo")

    if __name__ == "__main__":
        main()

So läuft main nur beim Starten, und wer importiert, bekommt nur die
Funktionen. Wie man eigene Funktionen schreibt und aufruft, kennen Sie
aus Aufgabe 1_037 und 1_038.
"""

ZEICHENVORRAT = 62  # Groß- und Kleinbuchstaben und Ziffern
VERSUCHE_PRO_SEKUNDE = 10_000_000_000
SEKUNDEN_PRO_JAHR = 365 * 24 * 60 * 60


def kombinationen(laenge):
    """Gibt zurück, wie viele Passwörter dieser Länge es gibt."""
    return ZEICHENVORRAT**laenge


def jahre_zum_raten(laenge):
    """Gibt zurück, wie viele Jahre das Durchprobieren aller Passwörter dieser Länge dauert."""
    return kombinationen(laenge) / VERSUCHE_PRO_SEKUNDE / SEKUNDEN_PRO_JAHR


def bewertung(jahre):
    """Gibt unsicher (unter 1 Jahr), mittel (unter 100 Jahren) oder sicher zurück."""
    if jahre < 1:
        return "unsicher"
    if jahre < 100:
        return "mittel"
    return "sicher"


def main():
    """Fragt die Länge ab und gibt Anzahl, Dauer und Bewertung aus."""
    laenge = int(input("Länge des Passworts: "))
    jahre = jahre_zum_raten(laenge)
    print(f"Mögliche Passwörter: {kombinationen(laenge)}")
    print(f"Jahre zum Durchprobieren: {jahre:.1f}")
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
