# Automatisch erzeugt aus lehrkraft/muster/4_012_lizenzen.py - nicht von Hand ändern.
# vorlage-hash: 26d72aa8cdc131f9
# text-hash: 146085a841b87779
# thema: klassen
# inhalt: `@dataclass` und `field`

# Felder mit Werten anlegen und lesen
lizenz = Lizenz("Office", 10, 120.0, ["Kaya"])
ergebnis = (lizenz.produkt, lizenz.plaetze, lizenz.preis_pro_platz, lizenz.nutzer)
assert ergebnis == ("Office", 10, 120.0, ["Kaya"]), (
    f'Lizenz("Office", 10, 120.0, ["Kaya"]) ergibt die Felder {ergebnis!r}, '
    "erwartet war ('Office', 10, 120.0, ['Kaya']).\nTipp: Die Reihenfolge der Felder ist auch die der Parameter."
)

# Lizenz ist eine Datenklasse mit genau diesen Feldern in dieser Reihenfolge
felder = list(getattr(Lizenz, "__dataclass_fields__", {}))
assert felder == ["produkt", "plaetze", "preis_pro_platz", "nutzer"], (
    f"Lizenz soll eine Datenklasse mit den Feldern produkt, plaetze, preis_pro_platz, nutzer sein; gefunden: {felder}."
)

# Standardwerte
lizenz = Lizenz("Editor")
ergebnis = (lizenz.plaetze, lizenz.preis_pro_platz, lizenz.nutzer)
assert ergebnis == (1, 0.0, []), (
    f'Lizenz("Editor") ergibt plaetze, preis_pro_platz und nutzer {ergebnis!r}, erwartet war (1, 0.0, []).'
)

# Felder als Schlüsselwort-Argumente
lizenz = Lizenz("VPN", preis_pro_platz=15.5, nutzer=["Lena"])
ergebnis = (lizenz.plaetze, lizenz.preis_pro_platz, lizenz.nutzer)
assert ergebnis == (1, 15.5, ["Lena"]), (
    f'Lizenz("VPN", preis_pro_platz=15.5, nutzer=["Lena"]) ergibt {ergebnis!r}, erwartet war (1, 15.5, [\'Lena\']).'
)

# __repr__ und __eq__ kommen von @dataclass
lizenz = Lizenz("Office", 3, 120.0)
erwartet = "Lizenz(produkt='Office', plaetze=3, preis_pro_platz=120.0, nutzer=[])"
assert repr(lizenz) == erwartet, f'repr(Lizenz("Office", 3, 120.0)) ergibt\n{repr(lizenz)}\nerwartet war\n{erwartet}'

# Lizenzen mit gleichen Feldern sind gleich
assert Lizenz("CAD", 2, 900.0) == Lizenz("CAD", 2, 900.0) and Lizenz("CAD", 2) != Lizenz("CAD", 3), (
    "Zwei Lizenzen mit denselben Feldern sollen gleich sein, mit verschiedenen Feldern ungleich."
)

# Jede Lizenz hat ihre eigene Liste
erste = Lizenz("Office", 5)
zweite = Lizenz("Office", 5)
erste.zuweisen("Kaya")
assert zweite.nutzer == [] and erste.nutzer is not zweite.nutzer, (
    f"Nach erste.zuweisen(\"Kaya\") hat die zweite Lizenz die Nutzer {zweite.nutzer!r}, erwartet war [].\n"
    "Tipp: Alle Lizenzen teilen sich dieselbe Liste. Nehmen Sie field(default_factory=list) als Standardwert."
)

# frei zählt die Plätze ohne Nutzer
for lizenz, erwartet in [
    (Lizenz("A", 10, 1.0, ["x", "y"]), 8),
    (Lizenz("A", 2, 1.0, ["x", "y"]), 0),
    (Lizenz("A"), 1),
    (Lizenz("A", 0), 0),
]:
    ergebnis = lizenz.frei()
    assert ergebnis == erwartet, f"{lizenz!r}.frei() ergibt {ergebnis!r}, erwartet war {erwartet}."

# zuweisen bis zum letzten Platz
lizenz = Lizenz("CAD", 2, 900.0)
lizenz.zuweisen("Nowak")
lizenz.zuweisen("Kaya")
assert lizenz.nutzer == ["Nowak", "Kaya"] and lizenz.frei() == 0, (
    f'Nach zuweisen("Nowak") und zuweisen("Kaya") bei 2 Plätzen ist nutzer {lizenz.nutzer!r} und frei() '
    f"{lizenz.frei()!r}, erwartet war ['Nowak', 'Kaya'] und 0.\n"
    "Tipp: Der letzte freie Platz darf noch vergeben werden."
)

