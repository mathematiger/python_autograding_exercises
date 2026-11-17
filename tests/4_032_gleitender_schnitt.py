# Automatisch erzeugt aus lehrkraft/muster/4_032_gleitender_schnitt.py - nicht von Hand ändern.
# vorlage-hash: e524aeee6e48afc1
# text-hash: 6b290896954aa307
# thema: kontrollfluss
# inhalt: Iterator-Protokoll

import inspect


def mittelwerte_von_hand(zeiten, breite):
    """Vergleichslösung: alle gleitenden Mittelwerte als Liste, mit einer Schleife über die Anfangsstellen."""
    ergebnis = []
    for anfang in range(len(zeiten) - breite + 1):
        ergebnis.append(sum(zeiten[anfang : anfang + breite]) / breite)
    return ergebnis


def gleich(liste_a, liste_b):
    """Vergleicht zwei Listen von Kommazahlen mit kleiner Toleranz."""
    if not isinstance(liste_a, list) or len(liste_a) != len(liste_b):
        return False
    for a, b in zip(liste_a, liste_b):
        if not isinstance(a, (int, float)) or abs(a - b) > 1e-9:
            return False
    return True


def holen(iterator, anzahl):
    """Ruft anzahl-mal next() auf; liefert (Werte, Ausnahme oder None)."""
    werte = []
    try:
        for _ in range(anzahl):
            werte.append(next(iterator))
    except Exception as ausnahme:
        return werte, ausnahme
    return werte, None


def ist_fertig(iterator):
    """Gibt zurück, ob next(iterator) StopIteration auslöst; andere Ausnahmen kommen als Text zurück."""
    try:
        wert = next(iterator)
    except StopIteration:
        return True
    except Exception as ausnahme:
        return f"{type(ausnahme).__name__}: {ausnahme}"
    return f"ein weiterer Wert {wert!r}"


# Das erste next() liefert den Mittelwert von 4 und 8
werte, fehler = holen(GleitenderSchnitt([4, 8, 6, 10, 2], 2), 1)
assert fehler is None and gleich(werte, [6.0]), (
    f"next(GleitenderSchnitt([4, 8, 6, 10, 2], 2)) ergibt {werte[0] if werte else fehler!r}, erwartet war 6.0.\n"
    "Tipp: Ohne __next__ meldet Python „object is not an iterator“."
)

# Das zweite next() rückt um eine Stelle weiter
werte, fehler = holen(GleitenderSchnitt([4, 8, 6, 10, 2], 2), 2)
assert fehler is None and gleich(werte, [6.0, 7.0]), (
    f"Zweimal next(...) bei [4, 8, 6, 10, 2], breite 2 ergibt {werte}"
    + (f" und dann {type(fehler).__name__}: {fehler}" if fehler else "")
    + ", erwartet waren 6.0 und 7.0.\nTipp: Erhöhen Sie in __next__ die gemerkte Stelle um 1."
)

# Nach dem letzten Fenster kommt StopIteration
schnitt = GleitenderSchnitt([4, 8, 6, 10, 2], 2)
werte, fehler = holen(schnitt, 4)
ende = ist_fertig(schnitt)
assert fehler is None and gleich(werte, [6.0, 7.0, 8.0, 6.0]) and ende is True, (
    f"Bei [4, 8, 6, 10, 2], breite 2 erwartet: viermal next() ergibt 6.0, 7.0, 8.0, 6.0, das fünfte StopIteration; "
    f"bekommen {werte}" + (f", Ausnahme {fehler!r}" if fehler else "") + f", danach {ende}.\n"
    "Tipp: Ein Fenster passt noch, solange stelle + breite <= len(zeiten) ist; sonst raise StopIteration "
    "(nicht return None)."
)

# Ein fertiger Iterator bleibt fertig
schnitt = GleitenderSchnitt([1, 2, 3], 3)
holen(schnitt, 1)
ergebnisse = [ist_fertig(schnitt) for _ in range(3)]
assert ergebnisse == [True, True, True], (
    f"Nach dem einzigen Fenster von [1, 2, 3], breite 3, soll jeder weitere next()-Aufruf StopIteration auslösen; "
    f"bekommen: {ergebnisse}."
)

# iter() gibt das Objekt selbst zurück
schnitt = GleitenderSchnitt([4, 8, 6], 2)
try:
    selbst = iter(schnitt)
except Exception as ausnahme:
    selbst = ausnahme
