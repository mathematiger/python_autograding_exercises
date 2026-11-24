# Automatisch erzeugt aus lehrkraft/muster/3_070_merkmalstabelle.py - nicht von Hand ändern.
# vorlage-hash: 396ad57faa53a205
# text-hash: 13023eaeb253a0f4
# thema: algorithmen
# inhalt: Sieb des Eratosthenes

def wert_von(funktion, *argumente):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def gezeigt(werte):
    """Zeigt kurze Listen ganz, lange nur mit Länge und Anfang."""
    if not isinstance(werte, list) or len(werte) <= 12:
        return repr(werte)
    return f"<{len(werte)} Zahlen: {werte[:5]} …>"


def ist_primzahl(zahl):
    """Vergleichslösung: prüft eine einzelne Zahl durch Teilen bis zur Wurzel (anderer Weg als das Sieb)."""
    if zahl < 2:
        return False
    teiler = 2
    while teiler * teiler <= zahl:
        if zahl % teiler == 0:
            return False
        teiler += 1
    return True


def vergleich_bis(n):
    """Vergleichslösung für kleine n: jede Zahl einzeln prüfen."""
    return [zahl for zahl in range(2, n + 1) if ist_primzahl(zahl)]


def vergleich_naechste(wunsch):
    """Vergleichslösung: von wunsch aufwärts jede Zahl einzeln prüfen."""
    while not ist_primzahl(wunsch):
        wunsch += 1
    return wunsch


def pruefe_bis(n, hinweis=""):
    """Prüft primzahlen_bis(n) gegen die Vergleichslösung; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(primzahlen_bis, n)
    erwartet = vergleich_bis(n)
    return ergebnis == erwartet, f"primzahlen_bis({n}) ergibt {gezeigt(ergebnis)}, erwartet war {gezeigt(erwartet)}.{hinweis}"


def pruefe_naechste(wuensche, hinweis=""):
    """Prüft naechste_primzahlen gegen die Vergleichslösung; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(naechste_primzahlen, list(wuensche))
    erwartet = [vergleich_naechste(wunsch) for wunsch in wuensche]
    text = f"naechste_primzahlen({gezeigt(wuensche)}) ergibt {gezeigt(ergebnis)}, erwartet war {gezeigt(erwartet)}.{hinweis}"
    return ergebnis == erwartet, text


def vergleich_sieb(n):
    """Vergleichslösung: für jedes k einzeln geprüft."""
    return [ist_primzahl(k) for k in range(n + 1)]


