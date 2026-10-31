"""Aufgabe 4_016 – Formularprüfung                                 Stufe 4 ★★★★☆

Auf der Webseite eines Systemhauses können Kundinnen und Kunden ein
Formular für eine Supportanfrage ausfüllen. Bevor die Anfrage gespeichert
wird, prüft der Server die Eingaben und zeigt verständliche Meldungen
neben den Feldern an. Die Prüfung soll in ein größeres Projekt, in dem
jede Funktion Typannotationen trägt und ein Prüfwerkzeug wie mypy vor
jeder Auslieferung nachsieht, ob alle Aufrufe zusammenpassen.

Ein Formular kommt als Dictionary an, das jedem Feldnamen den
eingegebenen Text zuordnet, etwa {"name": "Ada Lovelace", "alter": "36",
"email": ""}. Schreiben Sie die drei Funktionen vollständig, mit
Annotationen für jeden Parameter und den Rückgabewert. Verwenden Sie die
eingebauten Typen (list, dict, tuple) und für „oder None“ die Schreibweise
X | None.

- `fehlende_felder(formular, pflicht)`: formular ist ein Dictionary von
  Texten auf Texte, pflicht eine Liste von Feldnamen (Texten). Gibt die
  Liste der Pflichtfelder zurück, die im Formular fehlen oder nur
  Leerzeichen enthalten, in der Reihenfolge von pflicht.
- `lies_alter(text)`: text ist ein Text. Gibt das Alter als ganze Zahl
  zurück, wenn text ohne Leerzeichen am Rand nur aus Ziffern besteht und
  die Zahl höchstens 150 ist, sonst None.
- `meldungen(formular, pflicht, hinweise=None)`: formular und pflicht wie
  oben, hinweise ist ein Dictionary von Feldnamen auf eigene Meldungen
  oder None. Gibt eine Liste von Tupeln (feld, meldung) zurück, beide
  Texte: zuerst für jedes fehlende Pflichtfeld, in der Reihenfolge von
  pflicht, den Hinweis aus hinweise oder, wenn es keinen gibt, den Text
  "Bitte füllen Sie das Feld „<feld>“ aus."; danach, wenn das Feld
  "alter" ausgefüllt ist, aber lies_alter None liefert, das Tupel
  ("alter", "Bitte geben Sie das Alter als ganze Zahl von 0 bis 150 an.").

    formular = {"name": "Ada Lovelace", "alter": "zwölf", "email": "  "}
    fehlende_felder(formular, ["name", "email", "telefon"])   →  ["email", "telefon"]
    lies_alter(" 36 ")                                       →  36
    lies_alter("zwölf")                                      →  None
    meldungen(formular, ["name", "email"], {"email": "Ohne E-Mail können wir nicht antworten."})
        →  [("email", "Ohne E-Mail können wir nicht antworten."),
            ("alter", "Bitte geben Sie das Alter als ganze Zahl von 0 bis 150 an.")]

Grenzen: formular hat 0 bis 1000 Einträge, pflicht 0 bis 1000 Feldnamen
ohne Wiederholung; alle Schlüssel und Werte sind Texte mit höchstens 100
Zeichen. hinweise ist None oder ein Dictionary von Texten auf Texte.

Hintergrund: Python prüft Typen erst zur Laufzeit; eine Funktion nimmt
alles an, was man ihr gibt. Annotationen schreiben dazu, was gemeint
ist: hinter einem Parameter mit Doppelpunkt, für den Rückgabewert mit ->
vor dem Doppelpunkt der Funktion:

    def preis(netto: float, anzahl: int = 1) -> float:
        return netto * anzahl * 1.19

Für Sammlungen gibt man in eckigen Klammern an, was darin steht:
list[str] ist eine Liste von Texten, dict[str, int] ein Dictionary von
Texten auf ganze Zahlen, tuple[str, int] ein Paar aus Text und Zahl,
set[int] eine Menge von Zahlen. Das lässt sich schachteln:
list[tuple[str, int]] ist eine Liste solcher Paare.

Kann ein Wert auch fehlen, schreibt man int | None: entweder eine ganze
Zahl oder None. Ältere Programme schreiben dafür Optional[int] aus dem
Modul typing; das bedeutet dasselbe. Auch ein Parameter mit dem
Standardwert None bekommt diese Form: hinweise: dict[str, str] | None =
None. Eine Funktion ohne return wird mit -> None annotiert.

Python selbst beachtet die Annotationen nicht; preis("3", 2) läuft
trotzdem los. Sie stehen aber in funktion.__annotations__, und
typing.get_type_hints(funktion) liefert sie als Dictionary. Werkzeuge wie
mypy lesen sie und melden vor dem Start, wenn irgendwo ein Text an eine
Stelle kommt, an der eine Zahl stehen soll, oder wenn ein Ergebnis, das
None sein kann, ohne Prüfung weiterverwendet wird. Außerdem
dokumentieren Annotationen die Funktion für jeden, der sie benutzt.
"""

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


formular = {"name": "Ada Lovelace", "alter": "zwölf", "email": "  "}
print(fehlende_felder(formular, ["name", "email", "telefon"]))
print(lies_alter(" 36 "), lies_alter("zwölf"))
for feld, meldung in meldungen(formular, ["name", "email"], {"email": "Ohne E-Mail können wir nicht antworten."}):
    print(f"{feld}: {meldung}")
