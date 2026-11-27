"""Aufgabe 2_051 – Datenkontingent                               Stufe 2 ★★☆☆☆

Eine Außenstelle ist nur über einen Mobilfunk-Router ans Firmennetz
angebunden. Der Vertrag enthält ein Datenkontingent: So viele Gigabyte
(GB) dürfen in einem Kalendermonat übertragen werden, danach wird die
Verbindung stark gedrosselt. Damit das nicht passiert, warnt das
Monitoring, sobald an einem Tag mehr als der Tagesanteil verbraucht
wird: das Kontingent geteilt durch die Zahl der Tage dieses Monats.
Dafür braucht es die Tage im Monat, und im Februar hängen die vom
Schaltjahr ab. Schreiben Sie drei Funktionen:

- `ist_schaltjahr(jahr)` gibt True zurück, wenn jahr ein Schaltjahr ist,
  sonst False (Regeln im Hintergrund).
- `tage_im_monat(jahr, monat)` gibt die Zahl der Tage des Monats zurück
  (monat 1 ist Januar, 12 ist Dezember).
- `tagesanteil(kontingent, jahr, monat)` gibt das Kontingent geteilt
  durch die Tage dieses Monats zurück.

Benutzen Sie dafür nicht die Module calendar oder datetime.

    ist_schaltjahr(2024)          →  True
    ist_schaltjahr(1900)          →  False
    tage_im_monat(2024, 2)        →  29
    tage_im_monat(2025, 4)        →  30
    tagesanteil(300, 2025, 4)     →  10.0

Grenzen: 1 ≤ jahr ≤ 9999, 1 ≤ monat ≤ 12, kontingent ist eine ganze
Zahl mit 0 ≤ kontingent ≤ 100 000.

Hintergrund: Ein Jahr dauert etwa 365,2425 Tage. Damit der Kalender
nicht wegläuft, hat der Februar in Schaltjahren 29 statt 28 Tage. Die
Regeln des heutigen (gregorianischen) Kalenders: Ein Jahr ist ein
Schaltjahr, wenn es durch 4 teilbar ist, außer es ist durch 100
teilbar; durch 400 teilbare Jahre sind aber doch Schaltjahre. Also ist
2024 eins, 2023 nicht, 1900 nicht und 2000 schon. Ob eine Zahl durch
eine andere teilbar ist, prüft man mit dem Rest (Aufgabe 1_005):
jahr % 4 == 0. Mehrere Bedingungen verknüpft man mit and, or und not
(Aufgabe 1_020); Klammern machen klar, was zusammengehört:

    (a % 4 == 0 and a % 100 != 0) or a % 400 == 0

Die übrigen Monate haben immer gleich viele Tage: April, Juni,
September und November haben 30, alle anderen außer dem Februar 31.

Tipp: Mit in und einer Liste prüft man mehrere Monate auf einmal (Aufgabe
1_030): monat in [4, 6, 9, 11].
"""


def ist_schaltjahr(jahr):
    """Gibt True zurück, wenn jahr ein Schaltjahr ist."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def tage_im_monat(jahr, monat):
    """Gibt die Zahl der Tage des Monats im angegebenen Jahr zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def tagesanteil(kontingent, jahr, monat):
    """Gibt das Kontingent geteilt durch die Tage des Monats zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(ist_schaltjahr(2024))
print(ist_schaltjahr(1900))
print(tage_im_monat(2024, 2))
print(tage_im_monat(2025, 4))
print(tagesanteil(300, 2025, 4))
