"""Aufgabe 4_058 – Passworttresor                                Stufe 4 ★★★★☆

Die Skripte einer IT-Abteilung melden sich bei Diensten wie dem VPN
oder dem Wiki an. Die Zugangsdaten stehen nicht im Code, sondern in
einem Tresor, einem Dictionary Dienst → Eintrag. Ein Eintrag ist ein
Text aus drei Feldern, getrennt durch Semikolons: Benutzername,
Passwort und der letzte Tag, an dem es gilt (als Tagesnummer). Das
Passwort steht hexadezimal da, jedes Byte als zwei Ziffern 0–9 und
a–f; "67656865696d" ist "geheim". Das ist nur eine Schreibweise, keine
Verschlüsselung: Jeder kann es zurückverwandeln. Ein echter Tresor
verschlüsselt seine Einträge zusätzlich.

Wer den Tresor benutzt, soll nicht mit KeyError oder ValueError aus
dessen Innerem zu tun bekommen, sondern mit Fehlern, die zur jeweiligen
Schicht passen. Die Fehlerklassen sind vorgegeben (siehe unten).
Schreiben Sie:

- `lies_eintrag(tresor, dienst)` gibt (benutzer, passwort, gueltig_bis)
  zurück, das Passwort als Klartext, gueltig_bis als ganze Zahl.
  - Fehlt der Dienst, löst sie EintragFehlt aus, und zwar mit raise …
    from, sodass __cause__ der KeyError ist. Die Meldung nennt den
    Dienst.
  - Hat der Eintrag nicht genau drei Felder, löst sie EintragDefekt aus.
  - Ist gueltig_bis keine ganze Zahl, EintragDefekt mit dem ValueError
    von int() als __cause__.
  - Lässt sich das Passwort nicht dekodieren (bytes.fromhex oder
    decode("utf-8") scheitert), EintragDefekt mit raise … from None:
    Die ursprüngliche Ausnahme könnte Teile des Passworts enthalten und
    darf darum weder als __cause__ noch als __context__ im Traceback
    erscheinen. Die Meldung nennt den Dienst, aber nichts aus dem Feld.
- `verbinde_dienst(tresor, dienst, heute)` gibt (benutzer, passwort)
  zurück. Ist gueltig_bis kleiner als heute, löst sie EintragAbgelaufen
  aus. Jeder TresorFehler, auch der aus lies_eintrag, wird an dieser
  Schnittstelle zu DienstNichtVerfuegbar(dienst) mit dem TresorFehler
  als __cause__. Andere Ausnahmen fliegen unverändert weiter.
- `fehlerkette(fehler)` gibt die Namen der Ausnahmen zurück, die
  Python im Traceback zeigen würde, von außen nach innen: zuerst
  fehler, dann dessen __cause__; ist der None, dessen __context__, aber
  nur, wenn __suppress_context__ nicht True ist; und so weiter.

    tresor = {"vpn": "kim;67656865696d;400", "wiki": "ole;zz;500", "mail": "ada;616461;100"}
    verbinde_dienst(tresor, "vpn", 300)        →  ("kim", "geheim")
    verbinde_dienst(tresor, "drucker", 300)    →  DienstNichtVerfuegbar, Kette
        ["DienstNichtVerfuegbar", "EintragFehlt", "KeyError"]
    verbinde_dienst(tresor, "wiki", 300)       →  Kette ["DienstNichtVerfuegbar", "EintragDefekt"]
    verbinde_dienst(tresor, "mail", 300)       →  Kette ["DienstNichtVerfuegbar", "EintragAbgelaufen"]

Grenzen: Der Tresor hat 0 bis 1000 Einträge, jeder ist ein Text mit
höchstens 200 Zeichen. Benutzername und Passwort enthalten keine
Semikolons. heute und gueltig_bis liegen zwischen 0 und 100 000.

Hintergrund: Fängt man eine Ausnahme und löst im except-Zweig eine neue
aus, merkt Python sich die alte: Sie steht im Attribut __context__ der
neuen, und der Traceback zeigt beide mit „During handling of the above
exception, another exception occurred“. Das klingt nach einem zweiten
Fehler beim Aufräumen. Ist die neue Ausnahme dagegen eine bewusste
Übersetzung, schreibt man raise … from:

    try:
        port = int(text)
    except ValueError as fehler:
        raise KonfigFehler(f"Port {text!r} ist keine Zahl") from fehler

Dann steht die alte Ausnahme zusätzlich in __cause__, und der Traceback
sagt „The above exception was the direct cause of the following
exception“. Der Aufrufer sieht einen Fehler seiner Schicht (KonfigFehler,
eigene Fehlerklassen kennen Sie aus Aufgabe 4_056), und wer den Fehler
sucht, findet trotzdem die Ursache. So hält man Schnittstellen sauber:
Wer verbinde_dienst benutzt, muss nicht wissen, dass der Tresor intern
ein Dictionary ist.

raise … from None setzt __suppress_context__ auf True. Python zeigt die
alte Ausnahme dann nicht mehr an, obwohl sie noch in __context__ steht.
Das ist sinnvoll, wenn sie nichts zur Sache tut oder, wie hier,
vertrauliche Daten verraten könnte: Die Meldung eines UnicodeDecodeError
enthält die Bytes, die nicht passten.

    fehler.__cause__              # die mit from angegebene Ursache oder None
    fehler.__context__            # die Ausnahme, in deren except die neue entstand, oder None
    fehler.__suppress_context__   # True nach from None (und nach jedem from)

bytes kennen Sie aus Aufgabe 4_024. bytes.fromhex("6869") macht aus den
Hex-Ziffern die Bytes b"hi", und .decode("utf-8") macht daraus den Text
"hi". Ein Zeichen, das keine Hex-Ziffer ist (wie in "zz"), führt in
fromhex zu einem ValueError; Bytes, die kein gültiges UTF-8 sind (wie
bytes.fromhex("ff")), führen in decode zu einem UnicodeDecodeError, einer
Unterart von ValueError.
"""


class TresorFehler(Exception):
    """Oberklasse aller Fehler beim Lesen des Tresors."""


class EintragFehlt(TresorFehler):
    """Für den Dienst gibt es keinen Eintrag."""


class EintragDefekt(TresorFehler):
    """Der Eintrag lässt sich nicht lesen."""


class EintragAbgelaufen(TresorFehler):
    """Das Passwort gilt nicht mehr."""


class DienstNichtVerfuegbar(Exception):
    """Ein Dienst kann nicht benutzt werden; die Ursache steht in __cause__."""

    def __init__(self, dienst):
        """Merkt sich den Dienst und baut die Meldung."""
        super().__init__(f"Dienst {dienst} ist nicht verfügbar")
        self.dienst = dienst


def lies_eintrag(tresor, dienst):
    """Gibt (benutzer, passwort, gueltig_bis) zurück oder löst einen TresorFehler aus."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def verbinde_dienst(tresor, dienst, heute):
    """Gibt (benutzer, passwort) für den Dienst zurück oder löst DienstNichtVerfuegbar aus."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def fehlerkette(fehler):
    """Gibt die Namen der Ausnahmen zurück, die der Traceback zeigen würde, von außen nach innen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


tresor = {"vpn": "kim;67656865696d;400", "wiki": "ole;zz;500", "mail": "ada;616461;100"}
print(verbinde_dienst(tresor, "vpn", 300))
for dienst in ["drucker", "wiki", "mail"]:
    try:
        verbinde_dienst(tresor, dienst, 300)
    except DienstNichtVerfuegbar as fehler:
        print(fehler, fehlerkette(fehler))
