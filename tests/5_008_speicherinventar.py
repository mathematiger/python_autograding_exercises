# Automatisch erzeugt aus lehrkraft/muster/5_008_speicherinventar.py - nicht von Hand ändern.
# vorlage-hash: 5916c6f62624b828
# text-hash: 437e3900a2f03f77
# thema: klassen
# inhalt: `__new__`, Singleton, Unterklasse von int

def ausnahme_bei(aktion):
    """Führt aktion() aus und gibt den Namen der ausgelösten Ausnahme zurück, sonst None."""
    try:
        aktion()
    except Exception as fehler:
        return type(fehler).__name__
    return None


# Speicher ist eine Unterklasse von int und rechnet Texte um
s = Speicher("16G")
assert issubclass(Speicher, int) and type(s) is Speicher and s == 16384 and int(s) == 16384, (
    f"Speicher('16G') ergibt {int(s) if isinstance(s, int) else s!r} vom Typ {type(s).__name__}; erwartet war ein "
    "Speicher mit dem Wert 16384.\nTipp: Rechnen Sie in __new__ um und geben Sie super().__new__(cls, wert) zurück."
)

# Einheiten, Groß- und Kleinschreibung, Leerzeichen
for text, erwartet in [
    ("512M", 512), ("512 m", 512), ("  2g ", 2048), ("1T", 1024**2), (" 3 t", 3 * 1024**2),
    ("0G", 0), ("007M", 7), ("999999999T", 999999999 * 1024**2), ("1\tG", 1024),
]:
    try:
        ergebnis = int(Speicher(text))
    except ValueError as fehler:
        ergebnis = fehler
    assert ergebnis == erwartet, f"Speicher({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Ganze Zahlen ab 0 und andere Speicher werden übernommen
for wert, erwartet in [(0, 0), (8192, 8192), (10**12, 10**12), (Speicher("1G"), 1024)]:
    ergebnis = Speicher(wert)
    assert type(ergebnis) is Speicher and ergebnis == erwartet, (
        f"Speicher({wert!r}) ergibt {ergebnis!r} vom Typ {type(ergebnis).__name__}, erwartet war ein Speicher mit {erwartet}."
    )

# Ungültige Werte lösen ValueError aus
for wert in ["1.5G", "16", "G", "", "  ", "-1G", "16 GB", "16K", "1 6G", "+5M", -1, -10**12, 1.0, True, False, None, [16]]:
    art = ausnahme_bei(lambda: Speicher(wert))
    assert art == "ValueError", (
        f"Speicher({wert!r}) soll einen ValueError auslösen; ausgelöst wurde {art}.\n"
        "Tipp: Erlaubt sind nur ganze Zahlen ab 0 (ohne True/False) und Texte aus Ziffern und einer Einheit M, G oder T."
    )

# Die Ausgabe mit str in der größten passenden Einheit
for wert, erwartet in [
    (0, "0 MiB"), (1, "1 MiB"), (1023, "1023 MiB"), (1024, "1 GiB"), (1536, "1536 MiB"),
    (16384, "16 GiB"), (1024**2, "1 TiB"), (1024**2 + 1024, "1025 GiB"), (5 * 1024**2, "5 TiB"),
]:
    ergebnis = str(Speicher(wert))
    assert ergebnis == erwartet, (
        f"str(Speicher({wert})) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
        "Tipp: Versuchen Sie zuerst TiB, dann GiB; in __str__ rechnen Sie mit int(self)."
    )

# Rechnungen ergeben gewöhnliche Zahlen, Vergleiche funktionieren
a = Speicher("1G")
b = Speicher(512)
assert a + b == 1536 and a > b and sorted([a, b, 700]) == [512, 700, 1024] and f"{a}" == "1 GiB", (
    "Speicher('1G') + Speicher(512) soll 1536 ergeben, Speicher('1G') > Speicher(512) sein, sich mit gewöhnlichen "
    "Zahlen sortieren lassen, und f'{Speicher(\"1G\")}' soll '1 GiB' ergeben."
)

# Inventar() liefert immer dasselbe Objekt
Inventar().leeren()
erstes = Inventar()
zweites = Inventar()
assert erstes is zweites and type(erstes) is Inventar, (
    "Inventar() is Inventar() soll True sein.\n"
    "Tipp: Merken Sie sich das erste Objekt in __new__ in einem Klassenattribut und geben Sie es danach immer zurück."
)

