# Automatisch erzeugt aus lehrkraft/muster/4_006_virtuelle_maschinen.py - nicht von Hand ändern.
# vorlage-hash: e31413cc018888e7

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

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "VM('web01', 4, 8192)\nVM('test07', 2, 4096)\nGpuVM('ki01', 16, 65536)"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
