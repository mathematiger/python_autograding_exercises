# Automatisch erzeugt aus lehrkraft/muster/3_069_angriffsbericht.py - nicht von Hand ändern.
# vorlage-hash: f9c92f9ff81d4a23
# text-hash: 27655882eb65ddb9
# thema: algorithmen
# inhalt: Übung Algorithmen-Muster

ANGREIFER = ["203.0.113.7", "198.51.100.23", "203.0.113.7", "192.0.2.44", "198.51.100.23", "203.0.113.90"]
SPERRLISTE = ["192.0.2.44", "203.0.113.90", "198.51.100.1"]
GEBLOCKT = [4, 0, 12, 30, 7, 0, 0, 25]
ZEITPUNKTE = [500, 130, 910, 140, 125, 600, 610, 620]


def wert_von(funktion, *argumente):
    """Ruft funktion mit Kopien der Listen auf; ein Fehler wird als Text zurückgegeben."""
    kopien = [list(wert) if isinstance(wert, list) else wert for wert in argumente]
    try:
        return funktion(*kopien)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def gezeigt(werte):
    """Zeigt kurze Listen ganz, lange nur mit ihrer Länge."""
    return werte if len(werte) <= 10 else f"<{len(werte)} Einträge>"


def vergleich_angreifer(angreifer, sperrliste):
    """Vergleichslösung: prüft jede Adresse einzeln gegen die Liste (langsam, aber offensichtlich richtig)."""
    neu = []
    for adresse in angreifer:
        if adresse not in sperrliste and adresse not in neu:
            neu.append(adresse)
    return sorted(neu)


def vergleich_zeitraum(geblockt, anfragen):
    """Vergleichslösung: addiert jeden Zeitraum neu."""
    return [sum(geblockt[von : bis + 1]) for von, bis in anfragen]


def vergleich_fenster(zeitpunkte, k):
    """Vergleichslösung: für jeden Alarm als ersten die k nächsten späteren (langsam)."""
    if len(zeitpunkte) < k:
        return None
    kuerzeste = None
    for i in range(len(zeitpunkte)):
        spaeter = sorted(t for j, t in enumerate(zeitpunkte) if j != i and t >= zeitpunkte[i])
        if len(spaeter) >= k - 1:
            spanne = (spaeter[k - 2] if k > 1 else zeitpunkte[i]) - zeitpunkte[i]
            if kuerzeste is None or spanne < kuerzeste:
                kuerzeste = spanne
    return kuerzeste


def pruefe_angreifer(angreifer, sperrliste, hinweis=""):
    """Prüft neue_angreifer gegen die Vergleichslösung; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(neue_angreifer, angreifer, sperrliste)
    erwartet = vergleich_angreifer(angreifer, sperrliste)
    text = (
        f"neue_angreifer({gezeigt(angreifer)}, {gezeigt(sperrliste)}) ergibt {ergebnis!r}, "
        f"erwartet war {erwartet!r}.{hinweis}"
    )
    return ergebnis == erwartet, text


def pruefe_zeitraum(geblockt, anfragen, hinweis=""):
    """Prüft geblockt_im_zeitraum gegen die Vergleichslösung; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(geblockt_im_zeitraum, geblockt, anfragen)
    erwartet = vergleich_zeitraum(geblockt, anfragen)
    text = (
        f"geblockt_im_zeitraum({gezeigt(geblockt)}, {gezeigt(anfragen)}) ergibt {ergebnis!r}, "
        f"erwartet war {erwartet!r}.{hinweis}"
    )
    return ergebnis == erwartet, text


