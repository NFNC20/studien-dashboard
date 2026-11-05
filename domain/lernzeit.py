# Speichert das Lernzeitziel und die einzelnen Tage
class Lernzeit:
    def __init__(self, soll_stunden, tage):
        self.soll_stunden = soll_stunden
        self.tage = tage

 # Rechnet die gelernten Stunden aller Tage zusammen
    @property
    def ist_stunden(self):
        return sum(tag.gelernte_stunden for tag in self.tage)