def pruefe_sieb(n, hinweis=""):
    """Prüft sieb(n) gegen die Vergleichslösung; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(sieb, n)
    erwartet = vergleich_sieb(n)
    text = f"sieb({n}) ergibt {gezeigt(ergebnis)},\nerwartet war {gezeigt(erwartet)}.{hinweis}"
    if isinstance(ergebnis, list) and len(ergebnis) == len(erwartet) and ergebnis != erwartet:
        falsch = [k for k in range(n + 1) if ergebnis[k] != erwartet[k]]
        text += f"\nFalsch ist ist_prim[k] für k = {falsch[:10]}."
    return ergebnis == erwartet, text


# sieb: das Beispiel aus der Aufgabe
stimmt, text = pruefe_sieb(
    10, "\nTipp: Erst alles True außer 0 und 1, dann für jede Primzahl p die Vielfachen auf False setzen."
)
assert stimmt, text

# sieb: die Liste hat n + 1 Einträge
ergebnis = wert_von(sieb, 30)
assert isinstance(ergebnis, list) and len(ergebnis) == 31, (
    f"sieb(30) ergibt {gezeigt(ergebnis)}"
    + (f" mit {len(ergebnis)} Einträgen" if isinstance(ergebnis, list) else "")
    + ", erwartet war eine Liste mit 31 Einträgen (für 0 bis 30).\nTipp: [True] * (n + 1)"
)

# sieb: ein anderes n (nicht fest hinschreiben!)
stimmt, text = pruefe_sieb(30)
assert stimmt, text

# sieb: Quadrate von Primzahlen und n selbst werden gestrichen
stimmt, text = pruefe_sieb(49, "\nTipp: range(p * p, n + 1, p) beginnt bei p · p und schließt n mit ein.")
assert stimmt, text

# sieb: n = 1
stimmt, text = pruefe_sieb(1, "\nTipp: 0 und 1 sind keine Primzahlen.")
assert stimmt, text

# sieb: n = 0
stimmt, text = pruefe_sieb(0, "\nTipp: Bei n = 0 gibt es ist_prim[1] gar nicht.")
assert stimmt, text

# primzahlen_bis: das Beispiel aus der Aufgabe
stimmt, text = pruefe_bis(30, "\nTipp: Sammeln Sie alle k von 2 bis n, für die sieb(n)[k] True ist.")
assert stimmt, text

# primzahlen_bis: ein anderes n (nicht fest hinschreiben!)
stimmt, text = pruefe_bis(100)
assert stimmt, text

# primzahlen_bis: n selbst ist eine Primzahl und gehört dazu
stimmt, text = pruefe_bis(29, "\nTipp: Die Liste ist_prim braucht n + 1 Einträge, damit auch n selbst darin steht.")
assert stimmt, text

# primzahlen_bis: Quadrate von Primzahlen werden gestrichen
stimmt, text = pruefe_bis(
    49, "\nTipp: Das Streichen beginnt bei p · p; range(p * p, n + 1, p) schließt n mit ein."
)
assert stimmt, text

# primzahlen_bis: n = 2, die kleinste Primzahl
stimmt, text = pruefe_bis(2)
assert stimmt, text

# primzahlen_bis: n = 1 ergibt eine leere Liste
stimmt, text = pruefe_bis(1, "\nTipp: 1 ist keine Primzahl; setzen Sie ist_prim[0] und ist_prim[1] auf False.")
assert stimmt, text

# primzahlen_bis: n = 0 ergibt eine leere Liste
stimmt, text = pruefe_bis(0)
assert stimmt, text

# naechste_primzahlen: das Beispiel aus der Aufgabe
stimmt, text = pruefe_naechste(
    [1000, 24, 97, 2], "\nTipp: Sieben Sie einmal und gehen Sie dann von jedem Wunsch aufwärts bis zur ersten Primzahl."
)
assert stimmt, text

# naechste_primzahlen: andere Wünsche (nicht fest hinschreiben!)
stimmt, text = pruefe_naechste([500, 10, 8000])
assert stimmt, text

# naechste_primzahlen: ein Wunsch, der selbst eine Primzahl ist, bleibt
stimmt, text = pruefe_naechste([13, 101], "\nTipp: Gesucht ist die kleinste Primzahl ≥ wunsch, nicht > wunsch.")
assert stimmt, text

# naechste_primzahlen: die Reihenfolge der Wünsche bleibt, Doppelte auch
stimmt, text = pruefe_naechste([90, 8, 90, 3])
assert stimmt, text

# naechste_primzahlen: die nächste Primzahl liegt über dem größten Wunsch
stimmt, text = pruefe_naechste(
    [24], "\nTipp: Sieben Sie über max(wuensche) hinaus, sonst findet 24 keine Primzahl in der Liste."
)
assert stimmt, text

# naechste_primzahlen: eine große Lücke zwischen zwei Primzahlen
stimmt, text = pruefe_naechste(
    [492114], "\nTipp: Nach 492 113 kommt erst 492 227; sieben Sie bis max(wuensche) + 114."
)
assert stimmt, text

# naechste_primzahlen: der größte erlaubte Wunsch
stimmt, text = pruefe_naechste([10**6])
assert stimmt, text

# naechste_primzahlen: keine Wünsche
stimmt, text = pruefe_naechste([], "\nTipp: max([]) ist ein ValueError; prüfen Sie zuerst, ob es Wünsche gibt.")
assert stimmt, text

# Die Ausgabe des Programms
erwartet = (
    "[False, False, True, True, False, True, False, True, False, False, False]\n"
    "[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]\n[1009, 29, 97, 2]"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

zufall = Zufall(3070)

# sieb: viele zufällige n
for _ in range(100):
    stimmt, text = pruefe_sieb(zufall.randint(0, 1000))
    assert stimmt, text

# primzahlen_bis: viele zufällige n
for _ in range(150):
    stimmt, text = pruefe_bis(zufall.randint(0, 2000))
    assert stimmt, text

# Laufzeit: primzahlen_bis streicht statt zu teilen
ergebnis, schritte = zaehle_schritte(primzahlen_bis, 30000)
erlaubt = 10 * 30000
if ergebnis != vergleich_bis(30000):
    text = f"primzahlen_bis(30000) ergibt {gezeigt(ergebnis)}, erwartet waren die 3245 Primzahlen bis 30000."
else:
    text = (
        f"primzahlen_bis(30000) braucht {schritte} Schritte, erlaubt sind {erlaubt} (O(n log log n)). Jede Zahl "
        "einzeln durch Teilen zu prüfen braucht ein Vielfaches davon.\n"
        "Tipp: Teilen Sie gar nicht; streichen Sie mit range(p * p, n + 1, p) die Vielfachen jeder Primzahl p."
    )
assert ergebnis == vergleich_bis(30000) and schritte <= erlaubt, text

# naechste_primzahlen: viele zufällige Wünsche
for _ in range(150):
    hoechstens = zufall.choice([30, 5000, 10**6])
    stimmt, text = pruefe_naechste([zufall.randint(2, hoechstens) for _ in range(zufall.randint(1, 8))])
    assert stimmt, text

# Laufzeit: naechste_primzahlen siebt nur einmal
wuensche = [zufall.randint(2, 3000) for _ in range(3000)]
ergebnis, schritte = zaehle_schritte(naechste_primzahlen, list(wuensche))
erlaubt = 20 * 3000 + 20 * len(wuensche)
erwartet = [vergleich_naechste(wunsch) for wunsch in wuensche]
if ergebnis != erwartet:
    text = f"naechste_primzahlen mit 3000 Wünschen bis 3000 ergibt {gezeigt(ergebnis)}, erwartet war {gezeigt(erwartet)}."
else:
    text = (
        f"naechste_primzahlen mit 3000 Wünschen bis 3000 braucht {schritte} Schritte, erlaubt sind {erlaubt}.\n"
        "Tipp: Sieben Sie nur einmal bis max(wuensche) + 114 und schauen Sie dann je Wunsch in der Liste ist_prim "
        "nach, statt für jeden Wunsch neu zu sieben, jede Zahl durch Teilen zu prüfen oder alle Primzahlen "
        "durchzugehen."
    )
assert ergebnis == erwartet and schritte <= erlaubt, text

# Obere Grenze: sieb(1 100 000)
ergebnis = wert_von(sieb, 1100000)
stimmt = isinstance(ergebnis, list) and len(ergebnis) == 1100001 and sum(ergebnis) == 85714
assert stimmt, (
    f"sieb(1100000) ergibt {gezeigt(ergebnis)}, erwartet war eine Liste mit 1 100 001 Einträgen, "
    "davon 85714 True."
)

# Obere Grenze: primzahlen_bis(10**6)
ergebnis = wert_von(primzahlen_bis, 10**6)
stimmt = isinstance(ergebnis, list) and len(ergebnis) == 78498 and ergebnis[:3] == [2, 3, 5] and ergebnis[-1] == 999983
assert stimmt, (
    f"primzahlen_bis(10**6) ergibt {gezeigt(ergebnis)}, erwartet waren 78 498 Primzahlen von 2 bis 999 983."
)

# Obere Grenze: naechste_primzahlen mit 10 000 Wünschen bis 10**6
wuensche = [zufall.randint(2, 10**6) for _ in range(10000)]
ergebnis = wert_von(naechste_primzahlen, list(wuensche))
stichprobe = zufall.sample(range(10000), 200)
stimmt = isinstance(ergebnis, list) and len(ergebnis) == 10000
for i in stichprobe:
    if stimmt and ergebnis[i] != vergleich_naechste(wuensche[i]):
        stimmt = False
        text = (
            f"naechste_primzahlen mit 10 000 Wünschen: Für den Wunsch {wuensche[i]} (Position {i}) kommt "
            f"{ergebnis[i]} heraus, erwartet war {vergleich_naechste(wuensche[i])}."
        )
if not isinstance(ergebnis, list) or len(ergebnis) != 10000:
    text = f"naechste_primzahlen mit 10 000 Wünschen ergibt {gezeigt(ergebnis)}, erwartet waren 10 000 Primzahlen."
assert stimmt, text
