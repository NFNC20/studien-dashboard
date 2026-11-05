from enum import Enum

# Alle Tage für die Lernzeit mit Enum definieren
class Wochentag(Enum):
    MONTAG = "Montag"
    DIENSTAG = "Dienstag"
    MITTWOCH = "Mittwoch"
    DONNERSTAG = "Donnerstag"
    FREITAG = "Freitag"
    SAMSTAG = "Samstag"
    SONNTAG = "Sonntag"

# Speichert Tag mit den gelernten Stunden
class Tag:
    def __init__(self, wochentag, gelernte_stunden):
        self.wochentag = wochentag
        self.gelernte_stunden = gelernte_stunden