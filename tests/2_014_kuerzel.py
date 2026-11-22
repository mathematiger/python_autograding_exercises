# Automatisch erzeugt aus lehrkraft/muster/2_014_kuerzel.py - nicht von Hand ändern.
# vorlage-hash: 4ffffe1ee2bcb044
# text-hash: b0f2873127fa2b07
# thema: texte_zahlen
# inhalt: Texte durchlaufen und neu aufbauen

# Die Vokale fallen weg (Leerzeichen zählen hier noch nicht)
ergebnis = kuerzel("Ware prüfen")
if ergebnis is None:
    hinweis = "Tipp: Geben Sie das Kürzel mit return zurück, statt es auszugeben."
else:
    hinweis = "Tipp: Hängen Sie nur die Zeichen an das Kürzel an, die nicht in VOKALE stehen."
assert isinstance(ergebnis, str) and ergebnis.replace(" ", "") == "Wrprfn", (
    f'kuerzel("Ware prüfen") ergibt {ergebnis!r}, erwartet war "Wrprfn".\n{hinweis}'
)

# Das Beispiel aus der Aufgabe
ergebnis = kuerzel("Ware prüfen")
if isinstance(ergebnis, str) and " " in ergebnis:
    hinweis = "\nTipp: Auch die Leerzeichen gehören nicht ins Kürzel."
else:
    hinweis = ""
assert ergebnis == "Wrprfn", f'kuerzel("Ware prüfen") ergibt {ergebnis!r}, erwartet war "Wrprfn".{hinweis}'

# Weitere Schritte (nicht fest hinschreiben!)
for schritt, erwartet in [
    ("Paket versenden", "Pktvrsndn"),
    ("Rechnung stellen", "Rchnngstlln"),
    ("Lieferschein drucken", "Lfrschndrckn"),
    ("Retoure buchen", "Rtrbchn"),
]:
    ergebnis = kuerzel(schritt)
    if isinstance(ergebnis, str) and " " in ergebnis:
        hinweis = "\nTipp: Auch die Leerzeichen gehören nicht ins Kürzel."
    else:
        hinweis = ""
    assert ergebnis == erwartet, f"kuerzel({schritt!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.{hinweis}"

# Großgeschriebene Vokale und Umlaute werden auch entfernt
for schritt, erwartet in [("Ware Ausgeben", "Wrsgbn"), ("Kunde Über Lieferung Informieren", "KndbrLfrngnfrmrn")]:
    ergebnis = kuerzel(schritt)
    if isinstance(ergebnis, str) and " " in ergebnis:
        hinweis = "Tipp: Auch die Leerzeichen gehören nicht ins Kürzel."
    else:
        hinweis = "Tipp: Vokale gibt es auch groß; die Konstante VOKALE enthält alle."
    assert ergebnis == erwartet, f"kuerzel({schritt!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n{hinweis}"

# Der erste Buchstabe bleibt, auch wenn er ein Vokal ist
for schritt, erwartet in [("Auftrag erfassen", "Aftrgrfssn"), ("Übergabe", "Übrgb"), ("ordnen", "ordnn")]:
    ergebnis = kuerzel(schritt)
    hinweis = ""
    if isinstance(ergebnis, str) and " " in ergebnis:
        hinweis = hinweis + "\nTipp: Auch die Leerzeichen gehören nicht ins Kürzel."
    if isinstance(ergebnis, str) and not ergebnis.startswith(schritt[0]):
        hinweis = hinweis + "\nTipp: Der erste Buchstabe kommt immer ins Kürzel; nur ab dem zweiten werden Vokale entfernt."
    assert ergebnis == erwartet, f"kuerzel({schritt!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.{hinweis}"

# Ein Name aus einem einzigen Buchstaben bleibt, wie er ist
for schritt in ["A", "X"]:
    ergebnis = kuerzel(schritt)
    if isinstance(ergebnis, str) and not ergebnis.startswith(schritt):
        hinweis = "\nTipp: Der erste Buchstabe kommt immer ins Kürzel, auch wenn er ein Vokal ist."
    else:
        hinweis = ""
    assert ergebnis == schritt, f"kuerzel({schritt!r}) ergibt {ergebnis!r}, erwartet war {schritt!r}.{hinweis}"

# Ein leerer Name ergibt ein leeres Kürzel
try:
    ergebnis = kuerzel("")
except IndexError as fehler:
    ergebnis = fehler
assert ergebnis == "", (
    f'kuerzel("") ergibt {ergebnis!r}, erwartet war "".\n'
    'Tipp: Bei einem leeren Text gibt es kein schritt[0]. Prüfen Sie diesen Fall zuerst.'
)

import ast
import inspect
import textwrap


def hat_for_schleife(funktion):
    """Gibt zurück, ob im Rumpf der Funktion eine for-Schleife steht (die Programmzeile unten zählt nicht mit)."""
    try:
        baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))
    except (OSError, TypeError, SyntaxError):
        return False
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.For):
            return True
    return False


# kuerzel benutzt eine for-Schleife
assert hat_for_schleife(kuerzel), (
    "Bauen Sie das Kürzel in kuerzel mit einer for-Schleife über die Zeichen auf.\n"
    "Tipp: Die for-Schleife unten im Programm zählt nicht; sie ruft kuerzel nur auf."
)

# Das Kürzel entsteht mit einer Schleife über die Zeichen, nicht mit replace
assert not verwendet("replace"), (
    "Benutzen Sie nicht replace.\n"
    "Tipp: Gehen Sie die Zeichen mit for durch und hängen Sie die passenden an einen neuen Text an."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "Auftrag erfassen: Aftrgrfssn\nWare kommissionieren: Wrkmmssnrn\nPaket versenden: Pktvrsndn"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Namen, verglichen mit einer Rechnung über replace
zufall = Zufall(2013)
BUCHSTABEN = "abcdefghijklmnopqrstuvwxyzäöüßABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ" + "aeiouAEIOU"
for _ in range(500):
    schritt = zufall.choice(BUCHSTABEN)
    for _ in range(zufall.randint(0, 12)):
        schritt = schritt + zufall.choice(BUCHSTABEN + "   ")
    rest = schritt[1:]
    for weg in VOKALE + " ":
        rest = rest.replace(weg, "")
    erwartet = schritt[0] + rest
    ergebnis = kuerzel(schritt)
    assert ergebnis == erwartet, f"kuerzel({schritt!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# An der oberen Grenze: 100 Zeichen
for schritt, erwartet in [
    ("Ab " * 33 + "A", "A" + "b" * 33),
    ("E" * 100, "E"),
    ("x" * 100, "x" * 100),
    ("Ü" + " " * 99, "Ü"),
]:
    ergebnis = kuerzel(schritt)
    assert ergebnis == erwartet, (
        f"Bei einem Namen mit 100 Zeichen, der mit {schritt[:6]!r} beginnt, ergibt kuerzel {ergebnis!r}, "
        f"erwartet war {erwartet!r}."
    )
