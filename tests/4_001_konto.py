# Automatisch erzeugt aus lehrkraft/muster/4_001_konto.py - nicht von Hand ändern.
# vorlage-hash: 7e40a7711a406eee
# text-hash: f4203ee01a0133c9
# thema: klassen
# inhalt: Klassen und Invarianten

# Attribute werden in __init__ gesetzt
k = Konto("Bo", 10)
assert (k.inhaber, k.stand) == ("Bo", 10), (
    f"Nach Konto('Bo', 10) erwartet inhaber='Bo' und stand=10, "
    f"gefunden: inhaber={getattr(k, 'inhaber', None)!r}, stand={getattr(k, 'stand', None)!r}."
)

# Ohne Anfangsstand ist der Stand 0
assert Konto("Cem").stand == 0, f"Konto('Cem').stand ergibt {Konto('Cem').stand!r}, erwartet war 0 (Standardwert)."

# einzahlen und abheben verändern den Stand
k = Konto("Bo", 10)
k.einzahlen(25)
k.abheben(5)
assert k.stand == 30, f"Nach Konto('Bo', 10), einzahlen(25), abheben(5) ist stand {k.stand!r}, erwartet war 30."

# Abheben über dem Stand löst ValueError aus und ändert nichts
k = Konto("Bo", 10)
try:
    k.abheben(50)
    fehler = None
except ValueError as ausnahme:
    fehler = ausnahme
assert fehler is not None and k.stand == 10, (
    "abheben(50) bei Stand 10 muss einen ValueError auslösen und den Stand bei 10 lassen; "
    f"Ausnahme: {fehler!r}, Stand danach: {k.stand!r}."
)

# Den ganzen Stand abheben ist erlaubt
k = Konto("Bo", 10)
try:
    k.abheben(10)
    fehler = None
except ValueError as ausnahme:
    fehler = ausnahme
assert fehler is None and k.stand == 0, (
    f"abheben(10) bei Stand 10 muss klappen und den Stand auf 0 setzen; Ausnahme: {fehler!r}, Stand danach: {k.stand!r}.\n"
    "Tipp: Verboten ist nur ein Betrag über dem Stand, also betrag > self.stand."
)

# Der kleinste positive Betrag 1 ist erlaubt
k = Konto("Bo", 10)
try:
    k.einzahlen(1)
    k.abheben(1)
    fehler = None
except ValueError as ausnahme:
    fehler = ausnahme
assert fehler is None and k.stand == 10, (
    "einzahlen(1) und danach abheben(1) bei Stand 10 müssen klappen, Stand danach 10; "
    f"Ausnahme: {fehler!r}, Stand danach: {k.stand!r}.\n"
    "Tipp: Verboten sind nur Beträge <= 0."
)

# Negative und Null-Beträge lösen ValueError aus
for methode, betrag in [("einzahlen", 0), ("einzahlen", -5), ("abheben", 0), ("abheben", -5)]:
    k = Konto("Bo", 10)
    try:
        getattr(k, methode)(betrag)
        geklappt = True
    except ValueError:
        geklappt = False
    assert not geklappt and k.stand == 10, f"{methode}({betrag}) muss einen ValueError auslösen, Stand bleibt 10."

# Große Beträge an der oberen Grenze
k = Konto("Bo", 10**9)
k.abheben(10**9)
k.einzahlen(10**9)
k.einzahlen(10**9)
assert k.stand == 2 * 10**9, (
    "Konto('Bo', 10**9), abheben(10**9), einzahlen(10**9), einzahlen(10**9): "
    f"erwartet stand {2 * 10**9}, bekommen {k.stand!r}."
)

# Viele zufällige Buchungen: Stand und ValueError stimmen mit einer Nachrechnung überein
zufall = Zufall(4001)
fehlerfall = None
for versuch in range(300):
    start = zufall.randint(0, 200)
    k = Konto("Zufall", start)
    erwartet = start
    buchungen = []
    for schritt in range(15):
        methode = zufall.choice(["einzahlen", "abheben"])
        betrag = zufall.randint(-20, 150)
        buchungen.append(f"{methode}({betrag})")
        erlaubt = betrag > 0 and (methode == "einzahlen" or betrag <= erwartet)
        try:
            getattr(k, methode)(betrag)
            ausgeloest = False
        except ValueError:
            ausgeloest = True
        if erlaubt:
            erwartet = erwartet + betrag if methode == "einzahlen" else erwartet - betrag
        if ausgeloest == erlaubt or k.stand != erwartet:
            fehlerfall = (start, buchungen, erlaubt, ausgeloest, erwartet, k.stand)
            break
    if fehlerfall is not None:
        break
assert fehlerfall is None, (
    f"Konto('Zufall', {fehlerfall[0]}), dann {', '.join(fehlerfall[1])}: "
    f"bei der letzten Buchung erwartet {'kein' if fehlerfall[2] else 'ein'} ValueError und stand {fehlerfall[4]}, "
    f"bekommen {'ein' if fehlerfall[3] else 'kein'} ValueError und stand {fehlerfall[5]!r}."
)

# __str__ liefert den beschriebenen Text
k = Konto("Anna", 120)
assert str(k) == "Konto von Anna: 120 Euro", f'str(Konto("Anna", 120)) ergibt {str(k)!r}, erwartet war "Konto von Anna: 120 Euro".'

# Die Ausgabe des Programms stimmt
assert AUSGABE == "Konto von Anna: 120 Euro", f'Erwartete Ausgabe: "Konto von Anna: 120 Euro" – Ihr Programm: "{AUSGABE}"'
