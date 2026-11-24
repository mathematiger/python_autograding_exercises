"""Aufgabe 5_049 – Uploadprüfung                                 Stufe 5 ★★★★★

Über das Kundenportal einer Firma laden Kundinnen und Kunden Dateien
hoch: Rechnungen, Fotos von defekten Geräten, Protokolle. Bevor eine
Datei auf dem Server landet, prüfen Regeln, ob sie unbedenklich ist. Die
Regeln schreiben verschiedene Teams als Erweiterungen (Plugins), und
jede Regel ist eine Funktion, die True (in Ordnung) oder False
(ablehnen) liefert. Damit niemand eine Regel umschreiben muss, wenn das
Portal eine neue Angabe zum Upload sammelt, nennt jede Regel als
Parameter nur die Angaben, die sie braucht: die Endungsprüfung nur
dateiname, der Virenscan nur inhalt und signaturen (Byte-Muster bekannter
Schadsoftware). Der Prüfer schaut sich die Parameterliste jeder Regel an
und ruft sie mit genau den passenden Angaben auf. Schreiben Sie mit
inspect.signature:

- `pflichtangaben(regel)` gibt die Liste der Namen aller Parameter
  zurück, die keinen Standardwert haben, in der Reihenfolge der
  Parameterliste. Ein Parameter mit ** gehört nicht dazu.
- `auswahl(regel, angaben)` gibt ein neues Dictionary mit genau den
  Angaben zurück, die die Regel bekommt: jede Angabe aus dem Dictionary
  angaben, deren Name ein Parameter der Regel ist (auch wenn ihr Wert
  None ist). Hat die Regel einen Parameter mit **, bekommt sie alle
  Angaben. Fehlt eine Angabe für einen Parameter mit Standardwert, wird
  er nicht übergeben. Fehlt eine Angabe für einen Parameter ohne
  Standardwert, löst die Funktion einen ValueError aus, dessen Meldung
  den Namen der Regel (regel.__name__) und den der fehlenden Angabe
  nennt.
- `aufrufwerte(regel, angaben)` gibt für den Prüfbericht an, mit welchen
  Werten die Regel tatsächlich arbeitet: ein Dictionary, das jedem
  Parameter der Regel seinen Wert zuordnet, also die passende Angabe oder
  sonst den Standardwert. Ein Parameter mit ** bekommt das Dictionary der
  übrigen Angaben (leer, wenn keine übrig sind). Fehlt eine Pflichtangabe,
  derselbe ValueError wie bei auswahl.
- `pruefe_upload(regeln, angaben)` ruft jede Regel der Liste regeln
  einmal mit ihrer Auswahl als benannten Argumenten auf und gibt die
  Liste der Namen der Regeln zurück, die False geliefert haben, in der
  Reihenfolge von regeln.

    ANGABEN = {"dateiname": "bericht.pdf", "groesse": 2_400_000,
               "inhalt": b"%PDF-1.7 ...", "benutzer": "lena"}

    pflichtangaben(virenscan)                →  ["inhalt", "signaturen"]
    pflichtangaben(erlaubte_endung)          →  ["dateiname"]
    pflichtangaben(alles_ausgefuellt)        →  []
    auswahl(erlaubte_endung, ANGABEN)        →  {"dateiname": "bericht.pdf"}
    auswahl(alles_ausgefuellt, ANGABEN)      →  alle vier Angaben
    auswahl(virenscan, ANGABEN)              →  ValueError: virenscan braucht die Angabe signaturen
    aufrufwerte(nicht_zu_gross, ANGABEN)     →  {"groesse": 2400000, "hoechstens": 10000000}
    aufrufwerte(alles_ausgefuellt, {"benutzer": "lena"})
                                             →  {"alles": {"benutzer": "lena"}}
    pruefe_upload(REGELN, VERDAECHTIG)       →  ["erlaubte_endung", "kein_programm", "virenscan"]

Grenzen: regeln hat 0 bis 200 Regeln. Jede Regel hat 0 bis 8 Parameter:
normale Parameter und Nur-Schlüsselwort-Parameter, jeweils mit oder ohne
Standardwert (auch None kann ein Standardwert sein), und höchstens einen
Parameter mit ** am Ende; keine Parameter mit einem einzelnen * davor
wie *args und keine Nur-Positions-Parameter. Eine Regel kann mit einem
Dekorator mit functools.wraps umhüllt sein. angaben hat 0 bis 50
Einträge; die Schlüssel sind gültige Python-Namen, aber nie der Name
eines Parameters mit **, die Werte beliebig (auch None). Jede Regel
liefert True oder False.

Hintergrund: Python-Funktionen sind Objekte, die man zur Laufzeit
untersuchen kann (Introspektion). Das Modul inspect liest dabei auch die
Parameterliste: inspect.signature(funktion) gibt ein Signature-Objekt
zurück, dessen Attribut parameters die Parameter in der Reihenfolge der
Parameterliste enthält, als Zuordnung Name → Parameter-Objekt:

    import inspect

    def melde(text, stufe=1, *, ziel, **extra):
        ...

    signatur = inspect.signature(melde)
    for parameter in signatur.parameters.values():
        print(parameter.name, parameter.kind, parameter.default)

    text    POSITIONAL_OR_KEYWORD   <class 'inspect._empty'>
    stufe   POSITIONAL_OR_KEYWORD   1
    ziel    KEYWORD_ONLY            <class 'inspect._empty'>
    extra   VAR_KEYWORD             <class 'inspect._empty'>

parameter.kind sagt, wie der Parameter übergeben wird: normal, nur mit
Namen (Aufgabe 4_020) oder als ** (Aufgabe 4_018; *args hieße
VAR_POSITIONAL). Man vergleicht mit den Konstanten der Klasse, etwa
parameter.kind == inspect.Parameter.VAR_KEYWORD. Hat ein Parameter
keinen Standardwert, steht in parameter.default die Markierung
inspect.Parameter.empty, eine eigene Klasse. Man prüft sie mit is, nicht
mit None: Bei def f(x=None) ist None ein echter Standardwert.

Ob ein Aufruf zur Parameterliste passt, prüft signatur.bind(*args,
**kwargs), und zwar nach denselben Regeln wie ein echter Aufruf, ohne
die Funktion auszuführen. Passt er nicht, kommt ein TypeError; sonst ein
BoundArguments-Objekt. Sein Attribut arguments ordnet jedem übergebenen
Parameter seinen Wert zu, apply_defaults() ergänzt die fehlenden mit
ihren Standardwerten (und einen Parameter mit ** mit {}):

    gebunden = signatur.bind("Platte voll", ziel="admin", raum=204)
    gebunden.arguments      →  {"text": "Platte voll", "ziel": "admin", "extra": {"raum": 204}}
    gebunden.apply_defaults()
    gebunden.arguments      →  {"text": "Platte voll", "stufe": 1, "ziel": "admin", "extra": {"raum": 204}}
    gebunden.args, gebunden.kwargs   # passend für melde(*gebunden.args, **gebunden.kwargs)
    signatur.bind(stufe=2)           →  TypeError: missing a required argument: 'text'
    signatur.bind_partial(stufe=2).arguments   →  {"stufe": 2}

bind_partial erlaubt, dass Pflichtangaben fehlen, etwa um einen Aufruf
Stück für Stück zusammenzusetzen. Ist eine Funktion mit functools.wraps
dekoriert (Aufgabe 4_022), folgt inspect.signature dem Verweis
__wrapped__ und zeigt die Parameter des Originals, nicht das
(*args, **kwargs) der Hülle. Darum ist signature besser als ein Blick in
funktion.__code__.co_varnames, das zudem auch die lokalen Variablen
enthält. Nach diesem Prinzip arbeitet etwa pytest: Eine Testfunktion
nennt als Parameter, was sie braucht, und pytest übergibt es ihr. Eine
Signatur kennt außerdem die Typannotationen der Parameter; mit ihnen
prüft man später Argumente automatisch.
"""

