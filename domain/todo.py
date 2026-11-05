# Klasse für eine einzelne ToDo-Aufgabe mit Name und Erledigungsstatus
class ToDo:

    def __init__(self, name, erledigt=False):
        self.name = name
        self.erledigt = erledigt