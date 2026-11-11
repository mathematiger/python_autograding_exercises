"""Aufgabe 4_020 – Aktorbefehle                                   Stufe 4 ★★★★☆

In einem Bürogebäude steuert eine Gebäudeautomation Jalousien, Lampen
und Lüfter über MQTT, ein Nachrichtenprotokoll für kleine Geräte: Ein
Befehl ist eine Nachricht an ein Topic, eine Adresse wie
"etage2/raum204/jalousie", und der Inhalt (die Payload) ist der neue
Wert als Text, etwa "75" für 75 % geschlossen. Zwei Einstellungen
bestimmen, wie die Nachricht zugestellt wird: qos (0, 1 oder 2: die
Nachricht kommt höchstens, mindestens oder genau einmal an) und retain
(ob der Server, der Broker, die letzte Nachricht des Topics aufhebt und
an Geräte schickt, die sich erst später dafür anmelden). Weil man diese
beiden bei einem Aufruf wie befehl("raum/licht", 1, True, 2) leicht
vertauscht, dürfen sie nur mit Namen übergeben werden. Vervollständigen Sie:

- `befehl(topic, wert, *, qos=0, retain=False)` gibt die Nachricht als
  Dictionary {"topic": …, "payload": …, "qos": …, "retain": …} zurück;
  payload ist str(wert). Ist qos nicht 0, 1 oder 2, löst die Funktion
  einen ValueError aus, dessen Meldung den falschen Wert enthält.
- `rampe(start, ziel, *, schritte)` gibt die Liste der Werte zurück, mit
  denen eine Lampe in schritte gleichen Schritten von start auf ziel
  gedimmt wird, ohne start, mit ziel. Der i-te Wert ist start +
  (ziel - start) * i // schritte für i von 1 bis schritte, also auf eine
  ganze Zahl abgerundet. schritte hat keinen Standardwert und muss immer
  mit Namen angegeben werden.
- `dimme(topic, start, ziel, *, schritte, qos=0, retain=False)` gibt für
  jeden Wert der Rampe einen Befehl an topic zurück. Die Funktion
  benutzt dafür rampe und befehl und reicht schritte, qos und retain mit
  Namen weiter.

    befehl("etage2/raum204/jalousie", 75)
        →  {"topic": "etage2/raum204/jalousie", "payload": "75", "qos": 0, "retain": False}
    befehl("etage2/raum204/licht", 40, retain=True, qos=1)
        →  {"topic": "etage2/raum204/licht", "payload": "40", "qos": 1, "retain": True}
    befehl("etage2/raum204/licht", 40, 1)       →  TypeError
    rampe(0, 100, schritte=4)                   →  [25, 50, 75, 100]
    rampe(80, 20, schritte=4)                   →  [65, 50, 35, 20]
    rampe(0, 10, schritte=3)                    →  [3, 6, 10]
    rampe(0, 100, 4)                            →  TypeError
    dimme("flur/licht", 0, 100, schritte=2, qos=1)
        →  [{"topic": "flur/licht", "payload": "50", "qos": 1, "retain": False},
            {"topic": "flur/licht", "payload": "100", "qos": 1, "retain": False}]

Grenzen: topic ist ein nicht leerer Text, wert eine ganze Zahl von 0
bis 100 oder ein Text wie "an" oder "aus". qos ist eine beliebige ganze
Zahl, retain True oder False. start und ziel sind ganze Zahlen von 0 bis
100, schritte eine ganze Zahl von 1 bis 10 000.

Hintergrund: Normalerweise kann man jedes Argument entweder nach seiner
Position oder mit seinem Namen übergeben (Aufgabe 2_012). Bei Funktionen
mit mehreren Einstellungen ist der Aufruf nach Position aber schwer zu
lesen und fehleranfällig: Was bedeuten True und 2 in befehl("licht", 1,
True, 2)? Ein einzelner Stern in der Parameterliste legt fest, dass alle
Parameter dahinter nur mit Namen übergeben werden dürfen
(Nur-Schlüsselwort-Parameter):

    def sende(text, *, laut=False, wiederholungen=1):
        ...

    sende("Hallo", laut=True)        # richtig
    sende("Hallo", True)             # TypeError: takes 1 positional argument but 2 were given

Hinter dem Stern dürfen auch Parameter ohne Standardwert stehen; dann
muss der Aufrufer sie angeben, und zwar mit Namen:

    def warte(*, sekunden):
        ...

    warte(sekunden=5)                # richtig
    warte()                          # TypeError: missing 1 required keyword-only argument

Der Stern allein nimmt, anders als *args in Aufgabe 4_018, keine
Argumente auf; er ist nur eine Trennlinie. Schreibt man *args, sind die
Parameter dahinter ebenfalls Nur-Schlüsselwort-Parameter. Die Reihenfolge der
benannten Argumente beim Aufruf ist egal. Viele Funktionen der
Standardbibliothek arbeiten so, etwa sorted(werte, *, key=None,
reverse=False): sorted(werte, True) ist ein Fehler, sorted(werte,
reverse=True) richtig. inspect.signature(funktion) zeigt die Parameter
an; ihre Art heißt dann KEYWORD_ONLY.
"""


def befehl(topic, wert, *, qos=0, retain=False):
    """Gibt eine MQTT-Nachricht als Dictionary zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def rampe(start, ziel, *, schritte):
    """Gibt die Zwischenwerte von start nach ziel in schritte Schritten zurück, ohne start."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def dimme(topic, start, ziel, *, schritte, qos=0, retain=False):
    """Gibt für jeden Wert der Rampe einen Befehl an topic zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(befehl("etage2/raum204/jalousie", 75))
print(rampe(0, 100, schritte=4), rampe(80, 20, schritte=4), rampe(0, 10, schritte=3))
print(len(dimme("flur/licht", 0, 100, schritte=2, qos=1)))
