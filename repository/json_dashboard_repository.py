import json
import os

# Domain-Klassen importieren
from domain.dashboard import Dashboard
from domain.semester import Semester
from domain.modul import Modul
from domain.pruefungsleistung import Pruefungsleistung
from domain.lernzeit import Lernzeit
from domain.tag import Tag, Wochentag
from domain.todo import ToDo
from domain.todo_liste import ToDoListe

# Basisklasse importieren
from repository.dashboard_repository import DashboardRepository

class JsonDashboardRepository(DashboardRepository):

    def __init__(self, dateipfad):
        # Speicherort der JSON-Datei festlegen
        self.dateipfad = dateipfad

    # Dashboard laden
    def lade_dashboard(self):

        # Falls noch keine Datei vorhanden ist leeres Dashboard
        if not os.path.exists(self.dateipfad):
            return self._erstelle_leeres_dashboard()

        with open(self.dateipfad, "r", encoding="utf-8") as file:
            data = json.load(file)

        titel = data.get("titel", "Studien Dashboard")

        # Semester und Module laden
        semester_liste = []
        for sem_data in data.get("semester", []):
            module_liste = []
            for mod_data in sem_data.get("module", []):

                # Standardmäßig keine Prüfungsleistung
                pruefung = None

                # Falls eine Note vorhanden ist
                if mod_data.get("pruefungsleistung"):
                    pruefung = Pruefungsleistung(
                        mod_data["pruefungsleistung"]["note"]
                    )

                # Modul erzeugen
                modul = Modul(
                    mod_data["name"],
                    mod_data["ects"],
                    mod_data["kapitel_gesamt"],
                    mod_data["kapitel_erledigt"],
                    pruefung
                )

                module_liste.append(modul)

            # Semester erzeugen
            semester_obj = Semester(sem_data["nummer"], module_liste)
            semester_liste.append(semester_obj)

        # Lernzeit laden
        lernzeit_data = data.get("lernzeit",{})
        tage_liste = []

        for tag_data in lernzeit_data.get("tage", []):
            tag_obj = Tag(
                Wochentag[tag_data["wochentag"]],
                tag_data["gelernte_stunden"]
            )

            tage_liste.append(tag_obj)

        lernzeit_obj = Lernzeit(
            lernzeit_data.get("soll_stunden", 30),
            tage_liste
        )

        # ToDo Liste laden
        todo_data = data.get("todo_liste", {})
        todos = [
            ToDo(t["name"], t["erledigt"])
            for t in todo_data.get("todos", [])
        ]

        todo_liste_obj = ToDoListe(
            todo_data.get("name", "Meine Aufgaben"),
            todos
        )

        # Komplettes Dashboard zurückgeben
        return Dashboard(
            titel,
            semester_liste,
            lernzeit_obj,
            todo_liste_obj
        )

    # Dashboard speichern
    def speichere_dashboard(self, dashboard):
        # Grundstruktur für JSON erstellen
        data = {
            "titel": dashboard.titel,
            "semester": [],
            "lernzeit": {
                "soll_stunden": dashboard.lernzeit.soll_stunden,
                "tage": []
            },
            "todo_liste": {
                "name": dashboard.todo_liste.name,
                "todos": []
            }
        }

        # Semester speichern
        for sem in dashboard.semester:
            sem_data = {
                "nummer": sem.nummer,
                "module": []
            }

            for mod in sem.module:

                mod_data = {
                    "name": mod.name,
                    "ects": mod.ects,
                    "kapitel_gesamt": mod.kapitel_gesamt,
                    "kapitel_erledigt": mod.kapitel_erledigt,
                    "pruefungsleistung": None
                }
                # Falls eine Note vorhanden ist
                if mod.pruefungsleistung:
                    mod_data["pruefungsleistung"] = {
                        "note": mod.pruefungsleistung.note
                    }

                sem_data["module"].append(mod_data)

            data["semester"].append(sem_data)

        # Lernzeit speichern
        for tag in dashboard.lernzeit.tage:

            data["lernzeit"]["tage"].append({
                    "wochentag": tag.wochentag.name,
                    "gelernte_stunden":tag.gelernte_stunden
            })

        # ToDos Speichern
        for todo in dashboard.todo_liste.todos:
            data["todo_liste"]["todos"].append({
                    "name": todo.name,
                    "erledigt": todo.erledigt
            })

        # JSON-Datei schreiben
        with open(self.dateipfad, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    # Leeres Dashboard
    def _erstelle_leeres_dashboard(self):
        # Standard-Wochentage erzeugen
        tage = [
            Tag(Wochentag.MONTAG, 0),
            Tag(Wochentag.DIENSTAG, 0),
            Tag(Wochentag.MITTWOCH, 0),
            Tag(Wochentag.DONNERSTAG, 0),
            Tag(Wochentag.FREITAG, 0),
            Tag(Wochentag.SAMSTAG, 0),
            Tag(Wochentag.SONNTAG, 0)
        ]

        # Lernzeit erzeugen
        lernzeit = Lernzeit(30, tage)

        # Leere ToDo-Liste
        todo_liste = ToDoListe("Meine Aufgaben", [])

        # Semester leer
        semester = []

        # Dashboard zurückgeben
        return Dashboard(
            "Studien Dashboard",
            semester,
            lernzeit,
            todo_liste
        )