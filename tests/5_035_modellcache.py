# Automatisch erzeugt aus lehrkraft/muster/5_035_modellcache.py - nicht von Hand ändern.
# vorlage-hash: 27620346dc773b6f
# text-hash: 364d329ac43b2895
# thema: datenstrukturen
# inhalt: weakref, WeakValueDictionary

import gc
import weakref


class Testmodell:
    """Ein Modell für die Tests: sagt voraus, ob die Summe der Messwerte die Schwelle erreicht."""

    def __init__(self, name, schwelle):
        """Legt das Modell an."""
        self.name = name
        self.schwelle = schwelle

    def vorhersage(self, messwerte):
        """True, wenn die Summe der Messwerte die Schwelle erreicht."""
        return sum(messwerte) >= self.schwelle


class Testlader:
    """Eine Ladefunktion, die mitzählt, welche Modelle sie geladen hat."""

    def __init__(self):
        """Noch nichts geladen."""
        self.geladen = []

    def __call__(self, name):
        """Lädt ein neues Testmodell; die Schwelle ist die Länge des Namens."""
        self.geladen.append(name)
        return Testmodell(name, len(name))


def aufraeumen():
    """Räumt auch Objekte in Referenzkreisen auf."""
    gc.collect()


def wert_von(aufruf):
    """Führt den Aufruf aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def hole_zweimal():
    """Holt dasselbe Modell zweimal, solange das erste noch benutzt wird."""
    lader = Testlader()
    cache = Modellcache(lader)
    erstes = cache.hole("presse")
    zweites = cache.hole("presse")
    return (type(erstes).__name__, getattr(erstes, "name", None), erstes is zweites, lader.geladen)


def zwei_namen():
    """Holt zwei verschiedene Modelle und gibt geladen() zurück, solange beide benutzt werden."""
    lader = Testlader()
    cache = Modellcache(lader)
    a = cache.hole("walze")
    b = cache.hole("bohrer")
    return (a is not b, lader.geladen, cache.geladen())


def nach_freigabe():
    """Gibt das einzige benutzte Modell frei und holt es danach erneut."""
    lader = Testlader()
    cache = Modellcache(lader)
    modell = cache.hole("presse")
    vorher = cache.geladen()
    del modell
    aufraeumen()
    nachher = cache.geladen()
    freigegeben = list(cache.freigegeben)
    cache.hole("presse")
    return (vorher, nachher, freigegeben, lader.geladen)


def haelt_nicht_fest():
    """Prüft mit einer eigenen schwachen Referenz, ob der Cache ein Modell am Leben hält."""
    cache = Modellcache(Testlader())
    modell = cache.hole("presse")
    beobachter = weakref.ref(modell)
    del modell
    aufraeumen()
    return beobachter() is None


# hole liefert das Modell von lader
ergebnis = wert_von(hole_zweimal)
assert isinstance(ergebnis, tuple) and ergebnis[:2] == ("Testmodell", "presse"), (
    f"cache.hole('presse') liefert {ergebnis!r}; erwartet war das Modell, das lader('presse') geladen hat.\n"
    "Tipp: Rufen Sie self.lader(name) auf und geben Sie das Ergebnis zurück."
)

# hole liefert dasselbe Objekt, solange es benutzt wird, und lädt nur einmal
assert ergebnis[2:] == (True, ["presse"]), (
    f"Zweimal hole('presse') ergibt (dasselbe Objekt, geladen) = {ergebnis[2:]!r}, erwartet war (True, ['presse']).\n"
    "Tipp: Speichern Sie jedes geladene Modell in einem weakref.WeakValueDictionary und schauen Sie dort zuerst nach."
)

# Verschiedene Namen ergeben verschiedene Modelle, geladen() ist sortiert
ergebnis = wert_von(zwei_namen)
assert ergebnis == (True, ["walze", "bohrer"], ["bohrer", "walze"]), (
    f"hole('walze') und hole('bohrer') ergeben (verschieden, geladen, cache.geladen()) = {ergebnis!r}, "
    "erwartet war (True, ['walze', 'bohrer'], ['bohrer', 'walze'])."
)

# Der Cache hält ein Modell nicht am Leben
ergebnis = wert_von(haelt_nicht_fest)
assert ergebnis is True, (
    f"Nach del modell lebt das Modell noch ({ergebnis!r}); der Cache soll es nicht festhalten.\n"
    "Tipp: Ein gewöhnliches Dictionary oder eine Liste hält ihre Werte stark fest; nehmen Sie weakref.WeakValueDictionary. "
    "Auch finalize darf das Modell nicht unter seinen Argumenten haben."
)

# Nach der Freigabe ist das Modell nicht mehr im Cache, und hole lädt neu
ergebnis = wert_von(nach_freigabe)
assert isinstance(ergebnis, tuple) and ergebnis[0] == ["presse"] and ergebnis[1] == [] and ergebnis[3] == ["presse", "presse"], (
    f"(geladen vorher, geladen nachher, freigegeben, Ladevorgänge) = {ergebnis!r}; "
    "erwartet war (['presse'], [], ['presse'], ['presse', 'presse'])."
)

# freigegeben enthält den Namen des freigegebenen Modells
assert ergebnis[2] == ["presse"], (
    f"Nach der Freigabe ist cache.freigegeben {ergebnis[2]!r}, erwartet war ['presse'].\n"
    "Tipp: weakref.finalize(modell, self.freigegeben.append, name) direkt nach dem Laden."
)


def reihenfolge_der_freigabe():
    """Gibt drei Modelle in anderer Reihenfolge frei, als sie geladen wurden."""
    cache = Modellcache(Testlader())
    a, b, c = cache.hole("a"), cache.hole("bb"), cache.hole("ccc")
    del b
    aufraeumen()
    schritt = list(cache.freigegeben)
    del c, a
    aufraeumen()
    return (schritt, cache.freigegeben, cache.geladen())


# freigegeben in der Reihenfolge der Freigabe
ergebnis = wert_von(reihenfolge_der_freigabe)
assert ergebnis == (["bb"], ["bb", "ccc", "a"], []), (
    f"(nach del b, am Ende, geladen) = {ergebnis!r}, erwartet war (['bb'], ['bb', 'ccc', 'a'], [])."
)


def vorhersagen_ohne_behalten():
    """Zwei Vorhersagen ohne behalten: das Modell wird jedes Mal neu geladen und wieder freigegeben."""
    lader = Testlader()
    cache = Modellcache(lader)
    ergebnisse = [cache.vorhersage("abc", [1, 1]), cache.vorhersage("abc", [2, 2])]
    aufraeumen()
    return (ergebnisse, lader.geladen, cache.geladen(), cache.freigegeben)


# vorhersage liefert die Vorhersage des Modells
ergebnis = wert_von(vorhersagen_ohne_behalten)
assert isinstance(ergebnis, tuple) and ergebnis[0] == [False, True], (
    f"vorhersage('abc', [1, 1]) und vorhersage('abc', [2, 2]) ergeben {ergebnis[0] if isinstance(ergebnis, tuple) else ergebnis!r}, "
    "erwartet war [False, True] (Schwelle 3).\nTipp: return self.hole(name).vorhersage(messwerte)"
)

# vorhersage ohne behalten hält das Modell nicht fest
assert ergebnis[1:] == (["abc", "abc"], [], ["abc", "abc"]), (
    f"Ohne behalten ergibt (Ladevorgänge, geladen(), freigegeben) {ergebnis[1:]!r}, erwartet war (['abc', 'abc'], [], ['abc', 'abc']).\n"
    "Tipp: Mit behalten=0 hält der Cache kein Modell stark fest."
)


def mit_behalten(behalten, namen):
    """Holt die Namen nacheinander (ohne sie selbst festzuhalten); gibt Ladevorgänge und geladen() zurück."""
    lader = Testlader()
    cache = Modellcache(lader, behalten)
    for name in namen:
        cache.vorhersage(name, [5])
    aufraeumen()
    return (lader.geladen, cache.geladen())


# behalten=1 im Beispiel: zweimal dasselbe Modell, nur einmal geladen
ergebnis = wert_von(lambda: mit_behalten(1, ["presse", "presse"]))
assert ergebnis == (["presse"], ["presse"]), (
    f"Mit behalten=1 ergibt zweimal vorhersage('presse', …) (Ladevorgänge, geladen) = {ergebnis!r}, erwartet war (['presse'], ['presse']).\n"
    "Tipp: Halten Sie das zuletzt geholte Modell in einer gewöhnlichen Liste fest."
)

# behalten=2: das am längsten nicht geholte fällt heraus
ergebnis = wert_von(lambda: mit_behalten(2, ["a", "b", "c", "a"]))
assert ergebnis == (["a", "b", "c", "a"], ["a", "c"]), (
    f"Mit behalten=2 und den Namen a, b, c, a ergibt (Ladevorgänge, geladen) {ergebnis!r}, erwartet war (['a', 'b', 'c', 'a'], ['a', 'c'])."
)

# behalten=2: ein erneut geholtes Modell rückt nach hinten
ergebnis = wert_von(lambda: mit_behalten(2, ["a", "b", "a", "c", "a", "b"]))
assert ergebnis == (["a", "b", "c", "b"], ["a", "b"]), (
    f"Mit behalten=2 und den Namen a, b, a, c, a, b ergibt (Ladevorgänge, geladen) {ergebnis!r}, erwartet war (['a', 'b', 'c', 'b'], ['a', 'b']).\n"
    "Tipp: Holt man ein Modell erneut, entfernen Sie es aus der Liste und hängen es hinten wieder an."
)

# behalten=2: dasselbe Modell mehrmals belegt nur einen Platz
ergebnis = wert_von(lambda: mit_behalten(2, ["a", "b", "b", "b", "a"]))
assert ergebnis == (["a", "b"], ["a", "b"]), (
    f"Mit behalten=2 und den Namen a, b, b, b, a ergibt (Ladevorgänge, geladen) {ergebnis!r}, erwartet war (['a', 'b'], ['a', 'b'])."
)


def behalten_und_benutzt():
    """Ein Modell, das außerhalb noch benutzt wird, bleibt im Cache, auch wenn es aus behalten herausfällt."""
    lader = Testlader()
    cache = Modellcache(lader, 1)
    festgehalten = cache.hole("a")
    cache.hole("b")
    cache.hole("c")
    aufraeumen()
    erneut = cache.hole("a")
    return (festgehalten is erneut, lader.geladen, cache.geladen())


# Ein von außen benutztes Modell bleibt im Cache, auch ohne behalten-Platz
ergebnis = wert_von(behalten_und_benutzt)
assert ergebnis == (True, ["a", "b", "c"], ["a"]), (
    f"(dasselbe Objekt, Ladevorgänge, geladen) = {ergebnis!r}, erwartet war (True, ['a', 'b', 'c'], ['a']): "
    "a lebt weiter, weil es außerhalb benutzt wird; c fällt heraus, sobald a wieder geholt wird."
)

# Der Cache benutzt WeakValueDictionary und finalize
assert verwendet("WeakValueDictionary") and verwendet("finalize"), "Benutzen Sie weakref.WeakValueDictionary für den Cache und weakref.finalize für freigegeben."

# Die Ausgabe des Programms
erwartet = "lade presse\nTrue\n['presse']\n[] ['presse']\nlade fraese\nTrue\n['presse', 'fraese']\nlade presse\nTrue\nFalse"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"


def vergleich_ladevorgaenge(behalten, namen):
    """Vergleichslösung: welche Namen geladen werden müssen, wenn nur die letzten behalten Namen leben."""
    zuletzt = []
    geladen = []
    for name in namen:
        if name not in zuletzt:
            geladen.append(name)
        else:
            zuletzt.remove(name)
        zuletzt.append(name)
        if len(zuletzt) > behalten:
            zuletzt.pop(0)
    return (geladen, sorted(zuletzt))


# Viele zufällige Folgen von Anfragen
zufall = Zufall(5035)
for _ in range(200):
    behalten = zufall.randint(0, 5)
    namen = [zufall.choice(["a", "bb", "ccc", "dddd", "eeeee", "f"]) for _ in range(zufall.randint(0, 20))]
    ergebnis = wert_von(lambda: mit_behalten(behalten, namen))
    erwartet = vergleich_ladevorgaenge(behalten, namen)
    assert ergebnis == erwartet, f"Mit behalten={behalten} und den Namen {namen} ergibt (Ladevorgänge, geladen) {ergebnis!r}, erwartet war {erwartet}."

# Obere Grenze: 10 000 Anfragen an 1000 Modelle mit behalten=100
namen = [f"maschine{zufall.randint(0, 999) if zufall.random() < 0.5 else zufall.randint(0, 120)}" for _ in range(10000)]
ergebnis = wert_von(lambda: mit_behalten(100, namen))
assert ergebnis == vergleich_ladevorgaenge(100, namen), "Bei 10 000 Anfragen mit behalten=100 stimmen Ladevorgänge oder geladen() nicht."
