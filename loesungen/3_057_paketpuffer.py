# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_057_paketpuffer.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_057_paketpuffer

"""Aufgabe 3_057 – Paketpuffer                                   Stufe 3 ★★★☆☆

Ein Router nimmt Datenpakete an einem schnellen Anschluss entgegen und
schickt sie über eine langsamere Leitung weiter. Kommen mehr Pakete an,
als er weiterschicken kann, legt er sie in einen Puffer, eine
Warteschlange mit begrenztem Platz. Ist der Puffer voll, wirft er jedes
weitere ankommende Paket weg (englisch tail drop: das Ende der Schlange
wird abgeschnitten). Die Netzwerkabteilung möchte für eine Leitung
nachrechnen, welche Pakete verloren gehen und wie lange die übrigen
warten. Dazu wird die Zeit in Takte eingeteilt:

- ankuenfte[t] ist die Liste der Pakete (ihre Namen), die im Takt t
  ankommen, in der Reihenfolge ihrer Ankunft.
- In jedem Takt t stellen sich zuerst die neuen Pakete einzeln hinten
  an. Liegen schon platz Pakete im Puffer, wird das neue Paket
  verworfen.
- Danach schickt der Router das vorderste Paket des Puffers weiter,
  falls einer darin liegt. Das Paket ist dann im Takt t gesendet.
- Nach dem letzten Takt von ankuenfte kommt nichts mehr an, der Router
  sendet aber in den folgenden Takten weiter, bis der Puffer leer ist.

Schreiben Sie zwei Funktionen:

- `weiterleiten(ankuenfte, platz)` gibt das Tupel (gesendet, verworfen)
  zurück: gesendet ist die Liste der Paare (takt, name) in der
  Reihenfolge des Sendens, verworfen die Liste der Namen der verworfenen
  Pakete in der Reihenfolge ihrer Ankunft. Benutzen Sie für den Puffer
  eine collections.deque.
- `wartezeiten(ankuenfte, platz)` gibt ein Dictionary zurück, das jedem
  gesendeten Paket die Zahl der Takte zuordnet, die es gewartet hat:
  Sendetakt minus Ankunftstakt. Benutzen Sie dafür weiterleiten.

    ankuenfte = [["a", "b", "c"], [], ["d", "e"], ["f"]]
    weiterleiten(ankuenfte, 2)
    →  ([(0, "a"), (1, "b"), (2, "d"), (3, "e"), (4, "f")], ["c"])
    wartezeiten(ankuenfte, 2)
    →  {"a": 0, "b": 1, "d": 0, "e": 1, "f": 1}

Im Takt 0 passen a und b in den Puffer, c wird verworfen; a wird sofort
gesendet. Im Takt 4 kommt nichts mehr an, f wird trotzdem noch gesendet.

Grenzen: ankuenfte hat 0 bis 10 000 Takte, insgesamt kommen 0 bis
100 000 Pakete an, ein Takt kann auch leer sein. Die Namen sind
verschiedene, nicht leere Texte. platz ist eine ganze Zahl von 1 bis
100 000. Ihre Lösung soll O(Takte + Pakete) Schritte brauchen.

Hintergrund: Eine Warteschlange (englisch Queue) arbeitet umgekehrt wie
der Stapel aus Aufgabe 3_056: Was zuerst hineinkommt, kommt zuerst
wieder heraus („first in, first out“), wie an einer Kasse. Mit einer
Liste ginge das über append und pop(0), aber pop(0) muss alle übrigen
Einträge um einen Platz nach vorn schieben; bei 100 000 wartenden
Paketen sind das 100 000 Schritte für ein einziges Paket. Das Modul
collections hat dafür die deque („double-ended queue“, sprich „deck“),
die an beiden Enden in einem Schritt anhängt und wegnimmt:

    from collections import deque

    schlange = deque()
    schlange.append("a")       # hinten anstellen:   deque(['a'])
    schlange.append("b")       #                     deque(['a', 'b'])
    schlange.popleft()         # vorn wegnehmen:     'a'
    len(schlange)              # 1
    schlange[0]                # das vorderste:      'b'

Eine leere deque ist wie eine leere Liste falsch, if schlange: fragt
also, ob noch etwas wartet; popleft() auf eine leere deque löst einen
IndexError aus. Für die Simulation merkt man sich im Puffer am besten
Paare (ankunftstakt, name); dann braucht wartezeiten nichts zu suchen.
Die Paare aus weiterleiten zerlegt eine Schleife for takt, name in
gesendet: wie bei enumerate (Aufgabe 2_021). Später, in Aufgabe 4_062, lernen Sie noch
maxlen und rotate kennen; maxlen hilft hier nicht, denn eine volle deque
mit maxlen wirft beim Anhängen das vorderste, älteste Paket hinaus, der
Router aber das neue.

Tipp: Gehen Sie die Takte mit einer while-Schleife durch, die läuft,
solange noch Takte von ankuenfte übrig sind oder der Puffer nicht leer
ist.
"""

from collections import deque


def weiterleiten(ankuenfte, platz):
    """Simuliert den Puffer und gibt (gesendet, verworfen) zurück."""
    puffer = deque()
    gesendet = []
    verworfen = []
    takt = 0
    while takt < len(ankuenfte) or puffer:
        if takt < len(ankuenfte):
            for name in ankuenfte[takt]:
                if len(puffer) < platz:
                    puffer.append(name)
                else:
                    verworfen.append(name)
        if puffer:
            gesendet.append((takt, puffer.popleft()))
        takt += 1
    return gesendet, verworfen


def wartezeiten(ankuenfte, platz):
    """Gibt für jedes gesendete Paket zurück, wie viele Takte es gewartet hat."""
    ankunft = {}
    for takt in range(len(ankuenfte)):
        for name in ankuenfte[takt]:
            ankunft[name] = takt
    gesendet, _ = weiterleiten(ankuenfte, platz)
    warten = {}
    for takt, name in gesendet:
        warten[name] = takt - ankunft[name]
    return warten


ankuenfte = [["a", "b", "c"], [], ["d", "e"], ["f"]]
print(weiterleiten(ankuenfte, 2))
print(wartezeiten(ankuenfte, 2))


# Idee: Eine deque ist der Puffer, eine while-Schleife zählt die Takte hoch, solange noch Takte von
# ankuenfte übrig sind oder etwas im Puffer liegt. In jedem Takt stellt sich jedes neue Paket mit append
# hinten an, wenn len(puffer) < platz ist, sonst kommt es in verworfen; danach nimmt popleft() das
# vorderste Paket und schreibt (takt, name) in gesendet. wartezeiten merkt sich in einem Dictionary den
# Ankunftstakt jedes Namens und zieht ihn vom Sendetakt ab.
# Anderer Weg: Paare (ankunftstakt, name) in den Puffer legen; dann kann weiterleiten die Wartezeiten
# gleich mitberechnen. Naiv wäre eine Liste mit pop(0): Jedes Senden verschiebt alle wartenden Pakete,
# bei einem vollen Puffer mit p Plätzen also O(Pakete · p).
# Typische Fehler: pop() statt popleft() (dann ist es ein Stapel), deque(maxlen=platz) (wirft das älteste
# statt des neuen Pakets hinaus), erst senden und dann anstellen, nach dem letzten Takt aufhören, obwohl
# noch Pakete warten.
# Laufzeit: O(Takte + Pakete), denn jedes Paket wird einmal angehängt und einmal weggenommen, beides O(1).
