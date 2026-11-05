# Klasse für ein Semester mit Nummer und Modulen
class Semester:
    def __init__(self, nummer, module):
        self.nummer = nummer
        self.module = module

    def berechne_durchschnitt(self):
        # Noten und zugehörige ECTS sammeln
        noten = []

        for modul in self.module:
            if modul.pruefungsleistung is not None:
                noten.append(
                    (modul.pruefungsleistung.note, modul.ects)
                )

        # Falls noch keine Prüfung vorhanden ist 0.0 zurückgeben
        if not noten:
            return 0.0

        # ECTS-gewichteten Durchschnitt berechnen
        gesamt = sum(note * ects for note, ects in noten)
        ects_summe = sum(ects for _, ects in noten)

        return gesamt / ects_summe