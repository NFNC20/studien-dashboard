import tkinter as tk
from tkinter import ttk

# Matplotlib für das Lernzeit-Diagramm
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Hauptansicht des Dashboards
class DashboardView:

    def __init__(self, controller):
        self.controller = controller

        # Hauptfenster erstellen
        self.root = tk.Tk()
        self.root.title("Studien-Dashboard")

        self.main = ttk.Frame(self.root, padding=10)
        self.main.pack(fill="both", expand=True)

        # Titel des Dashboards
        self.titel_label = ttk.Label(
            self.main,
            text=self.controller.dashboard.titel,
            font=("Arial", 20)
        )

        self.titel_label.pack(pady=10)

        # Notendurchschnitt anzeigen
        self.noten_frame = ttk.LabelFrame(self.main, text="Notendurchschnitt")
        self.noten_frame.pack(fill="x", pady=10)

        self.gesamt_label = ttk.Label(self.noten_frame, text="Gesamt: 0.00")
        self.gesamt_label.pack(anchor="w", padx=10, pady=5)
        self.aktualisiere_gesamt_note()

        # Semester-Buttons
        self.semester_frame = ttk.LabelFrame(self.main, text="Semester")

        self.semester_frame.pack(fill="x", pady=10)
        self.zeige_semester_buttons()

        # Mittlerer Bereich für ToDo-Liste und Modulfortschritt
        self.mitte_frame = ttk.Frame(self.main)

        self.mitte_frame.pack(fill="x", pady=10)

        # ToDo-Liste (links)
        self.todo_frame = ttk.LabelFrame(self.mitte_frame, text="ToDo-Liste")
        self.todo_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.todo_entry = ttk.Entry(self.todo_frame, width=30)
        self.todo_entry.pack(side="left", padx=5, pady=5)

        # Hinzufügen-Button
        ttk.Button(
            self.todo_frame,
            text="Hinzufügen",
            command=self.todo_hinzufuegen
        ).pack(side="left", padx=5)

        # Bereich für ToDos
        self.todo_list_frame = ttk.Frame(self.todo_frame)

        self.todo_list_frame.pack(fill="x", pady=5)
        self.zeige_todos()

        # Modulfortschritt (rechts)
        self.modul_frame = ttk.LabelFrame(self.mitte_frame, text="Modulfortschritt")
        self.modul_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        # Eingabebereich für neues Modul
        self.modul_input_frame = ttk.Frame(self.modul_frame)
        self.modul_input_frame.pack(fill="x", pady=5)

        # Modulname
        ttk.Label(self.modul_input_frame, text="Modul:").grid(row=0, column=0, padx=3)
        self.modul_name_entry = ttk.Entry(self.modul_input_frame, width=20)
        self.modul_name_entry.grid(row=0, column=1, padx=3)

        # ECTS
        ttk.Label(self.modul_input_frame, text="ECTS:").grid(row=0, column=2, padx=3)
        self.modul_ects_entry = ttk.Entry(self.modul_input_frame, width=5)
        self.modul_ects_entry.grid(row=0, column=3, padx=3)

        # Kapitel gesamt
        ttk.Label(self.modul_input_frame, text="Kapitel:").grid(row=0, column=4, padx=3)
        self.modul_kapitel_entry = ttk.Entry(self.modul_input_frame, width=5)
        self.modul_kapitel_entry.grid(row=0, column=5, padx=3)

        # Semester auswählen
        ttk.Label(self.modul_input_frame, text="Semester:").grid(row=1, column=0, padx=3, pady=5)

        self.semester_auswahl = ttk.Combobox(
            self.modul_input_frame,
            values=["1", "2", "3", "4", "5", "6"],
            width=4,
            state="readonly"
        )

        self.semester_auswahl.grid(row=1, column=1, padx=3, pady=5)
        self.semester_auswahl.set("1")

        # Modul hinzufügen
        ttk.Button(
            self.modul_input_frame,
            text="Modul hinzufügen",
            command=self.modul_hinzufuegen
        ).grid(row=1, column=2, columnspan=4, padx=3, pady=5)

        # Bereich für Module
        self.modul_liste_frame = ttk.Frame(self.modul_frame)
        self.modul_liste_frame.pack(fill="x", pady=5)
        self.zeige_modulfortschritt()

        # Lernzeit
        self.lernzeit_frame = ttk.LabelFrame(self.main, text="Lernzeit")
        self.lernzeit_frame.pack(fill="both", expand=True, pady=10)

        # Eingabefelder
        self.lernzeit_input_frame = ttk.Frame(self.lernzeit_frame)
        self.lernzeit_input_frame.pack(pady=10)

        self.lernzeit_eingaben = []
        tage = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
        for i, tag in enumerate(tage):
            ttk.Label(self.lernzeit_input_frame, text=tag).grid(row=0, column=i, padx=5)
            entry = ttk.Entry(self.lernzeit_input_frame, width=5)
            entry.grid(row=1, column=i, padx=5)
            self.lernzeit_eingaben.append(entry)

        self.zeige_lernzeit_eingaben()

        # Buttons
        self.lernzeit_button_frame = ttk.Frame(self.lernzeit_frame)
        self.lernzeit_button_frame.pack(pady=5)

        ttk.Button(
            self.lernzeit_button_frame,
            text="Lernzeit speichern",
            command=self.lernzeit_speichern
        ).pack(side="left", padx=5)

        ttk.Button(
            self.lernzeit_button_frame,
            text="Woche zurücksetzen",
            command=self.lernzeit_zuruecksetzen
        ).pack(side="left", padx=5)

        # Diagramm
        self.diagramm_frame = ttk.Frame(self.lernzeit_frame)
        self.diagramm_frame.pack(fill="both", expand=True)
        self.erstelle_lernzeit_diagramm()

    # Semester-Buttons anzeigen
    def zeige_semester_buttons(self):

        # Alte Buttons entfernen
        for widget in self.semester_frame.winfo_children():
            widget.destroy()

        # Semester horizontal anzeigen
        for semester in self.controller.dashboard.semester:

            ttk.Button(
                self.semester_frame,
                text=f"Semester {semester.nummer}",
                command=lambda s=semester:
                    self.zeige_semester(s)
            ).pack(side="left", padx=5)

    # Gesamtnotendurchschnitt
    def aktualisiere_gesamt_note(self):

        durchschnitt = (self.controller.berechne_gesamtnotendurchschnitt())
        self.gesamt_label.config(text=f"Gesamt: {durchschnitt:.2f}")

    # Semester öffnen und Module anzeigen
    def zeige_semester(self, semester):
        fenster = tk.Toplevel(self.root)
        fenster.title(f"Semester {semester.nummer}")

        ttk.Label(
            fenster,
            text=f"Semester {semester.nummer}",
            font=("Arial", 16)
        ).pack(pady=10)

        # Module anzeigen
        for modul in semester.module:
            row = ttk.Frame(fenster)
            row.pack(fill="x", padx=10, pady=5)

            ttk.Label(row, text=modul.name, width=30).pack(side="left")

            if modul.pruefungsleistung:

                # Bereits vorhandene Note anzeigen
                ttk.Label(
                    row,
                    text=(f"Note: " f"{modul.pruefungsleistung.note:.1f}")
                ).pack(side="left", padx=10)

                # Button zum Löschen der vorhandenen Prüfungsnote
                ttk.Button(
                    row,
                    text="Note löschen",
                    command=lambda m=modul, f=fenster: self.note_loeschen(m, f)
                ).pack(side="left", padx=5)

            else:
                ttk.Label(row, text="Noch keine Note").pack(side="left", padx=10)

        # Semesterdurchschnitt
        durchschnitt = (self.controller.berechne_semesterdurchschnitt(semester))
        ttk.Label(
            fenster,
            text=(f"Semesterdurchschnitt: " f"{durchschnitt:.2f}")
        ).pack(pady=10)

    # Note löschen
    def note_loeschen(self, modul, fenster):
        # Prüfungsleistung des Moduls entfernen
        modul.pruefungsleistung = None
        # Änderung dauerhaft speichern
        self.controller.speichern()

        # Semesterfenster schließen
        fenster.destroy()
        # Modul erscheint wieder im Modulfortschritt
        self.zeige_modulfortschritt()
        # Gesamtnotendurchschnitt aktualisieren
        self.aktualisiere_gesamt_note()

        # Semesterfenster erneut öffnen,damit der aktuelle Stand angezeigt wird
        self.zeige_semester(
            next(
                s for s in self.controller.dashboard.semester
                if modul in s.module
            )
        )

    # Modul hinzufügen
    def modul_hinzufuegen(self):
        # Eingaben auslesen
        name = (self.modul_name_entry.get().strip())

        try:
            ects = int(self.modul_ects_entry.get())
            kapitel_gesamt = int(self.modul_kapitel_entry.get())
            semester_nummer = int(self.semester_auswahl.get())
        except ValueError:
            return

        # Prüfen, ob Modulname vorhanden ist
        if not name:
            return
        # Prüfen, ob sinnvolle Werte eingegeben wurden
        if ects <= 0 or kapitel_gesamt <= 0:
            return

        # Modul über Controller erstellen
        self.controller.modul_hinzufuegen(
            semester_nummer,
            name,
            ects,
            kapitel_gesamt
        )

        # Eingabefelder leeren
        self.modul_name_entry.delete(0, tk.END)
        self.modul_ects_entry.delete(0, tk.END)
        self.modul_kapitel_entry.delete(0, tk.END)

        # Anzeige aktualisieren
        self.zeige_modulfortschritt()
        # Semester-Buttons aktualisieren
        self.zeige_semester_buttons()

    # Modulfortschitt anzeigen
    def zeige_modulfortschritt(self):
        # Alte Anzeige löschen
        for widget in self.modul_liste_frame.winfo_children():
            widget.destroy()

        # Alle Semester durchgehen
        for semester in self.controller.dashboard.semester:
            # Alle Module des Semesters durchgehen
            for modul in semester.module:

                # Nur Module ohne Note anzeigen
                if modul.pruefungsleistung is None:
                    row = ttk.Frame(self.modul_liste_frame)
                    row.pack(fill="x", pady=4)

                    # Modulname
                    ttk.Label(row, text=modul.name, width=20).pack(side="left")

                    # Fortschritt berechnen
                    fortschritt = (self.controller.berechne_modulfortschritt(modul))
                    # Balken
                    bar = ttk.Progressbar(row, length=120)
                    bar["value"] = fortschritt
                    bar.pack(side="left", padx=5)

                    # Prozent
                    ttk.Label(row, text=f"{fortschritt:.0f}%").pack(side="left", padx=3)
                    # Kapitelstand
                    ttk.Label(
                        row,
                        text=(f"{modul.kapitel_erledigt}/" f"{modul.kapitel_gesamt}")
                    ).pack(side="left", padx=5)

                    # Kapitel aktualisieren
                    entry = ttk.Entry(row, width=5)
                    entry.insert(0, str(modul.kapitel_erledigt))
                    entry.pack(side="left", padx=3)

                    ttk.Button(
                        row,
                        text="Update",
                        command=lambda m=modul, e=entry: self.kapitel_update(m, e)
                    ).pack(side="left", padx=3)

                    # Note
                    note_entry = ttk.Entry(row, width=5)
                    note_entry.pack(side="left", padx=3)

                    ttk.Button(
                        row,
                        text="Note",
                        command=lambda m=modul, e=note_entry: self.pruefung_eintragen(m, e)
                    ).pack(side="left", padx=3)

                    # Modul löschen
                    ttk.Button(
                        row,
                        text="X",
                        width=3,
                        command=lambda m=modul: self.modul_loeschen(m)
                    ).pack(side="right", padx=3)

    # Kapitel aktualisieren
    def kapitel_update(self, modul, entry):
        try:
            erledigt = int(entry.get())
        except ValueError:
            return

        # Wert begrenzen
        if erledigt < 0:
            erledigt = 0
        if erledigt > modul.kapitel_gesamt:
            erledigt = modul.kapitel_gesamt

        # Kapitel aktualisieren
        self.controller.kapitel_aktualisieren(modul, erledigt)
        # Anzeige aktualisieren
        self.zeige_modulfortschritt()

    # Prüfung eintragen
    def pruefung_eintragen(self, modul, entry):
        try:
            note = float(entry.get())
        except ValueError:
            return

        # Nur gültige Noten zulassen
        if note < 1.0 or note > 5.0:
            return

        # Note speichern
        self.controller.note_eintragen(modul, note)
        # Modul aus Fortschrittsbereich entfernen
        self.zeige_modulfortschritt()
        # Gesamtnote aktualisieren
        self.aktualisiere_gesamt_note()

    # Modul löschen
    def modul_loeschen(self, modul):
        self.controller.modul_loeschen(modul)
        # Anzeige aktualisieren
        self.zeige_modulfortschritt()
        # Semester aktualisieren
        self.zeige_semester_buttons()

    # ToDo-Liste anzeigen
    def zeige_todos(self):
        for widget in self.todo_list_frame.winfo_children():
            widget.destroy()

        for todo in self.controller.dashboard.todo_liste.todos:
            row = ttk.Frame(self.todo_list_frame)
            row.pack(fill="x", pady=2)

            var = tk.BooleanVar(value=todo.erledigt)
            ttk.Checkbutton(
                row,
                text=todo.name,
                variable=var,
                command=lambda t=todo, v=var: self.todo_toggle(t, v)
            ).pack(side="left")

            ttk.Button(
                row,
                text="X",
                width=3,
                command=lambda t=todo: self.todo_loeschen(t)
            ).pack(side="right")

    def todo_hinzufuegen(self):

        text = (self.todo_entry .get() .strip())
        if text:
            self.controller.add_todo(text)
            self.todo_entry.delete(0, tk.END)
            self.zeige_todos()

    def todo_toggle(self, todo, var):
        todo.erledigt = var.get()
        self.controller.speichern()
        self.zeige_todos()

    def todo_loeschen(self, todo):
        self.controller.delete_todo(todo)
        self.zeige_todos()

    # Lermzeit-Eingaben anzeigen
    def zeige_lernzeit_eingaben(self):
        tage = (self.controller .dashboard .lernzeit .tage)
        for i, tag in enumerate(tage):
            self.lernzeit_eingaben[i].delete(0, tk.END)
            self.lernzeit_eingaben[i].insert(0, str(tag.gelernte_stunden))

    def lernzeit_speichern(self):
        tage = (self.controller .dashboard .lernzeit .tage)
        for i, tag in enumerate(tage):
            try:
                stunden = float(self.lernzeit_eingaben[i].get())
            except ValueError:
                stunden = 0

            if stunden < 0:
                stunden = 0

            self.controller.setze_lernzeit_fuer_tag(tag.wochentag, stunden)

        self.aktualisiere_lernzeit_diagramm()

    def lernzeit_zuruecksetzen(self):
        self.controller.reset_lernzeit()
        self.zeige_lernzeit_eingaben()
        self.aktualisiere_lernzeit_diagramm()

    # Lernzeit Diagramm erstellen
    def erstelle_lernzeit_diagramm(self):
        fig = Figure(figsize=(4, 3))
        ax = fig.add_subplot(111)

        tage = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
        stunden = [
            tag.gelernte_stunden
            for tag in self.controller.dashboard.lernzeit.tage
        ]

        ax.bar(tage, stunden)
        ax.set_title("Lernzeit pro Tag")
        ax.set_ylabel("Stunden")

        self.canvas = FigureCanvasTkAgg(fig, master=self.diagramm_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def aktualisiere_lernzeit_diagramm(self):
        self.canvas.get_tk_widget().destroy()
        self.erstelle_lernzeit_diagramm()

    # GUI starten
    def start(self):
        self.root.mainloop()