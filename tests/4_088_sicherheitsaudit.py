# Automatisch erzeugt aus lehrkraft/muster/4_088_sicherheitsaudit.py - nicht von Hand ändern.
# vorlage-hash: 4ff63dbb92c32ef1
# text-hash: 298044f41a99ca80
# thema: algorithmen
# inhalt: Übung: Graphen

import copy

HOSTS = ["web", "db", "mail", "pc-01", "pc-02", "drucker", "backup"]
FREIGABEN = [("web", "db"), ("pc-01", "mail"), ("pc-02", "pc-01"), ("db", "backup")]
NETZ = {
    "internet": {"web": 3, "mail": 5, "vpn": 8},
    "web": {"db": 6, "mail": 2},
    "mail": {"pc-01": 1},
    "pc-01": {"db": 4, "backup": 9},
    "vpn": {"db": 2},
    "db": {"backup": 1},
}
UPDATES = {
    "kernel-6.8": [],
    "openssl-3.2": ["kernel-6.8"],
    "openssh-9.6": ["openssl-3.2"],
    "nginx-1.25": ["openssl-3.2"],
    "firmware-2.1": [],
}


def rufe(aufruf):
    """Führt aufruf() aus; liefert (Ergebnis, Fehlertext oder None)."""
    try:
        return aufruf(), None
    except Exception as fehler:
        return None, f"{type(fehler).__name__}: {fehler}"


def absturz(fehler):
    """Ergänzt eine Meldung um den Fehlertext, falls es einen gab."""
    return f"\nDer Aufruf löst {fehler} aus." if fehler else ""


def kurz(wert):
    """Kürzt lange Werte für Fehlermeldungen."""
    text = repr(wert)
    return text if len(text) <= 300 else text[:300] + " …"


def segmente_vergleich(hosts, freigaben):
    """Vergleichslösung: Breitensuche über die Freigaben."""
    nachbarn = {host: [] for host in hosts}
    for a, b in freigaben:
        nachbarn[a].append(b)
        nachbarn[b].append(a)
    gesehen = set()
    ergebnis = []
    for host in hosts:
        if host in gesehen:
            continue
        gesehen.add(host)
        gruppe, offen = [], [host]
        while offen:
            aktuell = offen.pop()
            gruppe.append(aktuell)
            for nachbar in nachbarn[aktuell]:
                if nachbar not in gesehen:
                    gesehen.add(nachbar)
                    offen.append(nachbar)
        ergebnis.append(sorted(gruppe))
    return sorted(ergebnis)


def aufwand_vergleich(netz, start, ziel):
    """Vergleichslösung nach Bellman und Ford: verbessert so lange über alle Verbindungen, bis sich nichts mehr ändert."""
    aufwand = {start: 0}
    geaendert = True
    while geaendert:
        geaendert = False
        for host, nachbarn in netz.items():
            if host not in aufwand:
                continue
            for nachbar, schritt in nachbarn.items():
                if nachbar not in aufwand or aufwand[host] + schritt < aufwand[nachbar]:
                    aufwand[nachbar] = aufwand[host] + schritt
                    geaendert = True
    return aufwand.get(ziel)


def wegfehler(netz, start, ziel, ergebnis):
    """Beschreibt, was an einem Ergebnis (aufwand, weg) nicht stimmt, oder gibt None zurück."""
    erwartet = aufwand_vergleich(netz, start, ziel)
    if erwartet is None:
        return None if ergebnis is None else f"Erwartet war None, {ziel!r} ist von {start!r} aus nicht erreichbar."
    if not isinstance(ergebnis, tuple) or len(ergebnis) != 2 or not isinstance(ergebnis[1], list):
        return f"Erwartet war ein Paar (aufwand, weg) mit dem Aufwand {erwartet}."
    aufwand, weg = ergebnis
    if not weg or weg[0] != start or weg[-1] != ziel:
        return f"Der Weg muss mit {start!r} beginnen und mit {ziel!r} enden."
    for von, nach in zip(weg, weg[1:]):
        if nach not in netz.get(von, {}):
            return f"Im Weg folgt {nach!r} auf {von!r}, aber von {von!r} führt keine Verbindung nach {nach!r}."
    summe = sum(netz[von][nach] for von, nach in zip(weg, weg[1:]))
    if summe != aufwand:
        return f"Die Verbindungen des Wegs kosten zusammen {summe}, zurückgegeben wurde aber der Aufwand {aufwand}."
    if aufwand != erwartet:
        return f"Der Weg kostet {aufwand}, der billigste kostet aber {erwartet}."
    return None


