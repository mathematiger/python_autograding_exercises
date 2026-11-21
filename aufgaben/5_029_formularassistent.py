"""Aufgabe 5_029 – Formularassistent                             Stufe 5 ★★★★★

Eine Anwendung soll neue Nutzer nicht mit einem großen Formular
erschlagen, sondern Schritt für Schritt durch die Anmeldung führen: Sie
zeigt eine Frage, wartet auf die Antwort, prüft sie und zeigt bei einer
ungültigen Antwort dieselbe Frage mit einem Hinweis noch einmal. Die
Oberfläche (Fenster, Terminal oder Webseite) soll dabei austauschbar
sein. Darum wird der Ablauf als Generator geschrieben: Er liefert mit
yield den Text, der angezeigt werden soll, und bekommt die Antwort mit
send zurück. Die Prüfungen ist_name, ist_alter und ist_email sind
vorgegeben. Vervollständigen Sie:

- `frage(text, ist_gueltig)` ist eine Generatorfunktion für eine
  einzelne Frage. Sie liefert zuerst text. Ist die gesendete Antwort
  ungültig (ist_gueltig(antwort) ist False), liefert sie
  "Ungültige Eingabe. " + text und wartet wieder, so oft wie nötig. Mit
  einer gültigen Antwort endet sie und gibt die Antwort mit return
  zurück.
- `anmeldeformular()` ist eine Generatorfunktion, die mit yield from
  nacheinander die drei Fragen "Name:", "Alter:" und "E-Mail:" an frage
  abgibt und am Ende das Dictionary {"name": …, "alter": …, "email": …}
  zurückgibt: den Namen ohne Leerzeichen am Rand, das Alter als int, die
  E-Mail-Adresse unverändert.
- `ausfuellen(formular, antworten)` spielt einen Formular-Generator mit
  einer Liste von Antworten durch, wie es eine Oberfläche täte: Es holt
  den ersten Text, schickt dann der Reihe nach die Antworten mit send
  und sammelt alle gelieferten Texte. Es gibt das Tupel (texte,
  ergebnis) zurück, wobei ergebnis der Rückgabewert des Formulars ist.
  Reichen die Antworten nicht, ist ergebnis None; übrige Antworten
  werden nicht benutzt.

    f = frage("Name:", ist_name)
    next(f)          →  "Name:"
    f.send("  ")     →  "Ungültige Eingabe. Name:"
    f.send("Ada")    →  StopIteration mit dem Wert "Ada"

    ausfuellen(anmeldeformular(), [" Ada ", "zwölf", "36", "ada@example.org"])
      →  (["Name:", "Alter:", "Ungültige Eingabe. Alter:", "E-Mail:"],
          {"name": "Ada", "alter": 36, "email": "ada@example.org"})
    ausfuellen(anmeldeformular(), ["Ada"])  →  (["Name:", "Alter:"], None)

Grenzen: Antworten sind beliebige Texte, antworten hat 0 bis 100 000
Einträge. ausfuellen bekommt einen frisch angelegten Generator, der
mindestens einen Text liefert, mit send Texte annimmt und am Ende
irgendeinen Wert zurückgibt.

Hintergrund: Ein Generator kann mit return einen Wert zurückgeben. Den
sieht man nicht über next() oder for, sondern nur an der Ausnahme
StopIteration, die das Ende meldet: Ihr Attribut value enthält den
Rückgabewert.

    def zaehler():
        x = yield "bereit"
        return x * 2

    g = zaehler()
    next(g)                   →  "bereit"
    try:
        g.send(21)
    except StopIteration as ende:
        ende.value            →  42

Mit yield from teilgenerator gibt ein Generator die Arbeit an einen
anderen ab: Bis der Teilgenerator endet, kommt alles, was er liefert,
direkt beim Aufrufer an, und alles, was der Aufrufer mit send schickt
(oder mit throw hineinwirft, Aufgaben 5_027 und 5_028), geht direkt an
den Teilgenerator. Der Ausdruck yield from … hat am Ende den
Rückgabewert des Teilgenerators:

    def bestellung():
        groesse = yield from zaehler()     # liefert "bereit", nimmt send(21) an
        farbe = yield "Farbe?"
        return groesse, farbe

Eine Schleife for wert in teilgenerator: yield wert sähe ähnlich aus,
reicht aber nur die gelieferten Werte nach außen weiter: Die mit send
geschickten Antworten kämen beim Teilgenerator nie an, und an seinen
Rückgabewert käme man nicht heran. So lassen sich große Abläufe aus
kleinen Generatoren zusammensetzen, die jeder für sich testbar sind.
"""


def ist_name(antwort):
    """Ein Name ist gültig, wenn nach dem Entfernen der Leerzeichen etwas übrig bleibt (vorgegeben)."""
    return antwort.strip() != ""


def ist_alter(antwort):
    """Ein Alter ist gültig, wenn es nur aus Ziffern besteht und von 16 bis 120 reicht (vorgegeben)."""
    return antwort.isdecimal() and antwort.isascii() and 16 <= int(antwort) <= 120


def ist_email(antwort):
    """Eine E-Mail-Adresse ist gültig, wenn genau ein @ mit Text davor und dahinter darin steht (vorgegeben)."""
    vorne, at, hinten = antwort.partition("@")
    return at == "@" and vorne != "" and hinten != "" and "@" not in hinten


def frage(text, ist_gueltig):
    """Liefert text, bis eine gültige Antwort gesendet wird, und gibt diese zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def anmeldeformular():
    """Fragt Name, Alter und E-Mail ab und gibt sie als Dictionary zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ausfuellen(formular, antworten):
    """Spielt das Formular mit den Antworten durch; gibt (texte, ergebnis) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(ausfuellen(anmeldeformular(), [" Ada ", "zwölf", "36", "ada@example.org"]))
print(ausfuellen(anmeldeformular(), ["Ada"]))
