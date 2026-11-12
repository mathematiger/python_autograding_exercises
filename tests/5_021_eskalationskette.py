# Automatisch erzeugt aus lehrkraft/muster/5_021_eskalationskette.py - nicht von Hand ändern.
# vorlage-hash: 519f99576ee27342
# text-hash: 795ef5bc65fd51fa
# thema: datenstrukturen
# inhalt: Eigene Sequenz mit abc.Sequence

STUFEN = ["Service-Desk", "Fachteam", "Hersteller"]


def versuche(aufruf):
    """Ruft aufruf() auf; liefert ("ok", Ergebnis) oder (Name der Ausnahme, None)."""
    try:
        return "ok", aufruf()
    except Exception as fehler:
        return type(fehler).__name__, None


# Die Klasse ist eine Sequence
assert issubclass(Eskalationskette, Sequence), "Eskalationskette soll von collections.abc.Sequence erben."

# len und Index wie im Beispiel
kette_test = Eskalationskette(STUFEN)
werte = (len(kette_test), kette_test[0], kette_test[2], kette_test[-1], kette_test[-3])
assert werte == (3, "Service-Desk", "Hersteller", "Hersteller", "Service-Desk"), (
    f"Für Eskalationskette({STUFEN!r}) ergeben len, [0], [2], [-1] und [-3] {werte!r}, "
    "erwartet war (3, 'Service-Desk', 'Hersteller', 'Hersteller', 'Service-Desk')."
)

# Ein Index außerhalb löst IndexError aus
for index in [3, -4, 10**20]:
    art, _ = versuche(lambda: kette_test[index])
    assert art == "IndexError", (
        f"kette[{index}] bei drei Stufen soll einen IndexError auslösen, bekommen: {art}.\n"
        "Tipp: Geben Sie den Index an ein Tupel weiter; das löst den IndexError selbst aus."
    )

# Ein Slice liefert eine neue Eskalationskette
teil = kette_test[1:]
assert type(teil) is Eskalationskette and list(teil) == ["Fachteam", "Hersteller"], (
    f"kette[1:] ergibt {teil!r} vom Typ {type(teil).__name__}, erwartet war Eskalationskette(['Fachteam', 'Hersteller']).\n"
    "Tipp: Prüfen Sie mit isinstance(index, slice) und verpacken Sie das Ergebnis in Eskalationskette(...)."
)

# Slices mit Schritt, rückwärts, leer und weit außerhalb
for auswahl in [slice(None, None, -1), slice(0, 3, 2), slice(5, 10), slice(-100, 100), slice(2, 0, -1)]:
    teil = kette_test[auswahl]
    erwartet = STUFEN[auswahl]
    assert type(teil) is Eskalationskette and list(teil) == erwartet, (
        f"kette[{auswahl.start}:{auswahl.stop}:{auswahl.step}] ergibt {teil!r}, erwartet war Eskalationskette({erwartet!r})."
    )

# in, index, count, for und reversed
ergebnis = (
    "Fachteam" in kette_test, "Vertrieb" in kette_test, kette_test.index("Hersteller"),
    kette_test.count("Fachteam"), list(kette_test), list(reversed(kette_test)),
)
erwartet = (True, False, 2, 1, STUFEN, STUFEN[::-1])
assert ergebnis == erwartet, f"in, index, count, list und reversed ergeben {ergebnis!r}, erwartet war {erwartet!r}."

# index, count, __iter__ und __reversed__ kommen von Sequence
selbst = [name for name in ["index", "count", "__iter__", "__reversed__"] if name in vars(Eskalationskette)]
assert selbst == [], (
    f"Eskalationskette definiert {selbst} selbst. Lassen Sie diese Methoden weg; Sequence liefert sie."
)

# in braucht O(1): kein Durchlaufen der Stufen
grosse = Eskalationskette(f"Stufe {nummer}" for nummer in range(10**5))
ergebnis, schritte = zaehle_schritte(lambda: ("Stufe 99999" in grosse, "Gibt es nicht" in grosse))
assert ergebnis == (True, False) and schritte <= 20, (
    f"In einer Kette mit 10**5 Stufen ergeben 'Stufe 99999' in kette und 'Gibt es nicht' in kette {ergebnis!r} "
    f"nach {schritte} ausgeführten Zeilen; erwartet waren (True, False) mit O(1) Schritten (höchstens 20).\n"
    "Tipp: Das geerbte __contains__ sieht jede Stufe an. Merken Sie sich die Namen in __init__ in einer Menge."
)

# Gleichheit
gleich = Eskalationskette(list(STUFEN)) == kette_test
anders = Eskalationskette(STUFEN[::-1]) == kette_test
mit_liste = kette_test == STUFEN
assert (gleich, anders, mit_liste) == (True, False, False), (
    "Eskalationskette(STUFEN) == Eskalationskette(STUFEN), dieselben Stufen rückwärts und der Vergleich mit der "
    f"Liste ergeben {(gleich, anders, mit_liste)!r}, erwartet war (True, False, False)."
)