def reihenfolge_vergleich(updates):
    """Vergleichslösung: sucht immer wieder das alphabetisch erste Update, dessen Voraussetzungen fertig sind."""
    fertig = []
    erledigt = set()
    while True:
        bereit = [u for u in updates if u not in erledigt and all(v in erledigt for v in updates[u])]
        if not bereit:
            break
        naechstes = min(bereit)
        fertig.append(naechstes)
        erledigt.add(naechstes)
    return fertig, sorted(u for u in updates if u not in erledigt)


def ring_meldung(updates):
    """Ruft einspielreihenfolge auf; liefert (ausgelöster ValueError oder None, anderes Ergebnis, Fehlertext)."""
    try:
        return None, einspielreihenfolge(updates), None
    except ValueError as fehler:
        return fehler, None, None
    except Exception as fehler:
        return None, None, f"{type(fehler).__name__}: {fehler}"


def zufallsnetz(zufall, anzahl, verbindungen):
    """Erzeugt ein zufälliges gerichtetes Netz mit Hosts h0 … h<anzahl-1>."""
    netz = {}
    for _ in range(verbindungen):
        von, nach = zufall.randrange(anzahl), zufall.randrange(anzahl)
        if von != nach:
            netz.setdefault(f"h{von}", {})[f"h{nach}"] = zufall.randint(1, 20)
    return netz


def zufallsupdates(zufall, anzahl, ring):
    """Erzeugt zufällige Updates u00 …; Voraussetzungen zeigen nach vorn, mit ring=True kommt vielleicht eine zurück."""
    namen = [f"u{nummer:02d}" for nummer in zufall.sample(range(100), anzahl)]
    updates = {}
    for position, name in enumerate(namen):
        updates[name] = zufall.sample(namen[:position], zufall.randint(0, min(3, position)))
    if ring and anzahl >= 2:
        frueh, spaet = sorted(zufall.sample(range(anzahl), 2))
        if namen[spaet] not in updates[namen[frueh]]:
            updates[namen[frueh]].append(namen[spaet])
    return updates


# segmente: das Beispiel
ergebnis, fehler = rufe(lambda: segmente(list(HOSTS), list(FREIGABEN)))
erwartet = [["backup", "db", "web"], ["drucker"], ["mail", "pc-01", "pc-02"]]
assert ergebnis == erwartet, (
    f"segmente(hosts, freigaben) im Beispiel ergibt {ergebnis!r}, erwartet war {erwartet!r}." + absturz(fehler)
    + "\nTipp: Vereinigen Sie für jede Freigabe die Gruppen beider Hosts und sammeln Sie am Ende die Hosts nach ihrer "
    "Wurzel."
)

# segmente: andere Hosts (nicht fest hinschreiben!)
hosts = ["srv-a", "srv-b", "srv-c", "srv-d"]
ergebnis, fehler = rufe(lambda: segmente(hosts, [("srv-d", "srv-a"), ("srv-c", "srv-b")]))
assert ergebnis == [["srv-a", "srv-d"], ["srv-b", "srv-c"]], (
    f"segmente({hosts}, [('srv-d', 'srv-a'), ('srv-c', 'srv-b')]) ergibt {ergebnis!r}, erwartet war "
    "[['srv-a', 'srv-d'], ['srv-b', 'srv-c']]." + absturz(fehler)
)

# segmente: über eine Kette von Freigaben gehört alles zusammen
hosts = ["e", "d", "c", "b", "a"]
freigaben = [("a", "b"), ("c", "d"), ("e", "d"), ("b", "c")]
ergebnis, fehler = rufe(lambda: segmente(hosts, freigaben))
assert ergebnis == [["a", "b", "c", "d", "e"]], (
    f"segmente({hosts}, {freigaben}) ergibt {ergebnis!r}, erwartet war [['a', 'b', 'c', 'd', 'e']]: Die letzte "
    "Freigabe verbindet zwei Segmente.\nTipp: Hängen Sie die Wurzel unter die andere Wurzel, nicht nur den Host."
    + absturz(fehler)
)

# segmente: ohne Freigaben ist jeder Host allein, auch eine Freigabe von einem Host zu sich selbst ändert nichts
ergebnis, fehler = rufe(lambda: (segmente(["web"], []), segmente(["db", "web"], [("web", "web")])))
assert ergebnis == ([["web"]], [["db"], ["web"]]), (
    f"segmente(['web'], []) und segmente(['db', 'web'], [('web', 'web')]) ergeben {ergebnis!r}, erwartet war "
    "([['web']], [['db'], ['web']])." + absturz(fehler)
)

