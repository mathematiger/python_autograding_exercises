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
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(gueltige_ports(["443", "https", " 22 ", "70000", "", "8080"]))
