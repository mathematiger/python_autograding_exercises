"""Aufgabe 5_045 – Prozessübergänge                              Stufe 5 ★★★★★

Ein Versandhändler will verstehen, wie Reklamationen in seinen drei
Kundencentern wirklich ablaufen. Jede Reklamation (ein Fall) durchläuft
Schritte wie eingang, pruefung, rueckfrage und versand, und das
Ticketsystem protokolliert für jeden Fall die Reihenfolge. Ein
Werkzeug zur Prozessanalyse zählt daraus die Übergänge: Wie oft folgt
auf pruefung eine rueckfrage, wie oft direkt versand? Aus diesen Zahlen
zeichnet es später ein Prozessdiagramm, in dem dicke Pfeile die
häufigen Wege zeigen.

Weil jedes Kundencenter sein Protokoll über das Netz liefert, wertet
das Werkzeug alle Standorte gleichzeitig aus, mit einem Thread je
Standort, und alle zählen in einen gemeinsamen Zähler. Die bisherige
Klasse AlterZaehler (unten vorgegeben) liest den alten Stand, prüft den
Übergang mit pruefe_schritt gegen den Prozesskatalog und schreibt dann
den neuen Stand. Seit dem Umbau auf Threads stimmen die Zahlen nicht
mehr: Es fehlen Übergänge, bei jedem Lauf andere.

    standorte = {
        "Hamburg": [["eingang", "pruefung", "versand"],
                    ["eingang", "pruefung", "rueckfrage", "pruefung", "versand"]],
        "Leipzig": [["eingang", "pruefung", "versand"]],
        "Köln":    [["eingang", "rueckfrage", "pruefung", "versand"]],
    }

Schreiben Sie:

- die Klasse `Uebergaenge`, die genauso zählt wie AlterZaehler, aber
  threadsicher ist: `__init__` legt das Dictionary zaehler (Paar
  (von, nach) → Anzahl) und eine Sperre threading.Lock() im Attribut
  sperre an. `zaehle(von, nach)` liest den alten Stand, ruft
  pruefe_schritt(von, nach) auf und schreibt den neuen Stand, alles
  zusammen unter der Sperre. Löst pruefe_schritt einen ValueError aus,
  wird nichts gezählt, der Fehler geht an den Aufrufer, und die Sperre
  ist danach wieder frei. `stand()` gibt unter der Sperre eine Kopie
  des Zählers zurück, nach den Paaren sortiert.
- `zaehle_faelle(zaehler, faelle)` zählt mit zaehler.zaehle jeden
  Übergang zwischen zwei aufeinanderfolgenden Schritten jedes Falls.
- `parallel_auswerten(standorte)` legt einen Uebergaenge-Zähler an,
  startet für jeden Standort einen Thread, der zaehle_faelle mit dessen
  Fällen ausführt, wartet auf alle und gibt zaehler.stand() zurück.

    parallel_auswerten(standorte)
    →  {("eingang", "pruefung"): 3, ("eingang", "rueckfrage"): 1,
        ("pruefung", "rueckfrage"): 1, ("pruefung", "versand"): 4,
        ("rueckfrage", "pruefung"): 2}

Grenzen: standorte hat 0 bis 10 Standorte mit je 0 bis 100 Fällen; ein
Fall hat 1 bis 10 Schritte, nicht leere Texte. pruefe_schritt löst bei
einem leeren Schritt einen ValueError aus.

Hintergrund: In Aufgabe 5_044 hat jeder Thread sein Ergebnis in sein
eigenes Attribut geschrieben; gemeinsam benutzt wurde nichts. Hier
schreiben alle Threads in dasselbe Dictionary, und das geht schief.
Python kann einen Thread zwischen zwei beliebigen Schritten anhalten
und einen anderen weiterlaufen lassen, bei jedem Warten auf das Netz,
eine Datei oder wie hier bei pruefe_schritt sogar sicher. So geht ein
Übergang verloren:

    Thread A: bisher = zaehler.get(paar, 0)     # liest 3
    Thread B: bisher = zaehler.get(paar, 0)     # liest auch 3
    Thread A: zaehler[paar] = bisher + 1        # schreibt 4
    Thread B: zaehler[paar] = bisher + 1        # schreibt auch 4, nicht 5

Das heißt Race Condition (Wettlaufsituation): Das Ergebnis hängt davon
ab, welcher Thread zufällig zuerst dran ist. Solche Fehler sind
tückisch, weil sie in kleinen Tests oft nicht auftreten und bei jedem
Lauf anders ausfallen. Probieren Sie es aus: Mit zaehle_faelle und
einem AlterZaehler in vier Threads mit je tausend Übergängen fehlt der
größte Teil.

Abhilfe ist eine Sperre (englisch lock, auch Mutex für „mutual
exclusion“, gegenseitiger Ausschluss). threading.Lock() kann immer nur
ein Thread zur Zeit halten; wer sie haben will, während ein anderer sie
hält, wartet. Den Abschnitt, in dem gelesen, gerechnet und geschrieben
wird (den kritischen Abschnitt), umschließt man mit der Sperre. Am
sichersten als Kontextmanager (Aufgabe 4_051), denn der gibt die Sperre
auch bei einer Ausnahme wieder frei:

    import threading

    class Konto:
        def __init__(self):
            self.stand = 0
            self.sperre = threading.Lock()

        def einzahlen(self, betrag):
            with self.sperre:            # wartet, bis die Sperre frei ist
                neu = self.stand + betrag
                self.stand = neu         # erst danach darf der Nächste lesen

sperre.acquire() und sperre.release() tun dasselbe von Hand; vergisst
man release (etwa weil vorher eine Ausnahme kommt), wartet jeder
weitere Thread für immer. Ein Lock lässt sich auch nicht zweimal vom
selben Thread nehmen; ruft eine Methode unter der Sperre eine andere
auf, die sie ebenfalls nimmt, hängt das Programm. Dafür gibt es
threading.RLock. Gesperrt wird so kurz wie möglich, aber so lange wie
nötig: Lesen und Schreiben müssen im selben Abschnitt stehen, sonst
hilft die Sperre nichts. Auch das Lesen für stand() gehört darunter,
damit niemand eine halb fertige Kopie sieht.
"""

