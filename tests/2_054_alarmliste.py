# Automatisch erzeugt aus lehrkraft/muster/2_054_alarmliste.py - nicht von Hand ändern.
# vorlage-hash: 7023920970f31ec3
# text-hash: 2bea19851f82a6ad
# thema: algorithmen
# inhalt: Element entfernen von Hand

BEISPIEL = ["web01", "db01", "web01", "mail01", "web01"]


def wert_von(funktion, alarme, server):
    """Ruft die Funktion mit einer Kopie der Liste auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(list(alarme), server)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_ohne_ersten(alarme, server):
    """Vergleichslösung: sucht die Stelle mit index und setzt die Liste aus zwei Stücken zusammen."""
    if server not in alarme:
        return list(alarme)
    stelle = alarme.index(server)
    return alarme[:stelle] + alarme[stelle + 1 :]


def vergleich_ohne_alle(alarme, server):
    """Vergleichslösung mit einer Comprehension."""
    return [alarm for alarm in alarme if alarm != server]


def pruefe(funktion, vergleich, alarme, server, hinweis=""):
    """Vergleicht die Funktion mit der Vergleichslösung und liefert (stimmt, Meldung)."""
    ergebnis = wert_von(funktion, alarme, server)
    erwartet = vergleich(alarme, server)
    text = f"{funktion.__name__}({alarme}, {server!r}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    return ergebnis == erwartet, text + hinweis


def erste_abweichung(ergebnis, erwartet):
    """Gibt die erste Stelle zurück, an der sich die beiden Listen unterscheiden, als Text mit beiden Werten."""
    if not isinstance(ergebnis, list):
        return "0 (keine Liste)"
    for stelle in range(min(len(ergebnis), len(erwartet))):
        if ergebnis[stelle] != erwartet[stelle]:
            return f"{stelle}: {ergebnis[stelle]!r} statt {erwartet[stelle]!r}"
    return f"{min(len(ergebnis), len(erwartet))} (eine Liste ist dort zu Ende)"


# ohne_ersten im Beispiel: es kommt eine Liste mit einem Eintrag weniger heraus
ergebnis = wert_von(ohne_ersten, BEISPIEL, "web01")
assert isinstance(ergebnis, list) and len(ergebnis) == 4, (
    f"ohne_ersten({BEISPIEL}, 'web01') ergibt {ergebnis!r}, erwartet war eine Liste mit 4 Einträgen.\n"
    "Tipp: Legen Sie eine neue leere Liste an, hängen Sie mit append an, was bleibt, und geben Sie sie mit return zurück."
)

# ohne_ersten im Beispiel: genau der älteste Alarm von web01 fällt weg
stimmt, text = pruefe(
    ohne_ersten, vergleich_ohne_ersten, BEISPIEL, "web01",
    "\nTipp: Merken Sie sich in einer Variablen mit True/False, ob Sie schon einen Alarm übersprungen haben.",
)
assert stimmt, text

# ohne_ersten mit einem anderen Server (nicht fest hinschreiben!)
stimmt, text = pruefe(ohne_ersten, vergleich_ohne_ersten, ["db01", "fs02", "db01", "fs02"], "fs02")
assert stimmt, text

# ohne_ersten lässt die übergebene Liste unverändert
alarme = list(BEISPIEL)
try:
    ohne_ersten(alarme, "db01")
except Exception:
    pass
assert alarme == BEISPIEL, (
    f"Nach ohne_ersten(alarme, 'db01') ist alarme {alarme}, erwartet war die unveränderte Liste {BEISPIEL}.\n"
    "Tipp: Bauen Sie eine neue Liste auf, statt aus alarme zu entfernen."
)

# ohne_ersten: der gesuchte Alarm steht ganz vorn
stimmt, text = pruefe(ohne_ersten, vergleich_ohne_ersten, ["mail01", "db01", "web01"], "mail01")
assert stimmt, text

# ohne_ersten: der gesuchte Alarm steht ganz hinten
stimmt, text = pruefe(ohne_ersten, vergleich_ohne_ersten, ["mail01", "db01", "web01"], "web01")
assert stimmt, text

# ohne_ersten: Server ohne Alarm, dann eine Kopie
stimmt, text = pruefe(ohne_ersten, vergleich_ohne_ersten, BEISPIEL, "fs01", "\nTipp: Fehlt der Server, bleibt alles drin.")
assert stimmt, text

# ohne_ersten: auch ohne Alarm des Servers eine neue Liste, nicht dieselbe
alarme = list(BEISPIEL)
try:
    ergebnis = ohne_ersten(alarme, "fs01")
except Exception as fehler:
    ergebnis = f"{type(fehler).__name__}: {fehler}"
assert ergebnis is not alarme, (
    f"ohne_ersten(alarme, 'fs01') gibt die übergebene Liste selbst zurück, erwartet war eine neue Liste (eine Kopie).\n"
    "Tipp: Wer später die neue Liste ändert, würde sonst auch die Anzeige der Kollegen ändern."
)

# ohne_ersten: leere Liste
stimmt, text = pruefe(ohne_ersten, vergleich_ohne_ersten, [], "web01")
assert stimmt, text

# ohne_ersten: ein einziger Alarm
stimmt, text = pruefe(ohne_ersten, vergleich_ohne_ersten, ["web01"], "web01")
assert stimmt, text

# ohne_ersten: lauter Alarme desselben Servers, nur einer fällt weg
stimmt, text = pruefe(ohne_ersten, vergleich_ohne_ersten, ["web01", "web01", "web01"], "web01")
assert stimmt, text

# ohne_alle im Beispiel
stimmt, text = pruefe(
    ohne_alle, vergleich_ohne_alle, BEISPIEL, "web01",
    "\nTipp: Hängen Sie jeden Alarm an die neue Liste an, der nicht von server stammt.",
)
assert stimmt, text

# ohne_alle mit einem anderen Server (nicht fest hinschreiben!)
stimmt, text = pruefe(ohne_alle, vergleich_ohne_alle, ["db01", "fs02", "db01", "fs02", "web03"], "db01")
assert stimmt, text

# ohne_alle: zwei gleiche Alarme direkt nacheinander
stimmt, text = pruefe(
    ohne_alle, vergleich_ohne_alle, ["web01", "web01", "db01", "web01", "web01"], "web01",
    "\nTipp: Wer beim Durchlaufen aus derselben Liste entfernt, überspringt den Eintrag dahinter.",
)
assert stimmt, text

# ohne_alle lässt die übergebene Liste unverändert
alarme = list(BEISPIEL)
try:
    ohne_alle(alarme, "web01")
except Exception:
    pass
assert alarme == BEISPIEL, (
    f"Nach ohne_alle(alarme, 'web01') ist alarme {alarme}, erwartet war die unveränderte Liste {BEISPIEL}."
)

# ohne_alle: Server ohne Alarm, dann eine Kopie
stimmt, text = pruefe(ohne_alle, vergleich_ohne_alle, BEISPIEL, "fs01")
assert stimmt, text

# ohne_alle: auch ohne Alarm des Servers eine neue Liste, nicht dieselbe
alarme = list(BEISPIEL)
try:
    ergebnis = ohne_alle(alarme, "fs01")
except Exception as fehler:
    ergebnis = f"{type(fehler).__name__}: {fehler}"
assert ergebnis is not alarme, (
    f"ohne_alle(alarme, 'fs01') gibt die übergebene Liste selbst zurück, erwartet war eine neue Liste (eine Kopie).\n"
    "Tipp: Wer später die neue Liste ändert, würde sonst auch die Anzeige der Kollegen ändern."
)

# ohne_alle: leere Liste
stimmt, text = pruefe(ohne_alle, vergleich_ohne_alle, [], "fs01")
assert stimmt, text

# ohne_alle: nur Alarme dieses Servers
stimmt, text = pruefe(ohne_alle, vergleich_ohne_alle, ["web01", "web01", "web01"], "web01")
assert stimmt, text

# ohne_alle: ähnliche Namen bleiben stehen
stimmt, text = pruefe(ohne_alle, vergleich_ohne_alle, ["web01", "web010", "web0", "Web01"], "web01")
assert stimmt, text

# Ohne remove(), pop() und index()
verboten = [name for name in ["remove", "pop", "index"] if verwendet(name)]
assert verboten == [], f"Ihr Code verwendet {verboten}. Bauen Sie stattdessen eine neue Liste mit append auf."

# Die Ausgabe des Programms
erwartet = "['db01', 'web01', 'mail01', 'web01']\n['db01', 'mail01']\n['web01', 'db01', 'web01', 'mail01', 'web01']"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# ohne_ersten: viele zufällige Alarmlisten
zufall = Zufall(2054)
namen = ["web01", "db01", "mail01", "fs01", "vpn01"]
faelle = []
for _ in range(300):
    alarme = [zufall.choice(namen) for _ in range(zufall.randint(0, 12))]
    faelle.append((alarme, zufall.choice(namen)))
for alarme, server in faelle:
    stimmt, text = pruefe(ohne_ersten, vergleich_ohne_ersten, alarme, server)
    assert stimmt, text

# ohne_alle: dieselben zufälligen Alarmlisten
for alarme, server in faelle:
    stimmt, text = pruefe(ohne_alle, vergleich_ohne_alle, alarme, server)
    assert stimmt, text

# Obere Grenze: 100 000 Alarme, der gesuchte Server steht oft darin
alarme = [zufall.choice(namen) for _ in range(100000)]
ergebnis = wert_von(ohne_ersten, alarme, "db01")
erwartet = vergleich_ohne_ersten(alarme, "db01")
assert ergebnis == erwartet, (
    f"Bei 100 000 Alarmen ergibt ohne_ersten(alarme, 'db01') eine Liste mit {len(ergebnis) if isinstance(ergebnis, list) else ergebnis!r} "
    f"Einträgen, erwartet waren {len(erwartet)}; erste Abweichung an Stelle {erste_abweichung(ergebnis, erwartet)}."
)
# Obere Grenze: ohne_alle bei 100 000 Alarmen
ergebnis = wert_von(ohne_alle, alarme, "db01")
erwartet = vergleich_ohne_alle(alarme, "db01")
assert ergebnis == erwartet, (
    f"Bei 100 000 Alarmen ergibt ohne_alle(alarme, 'db01') eine Liste mit {len(ergebnis) if isinstance(ergebnis, list) else ergebnis!r} "
    f"Einträgen, erwartet waren {len(erwartet)}; erste Abweichung an Stelle {erste_abweichung(ergebnis, erwartet)}."
)
