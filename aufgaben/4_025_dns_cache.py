"""Aufgabe 4_025 – DNS-Cache                                     Stufe 4 ★★★★☆

Ein Router im Büronetz löst für alle Rechner Namen wie www.firma.de in
IPv4-Adressen auf (Namensauflösung, DNS). Dazu fragt er einen
DNS-Server. Der Server antwortet mit einem Eintrag: Entweder ein
A-Eintrag ("A", "192.0.2.10") mit der Adresse, oder ein CNAME-Eintrag
("CNAME", "web01.firma.de"), der sagt, dass der Name nur ein anderer
Name (ein Alias) für web01.firma.de ist; dann muss man diesen Namen
weiter auflösen. Kennt der Server den Namen nicht, kommt None zurück.
Jede Anfrage kostet Zeit, darum soll der Router sich die Antworten in
einem Cache merken, aber höchstens für 256 Namen, weil sein Speicher
klein ist. Im Code simuliert die vorgegebene Funktion frage_server den
Server und schreibt jede Anfrage in die Liste ANFRAGEN. Vervollständigen
Sie:

- `aufloesen(name)` gibt die IPv4-Adresse zu name zurück, folgt dabei
  CNAME-Einträgen durch einen rekursiven Aufruf von aufloesen und gibt
  None zurück, wenn ein Name auf dem Weg unbekannt ist. Dekorieren Sie
  aufloesen mit @lru_cache(maxsize=256). Auch die Antwort None wird so
  gemerkt.
- `trefferquote()` gibt den Anteil der Aufrufe von aufloesen zurück,
  die der Cache beantwortet hat (Treffer geteilt durch alle Aufrufe, auch
  die rekursiven), als Kommazahl; 0.0, solange es keinen Aufruf gab.
- `eintrag_aendern(name, eintrag)` trägt eintrag unter name in ZONE ein
  (bei eintrag None wird name aus ZONE entfernt, falls er dort steht)
  und leert danach den Cache, damit keine veralteten Adressen mehr
  herauskommen. Dabei beginnen auch die Zahlen für trefferquote neu.

    aufloesen("shop.firma.de")  →  "192.0.2.10"
    ANFRAGEN                    →  ["shop.firma.de", "www.firma.de", "web01.firma.de"]
    aufloesen("www.firma.de")   →  "192.0.2.10"    (aus dem Cache, keine neue Anfrage)
    trefferquote()              →  0.25            (1 Treffer bei 4 Aufrufen)
    eintrag_aendern("web01.firma.de", ("A", "192.0.2.99"))
    aufloesen("shop.firma.de")  →  "192.0.2.99"

Grenzen: ZONE hat 0 bis 10 000 Einträge. Namen sind nicht leere Texte,
Adressen Texte wie "192.0.2.10". Eine Kette von CNAME-Einträgen ist
höchstens 100 lang und führt nie im Kreis. Ändern darf ZONE nur
eintrag_aendern.

Hintergrund: In Aufgabe 4_024 haben Sie einen Cache-Dekorator selbst
geschrieben. Die Standardbibliothek hat einen fertigen, besseren:
functools.lru_cache. Er merkt sich zu jeder Folge von Argumenten das
Ergebnis in einem Dictionary und ruft die Funktion bei einer
Wiederholung nicht mehr auf.

    from functools import lru_cache

    @lru_cache(maxsize=2)
    def quadrat(x):
        print("rechne", x)
        return x * x

    quadrat(3)               # druckt "rechne 3", gibt 9 zurück
    quadrat(3)               # druckt nichts: Treffer im Cache
    quadrat(4); quadrat(5)   # jetzt fliegt 3 heraus (maxsize=2)
    quadrat.cache_info()     →  CacheInfo(hits=1, misses=3, maxsize=2, currsize=2)
    quadrat.cache_clear()    # vergisst alles, auch hits und misses

maxsize begrenzt die Zahl der gemerkten Ergebnisse. Ist der Cache voll,
wirft lru_cache das Ergebnis hinaus, das am längsten nicht mehr
gebraucht wurde (least recently used, daher der Name). Mit
maxsize=None wächst der Cache unbegrenzt; dafür gibt es seit Python 3.9
die Kurzform @functools.cache. cache_info() liefert ein Tupel mit
benannten Feldern: hits (Treffer), misses (Aufrufe, bei denen gerechnet
werden musste), maxsize und currsize (gerade gemerkte Ergebnisse).
cache_parameters() liefert {"maxsize": …, "typed": …}.

Zwei Dinge sollte man wissen. Erstens müssen alle Argumente hashbar
sein (Aufgabe 4_003), sonst gibt es einen TypeError: Zahlen, Texte und
Tupel gehen, Listen und Dictionaries nicht. Zweitens ist der Cache nur
richtig, solange die Funktion zu denselben Argumenten immer dasselbe
liefert. Hängt das Ergebnis von Daten ab, die sich ändern können, wie
hier ZONE, muss man nach jeder Änderung cache_clear() aufrufen.

Ruft eine dekorierte Funktion sich selbst auf, geht auch dieser Aufruf
über den Namen und damit durch den Cache. So profitieren auch die
Zwischenschritte: Wer einmal shop.firma.de aufgelöst hat, bekommt
www.firma.de danach ohne Anfrage.
"""

from functools import lru_cache

ZONE = {
    "www.firma.de": ("CNAME", "web01.firma.de"),
    "web01.firma.de": ("A", "192.0.2.10"),
    "shop.firma.de": ("CNAME", "www.firma.de"),
    "mail.firma.de": ("A", "192.0.2.25"),
}
ANFRAGEN = []


def frage_server(name):
    """Fragt den simulierten DNS-Server nach dem Eintrag zu name und protokolliert die Anfrage in ANFRAGEN."""
    ANFRAGEN.append(name)
    return ZONE.get(name)


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
def aufloesen(name):
    """Gibt die IPv4-Adresse zu name zurück, folgt CNAME-Einträgen; None, wenn ein Name unbekannt ist."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def trefferquote():
    """Gibt den Anteil der Aufrufe von aufloesen zurück, die aus dem Cache kamen; 0.0 ohne Aufrufe."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def eintrag_aendern(name, eintrag):
    """Trägt eintrag unter name in ZONE ein (None entfernt ihn) und leert den Cache."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(aufloesen("shop.firma.de"))
print(ANFRAGEN)
print(aufloesen("www.firma.de"))
print(trefferquote())
eintrag_aendern("web01.firma.de", ("A", "192.0.2.99"))
print(aufloesen("shop.firma.de"))
