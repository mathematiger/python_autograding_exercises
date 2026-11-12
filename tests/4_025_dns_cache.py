# Automatisch erzeugt aus lehrkraft/muster/4_025_dns_cache.py - nicht von Hand ändern.
# vorlage-hash: 53c962da5f1ec7eb
# text-hash: e8266b0e7fb63eba
# thema: funktionen
# inhalt: functools.lru_cache

# aufloesen ist mit lru_cache dekoriert
assert hasattr(aufloesen, "cache_info") and hasattr(aufloesen, "cache_clear"), (
    "aufloesen hat keine Methoden cache_info und cache_clear. Dekorieren Sie die Funktion mit "
    "@lru_cache(maxsize=256) direkt über def aufloesen(name):."
)

# Der Cache behält höchstens 256 Namen
parameter = aufloesen.cache_parameters()
assert parameter["maxsize"] == 256, (
    f"aufloesen.cache_parameters() ergibt {parameter!r}, erwartet war maxsize 256.\n"
    "Tipp: Schreiben Sie @lru_cache(maxsize=256)."
)

BEISPIEL = {
    "www.firma.de": ("CNAME", "web01.firma.de"),
    "web01.firma.de": ("A", "192.0.2.10"),
    "shop.firma.de": ("CNAME", "www.firma.de"),
    "mail.firma.de": ("A", "192.0.2.25"),
}


def neu_beginnen(zone):
    """Setzt ZONE, ANFRAGEN und den Cache für den nächsten Test zurück."""
    ZONE.clear()
    ZONE.update(zone)
    ANFRAGEN.clear()
    aufloesen.cache_clear()


# Das Beispiel: CNAME-Kette wird verfolgt, jeder Name einmal angefragt
neu_beginnen(BEISPIEL)
ergebnis = aufloesen("shop.firma.de")
assert ergebnis == "192.0.2.10" and ANFRAGEN == ["shop.firma.de", "www.firma.de", "web01.firma.de"], (
    f'aufloesen("shop.firma.de") ergibt {ergebnis!r} mit den Anfragen {ANFRAGEN}, erwartet war "192.0.2.10" mit '
    "['shop.firma.de', 'www.firma.de', 'web01.firma.de'].\n"
    "Tipp: Bei einem CNAME-Eintrag rufen Sie aufloesen(wert) auf und geben dessen Ergebnis zurück."
)

# Der Zwischenschritt kommt aus dem Cache, ohne neue Anfrage
ergebnis = aufloesen("www.firma.de")
assert ergebnis == "192.0.2.10" and len(ANFRAGEN) == 3, (
    f'Nach aufloesen("shop.firma.de") ergibt aufloesen("www.firma.de") {ergebnis!r} und die Anfragen sind {ANFRAGEN}; '
    "erwartet war \"192.0.2.10\" ohne neue Anfrage.\n"
    "Tipp: Rufen Sie für den CNAME-Eintrag die dekorierte Funktion aufloesen auf, dann wird auch der "
    "Zwischenschritt gemerkt."
)

# trefferquote aus dem Beispiel: 1 Treffer bei 4 Aufrufen
ergebnis = trefferquote()
assert isinstance(ergebnis, float) and abs(ergebnis - 0.25) < 1e-9, (
    f"Nach aufloesen('shop.firma.de') und aufloesen('www.firma.de') ergibt trefferquote() {ergebnis!r}, "
    "erwartet war 0.25 (1 Treffer bei 4 Aufrufen, die rekursiven mitgezählt).\n"
    "Tipp: aufloesen.cache_info() liefert hits und misses; die Quote ist hits / (hits + misses)."
)

# eintrag_aendern leert den Cache, die neue Adresse kommt heraus
eintrag_aendern("web01.firma.de", ("A", "192.0.2.99"))
ergebnis = (aufloesen("shop.firma.de"), ZONE.get("web01.firma.de"))
assert ergebnis == ("192.0.2.99", ("A", "192.0.2.99")), (
    f'Nach eintrag_aendern("web01.firma.de", ("A", "192.0.2.99")) ergeben aufloesen("shop.firma.de") und '
    f'ZONE["web01.firma.de"] {ergebnis!r}, erwartet war ("192.0.2.99", ("A", "192.0.2.99")).\n'
    "Tipp: Rufen Sie nach der Änderung aufloesen.cache_clear() auf, sonst kommt die alte Adresse aus dem Cache."
)

# Ohne Aufrufe ist die Trefferquote 0.0
neu_beginnen(BEISPIEL)
ergebnis = trefferquote()
assert ergebnis == 0.0, (
    f"Direkt nach cache_clear() ergibt trefferquote() {ergebnis!r}, erwartet war 0.0.\n"
    "Tipp: Ohne Aufrufe sind hits + misses gleich 0; teilen Sie dann nicht, sondern geben Sie 0.0 zurück."
)

# eintrag_aendern beginnt auch die Zählung neu
aufloesen("mail.firma.de")
aufloesen("mail.firma.de")
eintrag_aendern("neu.firma.de", ("A", "192.0.2.77"))
ergebnis = (trefferquote(), aufloesen("neu.firma.de"))
assert ergebnis == (0.0, "192.0.2.77"), (
    f"Nach zwei Aufrufen und eintrag_aendern ergeben trefferquote() und aufloesen('neu.firma.de') {ergebnis!r}, "
    "erwartet war (0.0, '192.0.2.77')."
)

