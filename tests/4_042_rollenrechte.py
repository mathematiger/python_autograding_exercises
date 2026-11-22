# Automatisch erzeugt aus lehrkraft/muster/4_042_rollenrechte.py - nicht von Hand ändern.
# vorlage-hash: 3abd2eea14ae594b
# text-hash: 8ecf60425ca02761
# thema: kontrollfluss
# inhalt: chain und zip_longest

def wert_von(aufruf):
    """Führt den Aufruf (eine Funktion ohne Argumente) aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def als_liste(iterator):
    """Holt alle Werte aus einem Iterator; ein Fehler wird als Text zurückgegeben."""
    if isinstance(iterator, str):
        return iterator
    try:
        return list(iterator)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


class Zaehlquelle:
    """Ein Iterator über Namen, der mitzählt, wie viele schon abgeholt wurden."""

    def __init__(self, namen):
        """Merkt sich die Namen."""
        self.namen = list(namen)
        self.abgeholt = 0

    def __iter__(self):
        """Ein Iterator ist sein eigener Iterator."""
        return self

    def __next__(self):
        """Liefert den nächsten Namen und zählt mit."""
        if self.abgeholt >= len(self.namen):
            raise StopIteration
        self.abgeholt += 1
        return self.namen[self.abgeholt - 1]


def vergleich_rechte(rollen, rollenrechte):
    """Vergleichslösung mit zwei Schleifen und einer Liste."""
    rechte = []
    for rolle in rollen:
        for recht in rollenrechte[rolle]:
            if recht not in rechte:
                rechte.append(recht)
    return rechte


def vergleich_aenderungen(vorher, nachher):
    """Vergleichslösung mit Indizes."""
    geaendert = []
    for stelle in range(max(len(vorher), len(nachher))):
        alt = vorher[stelle] if stelle < len(vorher) else None
        neu = nachher[stelle] if stelle < len(nachher) else None
        if alt != neu:
            geaendert.append((stelle + 1, alt, neu))
    return geaendert


ROLLENRECHTE = {
    "vertrieb": ["crm_lesen", "angebote_schreiben"],
    "support": ["crm_lesen", "tickets_bearbeiten"],
}

# alle_konten im Beispiel
ergebnis = als_liste(wert_von(lambda: alle_konten(["root"], ["backup"], ["gast1", "gast2"])))
assert ergebnis == ["root", "backup", "gast1", "gast2"], (
    f'list(alle_konten(["root"], ["backup"], ["gast1", "gast2"])) ergibt {ergebnis!r}, '
    'erwartet war ["root", "backup", "gast1", "gast2"].\nTipp: chain(admins, dienstkonten, gaeste).'
)

# alle_konten mit leeren Gruppen
ergebnis = als_liste(wert_von(lambda: alle_konten([], ["svc"], [])))
ergebnis_leer = als_liste(wert_von(lambda: alle_konten([], [], [])))
assert ergebnis == ["svc"] and ergebnis_leer == [], (
    f'alle_konten([], ["svc"], []) ergibt {ergebnis!r} und alle_konten([], [], []) {ergebnis_leer!r}, erwartet war ["svc"] und [].'
)

# alle_konten gibt einen Iterator zurück, keine Liste
ergebnis = wert_von(lambda: alle_konten(["a"], ["b"], ["c"]))
assert not isinstance(ergebnis, (list, tuple, str)) and hasattr(ergebnis, "__next__"), (
    f"alle_konten gibt {type(ergebnis).__name__} zurück, erwartet war ein Iterator (etwa von chain), "
    "auf den man next(...) anwenden kann."
)

# alle_konten holt die Namen erst, wenn sie gebraucht werden
admins, dienste, gaeste = Zaehlquelle(["root", "admin"]), Zaehlquelle(["backup"]), Zaehlquelle(["gast"])
konten = wert_von(lambda: alle_konten(admins, dienste, gaeste))
erster = wert_von(lambda: next(konten))
abgeholt = [admins.abgeholt, dienste.abgeholt, gaeste.abgeholt]
assert erster == "root" and abgeholt == [1, 0, 0], (
    f"Nach alle_konten(...) und einem next(...) wurden aus den drei Quellen {abgeholt} Namen geholt, erwartet war "
    "[1, 0, 0].\nTipp: Bauen Sie keine Liste, sondern geben Sie chain(...) direkt zurück."
)

# alle_konten benutzt chain
assert verwendet("chain"), "Benutzen Sie in alle_konten itertools.chain."

# rechte_von im Beispiel
ergebnis = wert_von(lambda: rechte_von(["vertrieb", "support"], ROLLENRECHTE))
assert ergebnis == ["crm_lesen", "angebote_schreiben", "tickets_bearbeiten"], (
    f'rechte_von(["vertrieb", "support"], rollenrechte) ergibt {ergebnis!r}, '
    'erwartet war ["crm_lesen", "angebote_schreiben", "tickets_bearbeiten"].\n'
    "Tipp: crm_lesen kommt in beiden Rollen vor, steht aber nur einmal im Ergebnis."
)

# rechte_von: die Reihenfolge der Rollen bestimmt die Reihenfolge der Rechte
ergebnis = wert_von(lambda: rechte_von(["support", "vertrieb"], ROLLENRECHTE))
assert ergebnis == ["crm_lesen", "tickets_bearbeiten", "angebote_schreiben"], (
    f'rechte_von(["support", "vertrieb"], rollenrechte) ergibt {ergebnis!r}, '
    'erwartet war ["crm_lesen", "tickets_bearbeiten", "angebote_schreiben"] (nicht sortieren!).'
)

# rechte_von mit einer Rolle und mit anderen Rechten (nicht fest hinschreiben!)
rechte = {"admin": ["alles"], "leser": ["lesen", "suchen"], "leer": []}
ergebnis = wert_von(lambda: [rechte_von(["leser"], rechte), rechte_von(["admin", "leser"], rechte)])
assert ergebnis == [["lesen", "suchen"], ["alles", "lesen", "suchen"]], (
    f'rechte_von(["leser"], …) und rechte_von(["admin", "leser"], …) ergeben {ergebnis!r}, '
    'erwartet war [["lesen", "suchen"], ["alles", "lesen", "suchen"]].'
)

# rechte_von ohne Rollen und mit einer Rolle ohne Rechte
ergebnis = wert_von(lambda: [rechte_von([], rechte), rechte_von(["leer"], rechte), rechte_von(["leer", "admin"], rechte)])
assert ergebnis == [[], [], ["alles"]], (
    f'rechte_von([], …), rechte_von(["leer"], …) und rechte_von(["leer", "admin"], …) ergeben {ergebnis!r}, '
    'erwartet war [[], [], ["alles"]].'
)

# rechte_von: dieselbe Rolle zweimal und doppelte Rechte in einer Rolle
rechte = {"a": ["x", "y", "x"], "b": ["y", "z"]}
ergebnis = wert_von(lambda: rechte_von(["a", "b", "a"], rechte))
assert ergebnis == ["x", "y", "z"], f'rechte_von(["a", "b", "a"], {rechte}) ergibt {ergebnis!r}, erwartet war ["x", "y", "z"].'

# rechte_von verändert rollenrechte nicht
rechte = {"a": ["x", "y"], "b": ["y", "z"]}
wert_von(lambda: rechte_von(["a", "b"], rechte))
assert rechte == {"a": ["x", "y"], "b": ["y", "z"]}, (
    f"Nach rechte_von ist rollenrechte {rechte}, erwartet war es unverändert.\n"
    "Tipp: Hängen Sie nichts an die Listen in rollenrechte an; sammeln Sie die Rechte in einer neuen Liste."
)

# rechte_von benutzt chain.from_iterable oder chain
assert verwendet("from_iterable") or verwendet("chain"), "Benutzen Sie in rechte_von itertools.chain.from_iterable."

# aenderungen im Beispiel
ergebnis = wert_von(lambda: aenderungen(["a", "b", "c"], ["a", "x"]))
assert ergebnis == [(2, "b", "x"), (3, "c", None)], (
    f'aenderungen(["a", "b", "c"], ["a", "x"]) ergibt {ergebnis!r}, erwartet war [(2, "b", "x"), (3, "c", None)].\n'
    "Tipp: zip hört nach der kürzeren Liste auf; zip_longest füllt mit None auf."
)

# aenderungen: gleich lange Listen
ergebnis = wert_von(lambda: aenderungen(["lesen", "schreiben", "loeschen"], ["lesen", "lesen", "loeschen"]))
assert ergebnis == [(2, "schreiben", "lesen")], (
    f'aenderungen(["lesen", "schreiben", "loeschen"], ["lesen", "lesen", "loeschen"]) ergibt {ergebnis!r}, '
    'erwartet war [(2, "schreiben", "lesen")].'
)

# aenderungen: nachher ist länger, neue Zeilen haben alt = None
ergebnis = wert_von(lambda: aenderungen(["a"], ["a", "b", "c"]))
assert ergebnis == [(2, None, "b"), (3, None, "c")], (
    f'aenderungen(["a"], ["a", "b", "c"]) ergibt {ergebnis!r}, erwartet war [(2, None, "b"), (3, None, "c")].'
)

# aenderungen: keine Änderung und leere Exporte
ergebnis = wert_von(lambda: [aenderungen(["a", "b"], ["a", "b"]), aenderungen([], []), aenderungen([], ["n"]), aenderungen(["v"], [])])
assert ergebnis == [[], [], [(1, None, "n")], [(1, "v", None)]], (
    f"aenderungen für gleiche Listen, zwei leere, ([], ['n']) und (['v'], []) ergibt {ergebnis!r}, "
    "erwartet war [[], [], [(1, None, 'n')], [(1, 'v', None)]]."
)

# aenderungen benutzt zip_longest
assert verwendet("zip_longest"), "Benutzen Sie in aenderungen itertools.zip_longest."

# Die Ausgabe des Programms
erwartet = (
    "['root', 'backup', 'gast1', 'gast2']\n['crm_lesen', 'angebote_schreiben', 'tickets_bearbeiten']\n"
    "[(2, 'b', 'x'), (3, 'c', None)]"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Rollen und Exporte
zufall = Zufall(4042)
woerter = ["lesen", "schreiben", "loeschen", "export", "admin", "drucken", "vpn", "mail"]
for _ in range(300):
    rollenrechte = {}
    for rolle in ["r1", "r2", "r3", "r4"]:
        rollenrechte[rolle] = [zufall.choice(woerter) for _ in range(zufall.randint(0, 4))]
    rollen = [zufall.choice(list(rollenrechte)) for _ in range(zufall.randint(0, 5))]
    ergebnis = wert_von(lambda: rechte_von(rollen, rollenrechte))
    erwartet = vergleich_rechte(rollen, rollenrechte)
    assert ergebnis == erwartet, f"rechte_von({rollen}, {rollenrechte}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    vorher = [zufall.choice(woerter[:3]) for _ in range(zufall.randint(0, 5))]
    nachher = [zufall.choice(woerter[:3]) for _ in range(zufall.randint(0, 5))]
    ergebnis = wert_von(lambda: aenderungen(vorher, nachher))
    erwartet = vergleich_aenderungen(vorher, nachher)
    assert ergebnis == erwartet, f"aenderungen({vorher}, {nachher}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    gruppen = [[f"k{zufall.randint(0, 9)}" for _ in range(zufall.randint(0, 3))] for _ in range(3)]
    ergebnis = als_liste(wert_von(lambda: alle_konten(*gruppen)))
    assert ergebnis == gruppen[0] + gruppen[1] + gruppen[2], f"list(alle_konten(*{gruppen})) ergibt {ergebnis!r}."

# Laufzeit: rechte_von vergleicht jedes Recht nur mit wenigen anderen, nicht mit allen bisherigen
class Zaehltext(str):
    """Ein Text, der mitzählt, wie oft er mit == verglichen wird."""

    vergleiche = 0

    def __eq__(self, anderer):
        """Vergleicht wie ein Text und zählt mit."""
        Zaehltext.vergleiche += 1
        return str.__eq__(self, anderer)

    def __hash__(self):
        """Derselbe Hashwert wie beim gewöhnlichen Text."""
        return str.__hash__(self)


rechte = {"r1": [Zaehltext(f"x{stelle}") for stelle in range(2000)], "r2": [Zaehltext(f"x{stelle}") for stelle in range(0, 2000, 2)]}
Zaehltext.vergleiche = 0
ergebnis = wert_von(lambda: rechte_von(["r1", "r2"], rechte))
assert ergebnis == [f"x{stelle}" for stelle in range(2000)] and Zaehltext.vergleiche <= 9000, (
    f"rechte_von vergleicht bei 3000 Rechten (2000 verschiedene) {Zaehltext.vergleiche}-mal zwei Rechte; bei O(n) "
    "wären es höchstens einige Tausend.\nTipp: Prüfen Sie „schon gesehen?“ mit einer Menge, nicht mit in auf der Ergebnisliste."
)

# Obere Grenze: 1000 Rollen mit zusammen 100 000 Rechten, davon 50 000 verschiedene
rollenrechte = {f"rolle{nummer}": [f"recht{(nummer * 100 + stelle) % 50000}" for stelle in range(100)] for nummer in range(1000)}
rollen = list(rollenrechte)
ergebnis = wert_von(lambda: rechte_von(rollen, rollenrechte))
erwartet = list(dict.fromkeys(f"recht{zahl % 50000}" for zahl in range(100000)))
assert ergebnis == erwartet, (
    "Bei 1000 Rollen mit zusammen 100 000 Rechten stimmt das Ergebnis von rechte_von nicht."
    if isinstance(ergebnis, list) else f"Bei 1000 Rollen mit zusammen 100 000 Rechten ergibt rechte_von {ergebnis!r}."
)

# Obere Grenze: zwei Exporte mit 100 000 Zeilen
vorher = [f"z{stelle}" for stelle in range(100000)]
nachher = [f"z{stelle}" if stelle % 1000 else "neu" for stelle in range(99000)]
ergebnis = wert_von(lambda: aenderungen(vorher, nachher))
erwartet = vergleich_aenderungen(vorher, nachher)
assert ergebnis == erwartet, (
    f"Bei 100 000 und 99 000 Zeilen findet aenderungen {len(ergebnis) if isinstance(ergebnis, list) else ergebnis} "
    f"Änderungen, erwartet waren {len(erwartet)}."
)
