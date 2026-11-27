# Automatisch erzeugt aus lehrkraft/muster/4_051_trainingslauf.py - nicht von Hand ändern.
# vorlage-hash: d69636ac29fcbf5f
# text-hash: 21b1cdbf23fac697
# thema: fehler
# inhalt: with, __enter__ und __exit__

def uhr_mit(*zeiten):
    """Eine Uhr, die nacheinander die angegebenen Zeiten liefert."""
    return iter(zeiten).__next__


class Testfehler(Exception):
    """Eine Ausnahme, die nur im Test vorkommt."""


def mit_fehler(manager):
    """Löst im with-Block einen Testfehler aus; gibt zurück, ob er nach außen kam, und was as bekam."""
    bekommen = []
    try:
        with manager as wert:
            bekommen.append(wert)
            raise Testfehler("Speicher voll")
    except Testfehler:
        return ("weitergeflogen", bekommen)
    except Exception as fehler:
        return (f"{type(fehler).__name__}: {fehler}", bekommen)
    return ("verschluckt", bekommen)


def ohne_fehler(manager, block=None):
    """Führt einen with-Block ohne Fehler aus; gibt (was as bekam, was der Block sah) oder einen Fehlertext zurück."""
    try:
        with manager as wert:
            gesehen = block(wert) if block else None
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"
    return (wert, gesehen)


# Schrittzeit im Beispiel: ein Eintrag im Protokoll
protokoll = []
ergebnis = ohne_fehler(Schrittzeit(protokoll, "laden", uhr=uhr_mit(10.0, 12.5)))
assert protokoll == [("laden", 2.5, "ok")], (
    f"Nach dem with-Block enthält protokoll {protokoll!r}, erwartet war [('laden', 2.5, 'ok')].\n"
    "Tipp: In __enter__ self.start = self.uhr(), in __exit__ die Differenz zur jetzigen Zeit."
)

# Schrittzeit mit anderen Zeiten und einem anderen Schritt (nicht fest hinschreiben!)
protokoll = [("laden", 2.5, "ok")]
ohne_fehler(Schrittzeit(protokoll, "trainieren", uhr=uhr_mit(100, 460)))
assert protokoll == [("laden", 2.5, "ok"), ("trainieren", 360, "ok")], (
    f"protokoll enthält {protokoll!r}, erwartet war [('laden', 2.5, 'ok'), ('trainieren', 360, 'ok')] (hinten anhängen)."
)

# Schrittzeit: with … as liefert das Objekt selbst
manager = Schrittzeit([], "bewerten", uhr=uhr_mit(0, 1))
ergebnis = ohne_fehler(manager)
assert isinstance(ergebnis, tuple) and ergebnis[0] is manager, (
    f"with Schrittzeit(...) as s liefert für s {ergebnis!r}, erwartet war das Schrittzeit-Objekt.\nTipp: __enter__ soll self zurückgeben."
)

# Schrittzeit: nach dem Block steht die Dauer im Attribut dauer
manager = Schrittzeit([], "bereinigen", uhr=uhr_mit(3.0, 4.25))
ohne_fehler(manager)
assert getattr(manager, "dauer", None) == 1.25, f"Nach dem with-Block ist dauer {getattr(manager, 'dauer', None)!r}, erwartet war 1.25."

# Schrittzeit: auch bei einem Fehler ein Eintrag mit status "fehler"
protokoll = []
ergebnis = mit_fehler(Schrittzeit(protokoll, "trainieren", uhr=uhr_mit(5, 9)))
assert protokoll == [("trainieren", 4, "fehler")], (
    f"Bei einem Fehler im Block enthält protokoll {protokoll!r}, erwartet war [('trainieren', 4, 'fehler')].\n"
    "Tipp: typ ist in __exit__ None, wenn der Block normal endete, sonst die Klasse der Ausnahme."
)

# Schrittzeit: die Ausnahme wird nicht verschluckt
assert ergebnis[0] == "weitergeflogen", (
    f"Der Testfehler aus dem Block wurde {ergebnis[0]}, erwartet war, dass er nach außen weiterfliegt.\n"
    "Tipp: __exit__ soll False (oder nichts) zurückgeben; True verschluckt die Ausnahme."
)