# __eq__ gibt bei anderen Typen NotImplemented zurück
ergebnis = kette_test.__eq__(STUFEN)
assert ergebnis is NotImplemented, f"kette.__eq__(['Service-Desk', …]) ergibt {ergebnis!r}, erwartet war NotImplemented."

# __repr__
text = repr(kette_test[:2])
assert text == "Eskalationskette(['Service-Desk', 'Fachteam'])", (
    f"repr(kette[:2]) ergibt {text!r}, erwartet war \"Eskalationskette(['Service-Desk', 'Fachteam'])\"."
)

# Änderungen an der übergebenen Liste erreichen die Kette nicht
liste = ["A", "B"]
kopie = Eskalationskette(liste)
liste.append("C")
liste[0] = "Z"
assert list(kopie) == ["A", "B"] and "C" not in kopie and "A" in kopie, (
    f"Nach liste = ['A', 'B'], kette = Eskalationskette(liste), liste.append('C'), liste[0] = 'Z' ist die Kette "
    f"{list(kopie)!r} und 'C' in kette {'C' in kopie}; erwartet waren ['A', 'B'] und False.\n"
    "Tipp: Speichern Sie eine Kopie, am besten als Tupel."
)

# Auch ein Generator als Eingabe funktioniert
aus_generator = Eskalationskette(name for name in STUFEN)
assert list(aus_generator) == STUFEN and "Fachteam" in aus_generator, (
    f"Eskalationskette(name for name in STUFEN) ergibt {list(aus_generator)!r}, "
    f"'Fachteam' in kette {'Fachteam' in aus_generator}; erwartet waren {STUFEN!r} und True.\n"
    "Tipp: Ein Generator lässt sich nur einmal durchlaufen; machen Sie zuerst ein Tupel daraus und bauen Sie die Menge aus dem Tupel."
)

# naechste
ergebnis = (kette_test.naechste("Service-Desk"), kette_test.naechste("Fachteam"), kette_test.naechste("Hersteller"))
assert ergebnis == ("Fachteam", "Hersteller", None), (
    f"naechste für die drei Stufen ergibt {ergebnis!r}, erwartet war ('Fachteam', 'Hersteller', None)."
)
art, _ = versuche(lambda: kette_test.naechste("Vertrieb"))
assert art == "ValueError", f"kette.naechste('Vertrieb') soll einen ValueError auslösen, bekommen: {art}."

# Leere Kette
leer = Eskalationskette([])
ergebnis = (len(leer), list(leer), "x" in leer, repr(leer), versuche(lambda: leer[0])[0], leer == Eskalationskette(()))
assert ergebnis == (0, [], False, "Eskalationskette([])", "IndexError", True), (
    f"Für Eskalationskette([]) ergeben len, list, 'x' in, repr, [0] und == {ergebnis!r}, "
    "erwartet war (0, [], False, 'Eskalationskette([])', 'IndexError', True)."
)

# 300 zufällige Ketten und Slices gegen eine Liste
zufall = Zufall(5021)
for _ in range(300):
    namen = [f"S{nummer}" for nummer in zufall.sample(range(50), zufall.randint(0, 8))]
    kette_z = Eskalationskette(namen)
    start = zufall.choice([None, zufall.randint(-10, 10)])
    stop = zufall.choice([None, zufall.randint(-10, 10)])
    schritt = zufall.choice([None, 1, 2, 3, -1, -2])
    teil = kette_z[start:stop:schritt]
    index = zufall.randint(-10, 10)
    gesucht = f"S{zufall.randrange(50)}"
    bekommen = (list(teil), type(teil).__name__, versuche(lambda: kette_z[index]), gesucht in kette_z, len(kette_z))
    erwartet = (namen[start:stop:schritt], "Eskalationskette", versuche(lambda: namen[index]), gesucht in namen, len(namen))
    assert bekommen == erwartet, (
        f"Für Eskalationskette({namen!r}): [{start}:{stop}:{schritt}], [{index}], {gesucht!r} in, len ergeben\n"
        f"  {bekommen!r}\nerwartet\n  {erwartet!r}"
    )

# Obere Grenze: 10**5 Stufen, auch rückwärts und mit naechste
assert len(grosse) == 10**5 and grosse[-1] == "Stufe 99999" and grosse[::-50000] == Eskalationskette(
    ["Stufe 99999", "Stufe 49999"]
) and grosse.naechste("Stufe 99998") == "Stufe 99999", (
    "Bei 10**5 Stufen stimmen len, [-1], [::-50000] oder naechste nicht."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "Eskalationskette(['Fachteam', 'Hersteller'])\nHersteller None"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm gibt aus:\n{AUSGABE}"
