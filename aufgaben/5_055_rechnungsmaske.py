"""Aufgabe 5_055 – Rechnungsmaske                                Stufe 5 ★★★★★

Ein kleines IT-Systemhaus bekommt eine neue Eingabemaske, mit der die
Technikerinnen und Techniker nach einem Einsatz vor Ort gleich die
Rechnung erfassen: je Position eine Menge und einen Einzelpreis (netto).
Darunter zeigt die Maske die Nettosumme, die Umsatzsteuer und den
Bruttobetrag an. Die erste Fassung rechnete mit float, und schon in der
Testphase meldete die Buchhaltung Rechnungen, bei denen ein Cent fehlte.
Die neue Fassung rechnet mit dem Modul decimal. Schreiben Sie drei
Funktionen, die alle Beträge als decimal.Decimal zurückgeben:

- `lies_betrag(eingabe)` bekommt den Text aus einem Preisfeld der Maske,
  etwa "12,5" oder " 1.50 " (Komma oder Punkt als Dezimaltrennzeichen,
  Leerzeichen am Rand egal), und gibt den Betrag als Decimal zurück.
  Gültig ist alles, was Decimal nach dem Ersetzen des Kommas durch einen
  Punkt als endliche Zahl liest. Ist die Eingabe so nicht lesbar, keine
  endliche Zahl ("nan", "inf"), negativ oder geht sie nicht auf ganze
  Cent auf ("0,005"), löst die Funktion einen ValueError aus, damit die
  Maske das Feld rot markieren kann.
- `kaufmaennisch(betrag)` rundet einen Decimal kaufmännisch auf ganze
  Cent: ab einem halben Cent wird aufgerundet, bei negativen Beträgen
  vom Betrag her ebenso (-0,285 wird -0,29).
- `rechnungssumme(positionen, prozent)` bekommt eine Liste von Paaren
  (menge, einzelpreis) mit einer ganzen Zahl und einem Decimal sowie den
  Steuersatz in Prozent und gibt das Tupel (netto, steuer, brutto)
  zurück: netto ist die genaue Summe von menge · einzelpreis, steuer ist
  netto · prozent / 100 kaufmännisch gerundet, brutto ist netto + steuer.

    lies_betrag("12,5")                  →  Decimal('12.5')
    lies_betrag("12,345")                →  ValueError (kein ganzer Cent)
    kaufmaennisch(Decimal("0.285"))      →  Decimal('0.29')
    rechnungssumme([(3, Decimal("19.99")), (1, Decimal("1.50"))], 19)
                                         →  (Decimal('61.47'), Decimal('11.68'), Decimal('73.15'))
    rechnungssumme([(1, Decimal("1.50"))], 19)
                                         →  (Decimal('1.50'), Decimal('0.29'), Decimal('1.79'))

Im letzten Beispiel ist die Steuer genau 0,285 €. Die float-Fassung gab
round(1.50 * 19 / 100, 2), also 0.28, aus.

Grenzen: eingabe ist ein beliebiger Text mit höchstens 30 Zeichen; ist
er als Zahl lesbar, liegt sie zwischen -10**9 und 10**9. betrag in
kaufmaennisch ist ein endlicher Decimal zwischen -10**9 und 10**9 mit
höchstens 20 Nachkommastellen. positionen hat 0 bis 10 000 Einträge,
menge ist 1 bis 1000, einzelpreis ein Decimal von 0 bis 10**6, der auf
ganze Cent aufgeht. prozent ist eine ganze Zahl von 0 bis 100.

Hintergrund: In Aufgabe 2_043 haben Sie gesehen, dass 0.1 + 0.2 nicht
0.3 ist: float speichert Zahlen als Binärbrüche, und Zehntel und
Hundertstel lassen sich im Zweiersystem so wenig genau hinschreiben wie
1/3 im Zehnersystem. Für Messwerte genügt dann ein Vergleich mit
Toleranz. Bei Geld nicht: Eine Rechnung muss auf den Cent stimmen, und
kleine Fehler werden zu sichtbaren, sobald gerundet wird. Darum rechnet
Buchhaltungssoftware entweder in ganzen Cent (int) oder mit
Dezimalzahlen. Das Modul decimal rechnet im Zehnersystem, so wie man es
auf Papier tut:

    from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

    Decimal("0.1") + Decimal("0.2") == Decimal("0.3")   # True
    sum([Decimal("0.10")] * 10)                          # Decimal('1.00')
    Decimal("19.99") * 3                                 # Decimal('59.97')
    Decimal("1.50") * 19 / 100                           # Decimal('0.285')

Wichtig ist, woraus man einen Decimal baut. Aus einem Text oder einer
ganzen Zahl entsteht genau diese Zahl. Aus einem float übernimmt
Decimal dagegen den Fehler, der schon im float steckt:

    Decimal("0.1")    # Decimal('0.1')
    Decimal(0.1)      # Decimal('0.1000000000000000055511151231257827021181583404541015625')

Eingaben aus einer Maske sind ohnehin Texte; man gibt sie also direkt an
Decimal, nie über float(...). Kann Decimal einen Text nicht lesen,
löst es decimal.InvalidOperation aus. Das ist eine Unterart von
ArithmeticError (Aufgabe 3_030), kein ValueError; wer einen ValueError
verspricht, fängt InvalidOperation ab und löst mit raise ... from
fehler (Aufgabe 4_058) einen ValueError aus. Decimal liest auch "NaN" (keine Zahl) und
"Infinity"; ob ein Wert eine gewöhnliche Zahl ist, sagt
betrag.is_finite().

Ein Decimal merkt sich seine Nachkommastellen: Decimal("1.50") wird als
1.50 angezeigt, ist aber gleich Decimal("1.5"). Auf eine feste Zahl von
Stellen bringt man ihn mit quantize, dem man einen Decimal mit den
gewünschten Stellen als Muster und die Rundungsart mitgibt:

    CENT = Decimal("0.01")
    Decimal("0.285").quantize(CENT, rounding=ROUND_HALF_UP)   # Decimal('0.29')
    Decimal("0.285").quantize(CENT)                            # Decimal('0.28')
    round(0.285, 2)                                            # 0.28

ROUND_HALF_UP ist die kaufmännische Rundung: Hälften werden vom Betrag
her aufgerundet. Ohne rounding nimmt quantize ROUND_HALF_EVEN, die
„Bankrundung“, bei der Hälften zur geraden Ziffer gehen. Diese Regel
benutzt auch das eingebaute round, für Decimal wie für float. Bei
round(0.285, 2) kommt noch dazu, dass der float 0.285 in Wahrheit
0.28499999… ist; selbst ROUND_HALF_UP könnte das nicht mehr retten.
Ob ein Betrag auf ganze Cent aufgeht, prüft man ebenso:
betrag == betrag.quantize(CENT).

Bei der Division können unendlich viele Stellen entstehen, etwa bei
Decimal(1) / 3. Dann rundet decimal nach den Regeln seines Kontexts:
decimal.getcontext().prec ist die Zahl der gültigen Stellen, 28,
wenn man nichts ändert. Das reicht für Geldbeträge weit. Mit
decimal.localcontext() ändert man den Kontext nur für einen
with-Block (Aufgabe 4_051); der Kontext legt auch fest, welche Fehler
eine Ausnahme auslösen (traps), etwa InvalidOperation und
DivisionByZero. Gerundet wird für die Anzeige erst am Ende, mit
quantize, nicht in jedem Zwischenschritt.

Decimal und int lassen sich mischen (Decimal("19.99") * 3), Decimal und
float nicht: Decimal("1.5") + 0.1 ist ein TypeError, damit sich der
Fehler eines float nicht unbemerkt einschleicht.
"""

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

CENT = Decimal("0.01")


def lies_betrag(eingabe):
    """Liest einen nicht negativen Betrag in ganzen Cent aus dem Text eines Preisfelds; sonst ValueError."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def kaufmaennisch(betrag):
    """Rundet den Decimal betrag kaufmännisch (ROUND_HALF_UP) auf ganze Cent."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def rechnungssumme(positionen, prozent):
    """Gibt (netto, steuer, brutto) als Decimal zu den Paaren (menge, einzelpreis) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(lies_betrag("12,5"))
print(kaufmaennisch(Decimal("0.285")))
print(rechnungssumme([(3, Decimal("19.99")), (1, Decimal("1.50"))], 19))