# Schrittzeit: ohne uhr wird time.perf_counter benutzt
protokoll = []
ergebnis = ohne_fehler(Schrittzeit(protokoll, "laden"))
assert len(protokoll) == 1 and isinstance(protokoll[0][1], float) and 0 <= protokoll[0][1] < 5, (
    f"Ohne uhr ergibt Schrittzeit das Protokoll {protokoll!r}; erwartet war ein Eintrag mit einer kleinen Dauer in Sekunden."
)

# Probeeinstellung im Beispiel: im Block gelten die Probewerte
einstellungen = {"lernrate": 0.1, "epochen": 20}
ergebnis = ohne_fehler(Probeeinstellung(einstellungen, lernrate=0.01, seed=7), lambda e: dict(e))
assert isinstance(ergebnis, tuple) and ergebnis[1] == {"lernrate": 0.01, "epochen": 20, "seed": 7}, (
    f"Im with-Block bekommt as {ergebnis!r}, erwartet war {{'lernrate': 0.01, 'epochen': 20, 'seed': 7}}.\n"
    "Tipp: Tragen Sie in __enter__ die Probewerte ein und geben Sie self.einstellungen zurück."
)

# Probeeinstellung im Beispiel: danach gelten wieder die alten Werte
assert einstellungen == {"lernrate": 0.1, "epochen": 20}, (
    f"Nach dem with-Block ist einstellungen {einstellungen!r}, erwartet war {{'lernrate': 0.1, 'epochen': 20}}.\n"
    "Tipp: Merken Sie sich in __enter__ die alten Werte und welche Schlüssel neu sind."
)

# Probeeinstellung: es bleibt dasselbe Dictionary-Objekt
assert ergebnis[0] is einstellungen, "as soll genau das übergebene Dictionary bekommen, keine Kopie."

# Probeeinstellung mit anderen Werten: nur geänderte Schlüssel (nicht fest hinschreiben!)
einstellungen = {"batch": 32, "optimierer": "adam", "dropout": 0.2}
ergebnis = ohne_fehler(Probeeinstellung(einstellungen, batch=64), lambda e: dict(e))
assert ergebnis[1] == {"batch": 64, "optimierer": "adam", "dropout": 0.2} and einstellungen == {
    "batch": 32,
    "optimierer": "adam",
    "dropout": 0.2,
}, f"Probeeinstellung mit batch=64 ergibt im Block {ergebnis[1]!r} und danach {einstellungen!r}."

# Probeeinstellung: ein alter Wert None wird wiederhergestellt, nicht gelöscht
einstellungen = {"seed": None, "epochen": 5}
ohne_fehler(Probeeinstellung(einstellungen, seed=42, epochen=1))
assert einstellungen == {"seed": None, "epochen": 5}, (
    f"Nach Probeeinstellung(…, seed=42, epochen=1) ist einstellungen {einstellungen!r}, erwartet war {{'seed': None, 'epochen': 5}}.\n"
    "Tipp: Merken Sie sich mit in, ob ein Schlüssel vorher da war; None kann ein echter alter Wert sein."
)

# Probeeinstellung: auch nach einem Fehler gelten wieder die alten Werte
einstellungen = {"lernrate": 0.1}
ergebnis = mit_fehler(Probeeinstellung(einstellungen, lernrate=5.0, gpu=2))
assert einstellungen == {"lernrate": 0.1}, (
    f"Nach einem Fehler im Block ist einstellungen {einstellungen!r}, erwartet war {{'lernrate': 0.1}}.\n"
    "Tipp: __exit__ wird auch bei einer Ausnahme aufgerufen; stellen Sie dort alles wieder her."
)

# Probeeinstellung: die Ausnahme wird nicht verschluckt
assert ergebnis[0] == "weitergeflogen", f"Der Testfehler aus dem Block wurde {ergebnis[0]}, erwartet war, dass er weiterfliegt."

# Probeeinstellung ohne Probewerte und mit leeren Einstellungen
einstellungen = {"a": 1}
leer = {}
ergebnis = [ohne_fehler(Probeeinstellung(einstellungen), lambda e: dict(e)), ohne_fehler(Probeeinstellung(leer, x=1), lambda e: dict(e))]
assert [ergebnis[0][1], einstellungen, ergebnis[1][1], leer] == [{"a": 1}, {"a": 1}, {"x": 1}, {}], (
    f"Probeeinstellung ohne Probewerte und auf einem leeren Dictionary ergibt {ergebnis!r}, danach {einstellungen!r} und {leer!r}."
)

