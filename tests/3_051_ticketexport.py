# Automatisch erzeugt aus lehrkraft/muster/3_051_ticketexport.py - nicht von Hand ändern.
# vorlage-hash: 0beebf4564f71a8b
# text-hash: a23e397b3bcd2471
# thema: texte_zahlen
# inhalt: csv.reader und DictReader

BEISPIEL = (
    "nummer,betreff,prioritaet,stunden\n"
    '1041,"Drucker 2. OG, Papierstau",mittel,30\n'
    "1042,VPN bricht ab,hoch,2\n"
    '1043,"Passwort vergessen, Konto gesperrt",hoch,6\n'
    '1044,"Monitor zeigt ""kein Bild"" an",niedrig,80\n'
)
SPALTEN = ["nummer", "betreff", "prioritaet", "stunden"]


def aufruf(funktion, *argumente):
    """Ruft die Funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def als_text(kopf, zeilen):
    """Baut aus Kopfzeile und Zeilen (Listen von Feldern) einen CSV-Text, Felder mit Komma oder " in Anführungszeichen."""
    ausgabe = []
    for zeile in [kopf] + zeilen:
        teile = []
        for feld in zeile:
            if "," in feld or '"' in feld:
                feld = '"' + feld.replace('"', '""') + '"'
            teile.append(feld)
        ausgabe.append(",".join(teile))
    return "\n".join(ausgabe) + "\n"


def tickets_als_text(tickets, kopf=SPALTEN):
    """Baut aus Tickets (Dictionaries) einen CSV-Text mit den Spalten in der Reihenfolge von kopf."""
    zeilen = []
    for ticket in tickets:
        zeilen.append([ticket[spalte] for spalte in kopf])
    return als_text(kopf, zeilen)


def erwartet_ueberfaellig(tickets):
    """Vergleichslösung: rechnet direkt mit den Dictionaries, ohne CSV."""
    fristen = {"hoch": 4, "mittel": 24, "niedrig": 72}
    return [(t["nummer"], t["betreff"]) for t in tickets if int(t["stunden"]) > fristen[t["prioritaet"]]]


def ticket(nummer, betreff, prioritaet, stunden):
    """Ein Ticket als Dictionary mit Texten, so wie es im CSV steht."""
    return {"nummer": str(nummer), "betreff": betreff, "prioritaet": prioritaet, "stunden": str(stunden)}




def zeile_nummer(ergebnis, stelle):
    """Die Zeile an dieser Stelle; sonst eine Beschreibung, was stattdessen herauskam."""
    if not isinstance(ergebnis, list) or stelle >= len(ergebnis):
        return f"(keine Zeile {stelle}, felder ergab {ergebnis!r})"
    return ergebnis[stelle]


# felder im Beispiel: fünf Zeilen samt Kopfzeile
ergebnis = aufruf(felder, BEISPIEL)
assert isinstance(ergebnis, list) and len(ergebnis) == 5, (
    f"felder(text) ergibt {ergebnis!r}, erwartet war eine Liste mit 5 Zeilen (Kopfzeile und 4 Tickets).\n"
    "Tipp: for zeile in csv.reader(io.StringIO(text)): … und jede Zeile an eine Liste anhängen."
)

# felder im Beispiel: Kopfzeile und eine Zeile ohne Anführungszeichen
assert zeile_nummer(ergebnis, 0) == SPALTEN and zeile_nummer(ergebnis, 2) == ["1042", "VPN bricht ab", "hoch", "2"], (
    f"felder(text)[0] und [2] ergeben {zeile_nummer(ergebnis, 0)!r} und {zeile_nummer(ergebnis, 2)!r}, erwartet waren\n"
    f"{SPALTEN} und ['1042', 'VPN bricht ab', 'hoch', '2']."
)

# felder im Beispiel: das Komma in Anführungszeichen trennt keine Felder
assert zeile_nummer(ergebnis, 1) == ["1041", "Drucker 2. OG, Papierstau", "mittel", "30"], (
    f"felder(text)[1] ergibt {zeile_nummer(ergebnis, 1)!r}, erwartet war ['1041', 'Drucker 2. OG, Papierstau', 'mittel', '30'].\n"
    'Tipp: split(",") trennt auch am Komma im Betreff; csv.reader beachtet die Anführungszeichen.'
)