# segmente: hosts und freigaben bleiben unverändert
hosts, freigaben = list(HOSTS), list(FREIGABEN)
rufe(lambda: segmente(hosts, freigaben))
assert hosts == HOSTS and freigaben == FREIGABEN, (
    f"Nach segmente ist hosts {hosts!r} und freigaben {freigaben!r}; beide sollen unverändert bleiben."
)

# billigster_angriff: der Aufwand im Beispiel
ergebnis, fehler = rufe(lambda: billigster_angriff(copy.deepcopy(NETZ), "internet", "db"))
aufwand = ergebnis[0] if isinstance(ergebnis, tuple) and ergebnis else ergebnis
assert aufwand == 9, (
    f"billigster_angriff(netz, 'internet', 'db') ergibt {ergebnis!r}; erwartet war der Aufwand 9 über web.\n"
    "Tipp: Nicht der Weg mit den wenigsten Verbindungen zählt (über vpn: 10), sondern der mit dem kleinsten Aufwand."
    + absturz(fehler)
)

# billigster_angriff: der Weg im Beispiel
ergebnis, fehler = rufe(lambda: billigster_angriff(copy.deepcopy(NETZ), "internet", "db"))
assert ergebnis == (9, ["internet", "web", "db"]), (
    f"billigster_angriff(netz, 'internet', 'db') ergibt {ergebnis!r}, erwartet war (9, ['internet', 'web', 'db']).\n"
    "Tipp: Merken Sie sich beim Verbessern in vorgaenger, von wo aus ein Host erreicht wurde, und drehen Sie den Weg "
    "am Ende um." + absturz(fehler)
)

# billigster_angriff: ein anderes Ziel, der Weg geht über mehrere Hosts
ergebnis, fehler = rufe(lambda: billigster_angriff(copy.deepcopy(NETZ), "internet", "backup"))
assert ergebnis == (10, ["internet", "web", "db", "backup"]), (
    f"billigster_angriff(netz, 'internet', 'backup') ergibt {ergebnis!r}, erwartet war "
    "(10, ['internet', 'web', 'db', 'backup'])." + absturz(fehler)
)

# billigster_angriff: ein Umweg über mehr Hosts kann billiger sein
ergebnis, fehler = rufe(lambda: billigster_angriff(copy.deepcopy(NETZ), "web", "pc-01"))
assert ergebnis == (3, ["web", "mail", "pc-01"]), (
    f"billigster_angriff(netz, 'web', 'pc-01') ergibt {ergebnis!r}, erwartet war (3, ['web', 'mail', 'pc-01'])."
    + absturz(fehler)
)

# billigster_angriff: Verbindungen gelten nur in einer Richtung
ergebnis, fehler = rufe(lambda: billigster_angriff(copy.deepcopy(NETZ), "db", "internet"))
assert fehler is None and ergebnis is None, (
    f"billigster_angriff(netz, 'db', 'internet') ergibt {ergebnis!r}, erwartet war None: Von db führt nur eine "
    "Verbindung zu backup, und backup hat keine eigenen Verbindungen." + absturz(fehler)
)

# billigster_angriff: Start gleich Ziel, auch wenn der Host nicht in netz steht
ergebnis, fehler = rufe(lambda: (billigster_angriff(copy.deepcopy(NETZ), "web", "web"), billigster_angriff({}, "nas", "nas")))
assert ergebnis == ((0, ["web"]), (0, ["nas"])), (
    f"billigster_angriff(netz, 'web', 'web') und billigster_angriff({{}}, 'nas', 'nas') ergeben {ergebnis!r}, "
    "erwartet war ((0, ['web']), (0, ['nas']))." + absturz(fehler)
)

# billigster_angriff: ein Start, der nicht in netz steht
ergebnis, fehler = rufe(lambda: billigster_angriff(copy.deepcopy(NETZ), "laptop", "db"))
assert fehler is None and ergebnis is None, (
    f"billigster_angriff(netz, 'laptop', 'db') ergibt {ergebnis!r}, erwartet war None: laptop hat keine Verbindungen."
    + absturz(fehler) + "\nTipp: netz.get(host, {}) liefert für Hosts ohne eigene Verbindungen ein leeres Dictionary."
)