# Probeeinstellung verschachtelt: der innere Block stellt die Werte des äußeren wieder her
einstellungen = {"lernrate": 0.1, "epochen": 20}
gesehen = []
with Probeeinstellung(einstellungen, lernrate=0.05):
    with Probeeinstellung(einstellungen, lernrate=0.001, seed=1):
        gesehen.append(dict(einstellungen))
    gesehen.append(dict(einstellungen))
gesehen.append(dict(einstellungen))
erwartet = [{"lernrate": 0.001, "epochen": 20, "seed": 1}, {"lernrate": 0.05, "epochen": 20}, {"lernrate": 0.1, "epochen": 20}]
assert gesehen == erwartet, f"Verschachtelt sieht man nacheinander {gesehen!r}, erwartet war {erwartet!r}."

# Beide zusammen: ein Trainingsschritt mit Probeeinstellung, der abbricht
protokoll = []
einstellungen = {"lernrate": 0.1}
try:
    with Schrittzeit(protokoll, "trainieren", uhr=uhr_mit(0, 30)), Probeeinstellung(einstellungen, lernrate=9.9):
        raise Testfehler("Verlust ist NaN")
except Testfehler:
    pass
assert protokoll == [("trainieren", 30, "fehler")] and einstellungen == {"lernrate": 0.1}, (
    f"Nach einem abgebrochenen Schritt ist protokoll {protokoll!r} und einstellungen {einstellungen!r}, "
    "erwartet war [('trainieren', 30, 'fehler')] und {'lernrate': 0.1}."
)

# Die Ausgabe des Programms
erwartet = "[('laden', 2.5, 'ok')]\n{'lernrate': 0.01, 'epochen': 20, 'seed': 7}\n{'lernrate': 0.1, 'epochen': 20}"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Einstellungen, Probewerte und Zeiten
zufall = Zufall(4051)
for runde in range(300):
    schluessel = ["lernrate", "epochen", "batch", "seed", "dropout", "gpu", "optimierer"]
    einstellungen = {name: zufall.choice([None, 0, 1, 0.5, "adam"]) for name in zufall.sample(schluessel, zufall.randint(0, 7))}
    vorher = dict(einstellungen)
    probewerte = {name: zufall.randint(-5, 5) for name in zufall.sample(schluessel, zufall.randint(0, 7))}
    erwartet_im_block = {**vorher, **probewerte}
    manager = Probeeinstellung(einstellungen, **probewerte)
    if runde % 2 == 0:
        ergebnis = ohne_fehler(manager, lambda e: dict(e))
        im_block = ergebnis[1] if isinstance(ergebnis, tuple) else ergebnis
        assert im_block == erwartet_im_block, f"Probeeinstellung({vorher}, **{probewerte}) ergibt im Block {im_block!r}, erwartet war {erwartet_im_block!r}."
    else:
        mit_fehler(manager)
    assert einstellungen == vorher, f"Probeeinstellung({vorher}, **{probewerte}) hinterlässt {einstellungen!r}, erwartet war {vorher!r}."
    start = zufall.randint(0, 10**6) / 4
    dauer = zufall.randint(0, 10**4) / 4
    protokoll = []
    if runde % 2 == 0:
        ohne_fehler(Schrittzeit(protokoll, f"schritt{runde}", uhr=uhr_mit(start, start + dauer)))
    else:
        mit_fehler(Schrittzeit(protokoll, f"schritt{runde}", uhr=uhr_mit(start, start + dauer)))
    erwartet = [(f"schritt{runde}", start + dauer - start, "ok" if runde % 2 == 0 else "fehler")]
    assert protokoll == erwartet, f"Schrittzeit mit Start {start} und Ende {start + dauer} ergibt {protokoll!r}, erwartet war {erwartet!r}."

# Obere Grenze: 10 000 Einstellungen, 1000 Probewerte
einstellungen = {f"p{nummer}": nummer for nummer in range(10000)}
probewerte = {f"p{nummer}": -1 for nummer in range(0, 20000, 20)}
ergebnis = mit_fehler(Probeeinstellung(einstellungen, **probewerte))
assert einstellungen == {f"p{nummer}": nummer for nummer in range(10000)}, "Bei 10 000 Einstellungen und 1000 Probewerten stimmt der Zustand danach nicht."
