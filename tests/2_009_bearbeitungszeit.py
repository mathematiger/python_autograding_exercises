# Automatisch erzeugt aus lehrkraft/muster/2_009_bearbeitungszeit.py - nicht von Hand ändern.
# vorlage-hash: 511f712172d956e3
# thema: funktionen
# inhalt: Mehrere Rückgabewerte als Tupel

# Das Beispiel aus der Aufgabe ergibt (38, 95)
ergebnis = kuerzeste_und_laengste([42, 95, 61, 38])
if isinstance(ergebnis, list):
    hinweis = "\nTipp: Sie geben eine Liste zurück. Schreiben Sie return kuerzeste, laengste ohne eckige Klammern."
elif ergebnis == (95, 38):
    hinweis = "\nTipp: Die Reihenfolge ist vertauscht. Die kürzeste Zeit kommt zuerst."
elif ergebnis is None:
    hinweis = "\nTipp: Ihre Funktion gibt nichts zurück. Fehlt das return?"
else:
    hinweis = ""
assert ergebnis == (38, 95) and isinstance(ergebnis, tuple), (
    f"kuerzeste_und_laengste([42, 95, 61, 38]) ergibt {ergebnis!r}, erwartet war das Tupel (38, 95).{hinweis}"
)

# Weitere Messreihen (nicht fest 38 und 95 hinschreiben!)
for zeiten, erwartet in [
    ([120, 75, 98], (75, 120)),
    ([12, 13], (12, 13)),
    ([64, 31, 31, 200, 87], (31, 200)),
    ([18.5, 22.25, 9.75], (9.75, 22.25)),
]:
    ergebnis = kuerzeste_und_laengste(zeiten)
    assert ergebnis == erwartet and isinstance(ergebnis, tuple), (
        f"kuerzeste_und_laengste({zeiten}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    )

# Eine einzige Zeit ist zugleich die kürzeste und die längste
ergebnis = kuerzeste_und_laengste([50])
assert ergebnis == (50, 50), f"kuerzeste_und_laengste([50]) ergibt {ergebnis!r}, erwartet war (50, 50)."

# Die Ausgabe des Programms stimmt
assert AUSGABE == "Kürzeste Zeit: 38 s\nLängste Zeit: 95 s", (
    f"Erwartete Ausgabe:\nKürzeste Zeit: 38 s\nLängste Zeit: 95 s\nIhr Programm:\n{AUSGABE}"
)