# Unbekannte Namen ergeben None, auch am Ende einer Kette, und None wird gemerkt
neu_beginnen({"alt.firma.de": ("CNAME", "weg.firma.de")})
ergebnis = (aufloesen("gibtsnicht.de"), aufloesen("alt.firma.de"), aufloesen("gibtsnicht.de"))
assert ergebnis == (None, None, None) and ANFRAGEN == ["gibtsnicht.de", "alt.firma.de", "weg.firma.de"], (
    f"aufloesen für einen unbekannten Namen, einen CNAME auf einen unbekannten Namen und noch einmal den "
    f"unbekannten ergibt {ergebnis!r} mit den Anfragen {ANFRAGEN}; erwartet war (None, None, None) mit "
    "['gibtsnicht.de', 'alt.firma.de', 'weg.firma.de']."
)

# Ein Eintrag wird mit None entfernt, auch einer, den es gar nicht gibt
neu_beginnen(BEISPIEL)
aufloesen("mail.firma.de")
eintrag_aendern("mail.firma.de", None)
eintrag_aendern("nie.firma.de", None)
ergebnis = (aufloesen("mail.firma.de"), "mail.firma.de" in ZONE)
assert ergebnis == (None, False), (
    f'Nach eintrag_aendern("mail.firma.de", None) ergeben aufloesen("mail.firma.de") und "mail.firma.de" in ZONE '
    f"{ergebnis!r}, erwartet war (None, False).\n"
    "Tipp: Entfernen Sie den Namen mit ZONE.pop(name, None); das geht auch, wenn er fehlt."
)

# Wird der Cache voll, fliegt der am längsten nicht gebrauchte Name heraus
zone = {}
for nummer in range(300):
    zone[f"pc{nummer}.firma.de"] = ("A", f"10.0.{nummer // 256}.{nummer % 256}")
neu_beginnen(zone)
for nummer in range(300):
    aufloesen(f"pc{nummer}.firma.de")
anzahl_vorher = len(ANFRAGEN)
aufloesen("pc299.firma.de")
aufloesen("pc0.firma.de")
neue = ANFRAGEN[anzahl_vorher:]
assert neue == ["pc0.firma.de"], (
    "Nach 300 verschiedenen Namen und dann pc299 und pc0 erwartet: pc299 kommt aus dem Cache, pc0 wurde "
    f"verdrängt und muss neu angefragt werden; neue Anfragen: {neue}.\n"
    "Tipp: Mit maxsize=256 behält der Cache nur die 256 zuletzt gebrauchten Namen."
)


# Vergleichslösung: Kette in einer Schleife verfolgen
def aufloesen_von_hand(zone, name):
    """Folgt den CNAME-Einträgen mit einer Schleife; liefert Adresse und die Liste der besuchten Namen."""
    besucht = []
    while True:
        besucht.append(name)
        eintrag = zone.get(name)
        if eintrag is None:
            return None, besucht
        if eintrag[0] == "A":
            return eintrag[1], besucht
        name = eintrag[1]


# 100 zufällige Zonen mit Ketten und je 30 Anfragen
zufall = Zufall(4025)
for _ in range(100):
    namen = [f"h{nummer}.netz.de" for nummer in range(zufall.randint(1, 40))]
    zone = {}
    for stelle, name in enumerate(namen):
        wurf = zufall.random()
        if wurf < 0.15:
            continue
        if wurf < 0.6 or stelle == 0:
            zone[name] = ("A", f"198.51.100.{stelle}")
        else:
            # Ein CNAME zeigt nur auf einen Namen mit kleinerer Nummer oder einen unbekannten: kein Kreis
            ziel = zufall.choice(namen[:stelle] + ["fehlt.netz.de"])
            zone[name] = ("CNAME", ziel)
    neu_beginnen(zone)
    schon_angefragt = set()
    for _ in range(30):
        name = zufall.choice(namen)
        vorher = len(ANFRAGEN)
        ergebnis = aufloesen(name)
        erwartet, besucht = aufloesen_von_hand(zone, name)
        neu_erwartet = []
        for besuchter in besucht:
            if besuchter in schon_angefragt:
                break
            neu_erwartet.append(besuchter)
            schon_angefragt.add(besuchter)
        assert ergebnis == erwartet, f"In der Zone {zone} ergibt aufloesen({name!r}) {ergebnis!r}, erwartet war {erwartet!r}."
        assert ANFRAGEN[vorher:] == neu_erwartet, (
            f"In der Zone {zone} fragt aufloesen({name!r}) die Namen {ANFRAGEN[vorher:]} an, erwartet waren "
            f"{neu_erwartet} (jeder Name nur beim ersten Mal)."
        )

# Obere Grenze: 10 000 Einträge, Kette der Länge 100
zone = {}
for nummer in range(10000):
    zone[f"n{nummer}.de"] = ("A", f"203.0.113.{nummer % 256}")
for nummer in range(1, 100):
    zone[f"alias{nummer}.de"] = ("CNAME", f"alias{nummer - 1}.de")
zone["alias0.de"] = ("CNAME", "n42.de")
neu_beginnen(zone)
ergebnis = (aufloesen("alias99.de"), len(ANFRAGEN), aufloesen("alias50.de"), len(ANFRAGEN))
assert ergebnis == ("203.0.113.42", 101, "203.0.113.42", 101), (
    "Bei einer Kette alias99 → alias98 → … → alias0 → n42 ergeben aufloesen('alias99.de'), die Zahl der Anfragen, "
    f"aufloesen('alias50.de') und wieder die Zahl der Anfragen {ergebnis!r}, erwartet war "
    "('203.0.113.42', 101, '203.0.113.42', 101)."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "192.0.2.10\n['shop.firma.de', 'www.firma.de', 'web01.firma.de']\n192.0.2.10\n0.25\n192.0.2.99"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
