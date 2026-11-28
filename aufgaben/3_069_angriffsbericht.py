"""Aufgabe 3_069 – Angriffsbericht                               Stufe 3 ★★★☆☆

Ein kleines Sicherheitsteam überwacht den Webserver eines Kunden mit
einem Angriffserkennungssystem (englisch Intrusion Detection System,
IDS). Das IDS erkennt verdächtige Anfragen, etwa Versuche, über ein
Formular Datenbankbefehle einzuschleusen, und schreibt mit. Einmal pro
Woche entsteht daraus ein Bericht für den Kunden. Bisher rechnet ein
Skript mit verschachtelten Schleifen; seit das IDS an einem viel
besuchten Shop hängt, läuft es stundenlang. Schreiben Sie die drei
Funktionen des Berichts neu, sodass jede auch an den Grenzen schnell
ist:

- `neue_angreifer(angreifer, sperrliste)` bekommt die Adressen, von
  denen in dieser Woche Angriffe kamen (eine Adresse kann oft vorkommen),
  und die Sperrliste der Firewall. Sie gibt die Adressen zurück, die
  angegriffen haben, aber noch nicht gesperrt sind: jede nur einmal,
  alphabetisch sortiert.
- `geblockt_im_zeitraum(geblockt, anfragen)` bekommt eine Liste, in der
  geblockt[m] die Zahl der in Minute m abgewiesenen Anfragen ist, und
  eine Liste von Zeiträumen (von, bis), beide Minuten eingeschlossen.
  Sie gibt eine Liste mit der Summe der abgewiesenen Anfragen für jeden
  Zeitraum zurück, in derselben Reihenfolge.
- `kuerzestes_fenster(zeitpunkte, k)` bekommt die Zeitpunkte aller
  Alarme in Sekunden seit Wochenbeginn. Sie kommen von mehreren Sensoren
  und sind deshalb nicht sortiert. Die Funktion gibt die Länge der
  kürzesten Zeitspanne zurück, in der k Alarme liegen (Zeitpunkt des
  letzten minus Zeitpunkt des ersten dieser Alarme), oder None, wenn es
  weniger als k Alarme gibt. Je kürzer, desto heftiger war der Angriff.

    angreifer = ["203.0.113.7", "198.51.100.23", "203.0.113.7",
                 "192.0.2.44", "198.51.100.23", "203.0.113.90"]
    sperrliste = ["192.0.2.44", "203.0.113.90", "198.51.100.1"]
    neue_angreifer(angreifer, sperrliste)   →  ["198.51.100.23", "203.0.113.7"]

    geblockt = [4, 0, 12, 30, 7, 0, 0, 25]
    geblockt_im_zeitraum(geblockt, [(2, 4), (0, 7), (5, 6)])   →  [49, 78, 0]

    zeitpunkte = [500, 130, 910, 140, 125, 600, 610, 620]
    kuerzestes_fenster(zeitpunkte, 3)       →  15     (125, 130, 140)
    kuerzestes_fenster(zeitpunkte, 4)       →  120    (500, 600, 610, 620)
    kuerzestes_fenster(zeitpunkte, 9)       →  None

Grenzen: angreifer und sperrliste haben je 0 bis 100 000 Einträge, jeder
ist eine IPv4-Adresse als Text wie "203.0.113.7"; in beiden Listen sind
Doppelte möglich. geblockt hat 1 bis 100 000 Einträge, ganze Zahlen von
0 bis 10**6. anfragen hat 0 bis 100 000 Einträge, für jeden gilt
0 ≤ von ≤ bis < len(geblockt). zeitpunkte hat 0 bis 100 000 Einträge,
ganze Zahlen von 0 bis 10**9, Doppelte möglich (zwei Sensoren schlagen
in derselben Sekunde an); 1 ≤ k ≤ 100 000. Jede Funktion soll höchstens
O(n log n) Schritte brauchen, wobei n die Länge aller Eingaben zusammen
ist; geblockt_im_zeitraum sogar nur O(n), neue_angreifer O(n) bis auf
das Sortieren des Ergebnisses.

Hintergrund: In den letzten Aufgaben haben Sie mehrere Muster kennen-
gelernt, mit denen eine naive O(n²)-Lösung (Aufgabe 3_006) schnell wird.
Hier müssen Sie selbst wählen, welches zu welcher Frage passt:

- Menge (Aufgabe 3_063): x in menge kostet im Mittel O(1), x in liste
  dagegen O(n). Wer viele Fragen „kommt das vor?“ an dieselbe Liste
  stellt, macht sie vorher einmal zur Menge. Auch Doppelte verschwinden
  so (Aufgaben 2_028 und 3_019).
- Präfixsummen (Aufgabe 3_062): Wer viele Bereichssummen derselben
  Liste braucht, rechnet einmal summe[i] = Summe der ersten i Werte aus;
  danach ist jede Bereichssumme eine Subtraktion.
- Sortieren und dann einmal durchgehen (Aufgaben 3_064, 3_065): Nach
  dem Sortieren stehen zusammengehörige Werte nebeneinander. sorted
  kostet O(n log n), der Durchgang danach O(n).
- Zwei Zeiger und Sliding Window (Aufgaben 3_060, 3_061): In einer
  sortierten Liste wandern zwei Positionen nur vorwärts; ein Fenster
  fester Breite schiebt man Schritt für Schritt weiter, statt jedes Mal
  neu anzufangen.

Für jede Frage lohnt sich ein kurzer Blick auf die Grenzen: Bei 100 000
Einträgen sind O(n²) zehn Milliarden Schritte, O(n log n) nur etwa zwei
Millionen.
"""


def neue_angreifer(angreifer, sperrliste):
    """Gibt die angreifenden Adressen ohne Doppelte, die nicht auf der Sperrliste stehen, sortiert zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def geblockt_im_zeitraum(geblockt, anfragen):
    """Gibt für jeden Zeitraum (von, bis) die Summe der abgewiesenen Anfragen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def kuerzestes_fenster(zeitpunkte, k):
    """Gibt die kürzeste Zeitspanne zurück, in der k Alarme liegen, oder None bei weniger als k Alarmen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


angreifer = ["203.0.113.7", "198.51.100.23", "203.0.113.7", "192.0.2.44", "198.51.100.23", "203.0.113.90"]
sperrliste = ["192.0.2.44", "203.0.113.90", "198.51.100.1"]
print(neue_angreifer(angreifer, sperrliste))
print(geblockt_im_zeitraum([4, 0, 12, 30, 7, 0, 0, 25], [(2, 4), (0, 7), (5, 6)]))
print(kuerzestes_fenster([500, 130, 910, 140, 125, 600, 610, 620], 3))
