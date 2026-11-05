# Klasse ToDo importieren
from domain.todo import ToDo


# Verwaltet Sammlung von ToDo Aufgaben, mit Name und Liste von ToDos
class ToDoListe:

    def __init__(self, name, todos):
        self.name = name
        self.todos = todos

    def add_todo(self, text):
        # Neues ToDo-Objekt erstellen und zur Liste hinzufügen
        self.todos.append(
            ToDo(text)
        )

    def delete_todo(self, todo):
        # Vorhandenes ToDo aus der Liste entfernen
        self.todos.remove(todo)