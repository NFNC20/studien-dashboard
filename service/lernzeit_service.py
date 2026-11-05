# Verwaltung der Lernzeit pro Woche

class LernzeitService:
    def setze_lernzeit(self, lernzeit, wochentag, stunden):
        # Lernstunden für einen bestimmten Tag setzen
        for tag in lernzeit.tage:
            if tag.wochentag == wochentag:
                tag.gelernte_stunden = stunden

    def reset_lernzeit(self, lernzeit):
        # Alle Lernstunden auf 0 setzen
        for tag in lernzeit.tage:
            tag.gelernte_stunden = 0
