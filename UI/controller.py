import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDYears(self):
        years = self._model.getAllYears()
        for y in years:
            self._view._ddYear1.options.append(ft.dropdown.Option(y))
            self._view._ddYear2.options.append(ft.dropdown.Option(y))
        self._view.update_page()


    def handleBuildGraph(self, e):
        self._model.creaGrafo(self._view._ddYear1.value, self._view._ddYear2.value)
        n, e = self._model.getGraphDetails()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato:")
        )
        self._view._txt_result.controls.append(
            ft.Text(f"Nodi: {n} nodi")
        )
        self._view._txt_result.controls.append(
            ft.Text(f"Archi: {e} archi")
        )
        self._view.update_page()

    def handlePrintDetails(self, e):
        self._view._txt_result.controls.clear()
        num, comp_max_ordinata = self._model.getCompConnessaOrd()
        self._view._txt_result.controls.append(
            ft.Text(f"La componente maggiore è composta da {len(comp_max_ordinata)} nodi:")
        )
        for nodo, peso_max in comp_max_ordinata:
            self._view._txt_result.controls.append(
                ft.Text(f"Nodo: {nodo} - Peso Max Arco Incidente: {peso_max}")
            )
        self._view.update_page()

    def handleCercaTeamSfortunati(self, e):
        self._view._txt_result.controls.clear()
        try:
            k = int(self._view._txtInSoglia.value)
            m = int(self._view._txtInNumDiEdizioni.value)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text("Inserisci valori numerici interi per K ed M."))
            return

        best_score, best_teams = self._model.getTeamSfortunati(k, m)
        if not best_teams:
            self._view._txt_result.controls.append(
                ft.Text("Nessun team soddisfa i criteri richiesti (valori di M o K troppo alti).", color="red")
            )
        else:
            self._view._txt_result.controls.append(
                ft.Text(f"Trovati i {k} team più sfortunati!")
            )
            self._view._txt_result.controls.append(
                ft.Text(f"Indice di sfortuna globale: {best_score:.4f}")
            )
            for t in best_teams:
                indice = self._model.indice_sfortuna[t]
                self._view._txt_result.controls.append(
                    ft.Text(f"{t.name} - Indice sfortuna: {indice:.4f}")
                )
        self._view.update_page()
