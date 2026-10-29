# Automatisch erzeugt aus lehrkraft/muster/4_007_virtuelle_maschinen.py - nicht von Hand ändern.
# vorlage-hash: 8d45c883e939f33f
# text-hash: d514177d448cff5b
# thema: klassen
# inhalt: `classmethod` als Konstruktor

# aus_zeile erzeugt eine VM mit den Werten aus der Zeile
vm = VM.aus_zeile("web01;4;8192")
assert isinstance(vm, VM) and (vm.name, vm.vcpus, vm.ram_mib) == ("web01", 4, 8192), (
    f'VM.aus_zeile("web01;4;8192") ergibt {vm!r}, erwartet war VM(\'web01\', 4, 8192).\n'
    "Tipp: Zerlegen Sie die Zeile mit split, wandeln Sie die Zahlen mit int um und geben Sie cls(...) zurück."
)

# Weitere Zeilen (nicht fest hinschreiben!)
for zeile, erwartet in [
    ("db02;8;32768", ("db02", 8, 32768)),
    ("mail;2;4096", ("mail", 2, 4096)),
    ("backup-03;1;1024", ("backup-03", 1, 1024)),
]:
    vm = VM.aus_zeile(zeile)
    assert isinstance(vm, VM) and (vm.name, vm.vcpus, vm.ram_mib) == erwartet, (
        f"VM.aus_zeile({zeile!r}) ergibt {vm!r}, erwartet war eine VM mit Name, vCPUs und Speicher {erwartet}."
    )

# Zahlen werden als int gespeichert, nicht als Text
vm = VM.aus_zeile("web01;4;8192")
assert type(vm.vcpus) is int and type(vm.ram_mib) is int, (
    f"Nach VM.aus_zeile('web01;4;8192') ist vcpus {vm.vcpus!r} und ram_mib {vm.ram_mib!r}; erwartet waren Zahlen.\n"
    "Tipp: Wandeln Sie die Felder mit int(...) um."
)

# Leerzeichen um die Felder werden ignoriert
vm = VM.aus_zeile(" db02 ; 8 ; 32768")
assert (vm.name, vm.vcpus, vm.ram_mib) == ("db02", 8, 32768), (
    f'VM.aus_zeile(" db02 ; 8 ; 32768") ergibt {vm!r}, erwartet war VM(\'db02\', 8, 32768).\n'
    "Tipp: Entfernen Sie beim Namen die Leerzeichen mit strip()."
)

# Zu wenige oder zu viele Felder lösen ValueError aus
for zeile in ["web01;4", "web01;4;8192;ssd", "web01"]:
    try:
        vm = VM.aus_zeile(zeile)
        fehler = None
    except ValueError as ausnahme:
        fehler = ausnahme
    assert fehler is not None, (
        f"VM.aus_zeile({zeile!r}) muss einen ValueError auslösen, ergab aber {vm!r}.\n"
        "Tipp: Prüfen Sie mit len(...), ob split genau drei Felder geliefert hat."
    )

# Die Prüfungen aus __init__ gelten auch für aus_zeile
try:
    vm = VM.aus_zeile("web01;0;8192")
    fehler = None
except ValueError as ausnahme:
    fehler = ausnahme
assert fehler is not None, (
    f"VM.aus_zeile('web01;0;8192') muss einen ValueError auslösen (0 vCPUs), ergab aber {vm!r}.\n"
    "Tipp: Erzeugen Sie das Objekt mit cls(...), dann prüft __init__ die Werte."
)

# aus_katalog nimmt die Werte aus dem KATALOG
for name, groesse, erwartet in [
    ("test07", "M", ("test07", 2, 4096)),
    ("klein", "S", ("klein", 1, 2048)),
    ("gross", "XL", ("gross", 8, 16384)),
]:
    vm = VM.aus_katalog(name, groesse)
    assert isinstance(vm, VM) and (vm.name, vm.vcpus, vm.ram_mib) == erwartet, (
        f"VM.aus_katalog({name!r}, {groesse!r}) ergibt {vm!r}, erwartet war eine VM mit {erwartet}.\n"
        "Tipp: cls.KATALOG[groesse] liefert das Paar (vcpus, ram_mib)."
    )

# Eine unbekannte Größe löst ValueError aus
try:
    vm = VM.aus_katalog("test07", "XXL")
    fehler = None
except ValueError as ausnahme:
    fehler = ausnahme
except KeyError as ausnahme:
    fehler = ausnahme
assert isinstance(fehler, ValueError), (
    f"VM.aus_katalog('test07', 'XXL') muss einen ValueError auslösen; aufgetreten ist: {fehler!r} (None heißt: keine Ausnahme).\n"
    "Tipp: Ein unbekannter Schlüssel im Dictionary löst einen KeyError aus. Prüfen Sie vorher mit in."
)

