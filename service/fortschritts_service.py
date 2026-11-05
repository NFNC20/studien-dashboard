# Berechnung des Modulfortschritts

class FortschrittsService:
    def berechne_modulfortschritt(self, modul):
        # Falls keine Kapitel vorhanden → Fortschritt 0
        if modul.kapitel_gesamt == 0:
            return 0

        # Prozent berechnen
        return (modul.kapitel_erledigt / modul.kapitel_gesamt) * 100
