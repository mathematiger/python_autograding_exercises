# Automatisch erzeugt aus lehrkraft/muster/4_075_linkkosten.py - nicht von Hand ändern.
# vorlage-hash: 7d18d0265a889f78
# text-hash: 09dfd12b5fb2927b
# thema: algorithmen
# inhalt: Dijkstra mit heapq

import copy

NETZ = {
    "zentrale": {"rz": 100, "nord": 10, "sued": 10},
    "nord": {"zentrale": 10, "rz": 10, "ost": 100},
    "sued": {"zentrale": 10, "ost": 10},
    "rz": {"nord": 10, "zentrale": 100, "ost": 1},
    "ost": {"rz": 1, "sued": 10, "nord": 100},
    "lager": {"zentrale": 100},
}
KOSTEN = {"zentrale": 0, "nord": 10, "sued": 10, "rz": 20, "ost": 20}
VORGAENGER = {"nord": "zentrale", "sued": "zentrale", "rz": "nord", "ost": "sued"}


def wert_von(funktion, *argumente):
    """Ruft funktion mit Kopien der Argumente auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*copy.deepcopy(argumente))
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def kurz(wert):
    """Kürzt lange Werte für die Meldung."""
    text = repr(wert)
    return text if len(text) <= 300 else text[:200] + f" … ({len(wert)} Einträge)"


def teil(ergebnis, nummer):
    """Gibt Teil nummer des Paars von dijkstra zurück, oder das ganze Ergebnis, wenn es kein Paar ist."""
    if isinstance(ergebnis, tuple) and len(ergebnis) == 2:
        return ergebnis[nummer]
    return ergebnis


def vergleich_kosten(netz, start):
    """Langsame Vergleichslösung (Bellman-Ford): verbessert über alle Leitungen, bis sich nichts mehr ändert."""
    kosten = {start: 0}
    geaendert = True
    while geaendert:
        geaendert = False
        for von, nachbarn in netz.items():
            for nach, leitung in nachbarn.items():
                if von in kosten and (nach not in kosten or kosten[von] + leitung < kosten[nach]):
                    kosten[nach] = kosten[von] + leitung
                    geaendert = True
    return kosten


def fehler_im_vorgaenger(netz, start, kosten, vorgaenger):
    """Prüft, ob vorgaenger zu kosten passt; gibt eine Beschreibung des ersten Fehlers zurück oder None."""
    if not isinstance(vorgaenger, dict):
        return f"vorgaenger ist {kurz(vorgaenger)}, erwartet war ein Dictionary."
    if start in vorgaenger:
        return f"start {start!r} steht in vorgaenger; der Start hat keinen Vorgänger."
    if set(vorgaenger) != set(kosten) - {start}:
        fehlend = sorted(set(kosten) - {start} - set(vorgaenger))
        zuviel = sorted(set(vorgaenger) - set(kosten))
        return f"In vorgaenger fehlen {fehlend[:5]}, zu viel sind {zuviel[:5]}; erwartet war jeder erreichbare Router außer start."
    for router, vorher in vorgaenger.items():
        leitung = netz.get(vorher, {}).get(router)
        if leitung is None:
            return f"vorgaenger[{router!r}] ist {vorher!r}, aber es gibt keine Leitung von {vorher!r} nach {router!r}."
        if vorher not in kosten or kosten[vorher] + leitung != kosten[router]:
            return (
                f"vorgaenger[{router!r}] ist {vorher!r}, aber {vorher!r} kostet {kosten.get(vorher)} und die "
                f"Leitung {leitung}, zusammen nicht kosten[{router!r}] = {kosten[router]}."
            )
    return None


def fehler_im_weg(netz, start, ziel, ergebnis, erwartete_kosten):
    """Prüft, ob ergebnis ein günstigster Weg (kosten, weg) von start nach ziel ist; gibt den Fehler zurück oder None."""
    if not (isinstance(ergebnis, tuple) and len(ergebnis) == 2 and isinstance(ergebnis[1], list)):
        return f"ergibt {kurz(ergebnis)}, erwartet war ein Paar (gesamtkosten, weg) mit den Kosten {erwartete_kosten}."
    gesamt, weg = ergebnis
    if gesamt != erwartete_kosten:
        return f"ergibt die Kosten {gesamt}, erwartet waren {erwartete_kosten}."
    if not weg or weg[0] != start or weg[-1] != ziel:
        return f"ergibt den Weg {kurz(weg)}; er soll mit {start!r} beginnen und mit {ziel!r} enden."
    summe = 0
    for von, nach in zip(weg, weg[1:]):
        leitung = netz.get(von, {}).get(nach)
        if leitung is None:
            return f"ergibt den Weg {kurz(weg)}, aber es gibt keine Leitung von {von!r} nach {nach!r}."
        summe += leitung
    if summe != gesamt:
        return f"ergibt den Weg {kurz(weg)}, dessen Leitungen zusammen {summe} kosten, nicht {gesamt}."
    return None


def zufallsnetz(zufall, router, leitungen, hoechste_kosten):
    """Erzeugt ein Netz mit Routern r0, r1, … und bis zu leitungen gerichteten Leitungen."""
    netz = {}
    for _ in range(leitungen):
        von, nach = zufall.sample(range(router), 2)
        netz.setdefault(f"r{von}", {})[f"r{nach}"] = zufall.randint(1, hoechste_kosten)
    return netz


def sternnetz(zufall, router):
    """Netz, in dem start alle Router direkt, aber teuer erreicht; dazu billige Querleitungen.

    So bleiben fast alle Router lange offen, und wer in jeder Runde alle offenen durchsucht,
    braucht quadratisch viele Schritte.
    """
    netz = {"start": {}}
    for nummer in range(router):
        netz["start"][f"r{nummer}"] = zufall.randint(1000, 60000)
        netz[f"r{nummer}"] = {}
        for _ in range(2):
            nach = zufall.randrange(router)
            if nach != nummer:
                netz[f"r{nummer}"][f"r{nach}"] = zufall.randint(1, 100)
    return netz


def leitungszahl(netz):
    """Zählt die Leitungen eines Netzes."""
    return sum(len(nachbarn) for nachbarn in netz.values())


def routerzahl(netz):
    """Zählt alle Router, auch die, die nur als Nachbar vorkommen."""
    namen = set(netz)
    for nachbarn in netz.values():
        namen.update(nachbarn)
    return len(namen)


# dijkstra: die Kosten im Beispiel
ergebnis = wert_von(dijkstra, NETZ, "zentrale")
assert teil(ergebnis, 0) == KOSTEN, (
    f"dijkstra(netz, 'zentrale') ergibt als kosten {kurz(teil(ergebnis, 0))},\nerwartet war {KOSTEN}.\n"
    "Tipp: Geben Sie das Paar kosten, vorgaenger zurück. Der günstigste Weg nach rz geht über nord (10 + 10 = 20), "
    "nicht über die direkte Leitung (100); der Hintergrund zeigt, wie kosten entsteht."
)

# dijkstra: die Vorgänger im Beispiel
ergebnis = wert_von(dijkstra, NETZ, "zentrale")
assert teil(ergebnis, 1) == VORGAENGER, (
    f"dijkstra(netz, 'zentrale') ergibt als vorgaenger {kurz(teil(ergebnis, 1))},\nerwartet war {VORGAENGER}.\n"
    "Tipp: Wird ein Nachbar billiger, tragen Sie vorgaenger[nachbar] = router ein; start bekommt keinen Eintrag."
)

# dijkstra: von einem anderen Start aus
erwartet = {"lager": 0, "zentrale": 100, "nord": 110, "sued": 110, "rz": 120, "ost": 120}
ergebnis = wert_von(dijkstra, NETZ, "lager")
assert teil(ergebnis, 0) == erwartet, (
    f"dijkstra(netz, 'lager') ergibt als kosten {kurz(teil(ergebnis, 0))},\nerwartet war {erwartet}."
)

# dijkstra: ein billiger Umweg schlägt die direkte Leitung
netz = {"a": {"z": 50, "b": 1}, "b": {"c": 1}, "c": {"z": 1}}
ergebnis = wert_von(dijkstra, netz, "a")
erwartet = {"a": 0, "b": 1, "c": 2, "z": 3}
assert teil(ergebnis, 0) == erwartet, (
    f"Für {netz} ergibt dijkstra(netz, 'a') als kosten {kurz(teil(ergebnis, 0))},\nerwartet war {erwartet}.\n"
    "Tipp: Die Breitensuche aus 3_058 nimmt den Weg mit den wenigsten Sprüngen (a → z, Kosten 50). Nehmen Sie "
    "immer den günstigsten offenen Router mit heapq.heappop heraus, und legen Sie die Tupel als (kosten, router) "
    "in den Heap, damit nach den Kosten sortiert wird."
)

# dijkstra: ein schon gefundener Router kann noch billiger werden
netz = {"a": {"b": 1, "c": 2}, "b": {"d": 10}, "c": {"d": 1}, "d": {"e": 1}}
ergebnis = wert_von(dijkstra, netz, "a")
erwartet = ({"a": 0, "b": 1, "c": 2, "d": 3, "e": 4}, {"b": "a", "c": "a", "d": "c", "e": "d"})
assert ergebnis == erwartet, (
    f"Für {netz} ergibt dijkstra(netz, 'a')\n{kurz(ergebnis)},\nerwartet war {erwartet}.\n"
    "Tipp: d wird über b zuerst mit 11 gefunden, über c später mit 3. Verbessern Sie kosten[nachbar] immer, "
    "wenn neu < kosten[nachbar], und setzen Sie dann auch vorgaenger neu."
)

# dijkstra: Leitungen gelten nur in ihrer Richtung
netz = {"a": {"b": 5}, "b": {"c": 2}, "c": {"a": 1}}
ergebnis = wert_von(dijkstra, netz, "b")
erwartet = {"b": 0, "c": 2, "a": 3}
assert teil(ergebnis, 0) == erwartet, (
    f"Für {netz} ergibt dijkstra(netz, 'b') als kosten {kurz(teil(ergebnis, 0))},\nerwartet war {erwartet}.\n"
    "Tipp: Von b nach a geht es nur über c; die Leitung a → b kostet nur in Richtung b."
)

# dijkstra: ein Router ohne eigene Leitungen
netz = {"a": {"c": 1}, "c": {"b": 1, "d": 3}, "d": {"a": 2}}
ergebnis = wert_von(dijkstra, netz, "a")
erwartet = ({"a": 0, "c": 1, "b": 2, "d": 4}, {"c": "a", "b": "c", "d": "c"})
assert ergebnis == erwartet, (
    f"Für {netz} ergibt dijkstra(netz, 'a')\n{kurz(ergebnis)},\nerwartet war {erwartet}.\n"
    "Tipp: b ist kein Schlüssel von netz; netz.get(router, {}) statt netz[router]."
)

# dijkstra: nicht erreichbare Router fehlen
netz = {"a": {"b": 1}, "c": {"a": 1, "d": 1}}
ergebnis = wert_von(dijkstra, netz, "a")
erwartet = ({"a": 0, "b": 1}, {"b": "a"})
assert ergebnis == erwartet, (
    f"Für {netz} ergibt dijkstra(netz, 'a')\n{kurz(ergebnis)},\nerwartet war {erwartet}.\n"
    "Tipp: c und d sind von a aus nicht erreichbar und fehlen deshalb; tragen Sie auch kein math.inf ein."
)

# dijkstra: ein Start, der nicht im Netz vorkommt
ergebnis = wert_von(dijkstra, NETZ, "drucker")
assert ergebnis == ({"drucker": 0}, {}), (
    f"dijkstra(netz, 'drucker') ergibt {kurz(ergebnis)}, erwartet war ({{'drucker': 0}}, {{}}).\n"
    "Tipp: netz.get(router, {}) statt netz[router]."
)

# dijkstra: leeres Netz
ergebnis = wert_von(dijkstra, {}, "a")
assert ergebnis == ({"a": 0}, {}), f"dijkstra({{}}, 'a') ergibt {kurz(ergebnis)}, erwartet war ({{'a': 0}}, {{}})."

# dijkstra verändert das Netz nicht
netz = copy.deepcopy(NETZ)
try:
    dijkstra(netz, "zentrale")
except Exception:
    pass
assert netz == NETZ, f"Nach dijkstra(netz, 'zentrale') ist netz {kurz(netz)}; es sollte unverändert bleiben."

# weg_aus: das Beispiel
ergebnis = wert_von(weg_aus, VORGAENGER, "zentrale", "ost")
assert ergebnis == ["zentrale", "sued", "ost"], (
    f"weg_aus(vorgaenger, 'zentrale', 'ost') ergibt {kurz(ergebnis)}, erwartet war ['zentrale', 'sued', 'ost'].\n"
    "Tipp: Gehen Sie von ziel aus rückwärts zu vorgaenger[…], bis Sie bei start sind, und drehen Sie die Liste um."
)

# weg_aus: ein längerer Weg (nicht fest hinschreiben!)
vorgaenger = {"b": "a", "c": "b", "d": "c", "e": "d", "x": "a"}
ergebnis = wert_von(weg_aus, vorgaenger, "a", "e")
assert ergebnis == ["a", "b", "c", "d", "e"], (
    f"weg_aus({vorgaenger}, 'a', 'e') ergibt {kurz(ergebnis)}, erwartet war ['a', 'b', 'c', 'd', 'e']."
)

# weg_aus: Ziel und Start sind gleich
ergebnis = wert_von(weg_aus, VORGAENGER, "zentrale", "zentrale")
assert ergebnis == ["zentrale"], (
    f"weg_aus(vorgaenger, 'zentrale', 'zentrale') ergibt {kurz(ergebnis)}, erwartet war ['zentrale'].\n"
    "Tipp: Der Weg vom Start zu sich selbst besteht nur aus dem Start."
)

# weg_aus: ein nicht erreichbares Ziel
ergebnis = wert_von(weg_aus, VORGAENGER, "zentrale", "lager")
assert ergebnis is None, (
    f"weg_aus(vorgaenger, 'zentrale', 'lager') ergibt {kurz(ergebnis)}, erwartet war None, "
    "weil lager nicht in vorgaenger steht."
)

# route: das Beispiel
ergebnis = wert_von(route, NETZ, "zentrale", "rz")
assert ergebnis == (20, ["zentrale", "nord", "rz"]), (
    f"route(netz, 'zentrale', 'rz') ergibt {kurz(ergebnis)}, erwartet war (20, ['zentrale', 'nord', 'rz']).\n"
    "Tipp: kosten, vorgaenger = dijkstra(netz, start), dann return kosten[ziel], weg_aus(vorgaenger, start, ziel)."
)

# route: ein anderes Ziel von einem anderen Start
ergebnis = wert_von(route, NETZ, "lager", "ost")
assert ergebnis == (120, ["lager", "zentrale", "sued", "ost"]), (
    f"route(netz, 'lager', 'ost') ergibt {kurz(ergebnis)}, erwartet war (120, ['lager', 'zentrale', 'sued', 'ost'])."
)

# route: ein nicht erreichbares Ziel
ergebnis = wert_von(route, NETZ, "zentrale", "lager")
assert ergebnis is None, (
    f"route(netz, 'zentrale', 'lager') ergibt {kurz(ergebnis)}, erwartet war None: Die Leitung zwischen "
    "lager und zentrale ist nur in Richtung zentrale aktiv."
)

# route: Ziel und Start sind gleich
ergebnis = wert_von(route, NETZ, "rz", "rz")
assert ergebnis == (0, ["rz"]), f"route(netz, 'rz', 'rz') ergibt {kurz(ergebnis)}, erwartet war (0, ['rz'])."

# route: ein Start, der nicht im Netz vorkommt
ergebnis = wert_von(route, NETZ, "drucker", "zentrale")
assert ergebnis is None, f"route(netz, 'drucker', 'zentrale') ergibt {kurz(ergebnis)}, erwartet war None."

# route: bei gleich teuren Wegen ist jeder richtig
netz = {"a": {"b": 2, "c": 1}, "b": {"d": 2}, "c": {"e": 1}, "e": {"d": 2}}
fehler = fehler_im_weg(netz, "a", "d", wert_von(route, netz, "a", "d"), 4)
assert fehler is None, f"Für {netz} gibt es zwei Wege von a nach d mit Kosten 4.\nroute(netz, 'a', 'd') {fehler}"

# dijkstra benutzt heapq
assert verwendet("heappop") and verwendet("heappush"), (
    "dijkstra soll den günstigsten offenen Router mit heapq.heappop holen und neue Einträge mit "
    "heapq.heappush in den Heap legen (siehe Hintergrund)."
)

# Die Ausgabe des Programms
erwartet = (
    "[('nord', 10), ('ost', 20), ('rz', 20), ('sued', 10), ('zentrale', 0)]\n"
    "(20, ['zentrale', 'nord', 'rz'])\n(120, ['lager', 'zentrale', 'sued', 'ost'])\nNone"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Netze gegen eine langsame Vergleichslösung
zufall = Zufall(4075)
for _ in range(300):
    netz = zufallsnetz(zufall, zufall.randint(2, 8), zufall.randint(0, 14), zufall.choice([3, 20]))
    start = f"r{zufall.randint(0, 8)}"
    ziel = f"r{zufall.randint(0, 8)}"
    erwartet = vergleich_kosten(netz, start)
    ergebnis = wert_von(dijkstra, netz, start)
    assert teil(ergebnis, 0) == erwartet, (
        f"Für netz = {netz}\nergibt dijkstra(netz, {start!r}) als kosten {kurz(teil(ergebnis, 0))},\nerwartet war {erwartet}."
    )
    fehler = fehler_im_vorgaenger(netz, start, erwartet, teil(ergebnis, 1))
    assert fehler is None, f"Für netz = {netz}\nund dijkstra(netz, {start!r}): {fehler}"
    ergebnis = wert_von(route, netz, start, ziel)
    if ziel in erwartet:
        fehler = fehler_im_weg(netz, start, ziel, ergebnis, erwartet[ziel])
        assert fehler is None, f"Für netz = {netz}\nroute(netz, {start!r}, {ziel!r}) {fehler}"
    else:
        assert ergebnis is None, (
            f"Für netz = {netz}\nergibt route(netz, {start!r}, {ziel!r}) {kurz(ergebnis)}, erwartet war None."
        )

# Obere Grenze: 10 000 Router und 50 000 Leitungen
netz = zufallsnetz(zufall, 10000, 50000, 65535)
ergebnis = wert_von(dijkstra, netz, "r0")
kosten = teil(ergebnis, 0)
vorgaenger = teil(ergebnis, 1)
fehler = None
if not isinstance(kosten, dict) or kosten.get("r0") != 0:
    fehler = f"dijkstra ergibt {kurz(ergebnis)}."
else:
    for von, nachbarn in netz.items():
        for nach, leitung in nachbarn.items():
            if von in kosten and (nach not in kosten or kosten[von] + leitung < kosten[nach]):
                fehler = (
                    f"kosten[{nach!r}] ist {kosten.get(nach)}, aber über {von!r} (kosten {kosten[von]}, "
                    f"Leitung {leitung}) ginge es billiger."
                )
                break
        if fehler:
            break
if fehler is None:
    fehler = fehler_im_vorgaenger(netz, "r0", kosten, vorgaenger)
assert fehler is None, f"Bei {leitungszahl(netz)} Leitungen und dijkstra(netz, 'r0'): {fehler}"

# Laufzeit: der günstigste offene Router kommt aus dem Heap
netz = sternnetz(Zufall(75), 800)
grenze = 40 * (routerzahl(netz) + leitungszahl(netz))
try:
    _, schritte = zaehle_schritte(dijkstra, netz, "start")
except Exception as fehler:
    schritte = f"(Abbruch: {type(fehler).__name__}: {fehler})"
assert isinstance(schritte, int) and schritte <= grenze, (
    f"Für ein Netz mit {routerzahl(netz)} Routern und {leitungszahl(netz)} Leitungen braucht dijkstra {schritte} "
    f"Schritte, erlaubt sind 40 · ({routerzahl(netz)} + {leitungszahl(netz)}) = {grenze}.\n"
    "Tipp: Durchsuchen Sie nicht in jeder Runde alle offenen Router (das sind O(Router²) Schritte), sondern "
    "holen Sie den günstigsten mit heapq.heappop aus dem Heap."
)

# Laufzeit: veraltete Einträge im Heap werden übersprungen
anzahl = 300
netz = {"start": {}, "knoten": {}}
for nummer in range(1, anzahl + 1):
    netz["start"][f"a{nummer}"] = nummer
    netz[f"a{nummer}"] = {"knoten": 2 * anzahl - 2 * nummer + 1}
    netz["knoten"][f"b{nummer}"] = 1
grenze = 40 * (routerzahl(netz) + leitungszahl(netz))
try:
    _, schritte = zaehle_schritte(dijkstra, netz, "start")
except Exception as fehler:
    schritte = f"(Abbruch: {type(fehler).__name__}: {fehler})"
assert isinstance(schritte, int) and schritte <= grenze, (
    f"Im Netz, in dem der Router knoten {anzahl}-mal billiger wird und {anzahl} Leitungen hat, braucht dijkstra "
    f"{schritte} Schritte, erlaubt sind {grenze}.\n"
    "Tipp: Jede Verbesserung legt einen neuen Eintrag in den Heap; die alten kommen später heraus. Überspringen "
    "Sie einen Eintrag mit continue, wenn seine Kosten größer als kosten[router] sind, sonst geht knoten jedes "
    "Mal wieder alle seine Leitungen durch."
)


class Zaehlname(str):
    """Routername, der mitzählt, wie oft er in einem Dictionary oder einer Menge nachgeschlagen wird."""

    nachschlagen = 0

    def __hash__(self):
        """Zählt das Nachschlagen und gibt den Hashwert des Texts zurück."""
        Zaehlname.nachschlagen += 1
        return str.__hash__(self)


def mit_zaehlnamen(netz):
    """Ersetzt alle Routernamen im Netz durch Zaehlnamen."""
    neu = {}
    for von, nachbarn in netz.items():
        neu[Zaehlname(von)] = {Zaehlname(nach): leitung for nach, leitung in nachbarn.items()}
    return neu


# Laufzeit: auch min(…) über alle offenen Router sucht jede Runde alle durch
netz = mit_zaehlnamen(sternnetz(Zufall(75), 800))
grenze = 20 * (routerzahl(netz) + leitungszahl(netz))
Zaehlname.nachschlagen = 0
try:
    dijkstra(netz, Zaehlname("start"))
    fehler = None
except Exception as ausnahme:
    fehler = f"{type(ausnahme).__name__}: {ausnahme}"
gezaehlt = Zaehlname.nachschlagen
assert fehler is None and gezaehlt <= grenze, (
    f"Für ein Netz mit {routerzahl(netz)} Routern und {leitungszahl(netz)} Leitungen schlägt dijkstra "
    f"{gezaehlt}-mal einen Router in einem Dictionary oder einer Menge nach{f' ({fehler})' if fehler else ''}, "
    f"erlaubt sind {grenze}.\n"
    "Tipp: min(offen, key=kosten.get) geht in jeder Runde alle offenen Router durch, das sind O(Router²) "
    "Schritte; holen Sie den günstigsten mit heapq.heappop aus dem Heap."
)
