"""Aufgabe 5_028 – Budgetkonto                                   Stufe 5 ★★★★★

Für ein IT-Projekt ist ein festes Budget bewilligt, etwa für Hardware und
Lizenzen. Jede Ausgabe wird gegen das Budget gebucht; was das restliche
Budget übersteigt, lehnt die Buchhaltung ab. Wird eine Bestellung
storniert, kommt ihr Betrag zurück aufs Konto. Am Ende des Projekts wird
das Konto abgeschlossen, und der Abschluss muss im Protokoll stehen, ganz
gleich, ob das Projekt regulär endet oder die Auswertung mit einem Fehler
abbricht.

Das Konto soll ein Generator sein, der Buchungen mit send empfängt und
das restliche Budget zurückliefert. Die Ausnahme `Storno` ist
vorgegeben. Vervollständigen Sie:

- `budgetkonto(budget, protokoll)` ist eine Generatorfunktion. Das erste
  next() liefert das Budget. Danach gilt:
  - `send(betrag)` bucht die Ausgabe, wenn betrag höchstens so groß wie
    der Rest ist, und hängt "gebucht: <betrag>" an protokoll an. Sonst
    bleibt der Rest, und protokoll bekommt "abgelehnt: <betrag>". In
    beiden Fällen liefert send den Rest danach.
  - `throw(Storno(betrag))` schreibt betrag wieder gut, hängt
    "storniert: <betrag>" an und liefert den neuen Rest. Das Konto läuft
    danach normal weiter.
  - Endet das Konto, egal wie (close() oder eine andere hineingeworfene
    Ausnahme, die dann weiterläuft), hängt es genau einmal
    "Abschluss: Rest <rest>" an protokoll an.
- `abrechnen(budget, buchungen)` legt ein Protokoll und ein Konto an,
  startet es und geht die Buchungen durch: Eine Zahl ≥ 0 ist eine
  Ausgabe (send), eine negative Zahl -x storniert x (throw(Storno(x))).
  Danach schließt es das Konto mit close() und gibt das Protokoll zurück.

    protokoll = []
    konto = budgetkonto(1000, protokoll)
    next(konto)                 →  1000
    konto.send(300)             →  700
    konto.send(900)             →  700
    konto.throw(Storno(200))    →  900
    konto.close()
    protokoll  →  ["gebucht: 300", "abgelehnt: 900", "storniert: 200",
                   "Abschluss: Rest 900"]
    abrechnen(500, [200, -50, 400])  →  ["gebucht: 200", "storniert: 50",
                                         "abgelehnt: 400", "Abschluss: Rest 350"]

Grenzen: budget und alle Beträge sind ganze Zahlen von 0 bis 10**9;
buchungen hat 0 bis 20 000 Einträge von -10**9 bis 10**9. send, throw und
close werden nur nach dem ersten next() aufgerufen, nach dem Ende des
Kontos nicht mehr (außer close, das dann nichts mehr tut).

Hintergrund: Mit send schickt man einen Wert an das yield, an dem ein
Generator wartet (Aufgabe 5_027). Zwei weitere Methoden steuern ihn von
außen:

- generator.throw(ausnahme) löst die Ausnahme genau an diesem yield aus,
  so als stünde dort raise ausnahme. Fängt der Generator sie mit
  try/except ab und läuft bis zum nächsten yield weiter, liefert throw
  dessen Wert zurück. Fängt er sie nicht, endet der Generator, und die
  Ausnahme kommt beim Aufrufer von throw heraus.
- generator.close() wirft am wartenden yield die besondere Ausnahme
  GeneratorExit hinein. Der Generator soll dann enden; close() gibt
  nichts zurück. Ein Generator, der danach noch einmal yield erreicht,
  löst einen RuntimeError aus. GeneratorExit erbt darum nicht von
  Exception, damit ein except Exception sie nicht versehentlich
  verschluckt.

Aufräumen, das in jedem Fall geschehen muss, gehört in einen finally-
Block (Aufgabe 3_008) um die Schleife. Er läuft beim close(), bei einer
nicht abgefangenen Ausnahme aus throw und auch, wenn der Generator
normal ans Ende kommt:

    def leser(protokoll):
        protokoll.append("geöffnet")
        try:
            while True:
                try:
                    zeile = yield
                except ValueError:
                    protokoll.append("kaputte Zeile übersprungen")
                    continue
                protokoll.append(zeile)
        finally:
            protokoll.append("geschlossen")

    p = []
    g = leser(p)
    next(g)
    g.send("a")
    g.throw(ValueError())      # abgefangen, der Generator läuft weiter
    g.close()
    p  →  ["geöffnet", "a", "kaputte Zeile übersprungen", "geschlossen"]

Das innere try umfasst nur das yield, damit nur die hineingeworfene
Ausnahme abgefangen wird und nicht etwa ein Fehler beim Verarbeiten.
continue springt zurück zum nächsten yield, das den Wert für throw
liefert.

Wird ein Generator nie geschlossen, ruft Python close() selbst auf, wenn
er nicht mehr gebraucht wird, aber erst irgendwann; wer sich auf das
Aufräumen verlassen will, schließt ihn selbst, am sichersten in einem
try/finally beim Aufrufer.
"""


class Storno(Exception):
    """Wird in das Konto geworfen, um einen Betrag wieder gutzuschreiben (vorgegeben)."""

    def __init__(self, betrag):
        super().__init__(f"Storno über {betrag}")
        self.betrag = betrag


def budgetkonto(budget, protokoll):
    """Empfängt Ausgaben mit send und Stornos mit throw, liefert jeweils das restliche Budget."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def abrechnen(budget, buchungen):
    """Bucht alle Buchungen auf ein neues Konto, schließt es und gibt das Protokoll zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


protokoll = []
konto = budgetkonto(1000, protokoll)
print(next(konto), konto.send(300), konto.send(900), konto.throw(Storno(200)))
konto.close()
print(protokoll)
print(abrechnen(500, [200, -50, 400]))
