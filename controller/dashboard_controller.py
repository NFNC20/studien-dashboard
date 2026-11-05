from repository.json_dashboard_repository import JsonDashboardRepository
from service.noten_service import NotenService
from service.fortschritts_service import FortschrittsService
from service.lernzeit_service import LernzeitService
from domain.pruefungsleistung import Pruefungsleistung
from domain.modul import Modul
from domain.semester import Semester


class DashboardController:

    def __init__(self):
        # Repository für das Speichern und Laden erzeugen
        self.repository = JsonDashboardRepository("data/dashboard.json")
        # Dashboard aus der JSON-Datei laden
        self.dashboard = self.repository.lade_dashboard()

        # Services erzeugen
        self.noten_service = NotenService()
        self.fortschritts_service = FortschrittsService()
        self.lernzeit_service = LernzeitService()

    # Gesamtdurchschnitt aller bewerteten Module berechnen
    def berechne_gesamtnotendurchschnitt(self):
        return self.noten_service.berechne_gesamtnotendurchschnitt(self.dashboard.semester)

    # Durchschnitt für ein bestimmtes Semester berechnen
    def berechne_semesterdurchschnitt(self, semester):
        return self.noten_service.berechne_semesterdurchschnitt(semester)

    # Trägt eine Note für ein Modul ein und speichert
    def note_eintragen(self, modul, note):
        modul.pruefungsleistung = Pruefungsleistung(note)
        self.repository.speichere_dashboard(self.dashboard)

    # Module
    def modul_hinzufuegen(
        self,
        semester_nummer,
        name,
        ects,
        kapitel_gesamt
    ):
        # Prüfen, ob das gewünschte Semester bereits existiert
        semester = None

        for s in self.dashboard.semester:
            if s.nummer == semester_nummer:
                semester = s
                break

        # Falls das Semester noch nicht existiert, wird es erstellt
        if semester is None:
            semester = Semester(semester_nummer, [])
            self.dashboard.semester.append(semester)

        # Neues Modul erzeugen, Semester hinzufügen und speichern
        modul = Modul(name, ects, kapitel_gesamt, 0, None)
        semester.module.append(modul)

        self.repository.speichere_dashboard(self.dashboard)

    # Kapitel eines Moduls aktualisieren
    def kapitel_aktualisieren(self, modul, kapitel_erledigt):
        modul.kapitel_erledigt = kapitel_erledigt
        self.repository.speichere_dashboard(self.dashboard)

    #Entfernt ein Modul aus dem Semester
    def modul_loeschen(self, modul):
        for semester in self.dashboard.semester:
            if modul in semester.module:
                semester.module.remove(modul)
                break

        self.repository.speichere_dashboard(self.dashboard)

    # Fortschittsberechnung für ein Modul
    def berechne_modulfortschritt(self, modul):
        return self.fortschritts_service.berechne_modulfortschritt(modul)
    
    # ToDo Liste
    def add_todo(self, text):
        self.dashboard.todo_liste.add_todo(text)
        self.repository.speichere_dashboard(self.dashboard)

    #Erledigungsstatus einer Aufgabe umschalten und speichern
    def toggle_todo(self, todo):
        todo.erledigt = not todo.erledigt
        self.repository.speichere_dashboard(self.dashboard)

    # Aufrage löschen
    def delete_todo(self, todo):
        self.dashboard.todo_liste.delete_todo(todo)
        self.repository.speichere_dashboard(self.dashboard)

    # Lernzeit
    def setze_lernzeit_fuer_tag(self, wochentag, stunden):
        self.lernzeit_service.setze_lernzeit(
            self.dashboard.lernzeit, 
            wochentag, 
            stunden
        )
        self.repository.speichere_dashboard(self.dashboard)

    # Lernzeit der Woche zurücksetzen
    def reset_lernzeit(self):
        self.lernzeit_service.reset_lernzeit(self.dashboard.lernzeit)
        self.repository.speichere_dashboard(self.dashboard)

    # Speichern
    def speichern(self):
        self.repository.speichere_dashboard(self.dashboard)