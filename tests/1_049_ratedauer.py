# Automatisch erzeugt aus lehrkraft/muster/1_049_ratedauer.py - nicht von Hand ändern.
# vorlage-hash: b22b6e69251901bf
# text-hash: 468d88c96d306152
# thema: programmaufbau
# inhalt: main und __name__

import ast

EINGABEN = ["10"]


def erwartete_zeilen(laenge):
    """Vergleichslösung: die drei Zeilen der Ausgabe bei dieser Länge."""
    jahre = 62**laenge / 10**10 / (365 * 24 * 3600)
    stufe = "unsicher" if jahre < 1 else "mittel" if jahre < 100 else "sicher"
    return [f"Mögliche Passwörter: {62**laenge}", f"Jahre zum Durchprobieren: {jahre:.1f}", f"Bewertung: {stufe}"]


def zeilen_bei(laenge):
    """Startet das Programm mit der Länge; liefert die Zeilen der Ausgabe oder den Abbruch als Text."""
    try:
        return starte(str(laenge)).splitlines()
    except Exception as fehler:
        return [f"(Abbruch: {type(fehler).__name__}: {fehler})"]


def bewertung_stimmt(laenge):
    """Liefert (stimmt, Meldung) für die Zeile mit der Bewertung."""
    zeilen = zeilen_bei(laenge)
    erwartet = erwartete_zeilen(laenge)[2]
    tatsaechlich = zeilen[2] if len(zeilen) > 2 else "(keine dritte Zeile)"
    text = f"Bei Länge {laenge} erwartet als dritte Zeile: {erwartet}\nIhr Programm gibt aus:\n" + "\n".join(zeilen)
    return vergleichbar(tatsaechlich) == vergleichbar(erwartet), text


def ist_namensabfrage(knoten):
    """True, wenn knoten ein if mit der Bedingung __name__ == "__main__" ist."""
    if not isinstance(knoten, ast.If) or not isinstance(knoten.test, ast.Compare):
        return False
    teile = [knoten.test.left, *knoten.test.comparators]
    namen = [teil.id for teil in teile if isinstance(teil, ast.Name)]
    texte = [teil.value for teil in teile if isinstance(teil, ast.Constant)]
    return namen == ["__name__"] and texte == ["__main__"] and isinstance(knoten.test.ops[0], ast.Eq)


def ruft_main_auf(anweisungen):
    """True, wenn unter den Anweisungen ein Aufruf main() steht."""
    for anweisung in anweisungen:
        if isinstance(anweisung, ast.Expr) and isinstance(anweisung.value, ast.Call):
            funktion = anweisung.value.func
            if isinstance(funktion, ast.Name) and funktion.id == "main":
                return True
    return False


def importiere():
    """Führt die Datei aus wie bei import ratedauer; liefert (Namensraum, Ausgaben, Fragen, Fehler)."""
    ausgaben = []
    fragen = []

    def eigenes_print(*werte, **_):
        """Merkt sich die Ausgabe, statt sie anzuzeigen."""
        ausgaben.append(" ".join(str(wert) for wert in werte))

    def eigenes_input(frage=""):
        """Merkt sich die Frage und antwortet mit 10."""
        fragen.append(frage)
        return "10"

    namensraum = {"__name__": "ratedauer", "print": eigenes_print, "input": eigenes_input}
    with open(__file__, encoding="utf-8") as datei:
        quelltext = datei.read()
    try:
        exec(compile(quelltext, __file__, "exec"), namensraum)
    except Exception as fehler:
        return namensraum, ausgaben, fragen, f"{type(fehler).__name__}: {fehler}"
    return namensraum, ausgaben, fragen, None


with open(__file__, encoding="utf-8") as datei:
    BAUM = ast.parse(datei.read())

# Das Programm läuft überhaupt: Es gibt etwas aus
assert AUSGABE.strip() != "", (
    "Ihr Programm gibt nichts aus.\n"
    "Tipp: main ist nur definiert; rufen Sie die Funktion ganz unten mit main() auf."
)

