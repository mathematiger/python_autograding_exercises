# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_051_datenkontingent.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_051_datenkontingent

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

Tipp: Mit in und einer Liste prüft man mehrere Monate auf einmal:
monat in [4, 6, 9, 11].
"""


def ist_schaltjahr(jahr):
    """Gibt True zurück, wenn jahr ein Schaltjahr ist."""
    return (jahr % 4 == 0 and jahr % 100 != 0) or jahr % 400 == 0


def tage_im_monat(jahr, monat):
    """Gibt die Zahl der Tage des Monats im angegebenen Jahr zurück."""
    if monat == 2:
        if ist_schaltjahr(jahr):
            return 29
        return 28
    if monat in [4, 6, 9, 11]:
        return 30
    return 31


def tagesanteil(kontingent, jahr, monat):
    """Gibt das Kontingent geteilt durch die Tage des Monats zurück."""
    return kontingent / tage_im_monat(jahr, monat)


print(ist_schaltjahr(2024))
print(ist_schaltjahr(1900))
print(tage_im_monat(2024, 2))
print(tage_im_monat(2025, 4))
print(tagesanteil(300, 2025, 4))


# Idee: Die drei Regeln stecken in einem Ausdruck: durch 4 und nicht durch 100 teilbar, oder durch
# 400 teilbar. tage_im_monat fragt zuerst nach dem Februar und benutzt dort ist_schaltjahr, dann
# nach den vier Monaten mit 30 Tagen; alle übrigen haben 31. tagesanteil teilt das Kontingent durch
# das Ergebnis von tage_im_monat.
# Anderer Weg: die Regeln als if-Kette von der seltensten her prüfen (durch 400 → True, durch 100 →
# False, durch 4 → True, sonst False), oder die Monatslängen in einer Liste ablegen:
# [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][monat - 1] und im Schaltjahr für den Februar 1
# dazuzählen. In echten Programmen nimmt man calendar.isleap und calendar.monthrange.
# Typische Fehler: nur jahr % 4 == 0 prüfen (1900 wird Schaltjahr), die Regel für 400 vergessen (2000
# wird keins), and und or ohne Klammern so mischen, dass etwas anderes herauskommt, oder Monate mit
# 30 Tagen verwechseln (Merkhilfe: die Fingerknöchel der Faust).
