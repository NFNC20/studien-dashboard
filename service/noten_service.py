# Service zur Berechnung von Notendurchschnitten

class NotenService:

    def berechne_gesamtnotendurchschnitt(self, semester_liste):
        # Alle vorhandenen Noten und ECTS sammeln
        noten = []

        for semester in semester_liste:
            for modul in semester.module:
                if modul.pruefungsleistung is not None:
                    noten.append(
                        (
                            modul.pruefungsleistung.note,
                            modul.ects
                        )
                    )

        # Falls noch keine Noten vorhanden sind
        if not noten:
            return 0.0

        # Gesamtnote ECTS-gewichtet berechnen
        gesamt = sum(note * ects for note, ects in noten)
        ects_summe = sum(ects for _, ects in noten)

        return gesamt / ects_summe

    def berechne_semesterdurchschnitt(self, semester):
        # Durchschnitt des Semesters über die Domain-Klasse berechnen
        return semester.berechne_durchschnitt()