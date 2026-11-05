from controller.dashboard_controller import DashboardController
from view.dashboard_view import DashboardView

# Haputprogramm und Einstiegspunkt der Anwendung
def main():
    # Controller und GUI erzeugen (lädt Dashboard + Services)
    controller = DashboardController()
    view = DashboardView(controller)

    # GUI starten
    view.start()


# Nur ausführen, wenn Datei direkt gestartet wird
if __name__ == "__main__":
    main()
