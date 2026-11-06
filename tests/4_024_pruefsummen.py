# Automatisch erzeugt aus lehrkraft/muster/4_024_pruefsummen.py - nicht von Hand ändern.
# vorlage-hash: c0eeafa94244045d
# text-hash: fa1cacf91ab32612
# thema: funktionen
# inhalt: Zähl- und Cache-Dekoratoren

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "6d0dae2a40d2\n68d3fe5a4898\n6d0dae2a40d2\n6d0dae2a40d2\n2 2"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"

@zaehle
def pruefe_passwort(passwort, *, mindestlaenge=12):
    """Prüft, ob ein Passwort lang genug ist."""
    return len(passwort) >= mindestlaenge


# zaehle zählt jeden Aufruf und reicht Argumente nach Position und Namen weiter
ergebnis = (pruefe_passwort.aufrufe, pruefe_passwort("kurz"), pruefe_passwort("kurz", mindestlaenge=4), pruefe_passwort.aufrufe)
assert ergebnis == (0, False, True, 2), (
    f"aufrufe zu Beginn, pruefe_passwort('kurz'), pruefe_passwort('kurz', mindestlaenge=4) und aufrufe danach "
    f"ergeben {ergebnis!r}, erwartet war (0, False, True, 2).\n"
    "Tipp: Setzen Sie huelle.aufrufe = 0 vor dem return im Dekorator und erhöhen Sie es in der Hülle."
)

@zaehle
def sperre(konto):
    """Sperrt ein Konto."""
    return f"{konto} gesperrt"


# Zwei gezählte Funktionen haben getrennte Zähler
ergebnis = (sperre("kim"), sperre("ali"), sperre("bo"))
assert ergebnis == ("kim gesperrt", "ali gesperrt", "bo gesperrt") and (sperre.aufrufe, pruefe_passwort.aufrufe) == (3, 2), (
    f"Nach drei Aufrufen von sperre (Ergebnisse {ergebnis!r}) ist sperre.aufrufe {sperre.aufrufe!r} und "
    f"pruefe_passwort.aufrufe {pruefe_passwort.aufrufe!r}; erwartet waren 3 und 2.\n"
    "Tipp: Jede Hülle braucht ihren eigenen Zähler als Attribut, keinen gemeinsamen globalen."
)

# zaehle zählt auch Aufrufe, die mit einer Ausnahme enden, und gibt die Ausnahme weiter
fehler_original = PermissionError("kein Zugriff")


@zaehle
def lies_akte(nummer):
    """Liest eine Personalakte, für die die Rechte fehlen."""
    raise fehler_original


try:
    lies_akte(7)
    gefangen = None
except Exception as fehler:
    gefangen = fehler
assert gefangen is fehler_original and lies_akte.aufrufe == 1, (
    f"lies_akte(7) löst {gefangen!r} aus, aufrufe ist danach {lies_akte.aufrufe!r}; erwartet war derselbe "
    "PermissionError und aufrufe 1.\nTipp: Erhöhen Sie den Zähler vor dem Aufruf von funktion."
)

# zwischenspeicher ruft die Funktion je Argumente nur einmal auf
berechnet = []


@zwischenspeicher
def rechte(benutzer, bereich):
    """Gibt die Rechte eines Benutzers in einem Bereich zurück."""
    berechnet.append((benutzer, bereich))
    return f"{benutzer}:{bereich}:lesen"


ergebnis = [rechte("kim", "lohn"), rechte("kim", "lager"), rechte("kim", "lohn"), rechte("ali", "lohn"), rechte("kim", "lohn")]
erwartet = ["kim:lohn:lesen", "kim:lager:lesen", "kim:lohn:lesen", "ali:lohn:lesen", "kim:lohn:lesen"]
assert ergebnis == erwartet and berechnet == [("kim", "lohn"), ("kim", "lager"), ("ali", "lohn")] and rechte.treffer == 2, (
    f"Fünf Aufrufe von rechte ergeben {ergebnis!r}, berechnet wurde für {berechnet!r}, treffer ist {rechte.treffer!r}; "
    f"erwartet war {erwartet!r}, berechnet nur für ('kim', 'lohn'), ('kim', 'lager'), ('ali', 'lohn') und treffer 2.\n"
    "Tipp: Nehmen Sie das Tupel args als Schlüssel eines Dictionarys."
)

# Ohne Argumente
berechnet = []


@zwischenspeicher
def richtlinie():
    """Lädt die Passwortrichtlinie."""
    berechnet.append("geladen")
    return {"mindestlaenge": 12}


ergebnis = (richtlinie(), richtlinie(), richtlinie())
assert ergebnis == ({"mindestlaenge": 12},) * 3 and berechnet == ["geladen"] and richtlinie.treffer == 2, (
    f"Dreimal richtlinie() ergibt {ergebnis!r}, berechnet wurde {len(berechnet)}-mal, treffer ist "
    f"{richtlinie.treffer!r}; erwartet war einmal berechnet und treffer 2."
)