# Auf einer Unterklasse entsteht ein Objekt der Unterklasse
vm = GpuVM.aus_zeile("ki01;16;65536")
assert type(vm) is GpuVM and (vm.name, vm.vcpus, vm.ram_mib) == ("ki01", 16, 65536), (
    f'GpuVM.aus_zeile("ki01;16;65536") ergibt {vm!r}, erwartet war GpuVM(\'ki01\', 16, 65536).\n'
    "Tipp: Schreiben Sie cls(...) statt VM(...)."
)

# Die Unterklasse benutzt ihren eigenen KATALOG
vm = GpuVM.aus_katalog("ki02", "M")
assert type(vm) is GpuVM and (vm.vcpus, vm.ram_mib) == (4, 16384), (
    f'GpuVM.aus_katalog("ki02", "M") ergibt {vm!r}, erwartet war GpuVM(\'ki02\', 4, 16384).\n'
    "Tipp: Schreiben Sie cls.KATALOG statt VM.KATALOG und cls(...) statt VM(...)."
)

# Größen, die es nur im Katalog der Oberklasse gibt, sind für die Unterklasse unbekannt
try:
    vm = GpuVM.aus_katalog("ki03", "S")
    fehler = None
except ValueError as ausnahme:
    fehler = ausnahme
except KeyError as ausnahme:
    fehler = ausnahme
assert isinstance(fehler, ValueError), (
    f"GpuVM.aus_katalog('ki03', 'S') muss einen ValueError auslösen, denn GpuVM.KATALOG kennt kein S; aufgetreten ist: {fehler!r} (None heißt: keine Ausnahme).\n"
    "Tipp: Prüfen Sie die Größe in cls.KATALOG, nicht in VM.KATALOG."
)

# Größte erlaubte Werte
vm = VM.aus_zeile("riesig;1024;4194304")
assert (vm.name, vm.vcpus, vm.ram_mib) == ("riesig", 1024, 4194304), (
    f'VM.aus_zeile("riesig;1024;4194304") ergibt {vm!r}, erwartet war VM(\'riesig\', 1024, 4194304).'
)

# Viele zufällige Zeilen für VM und GpuVM, mit Leerzeichen und falscher Feldzahl
zufall = Zufall(4006)
fehlerfall = None
for versuch in range(500):
    klasse = zufall.choice([VM, GpuVM])
    name = "".join(zufall.choice("abcxyz019-") for _ in range(zufall.randint(1, 6)))
    werte = [name, str(zufall.randint(1, 1024)), str(zufall.randint(1, 4194304))]
    anzahl = zufall.choice([1, 2, 3, 3, 3, 4, 5])
    felder = (werte + ["ssd", "x"])[:anzahl]
    zeile = ";".join(" " * zufall.randint(0, 2) + feld + " " * zufall.randint(0, 2) for feld in felder)
    try:
        vm = klasse.aus_zeile(zeile)
        bekommen = (type(vm).__name__, vm.name, vm.vcpus, vm.ram_mib)
    except ValueError:
        bekommen = "ValueError"
    erwartet = (klasse.__name__, name, int(werte[1]), int(werte[2])) if anzahl == 3 else "ValueError"
    if bekommen != erwartet:
        fehlerfall = f"{klasse.__name__}.aus_zeile({zeile!r}) ergibt {bekommen!r}, erwartet war {erwartet!r} (Klasse, Name, vCPUs, Speicher)."
        break
assert fehlerfall is None, fehlerfall

# Viele zufällige Katalog-Bestellungen für VM und GpuVM, auch mit unbekannten Größen
zufall = Zufall(40062)
fehlerfall = None
for versuch in range(300):
    klasse = zufall.choice([VM, GpuVM])
    groesse = zufall.choice(["S", "M", "L", "XL", "XXL", "m", ""])
    try:
        vm = klasse.aus_katalog("vm", groesse)
        bekommen = (type(vm).__name__, vm.vcpus, vm.ram_mib)
    except ValueError:
        bekommen = "ValueError"
    except KeyError:
        bekommen = "KeyError"
    erwartet = (klasse.__name__, *klasse.KATALOG[groesse]) if groesse in klasse.KATALOG else "ValueError"
    if bekommen != erwartet:
        fehlerfall = f"{klasse.__name__}.aus_katalog('vm', {groesse!r}) ergibt {bekommen!r}, erwartet war {erwartet!r} (Klasse, vCPUs, Speicher)."
        break
assert fehlerfall is None, fehlerfall

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "VM('web01', 4, 8192)\nVM('test07', 2, 4096)\nGpuVM('ki01', 16, 65536)"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
