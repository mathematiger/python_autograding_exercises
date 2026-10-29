"""Aufgabe 3_012 – Grenzwerte für Portbereiche                    Stufe 3 ★★★☆☆

Ein Netzwerkdienst lauscht auf einem Port, einer Nummer, über die ein
Rechner mehrere Dienste gleichzeitig anbieten kann, etwa 443 für HTTPS.
Die Portnummern sind in drei Bereiche eingeteilt:

    0 bis 1023          "System"       (bekannte Dienste wie 22 für SSH)
    1024 bis 49151      "Registriert"  (für Anwendungen angemeldet)
    49152 bis 65535     "Dynamisch"    (vom Betriebssystem frei vergeben)

Ein Werkzeug zur Firewall-Konfiguration ordnet jede Portnummer mit der
Funktion `portbereich(port)` einem Bereich zu. Sie steht schon im Code
und gibt den Namen des Bereichs zurück; eine Zahl unter 0 oder über 65535
ist keine Portnummer und löst einen ValueError aus.

Schreiben Sie die Funktion `testfaelle()`, die eine Liste von Testfällen
(port, erwartet) zurückgibt. erwartet ist der Name des Bereichs oder der
Text "ValueError", wenn ein ValueError kommen muss:

    [(22, "System"), (70000, "ValueError"), …]

Die Tests dieser Aufgabe prüfen Ihre Testfälle mit der richtigen
portbereich und mit vielen fehlerhaften Fassungen, bei denen eine der
Grenzen um eins oder um mehr verschoben ist. Jede fehlerhafte Fassung muss
an mindestens einem Testfall scheitern. Weil man nicht alle 65 536 Ports
ausprobieren kann, dürfen Sie höchstens 12 Testfälle angeben: Wählen Sie
sie systematisch.

Grenzen: 1 bis 12 Testfälle; jeder port ist eine ganze Zahl mit
-10**6 ≤ port ≤ 10**6, jedes erwartet einer der Texte "System",
"Registriert", "Dynamisch" oder "ValueError".

Hintergrund: Bei einem Blackbox-Test kennt man nur die Beschreibung, nicht
den Code. Um mit wenigen Testfällen viel zu finden, teilt man die
möglichen Eingaben in Äquivalenzklassen ein: Gruppen von Eingaben, die
laut Beschreibung gleich behandelt werden. Hier sind das fünf Klassen:
zu klein (unter 0), System, Registriert, Dynamisch und zu groß (über
65535). Aus jeder Klasse genügt im Prinzip ein Vertreter, denn wenn die
Funktion für 500 richtig "System" sagt, wird sie es auch für 501 tun.

Fehler sitzen aber besonders gern an den Rändern der Klassen: Wer
port < 1023 statt port <= 1023 schreibt, ordnet genau den einen Port 1023
falsch ein. Darum testet man zusätzlich die Grenzwerte, und zwar an jeder
Grenze beide Seiten: den letzten Wert der einen Klasse und den ersten der
nächsten. Bei einer Altersgrenze ab 18 wären das 17 und 18. Zusammen mit
den Vertretern ergibt das wenige, aber scharfe Testfälle; eine Grenze, an
der man nur eine Seite testet, kann sich unbemerkt verschieben.

Tipp: Zählen Sie zuerst die Grenzen: Wie viele Paare von Grenzwerten
brauchen Sie, und wie viele Testfälle bleiben dann noch für Vertreter?
"""


def portbereich(port):
    """Gibt "System", "Registriert" oder "Dynamisch" zurück; ValueError, wenn port keine Portnummer ist."""
    if port < 0 or port > 65535:
        raise ValueError(f"Keine Portnummer: {port}")
    if port <= 1023:
        return "System"
    if port <= 49151:
        return "Registriert"
    return "Dynamisch"


def testfaelle():
    """Gibt eine Liste von höchstens 12 Testfällen (port, erwartet) für portbereich zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ergebnis_von(funktion, port):
    """Ruft funktion(port) auf und gibt das Ergebnis zurück, bei einem ValueError den Text "ValueError"."""
    try:
        return funktion(port)
    except ValueError:
        return "ValueError"


for port, erwartet in testfaelle():
    print(f"portbereich({port}) ergibt {ergebnis_von(portbereich, port)}, erwartet: {erwartet}")