assert selbst is schnitt, (
    f"iter(schnitt) ergibt {selbst!r}, erwartet war schnitt selbst.\nTipp: __iter__ gibt bei einem Iterator return self zurück."
)

# list() und for funktionieren
liste = list(GleitenderSchnitt([4, 8, 6, 10, 2], 2))
summe = 0
for wert in GleitenderSchnitt([4, 8, 6, 10, 2], 2):
    summe = summe + wert
assert gleich(liste, [6.0, 7.0, 8.0, 6.0]) and abs(summe - 27.0) < 1e-9, (
    f"list(GleitenderSchnitt([4, 8, 6, 10, 2], 2)) ergibt {liste}, erwartet [6.0, 7.0, 8.0, 6.0]; "
    f"die Summe in einer for-Schleife ist {summe}, erwartet 27.0."
)

# Ein halb verbrauchter Iterator macht dort weiter, wo er steht (wie im Beispiel)
schnitt = GleitenderSchnitt([4, 8, 6, 10, 2], 2)
anfang, _ = holen(schnitt, 2)
rest = list(schnitt)
nochmal = list(schnitt)
assert gleich(anfang, [6.0, 7.0]) and gleich(rest, [8.0, 6.0]) and nochmal == [], (
    f"Nach zweimal next() erwartet list(schnitt) == [8.0, 6.0] und ein zweites list(schnitt) == []; "
    f"bekommen {rest} und {nochmal}."
    + ("\nTipp: __iter__ darf nicht von vorn anfangen, sondern gibt self zurück; der Stand liegt im Objekt."
       if len(rest) > 2 else "")
)

# Andere Breite: je drei Zeiten
liste = list(GleitenderSchnitt([3, 6, 9, 12], 3))
assert gleich(liste, [6.0, 9.0]), (
    f"list(GleitenderSchnitt([3, 6, 9, 12], 3)) ergibt {liste}, erwartet war [6.0, 9.0]."
    + ("\nTipp: Teilen Sie die Summe des Fensters durch breite, nicht durch eine feste Zahl."
       if len(liste) == 2 else "")
)

# breite 1: die Zeiten selbst
liste = list(GleitenderSchnitt([5, 0, 7], 1))
assert gleich(liste, [5.0, 0.0, 7.0]), f"list(GleitenderSchnitt([5, 0, 7], 1)) ergibt {liste}, erwartet war [5.0, 0.0, 7.0]."

# breite gleich der Länge: genau ein Fenster
liste = list(GleitenderSchnitt([2, 4, 9], 3))
assert gleich(liste, [5.0]), (
    f"list(GleitenderSchnitt([2, 4, 9], 3)) ergibt {liste}, erwartet war [5.0]."
    + ("\nTipp: Das letzte Fenster passt noch, wenn stelle + breite == len(zeiten) ist (<=, nicht <)."
       if liste == [] else "")
)

# breite größer als die Liste: kein Fenster
liste = list(GleitenderSchnitt([2, 4], 3))
assert liste == [], f"list(GleitenderSchnitt([2, 4], 3)) ergibt {liste}, erwartet war []."

# Leere Liste: kein Fenster
schnitt = GleitenderSchnitt([], 1)
ende = ist_fertig(schnitt)
assert ende is True, f"next(GleitenderSchnitt([], 1)) soll StopIteration auslösen, bekommen: {ende}."

# Die Liste zeiten wird nicht verändert
zeiten = [4, 8, 6, 10, 2]
list(GleitenderSchnitt(zeiten, 2))
assert zeiten == [4, 8, 6, 10, 2], f"Nach dem Durchlaufen ist zeiten {zeiten}, erwartet war unverändert [4, 8, 6, 10, 2]."

# Faul: Das Erzeugen berechnet nicht schon alle Mittelwerte
class Zaehlzeiten(list):
    """Eine Liste, die mitzählt, wie oft sie gelesen wird."""

    lesezugriffe = 0

    def __getitem__(self, index):
        """Zählt den Zugriff und liest dann wie eine Liste."""
        Zaehlzeiten.lesezugriffe += 1
        return list.__getitem__(self, index)

    def __iter__(self):
        """Zählt auch das Durchlaufen der ganzen Liste."""
        Zaehlzeiten.lesezugriffe += 1
        return list.__iter__(self)