# billigster_angriff: netz bleibt unverändert
netz = copy.deepcopy(NETZ)
rufe(lambda: billigster_angriff(netz, "internet", "backup"))
assert netz == NETZ, f"Nach billigster_angriff ist netz {netz!r}; es soll unverändert bleiben."

# einspielreihenfolge: das Beispiel
ergebnis, fehler = rufe(lambda: einspielreihenfolge(copy.deepcopy(UPDATES)))
erwartet = ["firmware-2.1", "kernel-6.8", "openssl-3.2", "nginx-1.25", "openssh-9.6"]
assert ergebnis == erwartet, (
    f"einspielreihenfolge(updates) im Beispiel ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Legen Sie die Updates, deren Voraussetzungen alle eingespielt sind, in einen Heap und nehmen Sie mit "
    "heappop immer das alphabetisch erste." + absturz(fehler)
)

# einspielreihenfolge: jedes Update steht hinter seinen Voraussetzungen
updates = {"z-agent": [], "y-db": ["z-agent"], "x-app": ["y-db"]}
ergebnis, fehler = rufe(lambda: einspielreihenfolge(updates))
assert ergebnis == ["z-agent", "y-db", "x-app"], (
    f"einspielreihenfolge({updates}) ergibt {ergebnis!r}, erwartet war ['z-agent', 'y-db', 'x-app']: Alphabetisch "
    "entscheidet nur zwischen Updates, die gerade dürfen." + absturz(fehler)
)

# einspielreihenfolge: ein neu bereites Update kann vor älteren bereiten drankommen
updates = {"b-base": [], "z-tool": [], "a-patch": ["b-base"]}
ergebnis, fehler = rufe(lambda: einspielreihenfolge(updates))
assert ergebnis == ["b-base", "a-patch", "z-tool"], (
    f"einspielreihenfolge({updates}) ergibt {ergebnis!r}, erwartet war ['b-base', 'a-patch', 'z-tool']: Nach b-base "
    "darf a-patch, und das ist alphabetisch vor z-tool.\nTipp: Eine deque hält die Reihenfolge des Bereitwerdens, ein "
    "Heap liefert das alphabetisch erste." + absturz(fehler)
)

# einspielreihenfolge: keine Updates
ergebnis, fehler = rufe(lambda: einspielreihenfolge({}))
assert ergebnis == [], f"einspielreihenfolge({{}}) ergibt {ergebnis!r}, erwartet war []." + absturz(fehler)

# einspielreihenfolge: ein Ring löst einen ValueError aus
ausnahme, ergebnis, fehler = ring_meldung({"a": ["b"], "b": ["a"], "c": []})
assert ausnahme is not None, (
    f"einspielreihenfolge({{'a': ['b'], 'b': ['a'], 'c': []}}) ergibt {ergebnis!r}, erwartet war ein ValueError: a "
    "und b setzen sich gegenseitig voraus." + absturz(fehler)
)

# einspielreihenfolge: die Meldung nennt die Updates ohne Platz
ausnahme, _, _ = ring_meldung({"a-ssl": ["b-ssh"], "b-ssh": ["a-ssl"], "c-web": ["b-ssh"], "d-dns": []})
meldung = str(ausnahme)
assert ausnahme is not None and all(name in meldung for name in ["a-ssl", "b-ssh", "c-web"]) and "d-dns" not in meldung, (
    f"Bei {{'a-ssl': ['b-ssh'], 'b-ssh': ['a-ssl'], 'c-web': ['b-ssh'], 'd-dns': []}} lautet die Meldung "
    f"{meldung!r}; sie soll a-ssl, b-ssh und c-web nennen (c-web hängt am Ring), aber nicht d-dns.\nTipp: Es sind "
    "genau die Updates, deren Zähler am Ende noch nicht 0 ist."
)

# einspielreihenfolge: ein Update, das sich selbst voraussetzt
ausnahme, ergebnis, fehler = ring_meldung({"kernel": ["kernel"]})
assert ausnahme is not None and "kernel" in str(ausnahme), (
    f"einspielreihenfolge({{'kernel': ['kernel']}}) ergibt {ergebnis!r}, erwartet war ein ValueError, der kernel "
    f"nennt; Meldung: {str(ausnahme)!r}." + absturz(fehler)
)

# einspielreihenfolge: updates bleibt unverändert
updates = copy.deepcopy(UPDATES)
rufe(lambda: einspielreihenfolge(updates))
assert updates == UPDATES, f"Nach einspielreihenfolge ist updates {updates!r}; es soll unverändert bleiben."