import inspect


def erlaubte_endung(dateiname, endungen=(".pdf", ".png", ".jpg", ".txt")):
    """Die Datei hat eine der erlaubten Endungen."""
    return dateiname.lower().endswith(endungen)


def nicht_zu_gross(groesse, *, hoechstens=10_000_000):
    """Die Datei ist höchstens 10 MB groß."""
    return groesse <= hoechstens


def kein_programm(inhalt):
    """Der Inhalt beginnt nicht mit "MZ", der Kennung eines Windows-Programms."""
    return not inhalt.startswith(b"MZ")


def virenscan(inhalt, *, signaturen):
    """Im Inhalt kommt keines der Byte-Muster bekannter Schadsoftware vor."""
    return not any(signatur in inhalt for signatur in signaturen)


def alles_ausgefuellt(**alles):
    """Keine Angabe ist leer."""
    return all(wert not in ("", b"", None) for wert in alles.values())


def pflichtangaben(regel):
    """Gibt die Namen der Parameter ohne Standardwert zurück, ohne den Parameter mit **."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def auswahl(regel, angaben):
    """Gibt die Angaben zurück, die die Regel als benannte Argumente bekommt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def aufrufwerte(regel, angaben):
    """Gibt jedem Parameter der Regel den Wert, mit dem sie arbeitet, auch Standardwerte."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def pruefe_upload(regeln, angaben):
    """Ruft jede Regel mit ihren Angaben auf und gibt die Namen der Regeln zurück, die ablehnen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


ANGABEN = {"dateiname": "bericht.pdf", "groesse": 2_400_000, "inhalt": b"%PDF-1.7 ...", "benutzer": "lena"}
VERDAECHTIG = {
    "dateiname": "rechnung.pdf.exe",
    "groesse": 80_000,
    "inhalt": b"MZ\x90\x00 ... EICAR ...",
    "benutzer": "lena",
    "signaturen": [b"EICAR", b"X5O!P%"],
}
REGELN = [erlaubte_endung, nicht_zu_gross, kein_programm, virenscan, alles_ausgefuellt]

print(pflichtangaben(virenscan))
print(auswahl(erlaubte_endung, ANGABEN))
print(aufrufwerte(nicht_zu_gross, ANGABEN))
print(pruefe_upload(REGELN, VERDAECHTIG))