# felder im Beispiel: "" im Feld wird zu einem Anführungszeichen
assert zeile_nummer(ergebnis, 4) == ["1044", 'Monitor zeigt "kein Bild" an', "niedrig", "80"], (
    f"felder(text)[4] ergibt {zeile_nummer(ergebnis, 4)!r}, erwartet war ['1044', 'Monitor zeigt \"kein Bild\" an', 'niedrig', '80']."
)

# felder mit einem anderen Text (nicht fest hinschreiben!)
anderer = 'a,b\n"x, y",z\n1,"2"\n'
ergebnis = aufruf(felder, anderer)
assert ergebnis == [["a", "b"], ["x, y", "z"], ["1", "2"]], (
    f"felder({anderer!r}) ergibt {ergebnis!r}, erwartet war [['a', 'b'], ['x, y', 'z'], ['1', '2']]."
)

# felder überspringt leere Zeilen
mit_luecken = "a,b\n\n1,2\n\n\n3,4\n\n"
ergebnis = aufruf(felder, mit_luecken)
assert ergebnis == [["a", "b"], ["1", "2"], ["3", "4"]], (
    f"felder({mit_luecken!r}) ergibt {ergebnis!r}, erwartet war [['a', 'b'], ['1', '2'], ['3', '4']].\n"
    "Tipp: csv.reader liefert für eine leere Zeile die leere Liste []; hängen Sie sie nicht an."
)

# felder: letzte Zeile ohne Zeilenumbruch
ergebnis = aufruf(felder, "a,b\n1,2")
assert ergebnis == [["a", "b"], ["1", "2"]], f"felder('a,b\\n1,2') ergibt {ergebnis!r}, erwartet war [['a', 'b'], ['1', '2']]."

# felder: nur die Kopfzeile
ergebnis = aufruf(felder, "nummer,betreff,prioritaet,stunden\n")
assert ergebnis == [SPALTEN], f"felder bei nur einer Kopfzeile ergibt {ergebnis!r}, erwartet war [{SPALTEN}]."

# ueberfaellige im Beispiel: drei Tickets
ergebnis = aufruf(ueberfaellige, BEISPIEL)
assert isinstance(ergebnis, list) and len(ergebnis) == 3, (
    f"ueberfaellige(text) ergibt {ergebnis!r}, erwartet waren 3 Tickets (1041, 1043, 1044).\n"
    'Tipp: csv.DictReader gibt jede Zeile als Dictionary; vergleichen Sie int(ticket["stunden"]) mit '
    'FRISTEN[ticket["prioritaet"]].'
)

# ueberfaellige im Beispiel: Paare (nummer, betreff)
erwartet = [
    ("1041", "Drucker 2. OG, Papierstau"),
    ("1043", "Passwort vergessen, Konto gesperrt"),
    ("1044", 'Monitor zeigt "kein Bild" an'),
]
assert ergebnis == erwartet, f"ueberfaellige(text) ergibt {ergebnis!r},\nerwartet war {erwartet}."

# ueberfaellige: andere Tickets (nicht fest hinschreiben!)
tickets = [ticket(7, "Maus defekt", "niedrig", 73), ticket(8, "Server down", "hoch", 3), ticket(9, "Neuer Laptop", "mittel", 25)]
ergebnis = aufruf(ueberfaellige, tickets_als_text(tickets))
assert ergebnis == erwartet_ueberfaellig(tickets), (
    f"Für\n{tickets_als_text(tickets)}ergibt ueberfaellige {ergebnis!r}, erwartet war {erwartet_ueberfaellig(tickets)}."
)

# ueberfaellige: Spalten in anderer Reihenfolge
kopf = ["stunden", "prioritaet", "nummer", "betreff"]
text = tickets_als_text(tickets, kopf)
ergebnis = aufruf(ueberfaellige, text)
assert ergebnis == erwartet_ueberfaellig(tickets), (
    f"Für\n{text}ergibt ueberfaellige {ergebnis!r}, erwartet war {erwartet_ueberfaellig(tickets)}.\n"
    "Tipp: Mit csv.DictReader greifen Sie über den Spaltennamen zu, egal an welcher Stelle die Spalte steht."
)