zufall = Zufall(4088)

# Viele zufällige Segmente im Vergleich mit einer Breitensuche
for _ in range(100):
    hosts = [f"h{nummer}" for nummer in zufall.sample(range(100), zufall.randint(1, 15))]
    freigaben = [(zufall.choice(hosts), zufall.choice(hosts)) for _ in range(zufall.randint(0, 15))]
    ergebnis, fehler = rufe(lambda: segmente(hosts, freigaben))
    erwartet = segmente_vergleich(hosts, freigaben)
    assert ergebnis == erwartet, (
        f"segmente({hosts}, {freigaben}) ergibt {ergebnis!r}, erwartet war {erwartet!r}." + absturz(fehler)
    )

# Viele zufällige Netze im Vergleich mit dem Verfahren von Bellman und Ford
for _ in range(100):
    anzahl = zufall.randint(1, 10)
    netz = zufallsnetz(zufall, anzahl, zufall.randint(0, 25))
    start, ziel = f"h{zufall.randrange(anzahl)}", f"h{zufall.randrange(anzahl)}"
    ergebnis, fehler = rufe(lambda: billigster_angriff(copy.deepcopy(netz), start, ziel))
    problem = f"Der Aufruf löst {fehler} aus." if fehler else wegfehler(netz, start, ziel, ergebnis)
    assert problem is None, f"billigster_angriff({netz}, {start!r}, {ziel!r}) ergibt {ergebnis!r}.\n{problem}"

# Viele zufällige Updates im Vergleich mit einer langsamen Lösung
for _ in range(100):
    updates = zufallsupdates(zufall, zufall.randint(0, 12), zufall.random() < 0.3)
    ausnahme, ergebnis, fehler = ring_meldung(copy.deepcopy(updates))
    erwartet, ohne_platz = reihenfolge_vergleich(updates)
    if ohne_platz:
        assert ausnahme is not None and all(name in str(ausnahme) for name in ohne_platz), (
            f"einspielreihenfolge({updates}) ergibt {ergebnis!r}, Meldung {str(ausnahme)!r}; erwartet war ein "
            f"ValueError, der {ohne_platz} nennt." + absturz(fehler)
        )
    else:
        assert ergebnis == erwartet, (
            f"einspielreihenfolge({updates}) ergibt {ergebnis!r}, erwartet war {erwartet!r}." + absturz(fehler)
            + ("" if ausnahme is None else f"\nEs kam ValueError({str(ausnahme)!r}), obwohl es keinen Ring gibt.")
        )