# Auch die Ergebnisse None, False und 0 werden gemerkt
berechnet = []


BEFUNDE = {"a": None, "b": False, "c": 0, "d": ""}


@zwischenspeicher
def befund(konto):
    """Gibt den Prüfbefund eines Kontos zurück."""
    berechnet.append(konto)
    return BEFUNDE[konto]


ergebnis = [befund(konto) for konto in "abcdabcd"]
assert ergebnis == [None, False, 0, ""] * 2 and berechnet == ["a", "b", "c", "d"] and befund.treffer == 4, (
    f"befund für 'a', 'b', 'c', 'd' (Ergebnisse None, False, 0, '') und dann noch einmal ergibt {ergebnis!r}, "
    f"berechnet wurde für {berechnet!r}, treffer ist {befund.treffer!r}; erwartet war jedes Konto nur einmal "
    "berechnet und treffer 4.\n"
    "Tipp: speicher.get(args) ist auch None oder falsch, wenn das gemerkte Ergebnis None, False oder 0 ist; fragen "
    "Sie mit args in speicher."
)

# Eine Ausnahme wird nicht gemerkt, sondern weitergegeben; der nächste Aufruf rechnet neu
gesperrt = {"kim"}
fehler_original = PermissionError("gesperrt")


@zwischenspeicher
def anmelden(benutzer):
    """Meldet einen Benutzer an, gesperrte Benutzer lösen einen Fehler aus."""
    if benutzer in gesperrt:
        raise fehler_original
    return f"{benutzer} angemeldet"


try:
    anmelden("kim")
    gefangen = None
except Exception as fehler:
    gefangen = fehler
gesperrt.clear()
ergebnis = anmelden("kim")
assert gefangen is fehler_original and ergebnis == "kim angemeldet" and anmelden.treffer == 0, (
    f"anmelden('kim') löst zuerst {gefangen!r} aus; nach dem Entsperren ergibt es {ergebnis!r}, treffer ist "
    f"{anmelden.treffer!r}. Erwartet war derselbe PermissionError, dann 'kim angemeldet' und treffer 0.\n"
    "Tipp: Merken Sie sich das Ergebnis erst, wenn funktion ohne Ausnahme zurückgekehrt ist."
)

# leeren vergisst die gemerkten Ergebnisse, treffer bleibt stehen
ROLLEN = {"kim": "gast"}


@zwischenspeicher
def darf_lohndaten_sehen(benutzer):
    """Nur die Rolle personal darf Lohndaten sehen."""
    return ROLLEN[benutzer] == "personal"


vorher = (darf_lohndaten_sehen("kim"), darf_lohndaten_sehen("kim"))
ROLLEN["kim"] = "personal"
veraltet = darf_lohndaten_sehen("kim")
darf_lohndaten_sehen.leeren()
nachher = (darf_lohndaten_sehen("kim"), darf_lohndaten_sehen("kim"))
assert (vorher, veraltet, nachher, darf_lohndaten_sehen.treffer) == ((False, False), False, (True, True), 3), (
    f"Vor der Rechteänderung {vorher!r}, danach ohne leeren {veraltet!r}, nach leeren() {nachher!r}, treffer "
    f"{darf_lohndaten_sehen.treffer!r}; erwartet war (False, False), False, (True, True) und treffer 3.\n"
    "Tipp: leeren ist eine innere Funktion, die das Dictionary der Closure leert, z. B. mit speicher.clear()."
)

@zwischenspeicher
def plus_eins(x):
    """Rechnet x + 1."""
    return x + 1


@zwischenspeicher
def mal_zwei(x):
    """Rechnet x * 2."""
    return x * 2


# Zwei Zwischenspeicher sind voneinander unabhängig
ergebnis = (plus_eins(3), mal_zwei(3), plus_eins(3), mal_zwei(5))
plus_eins.leeren()
ergebnis = ergebnis + (mal_zwei(3), plus_eins.treffer, mal_zwei.treffer)
assert ergebnis == (4, 6, 4, 10, 6, 1, 1), (
    f"plus_eins(3), mal_zwei(3), plus_eins(3), mal_zwei(5), dann plus_eins.leeren(), mal_zwei(3) und die beiden "
    f"treffer ergeben {ergebnis!r}, erwartet war (4, 6, 4, 10, 6, 1, 1).\n"
    "Tipp: Legen Sie speicher als lokale Variable in zwischenspeicher an, nicht global; leeren darf nur den eigenen "
    "Speicher leeren."
)