# ueberfaellige: genau an der Frist ist ein Ticket noch nicht überfällig
tickets = [ticket(1, "a", "hoch", 4), ticket(2, "b", "mittel", 24), ticket(3, "c", "niedrig", 72), ticket(4, "d", "hoch", 5)]
ergebnis = aufruf(ueberfaellige, tickets_als_text(tickets))
assert ergebnis == [("4", "d")], (
    f"Bei Tickets genau an der Frist (4, 24, 72 Stunden) und einem mit 5 Stunden bei hoch ergibt ueberfaellige "
    f"{ergebnis!r}, erwartet war [('4', 'd')].\nTipp: „länger als die Frist“ heißt > und nicht >=."
)

# ueberfaellige: stunden als Zahl vergleichen, nicht als Text
tickets = [ticket(1, "a", "mittel", 100), ticket(2, "b", "mittel", 3)]
ergebnis = aufruf(ueberfaellige, tickets_als_text(tickets))
assert ergebnis == [("1", "a")], (
    f"Bei 100 und 3 Stunden (mittel) ergibt ueberfaellige {ergebnis!r}, erwartet war [('1', 'a')].\n"
    'Tipp: Als Text ist "100" < "24"; wandeln Sie stunden mit int um.'
)

# ueberfaellige: leere Zeilen zwischen den Tickets
text = "nummer,betreff,prioritaet,stunden\n\n1,x,hoch,9\n\n"
ergebnis = aufruf(ueberfaellige, text)
assert ergebnis == [("1", "x")], f"ueberfaellige({text!r}) ergibt {ergebnis!r}, erwartet war [('1', 'x')]."

# ueberfaellige: Randfall ohne Tickets
ergebnis = aufruf(ueberfaellige, "nummer,betreff,prioritaet,stunden\n")
assert ergebnis == [], f"Ohne Tickets ergibt ueberfaellige {ergebnis!r}, erwartet war []."

# ueberfaellige: Randfall 0 Stunden
ergebnis = aufruf(ueberfaellige, "nummer,betreff,prioritaet,stunden\n5,neu,hoch,0")
assert ergebnis == [], f"Bei einem Ticket mit 0 Stunden ergibt ueberfaellige {ergebnis!r}, erwartet war []."

zufall = Zufall(3051)
woerter = ["Drucker", "VPN", "Konto", "Mail", "Monitor", "Ärger", ",", '"', "kein Bild", "WLAN, OG"]
exporte = []
for _ in range(200):
    tickets = []
    for nummer in range(zufall.randint(0, 8)):
        betreff = " ".join(zufall.choice(woerter) for _ in range(zufall.randint(1, 4)))
        tickets.append(ticket(nummer, betreff, zufall.choice(["hoch", "mittel", "niedrig"]), zufall.randint(0, 100)))
    kopf = zufall.sample(SPALTEN, 4)
    exporte.append((tickets, kopf, tickets_als_text(tickets, kopf)))

# Viele zufällige Exporte mit Kommas und Anführungszeichen: felder
for tickets, kopf, text in exporte:
    zeilen = [kopf] + [[t[spalte] for spalte in kopf] for t in tickets]
    ergebnis = aufruf(felder, text)
    assert ergebnis == zeilen, f"felder({text!r})\nergibt   {ergebnis!r}\nerwartet {zeilen}"

# Viele zufällige Exporte mit Kommas und Anführungszeichen: ueberfaellige
for tickets, kopf, text in exporte:
    ergebnis = aufruf(ueberfaellige, text)
    assert ergebnis == erwartet_ueberfaellig(tickets), (
        f"ueberfaellige({text!r})\nergibt   {ergebnis!r}\nerwartet {erwartet_ueberfaellig(tickets)}"
    )

# Obere Grenze: 10 000 Tickets
tickets = [ticket(n, f"Fall {n}, Teil {n % 7}", zufall.choice(["hoch", "mittel", "niedrig"]), zufall.randint(0, 10000)) for n in range(10000)]
text = tickets_als_text(tickets)
ergebnis = aufruf(ueberfaellige, text)
assert ergebnis == erwartet_ueberfaellig(tickets), "Bei 10 000 Tickets stimmt ueberfaellige nicht."