def kette(anzahl):
    """Hosts h0 … h<anzahl-1>, jeder mit dem nächsten freigegeben, dazu ein paar Querverbindungen."""
    hosts = [f"h{nummer}" for nummer in range(anzahl)]
    freigaben = [(hosts[nummer], hosts[nummer + 1]) for nummer in range(anzahl - 1)]
    freigaben += [(hosts[nummer], hosts[nummer // 2]) for nummer in range(0, anzahl, 7)]
    return hosts, freigaben


# Laufzeit: segmente wächst fast linear
_, schritte_klein = zaehle_schritte(segmente, *kette(200))
ergebnis, schritte_gross = zaehle_schritte(segmente, *kette(800))
assert isinstance(ergebnis, list) and len(ergebnis) == 1 and schritte_gross <= 6 * schritte_klein, (
    f"segmente braucht für eine Kette aus 200 Hosts {schritte_klein} Schritte, für 800 Hosts {schritte_gross}; bei "
    "fast O(Hosts + Freigaben) wäre es etwa das Vierfache.\nTipp: Nicht bei jeder Freigabe alle Hosts umnummerieren, "
    "sondern nur eine Wurzel umhängen; die kleinere Gruppe unter die größere, mit Pfadkompression."
)


def gitter(anzahl):
    """Ein Netz, in dem jeder Host vier Nachbarn hat; das Ziel ist nicht erreichbar."""
    netz = {}
    for nummer in range(anzahl):
        netz[f"h{nummer}"] = {f"h{(nummer * 7 + versatz) % anzahl}": 1 + (nummer + versatz) % 9 for versatz in (1, 2, 3, 5)}
    return netz


# Laufzeit: billigster_angriff wächst mit (Hosts + Verbindungen) · log Hosts
_, schritte_klein = zaehle_schritte(billigster_angriff, gitter(300), "h0", "nirgends")
ergebnis, schritte_gross = zaehle_schritte(billigster_angriff, gitter(1200), "h0", "nirgends")
assert ergebnis is None and schritte_gross <= 7 * schritte_klein, (
    f"billigster_angriff zu einem unerreichbaren Ziel braucht bei 300 Hosts {schritte_klein} Schritte, bei 1200 Hosts "
    f"{schritte_gross} (Ergebnis {ergebnis!r}, erwartet None); bei O((Hosts + Verbindungen) · log Hosts) wäre es "
    "etwa das Viereinhalbfache.\nTipp: Holen Sie den billigsten offenen Host mit heapq.heappop, statt ihn jedes Mal zu "
    "suchen."
)


def updatekette(anzahl):
    """Updates, von denen jedes die beiden vorigen voraussetzt."""
    namen = [f"u{nummer:05d}" for nummer in range(anzahl)]
    return {name: namen[max(0, nummer - 2):nummer] for nummer, name in enumerate(namen)}


# Laufzeit: einspielreihenfolge wächst mit (Updates + Voraussetzungen) · log Updates
_, schritte_klein = zaehle_schritte(einspielreihenfolge, updatekette(300))
ergebnis, schritte_gross = zaehle_schritte(einspielreihenfolge, updatekette(1200))
assert ergebnis == sorted(updatekette(1200)) and schritte_gross <= 6 * schritte_klein, (
    f"einspielreihenfolge braucht bei 300 Updates {schritte_klein} Schritte, bei 1200 Updates {schritte_gross}; "
    "erwartet war etwa das Vierfache.\nTipp: Zählen Sie die fehlenden Voraussetzungen und senken Sie die Zähler, statt "
    "immer wieder alle Updates durchzusehen."
)

# Obere Grenze: 100000 Hosts und 200000 Freigaben
zufall = Zufall(100_000)
hosts = [f"host-{nummer:06d}" for nummer in range(100_000)]
freigaben = [(hosts[zufall.randrange(100_000)], hosts[zufall.randrange(100_000)]) for _ in range(200_000)]
freigaben += [(hosts[nummer], hosts[nummer + 1]) for nummer in range(0, 1000)]
ergebnis, fehler = rufe(lambda: segmente(hosts, freigaben))
erwartet = segmente_vergleich(hosts, freigaben)
assert ergebnis == erwartet, (
    f"Bei 100000 Hosts und 201000 Freigaben ergibt segmente {len(ergebnis) if isinstance(ergebnis, list) else '?'} "
    f"Segmente, beginnend mit {kurz(ergebnis)[:200]}; erwartet waren {len(erwartet)} Segmente, beginnend mit "
    f"{kurz(erwartet)[:200]}." + absturz(fehler)
)

# Obere Grenze: 10000 Hosts mit 50000 Verbindungen
netz = gitter(10_000)
for nummer in range(10_000):
    netz[f"h{nummer}"][f"h{(nummer + 1) % 10_000}"] = 1000
ergebnis, fehler = rufe(lambda: billigster_angriff(netz, "h0", "h9999"))
problem = f"Der Aufruf löst {fehler} aus." if fehler else wegfehler(netz, "h0", "h9999", ergebnis)
assert problem is None, f"Bei 10000 Hosts und 50000 Verbindungen ergibt billigster_angriff(netz, 'h0', 'h9999') {kurz(ergebnis)}.\n{problem}"

# Obere Grenze: 10000 Updates mit fast 50000 Voraussetzungen
zufall = Zufall(10_000)
namen = [f"sec-{nummer:05d}" for nummer in zufall.sample(range(10_000), 10_000)]
updates = {name: zufall.sample(namen[max(0, position - 50):position], min(5, position)) for position, name in enumerate(namen)}
ergebnis, fehler = rufe(lambda: einspielreihenfolge(updates))
platz = {update: position for position, update in enumerate(ergebnis)} if isinstance(ergebnis, list) else {}
verletzt = [(u, v) for u, voraus in updates.items() for v in voraus if not (u in platz and v in platz and platz[v] < platz[u])]
assert isinstance(ergebnis, list) and len(ergebnis) == 10_000 and not verletzt and ergebnis[0] == min(u for u in updates if not updates[u]), (
    f"Bei 10000 Updates ergibt einspielreihenfolge {kurz(ergebnis)}; erwartet war eine Liste aller 10000 Updates, jedes "
    f"hinter seinen Voraussetzungen{f', aber z. B. {verletzt[0][0]} steht nicht hinter {verletzt[0][1]}' if verletzt else ''}."
    + absturz(fehler)
)
