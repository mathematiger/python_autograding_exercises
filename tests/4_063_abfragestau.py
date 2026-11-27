# Automatisch erzeugt aus lehrkraft/muster/4_063_abfragestau.py - nicht von Hand ändern.
# vorlage-hash: f49bc84a23b90bab
# text-hash: f4f0b0785557775d
# thema: algorithmen
# inhalt: Monotoner Stack

BEISPIEL = [3, 5, 4, 4, 8, 2, 6]


def ergebnis_von(wartend):
    """Ruft bis_mehr mit einer Kopie auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return bis_mehr(list(wartend))
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def langsam(wartend):
    """Vergleichslösung: sucht von jeder Minute aus nach rechts (O(n²), nur für kleine Listen)."""
    abstaende = []
    for stelle, wert in enumerate(wartend):
        abstand = 0
        for spaeter in range(stelle + 1, len(wartend)):
            if wartend[spaeter] > wert:
                abstand = spaeter - stelle
                break
        abstaende.append(abstand)
    return abstaende


def erster_abstand(wartend, stelle):
    """Vergleichslösung für eine einzelne Minute: sucht nach rechts die erste höhere."""
    for spaeter in range(stelle + 1, len(wartend)):
        if wartend[spaeter] > wartend[stelle]:
            return spaeter - stelle
    return 0


def pruefe(wartend, hinweis=""):
    """Vergleicht bis_mehr mit der Vergleichslösung; liefert (stimmt, Meldung mit der ersten Abweichung)."""
    ergebnis = ergebnis_von(wartend)
    erwartet = langsam(wartend)
    text = f"bis_mehr({wartend})\nergibt   {ergebnis!r}\nerwartet {erwartet}"
    if isinstance(ergebnis, list) and len(ergebnis) == len(erwartet):
        for stelle, (ihr, soll) in enumerate(zip(ergebnis, erwartet)):
            if ihr != soll:
                text += f"\nErste Abweichung bei Minute {stelle} (Wert {wartend[stelle]}): {ihr!r} statt {soll}."
                break
    return ergebnis == erwartet, text + hinweis


def lesezugriffe(wartend):
    """Ruft bis_mehr mit einer Zaehlliste auf; liefert die Zahl der Lesezugriffe oder den Fehler als Text."""
    liste = Zaehlliste(wartend)
    try:
        bis_mehr(liste)
    except Exception as fehler:
        return f"(Abbruch: {type(fehler).__name__}: {fehler})"
    return liste.lesezugriffe


# Im Beispiel kommt eine gleich lange Liste heraus
ergebnis = ergebnis_von(BEISPIEL)
assert isinstance(ergebnis, list) and len(ergebnis) == 7, (
    f"bis_mehr({BEISPIEL}) ergibt {ergebnis!r}, erwartet war eine Liste mit 7 Abständen."
)

# Das Beispiel
stimmt, text = pruefe(BEISPIEL, "\nTipp: Gleich viele Wartende zählen nicht als mehr, darum < und nicht <=.")
assert stimmt, text

# Ein anderes Protokoll (nicht fest hinschreiben!)
stimmt, text = pruefe([1, 2, 3, 0, 10])
assert stimmt, text

# Ohne höhere Minute steht 0
stimmt, text = pruefe([9, 7, 7, 1], "\nTipp: Minuten, die am Ende noch auf dem Stapel liegen, behalten 0.")
assert stimmt, text

# Gleich hohe Minuten warten auf eine echt höhere
stimmt, text = pruefe([4, 4, 4, 5])
assert stimmt, text

# Die Liste wartend bleibt unverändert
wartend = list(BEISPIEL)
try:
    bis_mehr(wartend)
except Exception:
    pass
assert wartend == BEISPIEL, f"Nach bis_mehr(wartend) ist wartend {wartend}, erwartet war die unveränderte Liste {BEISPIEL}."

# Randfall: leeres Protokoll
stimmt, text = pruefe([])
assert stimmt, text

# Randfall: eine einzige Minute
stimmt, text = pruefe([0])
assert stimmt, text

# Randfall: lauter Nullen
stimmt, text = pruefe([0, 0, 0])
assert stimmt, text

# Randfall: obere Grenze der Werte
stimmt, text = pruefe([999999, 1000000, 0, 1000000])
assert stimmt, text

# Viele zufällige Protokolle
zufall = Zufall(4063)
for _ in range(500):
    wartend = [zufall.randint(0, 6) for _ in range(zufall.randint(0, 12))]
    stimmt, text = pruefe(wartend)
    assert stimmt, text

# Obere Grenze: 100 000 Minuten mit Werten bis 1 000 000
wartend = [zufall.randint(0, 1000000) for _ in range(100000)]
ergebnis = ergebnis_von(wartend)
assert isinstance(ergebnis, list) and len(ergebnis) == 100000, f"Bei 100 000 Minuten ergibt bis_mehr {str(ergebnis)[:200]}."

# Obere Grenze: die Abstände stimmen an Stichproben
fehler = [stelle for stelle in range(0, 100000, 997) if ergebnis[stelle] != erster_abstand(wartend, stelle)] if isinstance(ergebnis, list) and len(ergebnis) == 100000 else ["(Liste fehlt)"]
assert fehler == [], f"Bei 100 000 Minuten stimmt der Abstand an den Stellen {fehler[:5]} nicht."

# Laufzeit: ein lange abnehmendes Protokoll in O(n)
abnehmend = list(range(2000, 0, -1)) + [5000]
zugriffe = lesezugriffe(abnehmend)
assert isinstance(zugriffe, int) and zugriffe <= 10 * len(abnehmend), (
    f"Für ein abnehmendes Protokoll mit {len(abnehmend)} Minuten liest Ihre Lösung {zugriffe}-mal aus wartend,\n"
    f"erlaubt sind 10 · {len(abnehmend)} = {10 * len(abnehmend)} (O(n)).\n"
    "Tipp: Suchen Sie nicht von jeder Minute aus nach rechts, sondern legen Sie die offenen Minuten auf einen Stapel."
)

# Laufzeit: viermal so viele Minuten, etwa viermal so viele Zugriffe
klein = lesezugriffe([zufall.randint(0, 50) for _ in range(5000)])
gross = lesezugriffe([zufall.randint(0, 50) for _ in range(20000)])
assert isinstance(klein, int) and isinstance(gross, int) and gross <= 6 * klein, (
    f"Für 5000 Minuten liest Ihre Lösung {klein}-mal, für 20 000 Minuten {gross}-mal aus wartend.\n"
    "Bei O(n) wären es etwa viermal so viele, bei O(n²) sechzehnmal so viele."
)
