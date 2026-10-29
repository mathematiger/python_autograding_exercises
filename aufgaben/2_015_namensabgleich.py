"""Aufgabe 2_015 – Namensabgleich                                Stufe 2 ★★☆☆☆

Eine Firma führt zwei Kundendatenbanken zusammen. In der alten stehen die
Namen als "Vorname Nachname", oft mit überflüssigen Leerzeichen, weil sie
von Hand eingetippt wurden: "  Anna   Maria Schulz ". In der neuen stehen
sie als "Nachname, Vornamen": "Schulz, Anna Maria". Um doppelte Kunden zu
finden, sollen alle alten Namen in die neue Schreibweise gebracht werden.

Schreiben Sie die Funktion `neue_schreibweise(name)`. Das letzte Wort ist
der Nachname, alle Wörter davor sind die Vornamen. Zwischen den Vornamen
steht genau ein Leerzeichen, überflüssige Leerzeichen fallen weg. Besteht
der Name nur aus einem Wort, bleibt es allein stehen, ohne Komma. Ein Name
ohne Wörter ergibt einen leeren Text.

    neue_schreibweise("Anna Maria Schulz")       →  "Schulz, Anna Maria"
    neue_schreibweise("  Jonas    Weber ")       →  "Weber, Jonas"
    neue_schreibweise("Cher")                    →  "Cher"
    neue_schreibweise("   ")                     →  ""

Grenzen: 0 ≤ len(name) ≤ 1000. name besteht aus Buchstaben (auch Umlauten
und ß), Bindestrichen und Leerzeichen; Wörter sind durch ein oder mehrere
Leerzeichen getrennt, und am Anfang und Ende dürfen Leerzeichen stehen.

Hintergrund: text.split() zerlegt einen Text an den Leerzeichen in eine
Liste von Wörtern. Ohne Argument behandelt split mehrere Leerzeichen
hintereinander wie eines und lässt Leerzeichen am Rand weg:

    "  Ware   prüfen ".split()   →  ["Ware", "prüfen"]
    "   ".split()                →  []

Das Gegenstück ist join: " ".join(liste) setzt die Texte einer Liste
wieder zu einem Text zusammen, mit dem Text vor dem Punkt als Trenner
dazwischen. ", ".join(["a", "b", "c"]) ergibt "a, b, c", und die leere
Liste ergibt den leeren Text. Mit Indizes und Slicing kommen Sie an Teile
der Liste: woerter[-1] ist das letzte Wort, woerter[:-1] die Liste aller
Wörter davor.
"""


def neue_schreibweise(name):
    """Gibt den Namen als "Nachname, Vornamen" zurück, ohne überflüssige Leerzeichen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


for name in ["Anna Maria Schulz", "  Jonas    Weber ", "Cher"]:
    print(f"{name!r} → {neue_schreibweise(name)!r}")
