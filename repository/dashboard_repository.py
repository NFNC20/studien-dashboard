# Schnittstelle zum Speichern und Laden des Dashboards
class DashboardRepository:
    def lade_dashboard(self):
        # Wird in der Repository Klasse überschrieben
        raise NotImplementedError()

    def speichere_dashboard(self, dashboard):
        raise NotImplementedError()
