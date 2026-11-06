"""Aufgabe 3_024 – Stromeffizienz                                Stufe 3 ★★★☆☆

Ein Rechenzentrum will zeigen, wie sparsam es mit Strom umgeht. Die
übliche Kennzahl dafür ist die PUE (Power Usage Effectiveness): der
Stromverbrauch des ganzen Rechenzentrums geteilt durch den Verbrauch
der IT-Geräte allein. Eine PUE von 1.0 hieße, dass jede Kilowattstunde
in Server, Speicher und Netz fließt; Kühlung, Verluste in der USV und
Licht machen den Wert größer, gut sind etwa 1.2 bis 1.4.

Zwei Zähler werden jede Stunde abgelesen, und die Gebäudetechnik
exportiert die Werte als Textzeilen. Die erste Zeile ist eine
Kopfzeile, jede weitere hat die Form "stunde;gesamt;it" mit dem
Verbrauch in kWh. War ein Zähler gestört, steht dort "-" statt einer
Zahl. Die Zeilen kommen als Liste oder als Iterator, etwa direkt aus
einer geöffneten Datei. Schreiben Sie vier Funktionen:

- `messungen(zeilen)` ist ein Generator: Er überspringt die Kopfzeile
  und liefert für jede Zeile ohne "-" das Tupel (stunde, gesamt, it)
  aus ganzen Zahlen, in der Reihenfolge der Zeilen.
- `pue_je_stunde(zeilen)` gibt ein Dictionary zurück, das jeder Stunde
  mit gültiger Messung ihre PUE gesamt / it zuordnet, gerundet auf zwei
  Nachkommastellen. Benutzen Sie messungen und eine Dict Comprehension.
- `gesamt_pue(zeilen)` gibt die PUE über alle gültigen Messungen
  zurück, also die Summe aller gesamt-Werte geteilt durch die Summe
  aller it-Werte, gerundet auf zwei Nachkommastellen (nicht der
  Mittelwert der Stundenwerte). Benutzen Sie messungen und
  Generator-Ausdrücke in sum.
- `kritische_stunden(pue, grenze)` bekommt ein Dictionary wie von
  pue_je_stunde und gibt mit einer List Comprehension die Stunden
  zurück, deren PUE größer als grenze ist, in der Reihenfolge des
  Dictionarys.

    zeilen = ["stunde;gesamt;it", "0;390;300", "1;-;290", "2;480;300", "3;300;200"]
    list(messungen(zeilen))          →  [(0, 390, 300), (2, 480, 300), (3, 300, 200)]
    pue_je_stunde(zeilen)            →  {0: 1.3, 2: 1.6, 3: 1.5}
    gesamt_pue(zeilen)               →  1.46   (1170 / 800)
    kritische_stunden({0: 1.3, 2: 1.6, 3: 1.5}, 1.45)  →  [2, 3]

pue_je_stunde, gesamt_pue und kritische_stunden kommen ohne for- oder
while-Schleife als eigene Anweisung aus.

Grenzen: zeilen liefert die Kopfzeile und danach 0 bis 100 000 Zeilen;
zeilen kann eine Liste oder ein Iterator sein und wird deshalb nur
einmal durchlaufen. Die Stunden sind verschiedene ganze Zahlen von 0
bis 10**6 in aufsteigender Reihenfolge. gesamt und it sind ganze Zahlen
mit 1 ≤ it ≤ gesamt ≤ 10**6 oder "-", in einer Zeile können auch beide
"-" sein. Für gesamt_pue gibt es mindestens eine gültige Messung.
pue hat 0 bis 100 000 Einträge mit Werten von 1.0 bis 10**6, grenze ist
eine Kommazahl von 1.0 bis 10.0. Ihre Lösung soll O(n) Schritte
brauchen.

Hintergrund: Diese Aufgabe verbindet, was Sie seit Aufgabe 3_017
gelernt haben. Eine List Comprehension [x for x in werte if …] baut
eine neue Liste (Aufgabe 3_017), eine Dict Comprehension
{k: v for k, v in paare} ein Dictionary (Aufgabe 3_018), eine Set
Comprehension {x for x in werte} eine Menge (Aufgabe 3_019). for holt
sich mit iter() einen Iterator und ruft next() auf, bis StopIteration
kommt; next(zeiger) holt auch von Hand genau ein Element, zum Beispiel
eine Kopfzeile (Aufgabe 3_020). Ein Iterator ist nach einem Durchlauf
verbraucht; wer die Werte zweimal braucht, sammelt sie mit list(…)
(Aufgabe 3_021). Eine Funktion mit yield ist ein Generator, der jeden
Wert erst liefert, wenn er abgeholt wird (Aufgabe 3_022), und ein
Generator-Ausdruck (x for x in werte) in sum, any oder all rechnet
ohne Zwischenliste (Aufgabe 3_023).
"""


def messungen(zeilen):
    """Liefert für jede gültige Zeile nach der Kopfzeile das Tupel (stunde, gesamt, it)."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def pue_je_stunde(zeilen):
    """Gibt zu jeder Stunde mit gültiger Messung die PUE zurück, auf zwei Stellen gerundet."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def gesamt_pue(zeilen):
    """Gibt die Summe aller gesamt-Werte geteilt durch die Summe aller it-Werte zurück, auf zwei Stellen gerundet."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def kritische_stunden(pue, grenze):
    """Gibt die Stunden zurück, deren PUE größer als grenze ist."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


zeilen = ["stunde;gesamt;it", "0;390;300", "1;-;290", "2;480;300", "3;300;200"]
print(list(messungen(zeilen)))
print(pue_je_stunde(zeilen))
print(gesamt_pue(iter(zeilen)))
print(kritische_stunden(pue_je_stunde(zeilen), 1.45))
