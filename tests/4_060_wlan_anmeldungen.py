# Automatisch erzeugt aus lehrkraft/muster/4_060_wlan_anmeldungen.py - nicht von Hand ändern.
# vorlage-hash: 5f90fff1e87c64d4
# text-hash: a4c3267627598cc8
# thema: datenstrukturen
# inhalt: collections.defaultdict

BEISPIEL = [
    ("ap-eg", "Firma", "laptop-ada"),
    ("ap-og", "Gast", "handy-bo"),
    ("ap-eg", "Gast", "tablet-cem"),
    ("ap-eg", "Firma", "handy-dana"),
    ("ap-og", "Firma", "laptop-ada"),
]


def wert_von(funktion, anmeldungen):
    """Ruft die Funktion mit einer Kopie der Liste auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(list(anmeldungen))
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_geraete(anmeldungen):
    """Vergleichslösung mit setdefault."""
    ergebnis = {}
    for ap, _ssid, geraet in anmeldungen:
        ergebnis.setdefault(ap, []).append(geraet)
    return ergebnis


def vergleich_ssids(anmeldungen):
    """Vergleichslösung: für jeden AP alle SSIDs einsammeln, dann ohne Doppelte sortieren."""
    ergebnis = {}
    for ap, ssid, _geraet in anmeldungen:
        if ap not in ergebnis:
            ergebnis[ap] = []
        if ssid not in ergebnis[ap]:
            ergebnis[ap].append(ssid)
    return {ap: sorted(ssids) for ap, ssids in ergebnis.items()}


def vergleich_anzahl(anmeldungen):
    """Vergleichslösung mit zwei Ebenen von get."""
    ergebnis = {}
    for ap, ssid, _geraet in anmeldungen:
        innen = ergebnis.get(ssid, {})
        innen[ap] = innen.get(ap, 0) + 1
        ergebnis[ssid] = innen
    return ergebnis


def meldung(name, anmeldungen, ergebnis, erwartet, tipp=""):
    """Fehlermeldung mit Aufruf, Ergebnis und erwartetem Wert."""
    gezeigt = repr(anmeldungen) if len(anmeldungen) <= 8 else repr(anmeldungen[:8])[:-1] + ", …]"
    return f"{name}({gezeigt})\nergibt {ergebnis!r},\nerwartet war {erwartet!r}.{tipp}"


def nur_dicts(wert):
    """True, wenn wert ein gewöhnliches dict ist und alle Werte darin keine defaultdicts sind."""
    if type(wert) is not dict:
        return False
    for innen in wert.values():
        if isinstance(innen, dict) and type(innen) is not dict:
            return False
    return True


# geraete_je_ap im Beispiel: die Geräte je AP
ergebnis = wert_von(geraete_je_ap, BEISPIEL)
assert isinstance(ergebnis, dict) and dict(ergebnis) == vergleich_geraete(BEISPIEL), meldung(
    "geraete_je_ap", BEISPIEL, ergebnis, vergleich_geraete(BEISPIEL),
    "\nTipp: gruppen = defaultdict(list) und dann gruppen[ap].append(geraet).",
)

# geraete_je_ap gibt ein gewöhnliches Dictionary zurück
assert type(ergebnis) is dict, (
    f"geraete_je_ap ergibt ein {type(ergebnis).__name__}, erwartet war ein gewöhnliches dict.\nTipp: return dict(gruppen)."
)

# geraete_je_ap mit anderen Anmeldungen (nicht fest hinschreiben!)
anmeldungen = [("ap-keller", "Technik", "sensor-1"), ("ap-dach", "Technik", "kamera-2"), ("ap-keller", "Gast", "sensor-1")]
ergebnis = wert_von(geraete_je_ap, anmeldungen)
assert ergebnis == vergleich_geraete(anmeldungen), meldung("geraete_je_ap", anmeldungen, ergebnis, vergleich_geraete(anmeldungen))

# geraete_je_ap: ein Gerät, das sich mehrmals anmeldet, steht mehrmals darin
anmeldungen = [("ap-eg", "Firma", "laptop-ada"), ("ap-eg", "Gast", "laptop-ada"), ("ap-eg", "Firma", "laptop-ada")]
ergebnis = wert_von(geraete_je_ap, anmeldungen)
assert ergebnis == vergleich_geraete(anmeldungen), meldung(
    "geraete_je_ap", anmeldungen, ergebnis, vergleich_geraete(anmeldungen), "\nTipp: Eine Liste, keine Menge: jede Anmeldung zählt."
)

# geraete_je_ap: keine Anmeldungen
ergebnis = wert_von(geraete_je_ap, [])
assert ergebnis == {}, meldung("geraete_je_ap", [], ergebnis, {})

# ssids_je_ap im Beispiel
ergebnis = wert_von(ssids_je_ap, BEISPIEL)
assert isinstance(ergebnis, dict) and dict(ergebnis) == vergleich_ssids(BEISPIEL), meldung(
    "ssids_je_ap", BEISPIEL, ergebnis, vergleich_ssids(BEISPIEL),
    "\nTipp: defaultdict(set) sammelt jede SSID nur einmal; sorted(...) macht daraus eine sortierte Liste.",
)

# ssids_je_ap mit anderen Anmeldungen, eine SSID mehrmals am selben AP (nicht fest hinschreiben!)
anmeldungen = [
    ("ap-halle", "Lager", "scanner-1"),
    ("ap-halle", "Gast", "handy-bo"),
    ("ap-halle", "Lager", "scanner-2"),
    ("ap-buero", "Firma", "laptop-ada"),
]
ergebnis = wert_von(ssids_je_ap, anmeldungen)
assert ergebnis == vergleich_ssids(anmeldungen), meldung("ssids_je_ap", anmeldungen, ergebnis, vergleich_ssids(anmeldungen))

# ssids_je_ap: die Werte sind sortierte Listen und das Ergebnis ein gewöhnliches Dictionary
assert type(ergebnis) is dict and all(type(ssids) is list for ssids in ergebnis.values()), (
    f"ssids_je_ap ergibt {ergebnis!r}, erwartet war ein dict mit Listen als Werten.\n"
    "Tipp: Wandeln Sie jede Menge mit sorted(...) in eine Liste um und geben Sie ein neues dict zurück."
)

# ssids_je_ap: keine Anmeldungen
ergebnis = wert_von(ssids_je_ap, [])
assert ergebnis == {}, meldung("ssids_je_ap", [], ergebnis, {})

# anzahl_je_ssid_und_ap im Beispiel: die Zahlen stimmen
ergebnis = wert_von(anzahl_je_ssid_und_ap, BEISPIEL)
assert isinstance(ergebnis, dict) and {ssid: dict(innen) for ssid, innen in ergebnis.items()} == vergleich_anzahl(BEISPIEL), meldung(
    "anzahl_je_ssid_und_ap", BEISPIEL, ergebnis, vergleich_anzahl(BEISPIEL),
    "\nTipp: tabelle = defaultdict(lambda: defaultdict(int)) und tabelle[ssid][ap] += 1.",
)

# anzahl_je_ssid_und_ap mit anderen Anmeldungen (nicht fest hinschreiben!)
anmeldungen = [
    ("ap-1", "Firma", "a"), ("ap-2", "Firma", "b"), ("ap-1", "Firma", "c"),
    ("ap-3", "Labor", "d"), ("ap-1", "Firma", "a"),
]
ergebnis = wert_von(anzahl_je_ssid_und_ap, anmeldungen)
assert isinstance(ergebnis, dict) and {ssid: dict(innen) for ssid, innen in ergebnis.items()} == vergleich_anzahl(anmeldungen), meldung(
    "anzahl_je_ssid_und_ap", anmeldungen, ergebnis, vergleich_anzahl(anmeldungen)
)

# anzahl_je_ssid_und_ap: außen und innen gewöhnliche Dictionaries
assert nur_dicts(ergebnis), (
    f"anzahl_je_ssid_und_ap ergibt {ergebnis!r}; erwartet waren gewöhnliche dicts, außen und innen.\n"
    "Tipp: dict(tabelle) wandelt nur die äußere Ebene um; wandeln Sie auch jedes innere mit dict(...) um."
)

# anzahl_je_ssid_und_ap: ein Nachschlagen mit Tippfehler legt nichts an
try:
    ergebnis["Fimra"]
except KeyError:
    pass
except Exception:
    pass
assert "Fimra" not in ergebnis, (
    "Nach ergebnis[\"Fimra\"] steht die SSID \"Fimra\" im Ergebnis von anzahl_je_ssid_und_ap.\n"
    "Tipp: Ein defaultdict legt fehlende Schlüssel beim Lesen an; geben Sie ein gewöhnliches dict zurück."
)

# anzahl_je_ssid_und_ap: keine Anmeldungen
ergebnis = wert_von(anzahl_je_ssid_und_ap, [])
assert ergebnis == {}, meldung("anzahl_je_ssid_und_ap", [], ergebnis, {})

# Die Lösung benutzt defaultdict
assert verwendet("defaultdict"), "Gruppieren Sie mit collections.defaultdict, zum Beispiel defaultdict(list)."

# Viele zufällige Protokolle
zufall = Zufall(4060)
aps = ["ap-eg", "ap-og", "ap-keller", "ap-halle"]
ssids = ["Firma", "Gast", "Labor", "Technik"]
geraete = ["laptop-ada", "handy-bo", "tablet-cem", "drucker-3", "kamera-7"]
for _ in range(200):
    anmeldungen = [(zufall.choice(aps), zufall.choice(ssids), zufall.choice(geraete)) for _ in range(zufall.randint(0, 12))]
    ergebnis = wert_von(geraete_je_ap, anmeldungen)
    assert ergebnis == vergleich_geraete(anmeldungen), meldung("geraete_je_ap", anmeldungen, ergebnis, vergleich_geraete(anmeldungen))
    ergebnis = wert_von(ssids_je_ap, anmeldungen)
    assert ergebnis == vergleich_ssids(anmeldungen), meldung("ssids_je_ap", anmeldungen, ergebnis, vergleich_ssids(anmeldungen))
    ergebnis = wert_von(anzahl_je_ssid_und_ap, anmeldungen)
    assert ergebnis == vergleich_anzahl(anmeldungen), meldung(
        "anzahl_je_ssid_und_ap", anmeldungen, ergebnis, vergleich_anzahl(anmeldungen)
    )

# Obere Grenze: 100 000 Anmeldungen an 300 APs
anmeldungen = [(f"ap-{zufall.randint(1, 300)}", zufall.choice(ssids), f"geraet-{zufall.randint(1, 5000)}") for _ in range(100000)]
assert wert_von(geraete_je_ap, anmeldungen) == vergleich_geraete(anmeldungen), "Bei 100 000 Anmeldungen stimmt geraete_je_ap nicht."
# Obere Grenze: ssids_je_ap bei 100 000 Anmeldungen
assert wert_von(ssids_je_ap, anmeldungen) == vergleich_ssids(anmeldungen), "Bei 100 000 Anmeldungen stimmt ssids_je_ap nicht."
# Obere Grenze: anzahl_je_ssid_und_ap bei 100 000 Anmeldungen
assert wert_von(anzahl_je_ssid_und_ap, anmeldungen) == vergleich_anzahl(anmeldungen), (
    "Bei 100 000 Anmeldungen stimmt anzahl_je_ssid_und_ap nicht."
)