zeiten = Zaehlzeiten(range(1000))
schnitt = GleitenderSchnitt(zeiten, 10)
beim_erzeugen = Zaehlzeiten.lesezugriffe
assert beim_erzeugen <= 11, (
    f"GleitenderSchnitt(1000 Zeiten, 10) hat die Zeiten schon beim Erzeugen {beim_erzeugen}-mal gelesen; "
    "erlaubt sind höchstens 11 (ein Fenster). Es sieht so aus, als würden schon alle Mittelwerte im Voraus "
    "berechnet.\n"
    "Tipp: Berechnen Sie in __init__ keine Mittelwerte im Voraus; __next__ rechnet jeweils nur das nächste Fenster."
)

# Faul: Das Erzeugen rechnet noch nicht mit allen Zeiten
class Zaehlzahl(int):
    """Eine ganze Zahl, die mitzählt, wie oft mit ihr addiert oder subtrahiert wird."""

    rechenschritte = 0

    def __add__(self, andere):
        """Zählt die Addition und rechnet wie eine ganze Zahl."""
        Zaehlzahl.rechenschritte += 1
        return int.__add__(self, andere)

    def __radd__(self, andere):
        """Zählt die Addition von links (z. B. 0 + zahl in sum) und rechnet wie eine ganze Zahl."""
        Zaehlzahl.rechenschritte += 1
        return int.__radd__(self, andere)

    def __sub__(self, andere):
        """Zählt die Subtraktion und rechnet wie eine ganze Zahl."""
        Zaehlzahl.rechenschritte += 1
        return int.__sub__(self, andere)

    def __rsub__(self, andere):
        """Zählt die Subtraktion von links und rechnet wie eine ganze Zahl."""
        Zaehlzahl.rechenschritte += 1
        return int.__rsub__(self, andere)

zeiten = [Zaehlzahl(nummer) for nummer in range(1000)]
schnitt = GleitenderSchnitt(zeiten, 10)
beim_erzeugen = Zaehlzahl.rechenschritte
assert beim_erzeugen <= 20, (
    f"GleitenderSchnitt(1000 Zeiten, 10) hat beim Erzeugen schon {beim_erzeugen}-mal mit den Zeiten gerechnet; "
    "erlaubt sind höchstens 20 (zwei Fenster). Es sieht so aus, als würden schon alle Mittelwerte im Voraus "
    "berechnet.\n"
    "Tipp: Berechnen Sie in __init__ keine Mittelwerte im Voraus; __next__ rechnet jeweils nur das nächste Fenster."
)

# Weder __iter__ noch __next__ ist eine Generatorfunktion mit yield
generatoren = [
    name for name in ("__iter__", "__next__")
    if inspect.isgeneratorfunction(getattr(GleitenderSchnitt, name, None))
]
assert generatoren == [], (
    f"{', '.join(generatoren)} benutzt yield. Schreiben Sie das Protokoll von Hand: __iter__ gibt self zurück, "
    "__next__ liefert einen Wert mit return oder löst StopIteration aus."
)

# Viele zufällige Messreihen, verglichen mit einer Liste aller Mittelwerte
zufall = Zufall(4032)
for runde in range(400):
    zeiten = [zufall.randint(0, 100) for _ in range(zufall.randint(0, 12))]
    breite = zufall.randint(1, 6)
    erwartet = mittelwerte_von_hand(zeiten, breite)
    bekommen = list(GleitenderSchnitt(zeiten, breite))
    assert gleich(bekommen, erwartet), (
        f"list(GleitenderSchnitt({zeiten}, {breite})) ergibt {bekommen}, erwartet war {erwartet}."
    )

# Obere Grenze: 10 000 Zeiten bis 100 000, breite 100
zeiten = [(nummer * 7919) % 100_001 for nummer in range(10_000)]
erwartet = mittelwerte_von_hand(zeiten, 100)
bekommen = list(GleitenderSchnitt(zeiten, 100))
assert gleich(bekommen, erwartet), (
    f"Bei 10 000 Zeiten und breite 100 erwartet {len(erwartet)} Mittelwerte, die ersten {erwartet[:2]}, "
    f"die letzten {erwartet[-2:]}; bekommen {len(bekommen)}, die ersten {bekommen[:2]}, die letzten {bekommen[-2:]}."
)

# Die Ausgabe des Programms stimmt
assert vergleichbar(AUSGABE) == vergleichbar("6.0 7.0 [8.0, 6.0]"), f'Erwartete Ausgabe: "6.0 7.0 [8.0, 6.0]" – Ihr Programm: "{AUSGABE}"'
