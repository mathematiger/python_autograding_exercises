# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_034_portfreigaben.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_034_portfreigaben

"""Aufgabe 2_034 – Portfreigaben                                 Stufe 2 ★★☆☆☆

Wer in der Firma einen Dienst von außen erreichbar machen will, beantragt
bei der IT-Sicherheit eine Freigabe in der Firewall. Im Antragsformular
trägt man die Ports ein, die geöffnet werden sollen, etwa 443 für HTTPS
oder 25 für SMTP. Portnummern reichen von 0 bis 65535; Port 0 ist
reserviert und lässt sich nicht freigeben, gültig sind also 1 bis 65535.
Das Protokoll (TCP oder UDP) wählt man in einem eigenen Feld, in das
Portfeld gehört nur die reine Nummer; Bereiche wie 8000-8100 sieht das
Formular nicht vor. Es liefert jeden Eintrag als Text, und nicht alle sind
brauchbar: "https" statt 443, "8080/tcp" mit Protokoll, ein leeres Feld
oder ein Port wie 70000, den es gar nicht gibt. Vor dem Einspielen sollen
nur die gültigen Ports übrig bleiben; die übrigen gehen an die
Antragsteller zurück.

Vervollständigen Sie die Funktion `gueltige_ports(eintraege)`. Sie bekommt
eine Liste von Texten und gibt eine neue Liste mit den gültigen Ports als
ganze Zahlen zurück, in der Reihenfolge der Einträge. Gültig ist ein
Eintrag, wenn int(...) ihn umwandeln kann und die Zahl von 1 bis 65535
reicht. Alle anderen Einträge werden übersprungen; ein einziger kaputter
Eintrag darf die Funktion nicht abstürzen lassen. Kommt ein Port mehrmals
vor, steht er auch mehrmals im Ergebnis; doppelte Anträge prüft ein
späterer Schritt. Fangen Sie nur den ValueError ab.

    gueltige_ports(["443", "https", " 22 ", "70000", "", "8080"])
        →  [443, 22, 8080]
    gueltige_ports(["0", "65535", "-1", "8080/tcp"])
        →  [65535]
    gueltige_ports([])
        →  []

Die übergebene Liste bleibt unverändert.

Grenzen: 0 ≤ len(eintraege) ≤ 10 000, jeder Eintrag ist ein Text mit
höchstens 20 Zeichen aus den Ziffern 0 bis 9, Buchstaben, Leerzeichen und
den Zeichen "-", ".", ",", "/" und ":". Leerzeichen am Anfang und am Ende
stören int nicht.

Hintergrund: Mit try und except fangen Sie einen ValueError ab, statt das
Programm abstürzen zu lassen (Aufgabe 2_033). Steht das try in einer
Schleife, gilt es für jeden Durchlauf einzeln: Scheitert die Umwandlung
eines Eintrags, springt Python in den except-Block. Danach geht es hinter
dem try weiter, und zwar im selben Durchlauf. Mit continue (Aufgabe 2_008)
überspringen Sie im except-Block den Rest des Durchlaufs, und die Schleife
macht mit dem nächsten Eintrag weiter:

    for text in ["3", "drei", "5"]:
        try:
            zahl = int(text)
        except ValueError:
            print(text, "ist keine Zahl")
            continue
        print(zahl * 2)

Das gibt 6, „drei ist keine Zahl“ und 10 aus. Ohne continue liefe nach dem
except-Block auch print(zahl * 2), mit einem Wert aus dem vorigen
Durchlauf. Ins try gehört nur die Zeile, deren Fehler Sie abfangen wollen.
"""


def gueltige_ports(eintraege):
    """Gibt die gültigen Ports aus eintraege als Liste ganzer Zahlen zurück."""
    ports = []
    for eintrag in eintraege:
        try:
            port = int(eintrag)
        except ValueError:
            continue
        if 1 <= port <= 65535:
            ports.append(port)
    return ports


print(gueltige_ports(["443", "https", " 22 ", "70000", "", "8080"]))


# Idee: Die Funktion legt eine leere Liste an und geht alle Einträge durch. Im try-Block steht nur
# int(eintrag); scheitert die Umwandlung, überspringt continue im except-Block den Eintrag. Danach
# prüft ein ganz normales if, ob die Zahl von 1 bis 65535 reicht, und hängt sie dann an.
#
# Anderer Weg: das if und das append in den try-Block schreiben und im except-Block nur pass (eine
# Anweisung, die nichts tut). Das geht hier auch, zeigt aber nicht mehr, welche Zeile scheitern darf.
# Statt continue geht auch ein else-Block hinter dem except (Aufgabe 3_008).
#
# Typische Fehler: vorher mit isdigit() prüfen (dann fällt " 22 " durch), mit break oder return
# beim ersten kaputten Eintrag aufhören, < statt <= an den Grenzen, den Text statt der Zahl anhängen
# und except ohne ValueError (das verschluckt auch Fehler im eigenen Code).
#
# Weiter geht es mit Aufgabe 2_035: Dort fangen Sie zwei Arten von Fehlern in einem except ab.