def pruefe_fenster(zeitpunkte, k, erwartet, hinweis=""):
    """Prüft kuerzestes_fenster gegen einen erwarteten Wert; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(kuerzestes_fenster, zeitpunkte, k)
    text = f"kuerzestes_fenster({gezeigt(zeitpunkte)}, {k}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.{hinweis}"
    return ergebnis == erwartet, text


def zugriffe(funktion, liste, *weitere):
    """Ruft funktion mit liste als Zaehlliste auf; liefert (Ergebnis, Lesezugriffe)."""
    gezaehlt = Zaehlliste(liste)
    try:
        ergebnis = funktion(gezaehlt, *weitere)
    except Exception as fehler:
        ergebnis = f"{type(fehler).__name__}: {fehler}"
    return ergebnis, gezaehlt.lesezugriffe


def adresse(zufall, netze):
    """Erzeugt eine zufällige Adresse aus wenigen Netzen, damit Doppelte vorkommen."""
    return f"{zufall.choice(netze)}.{zufall.randint(0, 255)}"


# neue_angreifer: das Beispiel aus der Aufgabe
stimmt, text = pruefe_angreifer(
    ANGREIFER, SPERRLISTE, "\nTipp: Gesucht sind Adressen aus angreifer, die nicht in sperrliste stehen."
)
assert stimmt, text

# neue_angreifer: andere Adressen (nicht fest hinschreiben!)
stimmt, text = pruefe_angreifer(["192.0.2.9", "198.51.100.1", "192.0.2.10"], ["198.51.100.1"])
assert stimmt, text

# neue_angreifer: jede Adresse nur einmal
stimmt, text = pruefe_angreifer(
    ["192.0.2.5", "192.0.2.5", "192.0.2.5"], [],
    "\nTipp: Sammeln Sie die neuen Adressen in einer Menge, dann verschwinden Doppelte von selbst.",
)
assert stimmt, text

# neue_angreifer: alphabetisch sortiert, nicht in der Reihenfolge der Angriffe
stimmt, text = pruefe_angreifer(
    ["203.0.113.1", "192.0.2.1", "198.51.100.1"], [], "\nTipp: Geben Sie sorted(...) zurück."
)
assert stimmt, text

# neue_angreifer: alle schon gesperrt
stimmt, text = pruefe_angreifer(["192.0.2.44", "192.0.2.44"], ["192.0.2.44"])
assert stimmt, text

# neue_angreifer: keine Angriffe
stimmt, text = pruefe_angreifer([], SPERRLISTE)
assert stimmt, text

# neue_angreifer: leere Sperrliste
stimmt, text = pruefe_angreifer(ANGREIFER, [])
assert stimmt, text

# geblockt_im_zeitraum: das Beispiel aus der Aufgabe
stimmt, text = pruefe_zeitraum(GEBLOCKT, [(2, 4), (0, 7), (5, 6)], "\nTipp: Beide Minuten von und bis zählen mit.")
assert stimmt, text

# geblockt_im_zeitraum: andere Zeiträume (nicht fest hinschreiben!)
stimmt, text = pruefe_zeitraum(GEBLOCKT, [(3, 3), (1, 6), (6, 7)])
assert stimmt, text

# geblockt_im_zeitraum: ein Zeitraum, der in Minute 0 beginnt
stimmt, text = pruefe_zeitraum(
    [9, 1, 5], [(0, 0), (0, 1)],
    "\nTipp: Beginnt die Präfixsumme mit 0 (summe[0] = 0), braucht Minute 0 keinen Sonderfall.",
)
assert stimmt, text

# geblockt_im_zeitraum: ein Zeitraum bis zur letzten Minute
stimmt, text = pruefe_zeitraum([9, 1, 5], [(2, 2), (1, 2)])
assert stimmt, text

# geblockt_im_zeitraum: dieselbe Liste für mehrere Anfragen, in ihrer Reihenfolge
stimmt, text = pruefe_zeitraum([2, 3], [(1, 1), (0, 0), (1, 1), (0, 1)])
assert stimmt, text

# geblockt_im_zeitraum: eine einzige Minute
stimmt, text = pruefe_zeitraum([10**6], [(0, 0)])
assert stimmt, text

# geblockt_im_zeitraum: keine Anfragen
stimmt, text = pruefe_zeitraum(GEBLOCKT, [])
assert stimmt, text

# kuerzestes_fenster: das Beispiel mit k = 3
stimmt, text = pruefe_fenster(
    ZEITPUNKTE, 3, 15, "\nTipp: Die Alarme kommen unsortiert; sortieren Sie sie zuerst."
)
assert stimmt, text

# kuerzestes_fenster: das Beispiel mit k = 4 (nicht fest hinschreiben!)
stimmt, text = pruefe_fenster(
    ZEITPUNKTE, 4, 120,
    "\nTipp: In der sortierten Liste liegen k Alarme mit kürzester Spanne direkt nebeneinander: "
    "sortiert[i + k - 1] - sortiert[i].",
)
assert stimmt, text

# kuerzestes_fenster: zu wenige Alarme ergibt None
stimmt, text = pruefe_fenster(ZEITPUNKTE, 9, None)
assert stimmt, text

# kuerzestes_fenster: das kürzeste Fenster liegt ganz am Ende
stimmt, text = pruefe_fenster(
    [0, 100, 200, 300, 301, 302], 3, 2, "\nTipp: Prüfen Sie auch das letzte Fenster, das mit dem letzten Alarm endet."
)
assert stimmt, text

# kuerzestes_fenster: genau k Alarme
stimmt, text = pruefe_fenster([70, 10, 40], 3, 60)
assert stimmt, text

# kuerzestes_fenster: k = 1 ergibt 0
stimmt, text = pruefe_fenster([70, 10, 40], 1, 0, "\nTipp: Ein einzelner Alarm hat die Spanne 0.")
assert stimmt, text

# kuerzestes_fenster: Alarme in derselben Sekunde
stimmt, text = pruefe_fenster([500, 80, 500, 900], 2, 0)
assert stimmt, text

# kuerzestes_fenster: keine Alarme
stimmt, text = pruefe_fenster([], 1, None)
assert stimmt, text

# Die Ausgabe des Programms
erwartet = "['198.51.100.23', '203.0.113.7']\n[49, 78, 0]\n15"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

zufall = Zufall(3069)

# neue_angreifer: viele zufällige Listen
for _ in range(300):
    netze = zufall.sample(["192.0.2", "198.51.100", "203.0.113"], zufall.randint(1, 3))
    angreifer = [adresse(zufall, netze) for _ in range(zufall.randint(0, 15))]
    sperrliste = [adresse(zufall, netze) for _ in range(zufall.randint(0, 15))]
    sperrliste += zufall.sample(angreifer, min(len(angreifer), zufall.randint(0, 5)))
    stimmt, text = pruefe_angreifer(angreifer, sperrliste)
    assert stimmt, text

# geblockt_im_zeitraum: viele zufällige Zeiträume
for _ in range(300):
    geblockt = [zufall.randint(0, zufall.choice([3, 10**6])) for _ in range(zufall.randint(1, 15))]
    anfragen = []
    for _ in range(zufall.randint(0, 6)):
        von = zufall.randrange(len(geblockt))
        anfragen.append((von, zufall.randint(von, len(geblockt) - 1)))
    stimmt, text = pruefe_zeitraum(geblockt, anfragen)
    assert stimmt, text

# kuerzestes_fenster: viele zufällige Alarme
for _ in range(300):
    zeitpunkte = [zufall.randint(0, zufall.choice([20, 10**9])) for _ in range(zufall.randint(0, 10))]
    k = zufall.randint(1, 11)
    stimmt, text = pruefe_fenster(zeitpunkte, k, vergleich_fenster(zeitpunkte, k))
    assert stimmt, text

# Laufzeit: neue_angreifer fragt nicht jedes Mal die ganze Sperrliste ab
angreifer = [f"10.0.{i // 256}.{i % 256}" for i in range(0, 3000, 2)]
sperrliste = [f"10.0.{i // 256}.{i % 256}" for i in range(1, 3000, 2)]
ergebnis, anzahl = zugriffe(lambda gesperrt: neue_angreifer(angreifer, gesperrt), sperrliste)
erlaubt = 3 * len(sperrliste) + 10
assert ergebnis == sorted(angreifer) and anzahl <= erlaubt, (
    f"neue_angreifer mit 1500 Angreifern und 1500 gesperrten Adressen liest die Sperrliste {anzahl}-mal; erlaubt "
    f"sind {erlaubt} (O(n)). adresse not in sperrliste geht jedes Mal die ganze Liste durch, das sind über zwei "
    "Millionen Zugriffe.\nTipp: Machen Sie aus der Sperrliste einmal eine Menge (Aufgabe 3_063)."
    if ergebnis == sorted(angreifer)
    else f"neue_angreifer mit 1500 Angreifern ohne gesperrte darunter ergibt {gezeigt(ergebnis)}, erwartet waren alle."
)

# Laufzeit: geblockt_im_zeitraum addiert nicht jeden Zeitraum neu
geblockt = [zufall.randint(0, 100) for _ in range(2000)]
anfragen = [(zufall.randint(0, 100), zufall.randint(1900, 1999)) for _ in range(2000)]
ergebnis, anzahl = zugriffe(geblockt_im_zeitraum, geblockt, anfragen)
erlaubt = 3 * len(geblockt) + 2 * len(anfragen) + 10
assert ergebnis == vergleich_zeitraum(geblockt, anfragen) and anzahl <= erlaubt, (
    f"geblockt_im_zeitraum mit 2000 Minuten und 2000 langen Zeiträumen liest geblockt {anzahl}-mal; erlaubt sind "
    f"{erlaubt} (O(n)). Jeden Zeitraum neu zu addieren braucht fast vier Millionen Zugriffe.\n"
    "Tipp: Rechnen Sie einmal die Präfixsummen aus (Aufgabe 3_062); dann ist jeder Zeitraum eine Subtraktion."
    if ergebnis == vergleich_zeitraum(geblockt, anfragen)
    else "geblockt_im_zeitraum mit 2000 Minuten liefert falsche Summen."
)

# Laufzeit: kuerzestes_fenster vergleicht nicht jeden Alarm mit jedem
zeitpunkte = [zufall.randint(0, 10**9) for _ in range(2000)]
ergebnis, anzahl = zugriffe(kuerzestes_fenster, zeitpunkte, 50)
sortiert = sorted(zeitpunkte)
erwartet = min(sortiert[i + 49] - sortiert[i] for i in range(len(sortiert) - 49))
erlaubt = 3 * len(zeitpunkte) + 10
assert ergebnis == erwartet and anzahl <= erlaubt, (
    f"kuerzestes_fenster mit 2000 Alarmen und k = 50 liest zeitpunkte {anzahl}-mal; erlaubt sind {erlaubt} "
    "(O(n log n): einmal sortieren, dann einmal durchgehen).\n"
    "Tipp: sortiert = sorted(zeitpunkte) liest jeden Alarm einmal; danach arbeiten Sie nur noch mit sortiert."
    if ergebnis == erwartet
    else f"kuerzestes_fenster mit 2000 Alarmen und k = 50 ergibt {ergebnis!r}, erwartet war {erwartet}."
)

# Obere Grenze: neue_angreifer mit je 100 000 Adressen
angreifer = [f"10.{zufall.randint(0, 3)}.{zufall.randint(0, 255)}.{zufall.randint(0, 255)}" for _ in range(100000)]
sperrliste = [f"10.{zufall.randint(0, 3)}.{zufall.randint(0, 255)}.{zufall.randint(0, 255)}" for _ in range(100000)]
ergebnis = wert_von(neue_angreifer, angreifer, sperrliste)
erwartet = sorted(set(angreifer) - set(sperrliste))
assert ergebnis == erwartet, (
    f"neue_angreifer mit je 100 000 Adressen ergibt {gezeigt(ergebnis) if isinstance(ergebnis, list) else ergebnis}, "
    f"erwartet waren {len(erwartet)} Adressen, beginnend mit {erwartet[:3]}."
)

# Obere Grenze: geblockt_im_zeitraum mit 100 000 Minuten und 100 000 Zeiträumen
geblockt = [zufall.randint(0, 10**6) for _ in range(100000)]
anfragen = []
for _ in range(100000):
    von = zufall.randint(0, 99999)
    anfragen.append((von, zufall.randint(von, 99999)))
ergebnis = wert_von(geblockt_im_zeitraum, geblockt, anfragen)
praefix = [0]
for anzahl in geblockt:
    praefix.append(praefix[-1] + anzahl)
erwartet = [praefix[bis + 1] - praefix[von] for von, bis in anfragen]
assert ergebnis == erwartet, (
    f"geblockt_im_zeitraum mit 100 000 Minuten und 100 000 Zeiträumen ergibt "
    f"{gezeigt(ergebnis) if isinstance(ergebnis, list) else ergebnis}, erwartet war eine Liste, "
    f"beginnend mit {erwartet[:3]}."
)

# Obere Grenze: kuerzestes_fenster mit 100 000 Alarmen und großem k
zeitpunkte = [zufall.randint(0, 10**9) for _ in range(100000)]
sortiert = sorted(zeitpunkte)
erwartet = min(sortiert[i + 49999] - sortiert[i] for i in range(len(sortiert) - 49999))
stimmt, text = pruefe_fenster(
    zeitpunkte, 50000, erwartet,
    "\nTipp: Ein Ausschnitt sortiert[i:i + k] kostet k Schritte; lesen Sie nur die beiden Enden des Fensters.",
)
assert stimmt, text