import threading
import time


def pruefe_schritt(von, nach):
    """Prüft einen Übergang gegen den Prozesskatalog (hier nur nachgebildet; dabei kann ein anderer Thread drankommen)."""
    if not von or not nach:
        raise ValueError(f"leerer Prozessschritt im Übergang {von!r} → {nach!r}")
    time.sleep(0)  # die Anfrage an den Katalog gibt anderen Threads Gelegenheit zu laufen


class AlterZaehler:
    """Die bisherige Version: zählt richtig, solange nur ein Thread sie benutzt."""

    def __init__(self):
        """Legt den leeren Zähler an."""
        self.zaehler = {}

    def zaehle(self, von, nach):
        """Zählt den Übergang von → nach, ohne Sperre."""
        paar = (von, nach)
        bisher = self.zaehler.get(paar, 0)
        pruefe_schritt(von, nach)
        self.zaehler[paar] = bisher + 1


class Uebergaenge:
    """Ein threadsicherer Zähler für Übergänge zwischen Prozessschritten."""

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def zaehle_faelle(zaehler, faelle):
    """Zählt jeden Übergang zwischen zwei aufeinanderfolgenden Schritten jedes Falls."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def parallel_auswerten(standorte):
    """Wertet jeden Standort in einem eigenen Thread aus und gibt den gemeinsamen Stand zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


standorte = {
    "Hamburg": [
        ["eingang", "pruefung", "versand"],
        ["eingang", "pruefung", "rueckfrage", "pruefung", "versand"],
    ],
    "Leipzig": [["eingang", "pruefung", "versand"]],
    "Köln": [["eingang", "rueckfrage", "pruefung", "versand"]],
}
print(parallel_auswerten(standorte))
