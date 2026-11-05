# Klasse für ein Modul, für Noten, ETCS und Fortschritt
class Modul:
    def __init__(self, name, ects, kapitel_gesamt, kapitel_erledigt, pruefungsleistung=None):
        self.name = name
        self.ects = ects
        self.kapitel_gesamt = kapitel_gesamt
        self.kapitel_erledigt = kapitel_erledigt
        # Ist am Anfang None, weil die Note erst nach der Prüfung eingetragen wird
        self.pruefungsleistung = pruefungsleistung

    def berechne_fortschritt(self):
        # Falls keine Kapitel vorhanden sind, beträgt der Fortschritt 0 %
        if self.kapitel_gesamt == 0:
            return 0

        # Fortschritt anhand der erledigten Kapitel berechnen in %
        return (self.kapitel_erledigt / self.kapitel_gesamt) * 100