# functools.wraps übernimmt Name, Docstring und __wrapped__
angaben = (pruefsumme.__name__, sperre.__name__, mal_zwei.__doc__, pruefsumme.__wrapped__ is berechne_pruefsumme, getattr(sperre, "__wrapped__", None) is not None)
assert angaben == ("berechne_pruefsumme", "sperre", "Rechnet x * 2.", True, True), (
    f"Name von pruefsumme und sperre, Docstring von mal_zwei, pruefsumme.__wrapped__ ist berechne_pruefsumme, "
    f"sperre hat __wrapped__: {angaben!r}; erwartet war ('berechne_pruefsumme', 'sperre', 'Rechnet x * 2.', True, "
    "True).\nTipp: Schreiben Sie in beiden Dekoratoren @functools.wraps(funktion) über die Hülle."
)

# Viele zufällige Aufrufe: Ergebnisse, treffer und aufrufe stimmen mit einer Nachrechnung überein
zufall = Zufall(4024)


@zaehle
def langsam(*werte):
    """Bildet die SHA-256-Prüfsumme der Werte."""
    return hashlib.sha256(repr(werte).encode()).hexdigest()


schnell = zwischenspeicher(langsam)
gesehen = set()
treffer = 0
for nummer in range(1000):
    werte = tuple(zufall.randint(0, 3) for _ in range(zufall.randint(0, 3)))
    if zufall.random() < 0.05:
        schnell.leeren()
        gesehen.clear()
    if werte in gesehen:
        treffer = treffer + 1
    gesehen.add(werte)
    ergebnis = schnell(*werte)
    erwartet = hashlib.sha256(repr(werte).encode()).hexdigest()
    zustand = (schnell.treffer, langsam.aufrufe)
    assert ergebnis == erwartet and zustand == (treffer, nummer + 1 - treffer), (
        f"Beim {nummer + 1}. zufälligen Aufruf schnell(*{werte}) ergibt {ergebnis[:12]!r}…, treffer und aufrufe sind "
        f"{zustand!r}; erwartet waren {erwartet[:12]!r}… und {(treffer, nummer + 1 - treffer)!r}."
    )

# Jeder Aufruf braucht O(1) Schritte, egal wie viel schon im Speicher steht
quadrat = zwischenspeicher(lambda x: x * x)
for x in range(3000):
    quadrat(x)
_, schritte_spaet = zaehle_schritte(quadrat, 10**6)
_, treffer_spaet = zaehle_schritte(quadrat, 1500)
_, schritte_frueh = zaehle_schritte(zwischenspeicher(lambda x: x * x), 10**6)
assert schritte_spaet <= schritte_frueh + 5 and treffer_spaet <= schritte_frueh + 5, (
    f"Mit 3000 gemerkten Ergebnissen braucht ein neuer Aufruf {schritte_spaet} Schritte und ein Treffer "
    f"{treffer_spaet}, bei leerem Speicher {schritte_frueh}; erwartet war O(1), also etwa gleich viele.\n"
    "Tipp: Merken Sie sich die Ergebnisse in einem Dictionary mit args als Schlüssel, nicht in einer Liste, die "
    "Sie durchsuchen."
)


class GezaehlteZahl(int):
    """Ganze Zahl, die mitzählt, wie oft sie verglichen wird (in und index auf Listen laufen in C)."""

    vergleiche = 0

    def __eq__(self, anderes):
        """Vergleicht wie int und zählt den Vergleich."""
        GezaehlteZahl.vergleiche += 1
        return int.__eq__(self, anderes)

    __hash__ = int.__hash__


# Nachschlagen vergleicht nicht mit allen gemerkten Argumenten
plus_eins = zwischenspeicher(lambda x: x + 1)
for x in range(3000):
    plus_eins(GezaehlteZahl(x))
GezaehlteZahl.vergleiche = 0
ergebnis = (plus_eins(GezaehlteZahl(10**6)), plus_eins(GezaehlteZahl(1500)))
assert ergebnis == (10**6 + 1, 1501) and GezaehlteZahl.vergleiche <= 10, (
    f"Mit 3000 gemerkten Ergebnissen ergeben ein neuer Aufruf und ein Treffer {ergebnis!r} (erwartet "
    f"{(10**6 + 1, 1501)!r}) und vergleichen die Argumente {GezaehlteZahl.vergleiche}-mal mit gemerkten; erwartet "
    "war O(1), also höchstens ein paar Vergleiche.\n"
    "Tipp: Merken Sie sich die Ergebnisse in einem Dictionary mit args als Schlüssel, nicht in einer Liste, die "
    "Sie mit in oder index durchsuchen."
)

# An der oberen Grenze: 100 000 Ergebnisse
quadrat = zwischenspeicher(zaehle(lambda x, y: x * y))
for x in range(100000):
    quadrat(x, x)
ergebnis = (quadrat(99999, 99999), quadrat(0, 0), quadrat.treffer, quadrat.__wrapped__.aufrufe)
assert ergebnis == (99999 * 99999, 0, 2, 100000), (
    f"Nach 100 000 verschiedenen Aufrufen und zwei Wiederholungen ergeben das letzte und das erste Ergebnis, treffer "
    f"und die gezählten Aufrufe {ergebnis!r}; erwartet war {(99999 * 99999, 0, 2, 100000)!r}."
)
