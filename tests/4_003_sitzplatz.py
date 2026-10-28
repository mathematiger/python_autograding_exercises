# Automatisch erzeugt aus lehrkraft/muster/4_003_sitzplatz.py - nicht von Hand ändern.
# vorlage-hash: c4c96c26edba9d8b
# thema: klassen
# inhalt: `__eq__` und `__hash__`

# Gleiche Plätze sind gleich, auch wenn sie getrennt erzeugt wurden
a = Sitzplatz(1, "F", 7)
b = Sitzplatz(1, "F", 7)
assert a == b, (
    'Sitzplatz(1, "F", 7) == Sitzplatz(1, "F", 7) ergibt False, erwartet war True.\n'
    "Tipp: Vergleichen Sie in __eq__ Saal, Reihe und Nummer, nicht die Objekte selbst."
)

# Plätze, die sich in Saal, Reihe oder Nummer unterscheiden, sind verschieden (nicht immer True zurückgeben!)
for anderer in [Sitzplatz(2, "F", 7), Sitzplatz(1, "G", 7), Sitzplatz(1, "F", 8)]:
    gleich = Sitzplatz(1, "F", 7) == anderer
    assert gleich is False, f'Sitzplatz(1, "F", 7) == {anderer!r} ergibt {gleich!r}, erwartet war False.'

# != ist das Gegenteil von ==
assert Sitzplatz(3, "A", 1) != Sitzplatz(3, "A", 2) and not (Sitzplatz(3, "A", 1) != Sitzplatz(3, "A", 1)), (
    'Sitzplatz(3, "A", 1) != Sitzplatz(3, "A", 2) muss True sein und Sitzplatz(3, "A", 1) != Sitzplatz(3, "A", 1) False.'
)

# Vergleich mit etwas anderem als einem Sitzplatz ergibt False statt eines Fehlers
try:
    ergebnisse = [Sitzplatz(1, "F", 7) == (1, "F", 7), Sitzplatz(1, "F", 7) == "F7", Sitzplatz(1, "F", 7) == None]
    fehler = None
except Exception as ausnahme:
    ergebnisse = None
    fehler = ausnahme
assert ergebnisse == [False, False, False], (
    'Sitzplatz(1, "F", 7) == (1, "F", 7), == "F7" und == None sollen jeweils False ergeben; '
    f"Ergebnisse: {ergebnisse!r}, Ausnahme: {fehler!r}.\n"
    "Tipp: Prüfen Sie mit isinstance(other, Sitzplatz) und geben Sie sonst NotImplemented zurück."
)

# __eq__ gibt bei fremden Objekten NotImplemented zurück
ergebnis = Sitzplatz(1, "F", 7).__eq__((1, "F", 7))
assert ergebnis is NotImplemented, (
    f'Sitzplatz(1, "F", 7).__eq__((1, "F", 7)) ergibt {ergebnis!r}, erwartet war NotImplemented.\n'
    "Tipp: Mit NotImplemented darf auch das andere Objekt noch entscheiden, ob es gleich ist."
)

# Sitzplätze lassen sich hashen
try:
    hashwert = hash(Sitzplatz(1, "F", 7))
    fehler = None
except TypeError as ausnahme:
    hashwert = None
    fehler = ausnahme
assert fehler is None and isinstance(hashwert, int), (
    f'hash(Sitzplatz(1, "F", 7)) löst {fehler!r} aus bzw. ergibt {hashwert!r}, erwartet war eine ganze Zahl.\n'
    "Tipp: Wer __eq__ definiert, muss auch __hash__ definieren, sonst sind die Objekte nicht hashbar."
)

# Gleiche Plätze haben den gleichen Hashwert
for saal, reihe, nummer in [(1, "F", 7), (2, "A", 1), (5, "K", 12)]:
    erster = hash(Sitzplatz(saal, reihe, nummer))
    zweiter = hash(Sitzplatz(saal, reihe, nummer))
    assert erster == zweiter, (
        f"Zwei getrennt erzeugte Sitzplatz({saal}, {reihe!r}, {nummer}) haben die Hashwerte {erster} und {zweiter}; "
        "gleiche Objekte müssen den gleichen Hashwert haben.\n"
        "Tipp: Bilden Sie den Hash aus den Attributen, z. B. hash((self.saal, self.reihe, self.nummer)), nicht aus id(self)."
    )

# In einer Menge wird ein gebuchter Platz wiedergefunden
gebucht = {Sitzplatz(1, "F", 7), Sitzplatz(1, "F", 8)}
gefunden = [Sitzplatz(1, "F", 7) in gebucht, Sitzplatz(1, "F", 8) in gebucht, Sitzplatz(2, "F", 7) in gebucht]
assert gefunden == [True, True, False], (
    'Für gebucht = {Sitzplatz(1, "F", 7), Sitzplatz(1, "F", 8)} ergibt "in gebucht" für '
    f'(1, "F", 7), (1, "F", 8) und (2, "F", 7) {gefunden}, erwartet war [True, True, False].'
)

# Doppelte Plätze kommen in einer Menge nur einmal vor
buchungen = [Sitzplatz(1, "F", 7), Sitzplatz(1, "F", 8), Sitzplatz(1, "F", 7), Sitzplatz(2, "F", 7)]
anzahl = len(set(buchungen))
assert anzahl == 3, f"set() aus vier Buchungen mit einem doppelten Platz hat {anzahl} Elemente, erwartet waren 3."

# Sitzplätze funktionieren als Dictionary-Schlüssel
preise = {Sitzplatz(1, "A", 1): 15, Sitzplatz(1, "A", 2): 15, Sitzplatz(1, "F", 7): 9}
preis = preise.get(Sitzplatz(1, "F", 7))
assert preis == 9, f'preise.get(Sitzplatz(1, "F", 7)) ergibt {preis!r}, erwartet war 9.'

# Verschiedene Plätze verteilen sich auf viele Hashwerte (sonst werden große Mengen langsam)
saal = [Sitzplatz(1, reihe, nummer) for reihe in "ABCDEFGHIJ" for nummer in range(1, 21)]
verschiedene = len({hash(platz) for platz in saal})
assert verschiedene > 100, (
    f"Die 200 Plätze eines Saals haben nur {verschiedene} verschiedene Hashwerte; erwartet waren deutlich mehr als 100.\n"
    "Tipp: Ein fester Hashwert wie return 0 ist zwar erlaubt, macht Mengen aber so langsam wie eine Liste. "
    "Nehmen Sie alle Attribute in den Hash auf."
)

# Die Ausgabe des Programms stimmt
assert AUSGABE == "True\nFalse", f"Erwartete Ausgabe:\nTrue\nFalse\nIhr Programm:\n{AUSGABE}"
