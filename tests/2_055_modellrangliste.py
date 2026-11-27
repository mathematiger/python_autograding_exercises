# Automatisch erzeugt aus lehrkraft/muster/2_055_modellrangliste.py - nicht von Hand ändern.
# vorlage-hash: f38f088c40cf226b
# text-hash: fae89b82243a3fe2
# thema: algorithmen
# inhalt: Merge sortierter Listen

A = [("a3", 2.1), ("a1", 4.5), ("a2", 4.5), ("a4", 7.0)]
B = [("b2", 1.8), ("b1", 4.5), ("b3", 9.9)]


def ergebnis_von(rechner_a, rechner_b):
    """Ruft zusammenfuehren mit Kopien auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return zusammenfuehren(list(rechner_a), list(rechner_b))
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich(rechner_a, rechner_b):
    """Vergleichslösung: sortiert nach (Fehlerrate, Rechner, Stelle), also anders als verlangt."""
    markiert = [(rate, 0, stelle, name) for stelle, (name, rate) in enumerate(rechner_a)]
    markiert += [(rate, 1, stelle, name) for stelle, (name, rate) in enumerate(rechner_b)]
    return [(name, rate) for rate, _, _, name in sorted(markiert)]


def pruefe(rechner_a, rechner_b, hinweis=""):
    """Vergleicht zusammenfuehren mit der Vergleichslösung; liefert (stimmt, Meldung)."""
    ergebnis = ergebnis_von(rechner_a, rechner_b)
    erwartet = vergleich(rechner_a, rechner_b)
    text = f"zusammenfuehren({rechner_a}, {rechner_b})\nergibt   {ergebnis!r}\nerwartet {erwartet}"
    if isinstance(ergebnis, list) and len(ergebnis) == len(erwartet):
        for stelle, (ihr, soll) in enumerate(zip(ergebnis, erwartet)):
            if ihr != soll:
                text += f"\nErste Abweichung an Stelle {stelle}: {ihr!r} statt {soll!r}."
                break
    return ergebnis == erwartet, text + hinweis


def rangliste(zufall, buchstabe, laenge):
    """Erzeugt eine sortierte Rangliste mit Namen wie a0, a1, … und Fehlerraten mit einer Stelle."""
    raten = sorted(zufall.randint(0, 1000) / 10 for _ in range(laenge))
    return [(f"{buchstabe}{stelle}", rate) for stelle, rate in enumerate(raten)]


# Im Beispiel kommen alle sieben Paare heraus
ergebnis = ergebnis_von(A, B)
assert isinstance(ergebnis, list) and len(ergebnis) == 7, (
    f"zusammenfuehren(rechner_a, rechner_b) ergibt {ergebnis!r}, erwartet war eine Liste mit 7 Paaren.\n"
    "Tipp: Hängen Sie nach der ersten Schleife auch den Rest der Liste an, die noch nicht zu Ende ist."
)

# Im Beispiel sind die Fehlerraten aufsteigend
raten = [paar[1] for paar in ergebnis] if isinstance(ergebnis, list) else ergebnis
assert raten == [1.8, 2.1, 4.5, 4.5, 4.5, 7.0, 9.9], (
    f"Die Fehlerraten im Ergebnis sind {raten}, erwartet war [1.8, 2.1, 4.5, 4.5, 4.5, 7.0, 9.9].\n"
    "Tipp: Vergleichen Sie die Fehlerraten rechner_a[i][1] und rechner_b[j][1], nicht die Namen."
)

# Das Beispiel vollständig, mit Gleichstand bei 4.5
stimmt, text = pruefe(
    A, B, "\nTipp: Bei gleicher Fehlerrate kommt das Paar von Rechner A zuerst, also <= statt <."
)
assert stimmt, text

# Zwei andere Ranglisten (nicht fest hinschreiben!)
stimmt, text = pruefe([("x1", 0.5), ("x2", 3.0)], [("y1", 1.0), ("y2", 2.0), ("y3", 4.0)])
assert stimmt, text

# Alle Paare von B sind besser als die von A
stimmt, text = pruefe([("a1", 50.0), ("a2", 60.0)], [("b1", 10.0), ("b2", 20.0), ("b3", 30.0)])
assert stimmt, text

# Alle Paare von A sind besser als die von B
stimmt, text = pruefe([("a1", 1.0), ("a2", 2.0), ("a3", 3.0)], [("b1", 10.0)])
assert stimmt, text

# Gleichstand über mehrere Paare: A vor B, jede Liste in ihrer Reihenfolge
stimmt, text = pruefe(
    [("a1", 5.0), ("a2", 5.0)], [("b1", 5.0), ("b2", 5.0)],
    "\nTipp: Bei Gleichstand wählen Sie das Paar aus rechner_a.",
)
assert stimmt, text

# Die übergebenen Listen bleiben unverändert
a = list(A)
b = list(B)
try:
    zusammenfuehren(a, b)
except Exception:
    pass
assert a == A and b == B, (
    f"Nach dem Aufruf ist rechner_a {a} und rechner_b {b}; beide sollten unverändert bleiben.\n"
    "Tipp: Lesen Sie mit Stellen i und j, statt mit pop zu entfernen."
)

# Randfall: Rechner A liefert nichts
stimmt, text = pruefe([], B)
assert stimmt, text

# Randfall: Rechner B liefert nichts
stimmt, text = pruefe(A, [])
assert stimmt, text

# Randfall: beide leer
stimmt, text = pruefe([], [])
assert stimmt, text

# Randfall: Fehlerraten 0 und 100
stimmt, text = pruefe([("a1", 0.0), ("a2", 100.0)], [("b1", 0.0), ("b2", 100.0)])
assert stimmt, text

# Auch bei einer leeren Liste eine neue Liste, nicht die übergebene
b = list(B)
try:
    ergebnis = zusammenfuehren([], b)
except Exception as fehler:
    ergebnis = f"{type(fehler).__name__}: {fehler}"
assert ergebnis is not b, (
    "zusammenfuehren([], rechner_b) gibt rechner_b selbst zurück, erwartet war eine neue Liste.\n"
    "Tipp: Wer das Ergebnis später ändert, würde sonst auch die Rangliste von Rechner B ändern."
)

# Ohne sort() und sorted()
verboten = [name for name in ["sort", "sorted"] if verwendet(name)]
assert verboten == [], f"Ihr Code verwendet {verboten}. Führen Sie die Listen mit zwei Stellen i und j zusammen."

# Die Ausgabe des Programms
erwartet = str(vergleich(A, B))
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Ranglisten
zufall = Zufall(2055)
for _ in range(300):
    a = rangliste(zufall, "a", zufall.randint(0, 8))
    b = rangliste(zufall, "b", zufall.randint(0, 8))
    stimmt, text = pruefe(a, b)
    assert stimmt, text

# Laufzeit: jede Liste nur einmal durchgehen
a = rangliste(zufall, "a", 2000)
b = rangliste(zufall, "b", 2000)
try:
    _, schritte = zaehle_schritte(zusammenfuehren, a, b)
except Exception as fehler:
    schritte = f"(Abbruch: {type(fehler).__name__}: {fehler})"
assert isinstance(schritte, int) and schritte <= 20 * 4000, (
    f"Für zweimal 2000 Paare braucht Ihre Lösung {schritte} Schritte, erlaubt sind 20 · 4000 = 80000.\n"
    "Tipp: Suchen Sie nicht für jedes Paar die passende Stelle im Ergebnis, sondern vergleichen Sie nur die "
    "beiden vordersten Paare, die noch fehlen."
)

# Obere Grenze: zweimal 50 000 Paare
a = rangliste(zufall, "a", 50000)
b = rangliste(zufall, "b", 50000)
ergebnis = ergebnis_von(a, b)
erwartet = vergleich(a, b)
abweichung = "–"
if isinstance(ergebnis, list):
    for stelle, (ihr, soll) in enumerate(zip(ergebnis, erwartet)):
        if ihr != soll:
            abweichung = f"Stelle {stelle}: {ihr!r} statt {soll!r}"
            break
assert ergebnis == erwartet, (
    f"Bei zweimal 50 000 Paaren stimmt das Ergebnis nicht: {len(ergebnis) if isinstance(ergebnis, list) else ergebnis!r} "
    f"statt {len(erwartet)} Paaren, erste Abweichung: {abweichung}."
)