# Die ersten beiden Zeilen im Beispiel 10
assert AUSGABE.splitlines()[:2] == erwartete_zeilen(10)[:2], (
    f"Erwartet war bei Eingabe 10 zuerst:\n" + "\n".join(erwartete_zeilen(10)[:2]) + f"\nIhr Programm:\n{AUSGABE}"
)

# Im Beispiel 10 lautet die Bewertung mittel
stimmt, text = bewertung_stimmt(10)
assert stimmt, text + "\nTipp: print(f\"Bewertung: {bewertung(jahre)}\") als letzte Zeile in main."

# Bei Länge 8 ist das Passwort unsicher (nicht fest hinschreiben!)
stimmt, text = bewertung_stimmt(8)
assert stimmt, text + "\nTipp: Geben Sie das Ergebnis von bewertung(jahre) aus, nicht einen festen Text."

# Bei Länge 14 ist das Passwort sicher
stimmt, text = bewertung_stimmt(14)
assert stimmt, text

# main wird genau einmal aufgerufen: genau drei Zeilen Ausgabe
zeilen = zeilen_bei(12)
assert len(zeilen) == 3, (
    f"Bei Eingabe 12 gibt Ihr Programm {len(zeilen)} Zeilen aus, erwartet waren 3:\n" + "\n".join(zeilen) + "\n"
    "Tipp: Rufen Sie main nur einmal auf, und zwar ganz unten im if."
)

# Ganz unten steht if __name__ == "__main__":
abfragen = [knoten for knoten in BAUM.body if ist_namensabfrage(knoten)]
assert len(abfragen) == 1, (
    'In Ihrem Programm steht auf oberster Ebene kein if __name__ == "__main__":.\n'
    "Tipp: Die Zeile beginnt ganz links, ohne Einrückung, und __name__ hat vorn und hinten je zwei Unterstriche."
)

# Im if steht der Aufruf main()
assert len(abfragen) > 0 and ruft_main_auf(abfragen[0].body), (
    'Unter if __name__ == "__main__": steht kein Aufruf main().\n'
    "Tipp: Rücken Sie main() unter dem if um vier Leerzeichen ein."
)

# Außerhalb des if wird main nicht aufgerufen
assert not ruft_main_auf(BAUM.body), (
    "main() steht auch ohne if auf oberster Ebene. Dann läuft das Programm auch beim import.\n"
    'Tipp: Lassen Sie main() nur unter if __name__ == "__main__": stehen.'
)

# Beim import fragt das Programm nichts und gibt nichts aus
namensraum, ausgaben, fragen, fehler = importiere()
assert fehler is None and fragen == [] and ausgaben == [], (
    f"Beim import fragt Ihr Programm {fragen} und gibt {ausgaben} aus"
    + (f", dann bricht es ab mit {fehler}" if fehler else "")
    + ".\nErwartet war: nichts fragen, nichts ausgeben, nur die Funktionen bereitstellen.\n"
    'Tipp: Alles, was fragt oder ausgibt, gehört in main, und main() unter if __name__ == "__main__":.'
)

# Nach dem import ist die Funktion bewertung benutzbar
ergebnis = namensraum.get("bewertung", lambda jahre: "(fehlt)")(250)
assert ergebnis == "sicher", (
    f"Nach dem import ergibt bewertung(250) {ergebnis!r}, erwartet war 'sicher'.\n"
    "Tipp: Lassen Sie die Funktionen oben in der Datei, wie sie sind."
)

# Randfall: Länge 1
stimmt, text = bewertung_stimmt(1)
assert stimmt, text

# Alle Längen bis zur oberen Grenze 30
for laenge in range(1, 31):
    zeilen = zeilen_bei(laenge)
    assert vergleichbar("\n".join(zeilen)) == vergleichbar("\n".join(erwartete_zeilen(laenge))), (
        f"Bei Länge {laenge} erwartet:\n" + "\n".join(erwartete_zeilen(laenge)) + "\nIhr Programm:\n" + "\n".join(zeilen)
    )
