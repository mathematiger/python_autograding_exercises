# Automatisch erzeugt aus lehrkraft/muster/4_026_vm_platzierung.py - nicht von Hand ändern.
# vorlage-hash: f6c1fcc9103593d9
# text-hash: 34c25a4232ee4780
# thema: algorithmen
# inhalt: Rucksackproblem mit Tabelle

BEISPIEL = [("web", 4, 40), ("db", 6, 70), ("mail", 3, 25), ("build", 5, 50)]


def bewerte(vms, ram, namen):
    """Prüft eine Auswahl; gibt (Gesamtnutzen, Fehlerbeschreibung oder "") zurück."""
    if not isinstance(namen, list):
        return None, f"auswahl soll eine Liste zurückgeben, nicht {type(namen).__name__}."
    reihenfolge = [vm[0] for vm in vms]
    for name in namen:
        if name not in reihenfolge:
            return None, f"{name!r} ist keine der VMs."
    if len(set(namen)) != len(namen):
        return None, "Eine VM kommt mehrmals vor; jede VM gibt es nur einmal."
    if namen != [name for name in reihenfolge if name in namen]:
        return None, "Die Namen stehen nicht in der Reihenfolge von vms."
    belegt = sum(vm[1] for vm in vms if vm[0] in namen)
    if belegt > ram:
        return None, f"Die Auswahl braucht {belegt} GB, frei sind nur {ram} GB."
    return sum(vm[2] for vm in vms if vm[0] in namen), ""


# Vergleichslösung: anders gerechnet, über ein Dictionary belegter RAM → bester Nutzen
def bester_von_hand(vms, ram):
    """Merkt sich zu jeder erreichbaren RAM-Belegung den besten Nutzen."""
    beste = {0: 0}
    for _, bedarf, nutzen in vms:
        neu = dict(beste)
        for belegt, wert in beste.items():
            if belegt + bedarf <= ram and neu.get(belegt + bedarf, -1) < wert + nutzen:
                neu[belegt + bedarf] = wert + nutzen
        beste = neu
    return max(beste.values())


def pruefe_auswahl(vms, ram):
    """Prüft auswahl(vms, ram) gegen die Vergleichslösung; gibt eine Fehlermeldung oder "" zurück."""
    namen = auswahl(list(vms), ram)
    nutzen, fehler = bewerte(vms, ram, namen)
    if fehler:
        return f"auswahl({vms}, {ram}) ergibt {namen!r}. {fehler}"
    erwartet = bester_von_hand(vms, ram)
    if nutzen != erwartet:
        return f"auswahl({vms}, {ram}) ergibt {namen!r} mit Nutzen {nutzen}, möglich wären {erwartet}."
    return ""


# bester_nutzen aus dem Beispiel
ergebnis = bester_nutzen(BEISPIEL, 11)
assert ergebnis == 120, (
    f"bester_nutzen({BEISPIEL}, 11) ergibt {ergebnis!r}, erwartet war 120 (db und build).\n"
    "Tipp: Probieren Sie bei jeder VM beide Möglichkeiten, nehmen und nicht nehmen, und nehmen Sie das Bessere; "
    "gierig nach Nutzen pro GB zu wählen reicht nicht."
)

# auswahl aus dem Beispiel
ergebnis = auswahl(BEISPIEL, 11)
assert ergebnis == ["db", "build"], f"auswahl({BEISPIEL}, 11) ergibt {ergebnis!r}, erwartet war ['db', 'build']."

# Keine VM passt
ergebnis = (bester_nutzen(BEISPIEL, 2), auswahl(BEISPIEL, 2))
assert ergebnis == (0, []), f"Bei 2 GB frei ergeben bester_nutzen und auswahl {ergebnis!r}, erwartet war (0, [])."

# Keine VMs und kein freier RAM
ergebnis = (bester_nutzen([], 50), auswahl([], 50), bester_nutzen(BEISPIEL, 0), auswahl(BEISPIEL, 0))
assert ergebnis == (0, [], 0, []), (
    f"bester_nutzen([], 50), auswahl([], 50), bester_nutzen(…, 0) und auswahl(…, 0) ergeben {ergebnis!r}, "
    "erwartet war (0, [], 0, [])."
)

# Eine VM, die genau den freien RAM braucht, passt
vms = [("gross", 10, 99), ("klein", 3, 20)]
ergebnis = (bester_nutzen(vms, 10), auswahl(vms, 10))
assert ergebnis == (99, ["gross"]), (
    f"bester_nutzen({vms}, 10) und auswahl({vms}, 10) ergeben {ergebnis!r}, erwartet war (99, ['gross']).\n"
    "Tipp: Eine VM passt, wenn ihr RAM höchstens so groß ist wie der freie, also auch bei Gleichheit."
)

# Alle VMs passen zusammen
vms = [("a", 1, 5), ("b", 2, 7), ("c", 3, 1)]
ergebnis = (bester_nutzen(vms, 6), auswahl(vms, 6))
assert ergebnis == (13, ["a", "b", "c"]), f"Bei 6 GB frei ergeben beide Funktionen für {vms} {ergebnis!r}, erwartet war (13, ['a', 'b', 'c'])."