# Ein weiterer Aufruf von Inventar() löscht nichts
Inventar().leeren()
Inventar().hinzufuegen("db01", "64G")
Inventar().hinzufuegen("web01", 8192)
ergebnis = Inventar().gesamt()
assert type(ergebnis) is Speicher and ergebnis == 73728 and str(ergebnis) == "72 GiB", (
    f"Nach Inventar().hinzufuegen('db01', '64G') und Inventar().hinzufuegen('web01', 8192) ergibt "
    f"Inventar().gesamt() {ergebnis!r} vom Typ {type(ergebnis).__name__}; erwartet war Speicher 73728 (72 GiB).\n"
    "Tipp: Python ruft __init__ bei jedem Inventar() erneut auf; legen Sie die Daten nur beim ersten Mal in __new__ an. "
    "sum(...) ergibt ein int, das Sie noch in einen Speicher umwandeln."
)

# ram liefert den Speicher eines Servers, unbekannte Server ergeben KeyError
Inventar().leeren()
Inventar().hinzufuegen("db01", " 64 g ")
ergebnis = Inventar().ram("db01")
art = ausnahme_bei(lambda: Inventar().ram("db02"))
assert (type(ergebnis), int(ergebnis), str(ergebnis), art) == (Speicher, 65536, "64 GiB", "KeyError"), (
    f"Inventar().ram('db01') ergibt {ergebnis!r} vom Typ {type(ergebnis).__name__}, ram('db02') löst {art} aus; "
    "erwartet waren Speicher 65536 und KeyError."
)

# Doppelte Namen und ungültiger RAM lösen ValueError aus, ohne etwas zu ändern
Inventar().leeren()
Inventar().hinzufuegen("db01", "64G")
arten = [ausnahme_bei(lambda: Inventar().hinzufuegen("db01", "8G")), ausnahme_bei(lambda: Inventar().hinzufuegen("db02", "viel"))]
assert arten == ["ValueError", "ValueError"] and Inventar().gesamt() == 65536 and ausnahme_bei(lambda: Inventar().ram("db02")) == "KeyError", (
    f"hinzufuegen('db01', '8G') bei vorhandenem db01 und hinzufuegen('db02', 'viel') lösen {arten} aus, erwartet war "
    f"zweimal ValueError; danach soll gesamt() 65536 sein und db02 fehlen, gesamt() ist {Inventar().gesamt()!r}."
)

# Leeres Inventar
Inventar().leeren()
ergebnis = Inventar().gesamt()
assert type(ergebnis) is Speicher and ergebnis == 0 and str(ergebnis) == "0 MiB", (
    f"Ein leeres Inventar hat gesamt() {ergebnis!r} vom Typ {type(ergebnis).__name__}, erwartet war Speicher 0 (0 MiB)."
)

# 300 zufällige Angaben, nachgerechnet
zufall = Zufall(5008)
FAKTOR = {"M": 1, "G": 1024, "T": 1024**2}
for _ in range(300):
    zahl = zufall.choice([0, 1, zufall.randint(0, 2048), zufall.randint(0, 10**9 - 1)])
    einheit = zufall.choice("MGT")
    text = " " * zufall.randint(0, 2) + str(zahl) + " " * zufall.randint(0, 2) + zufall.choice([einheit, einheit.lower()]) + " " * zufall.randint(0, 2)
    erwartet = zahl * FAKTOR[einheit]
    ergebnis = Speicher(text)
    assert type(ergebnis) is Speicher and ergebnis == erwartet, f"Speicher({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    if erwartet != 0 and erwartet % 1024**2 == 0:
        anzeige = f"{erwartet // 1024**2} TiB"
    elif erwartet != 0 and erwartet % 1024 == 0:
        anzeige = f"{erwartet // 1024} GiB"
    else:
        anzeige = f"{erwartet} MiB"
    assert str(ergebnis) == anzeige, f"str(Speicher({text!r})) ergibt {str(ergebnis)!r}, erwartet war {anzeige!r}."

# An der oberen Grenze: 100 000 Server
Inventar().leeren()
for nummer in range(100000):
    Inventar().hinzufuegen(f"srv{nummer:06d}", ["8G", "512M", 1024, " 1 t"][nummer % 4])
ergebnis = Inventar().gesamt()
erwartet = 25000 * (8192 + 512 + 1024 + 1024**2)
assert ergebnis == erwartet and str(ergebnis) == "25837500 GiB" and Inventar().ram("srv099999") == 1024**2, (
    f"Bei 100 000 Servern ergibt gesamt() {ergebnis!r}, erwartet war {erwartet}."
)
Inventar().leeren()

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "16 GiB 16384 1536 MiB\nTrue 72 GiB"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