# Kein freier Platz: ValueError, nichts ändert sich
for plaetze in [2, 0]:
    lizenz = Lizenz("CAD", plaetze, 900.0, ["Nowak", "Kaya"][:plaetze])
    vorher = list(lizenz.nutzer)
    try:
        lizenz.zuweisen("Lena")
        fehler = None
    except ValueError as ausnahme:
        fehler = ausnahme
    assert fehler is not None and lizenz.nutzer == vorher, (
        f"zuweisen(\"Lena\") bei einer vollen Lizenz mit {plaetze} Plätzen muss einen ValueError auslösen und nichts "
        f"ändern; Ausnahme: {fehler!r}, nutzer danach: {lizenz.nutzer!r}."
    )

# Doppelter Name: ValueError, nichts ändert sich
lizenz = Lizenz("VPN", 5, 15.0, ["Lena"])
try:
    lizenz.zuweisen("Lena")
    fehler = None
except ValueError as ausnahme:
    fehler = ausnahme
assert fehler is not None and lizenz.nutzer == ["Lena"], (
    'zuweisen("Lena"), obwohl Lena schon einen Platz hat, muss einen ValueError auslösen und nichts ändern; '
    f"Ausnahme: {fehler!r}, nutzer danach: {lizenz.nutzer!r}."
)

# ungenutzte_kosten aus dem Beispiel und für eine leere Liste
office = Lizenz("Office", 3, 120.0, ["Kaya"])
cad = Lizenz("CAD", 2, 900.0, ["Nowak"])
for lizenzen, erwartet in [([office, cad], 1140.0), ([], 0), ([Lizenz("A", 4, 0.0)], 0), ([Lizenz("A", 3, 2.5, ["x", "y", "z"])], 0)]:
    ergebnis = ungenutzte_kosten(lizenzen)
    assert ergebnis == erwartet, f"ungenutzte_kosten({lizenzen!r}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Viele zufällige Lizenzen mit zufälligen Zuweisungen
zufall = Zufall(4012)
namen = ["Kaya", "Nowak", "Lena", "Jonas", "Meier", "Demir"]
for _ in range(300):
    lizenzen = []
    erwartet = 0
    protokoll = []
    for nummer in range(zufall.randint(0, 5)):
        plaetze = zufall.randint(0, 6)
        preis = zufall.randint(0, 10**4 * 4) / 4
        lizenz = Lizenz(f"P{nummer}", plaetze, preis)
        vergeben = []
        for _ in range(zufall.randint(0, 8)):
            name = zufall.choice(namen)
            erlaubt = name not in vergeben and len(vergeben) < plaetze
            try:
                lizenz.zuweisen(name)
                geklappt = True
            except ValueError:
                geklappt = False
            protokoll.append(f"P{nummer}.zuweisen({name!r})")
            if erlaubt:
                vergeben.append(name)
            assert geklappt == erlaubt and lizenz.nutzer == vergeben, (
                f"Lizenz(\"P{nummer}\", {plaetze}, {preis}), dann {', '.join(protokoll[-6:])}: beim letzten Aufruf "
                f"erwartet {'kein' if erlaubt else 'ein'} ValueError und nutzer {vergeben}, "
                f"bekommen {'kein' if geklappt else 'ein'} ValueError und nutzer {lizenz.nutzer!r}."
            )
        lizenzen.append(lizenz)
        erwartet += (plaetze - len(vergeben)) * preis
    ergebnis = ungenutzte_kosten(lizenzen)
    assert abs(ergebnis - erwartet) < 1e-6, f"ungenutzte_kosten({lizenzen!r}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# An der oberen Grenze: 100 000 Lizenzen mit 10**6 Plätzen zu 10**4 Euro
lizenzen = [Lizenz("Groß", 10**6, 10**4, ["Kaya"]) for _ in range(100000)]
ergebnis = ungenutzte_kosten(lizenzen)
erwartet = 100000 * (10**6 - 1) * 10**4
assert ergebnis == erwartet, (
    f"Für 100 000 Lizenzen mit 10**6 Plätzen zu 10**4 Euro und je einem Nutzer ergibt ungenutzte_kosten {ergebnis!r}, "
    f"erwartet war {erwartet}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "Lizenz(produkt='Office', plaetze=3, preis_pro_platz=120.0, nutzer=['Kaya'])\n1140.0"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