# Zwei kleine schlagen eine große
vms = [("gross", 6, 60), ("x", 3, 35), ("y", 3, 35)]
fehler = pruefe_auswahl(vms, 6)
ergebnis = bester_nutzen(vms, 6)
assert ergebnis == 70 and not fehler, (
    f"bester_nutzen({vms}, 6) ergibt {ergebnis!r}, erwartet war 70. {fehler}"
)

# Die Liste vms bleibt unverändert, und ein zweiter Aufruf rechnet mit den neuen VMs
vms = [("a", 5, 10), ("b", 5, 20)]
erster = bester_nutzen(vms, 5)
zweiter = bester_nutzen([("c", 5, 30)], 5)
assert (erster, zweiter, vms) == (20, 30, [("a", 5, 10), ("b", 5, 20)]), (
    f"bester_nutzen([('a', 5, 10), ('b', 5, 20)], 5) und danach bester_nutzen([('c', 5, 30)], 5) ergeben "
    f"{erster!r} und {zweiter!r}, erwartet war 20 und 30; vms danach: {vms!r}.\n"
    "Tipp: Legen Sie die gecachte Funktion innerhalb von bester_nutzen an, dann bekommt jeder Aufruf "
    "einen eigenen Cache."
)

# lru_cache wird benutzt
assert verwendet("lru_cache"), "Dekorieren Sie in bester_nutzen eine innere Funktion mit @lru_cache(maxsize=None)."


def fehlerfall_vergleich(anzahl, zufall, groesste_vm):
    """Prüft anzahl zufällige Fälle gegen die Vergleichslösung; gibt die erste Fehlermeldung oder "" zurück."""
    for _ in range(anzahl):
        vms = []
        for nummer in range(zufall.randint(0, 9)):
            vms.append((f"vm{nummer}", zufall.randint(1, groesste_vm), zufall.randint(0, 100)))
        ram = zufall.randint(0, 30)
        ergebnis = bester_nutzen(list(vms), ram)
        erwartet = bester_von_hand(vms, ram)
        if ergebnis != erwartet:
            return f"bester_nutzen({vms}, {ram}) ergibt {ergebnis!r}, erwartet war {erwartet}."
        fehler = pruefe_auswahl(vms, ram)
        if fehler:
            return fehler
    return ""


# 300 zufällige kleine Fälle
zufall = Zufall(4026)
fehler = fehlerfall_vergleich(300, zufall, 12)
assert not fehler, fehler

# Laufzeit: bester_nutzen mit 17 kleinen VMs, die alle zusammen passen (131 072 Teilmengen)
vms = [(f"vm{nummer}", nummer % 4 + 1, 10 + nummer) for nummer in range(17)]
ergebnis, schritte = zaehle_schritte(bester_nutzen, vms, 60)
assert ergebnis == bester_von_hand(vms, 60) and schritte < 50000, (
    f"bester_nutzen mit 17 VMs und 60 GB braucht {schritte} Schritte (Ergebnis {ergebnis!r}); erwartet war "
    "O(n · ram), hier also weit unter 50 000.\n"
    "Tipp: Ohne Cache wird jedes Paar (index, frei) immer wieder neu berechnet; dekorieren Sie die innere "
    "Funktion mit @lru_cache(maxsize=None) und geben Sie ihr nur die zwei Zahlen als Argumente."
)

# Laufzeit: auswahl mit denselben 17 VMs
ergebnis, schritte = zaehle_schritte(auswahl, vms, 60)
fehler = pruefe_auswahl(vms, 60)
assert not fehler and schritte < 50000, (
    f"auswahl mit 17 VMs und 60 GB braucht {schritte} Schritte; erwartet war O(n · ram), hier also weit unter "
    f"50 000. {fehler}"
)

# Obere Grenze: 100 VMs, 1000 GB frei
zufall = Zufall(40260)
vms = [(f"vm{nummer:03d}", zufall.randint(1, 120), zufall.randint(0, 10**6)) for nummer in range(100)]
ergebnis = bester_nutzen(vms, 1000)
erwartet = bester_von_hand(vms, 1000)
assert ergebnis == erwartet, f"bester_nutzen mit 100 VMs und 1000 GB ergibt {ergebnis!r}, erwartet war {erwartet}."

# Obere Grenze: auswahl mit 100 VMs und 1000 GB
fehler = pruefe_auswahl(vms, 1000)
assert not fehler, f"Mit 100 VMs und 1000 GB: {fehler[:300]}"

# Obere Grenze der VM-Größe: 1000 GB
vms = [("riesig", 1000, 10**6), ("rest", 1, 10**6 - 1)]
ergebnis = (bester_nutzen(vms, 1000), auswahl(vms, 1000))
assert ergebnis == (10**6, ["riesig"]), f"Für {vms} mit 1000 GB ergeben beide Funktionen {ergebnis!r}, erwartet war (1000000, ['riesig'])."

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "120\n['db', 'build']\n0"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
