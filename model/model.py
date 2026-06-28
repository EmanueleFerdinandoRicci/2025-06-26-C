import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._constructors = []
        self._idMapC = {}
        self._results = []
        self._best_sfortunati = []
        self._best_score = -1.0

    def getAllYears(self):
        return DAO.getAllYears()

    def getAllConstructors(self):
        self._constructors = DAO.getAllConstructors()
        return self._constructors

    def creaGrafo(self,y1,y2):
        self._graph.clear()
        self._constructors = DAO.getAllConstructors()
        for c in self._constructors:
            self._idMapC[c.constructorId] = c
        self._graph.add_nodes_from(self._constructors)
        self._results = DAO.getAllResults(y1,y2)
        for r in self._results:
            nodo = self._idMapC[r.cId]
            # Se l'anno non esiste ancora nel dizionario, creo una lista vuota
            if r.year not in nodo.results:
                nodo.results[r.year] = []
            # Appendo il risultato alla lista di quell'anno
            nodo.results[r.year].append(r)

        allEdges = DAO.getAllEdges(y1, y2, self._idMapC)
        pesi = DAO.getPesi(y1, y2, self._idMapC)
        dizionario_pesi = {}
        for p in pesi:
            dizionario_pesi[p.c] = p.numeroGare
        for e in allEdges:
            peso_totale = 0
            if e.constructor1 in dizionario_pesi:
                peso_totale += dizionario_pesi[e.constructor1]
            if e.constructor2 in dizionario_pesi:
                peso_totale += dizionario_pesi[e.constructor2]
            self._graph.add_edge(e.constructor1, e.constructor2, weight=peso_totale)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getCompConnessaOrd(self):
        comp_connesse = list(nx.connected_components(self._graph))
        if not comp_connesse:
            return 0, []

        num = len(comp_connesse)
        comp_max = max(comp_connesse, key=len)

        nodi_con_peso_max = []
        for n in comp_max:
            # Recupero tutti gli archi incidenti al nodo n con i loro dati (incluso il peso)
            archi_incidenti = self._graph.edges(n, data=True)

            if archi_incidenti:
                # Uso una list comprehension per estrarre solo il 'weight' di ogni arco incidente
                # e trovo il valore MASSIMO usando max()

                peso_massimo = max([dati['weight'] for u, v, dati in archi_incidenti])
            else:
                # Caso limite: se il nodo fosse isolato, il suo peso massimo incidente è 0
                peso_massimo = 0

            nodi_con_peso_max.append((n, peso_massimo))

        # Ordino la lista in senso decrescente basandomi sul peso massimo (x[1])
        nodi_con_peso_max.sort(key=lambda x: x[1], reverse=True)

        return num, nodi_con_peso_max

    def getTeamSfortunati(self, k, m):
        # 1. Recupero la componente connessa maggiore dal grafo
        comp_connesse = list(nx.connected_components(self._graph))
        if not comp_connesse:
            return 0, []
        comp_max = max(comp_connesse, key=len)

        # 2. Strutture dati per i team validi e l'indice di sfortuna
        squadre_valide = []
        self.indice_sfortuna = {}  # Lo salviamo per stamparlo nel controller

        # 3. Filtro i team validi e calcolo l'indice
        for nodo in comp_max:
            # Numero di campionati = numero di chiavi nel dizionario dei risultati
            num_campionati = len(nodo.results.keys())

            if num_campionati >= m:
                nP = 0
                nPtot = 0

                # Scorro tutte le liste dei piazzamenti nei vari anni
                for anno, risultati in nodo.results.items():
                    nPtot += len(risultati)
                    for r in risultati:
                        if r.position is not None:
                            nP += 1

                # Calcolo indice I
                if nPtot > 0:
                    I = 1 - (nP / nPtot)
                else:
                    I = 0

                self.indice_sfortuna[nodo] = I
                squadre_valide.append(nodo)

        # 4. FIX: ORDINO LA LISTA DI PARTENZA
        # Ordino i team validi in base all'indice di sfortuna (decrescente).
        # Così la ricorsione li processa e li salva già nel giusto ordine di stampa.
        squadre_valide.sort(key=lambda t: self.indice_sfortuna[t], reverse=True)

        # 5. Inizializzo variabili per la ricorsione
        self._best_sfortunati = []
        self._best_score = -1.0  # Inizializzato a -1 per aggiornarlo al primo giro

        # 6. Avvio la ricorsione
        self._ricorsione(parziale=[], squadre_valide=squadre_valide, start_index=0, k=k)

        return self._best_score, self._best_sfortunati

    def _ricorsione(self, parziale, squadre_valide, start_index, k):
        # CASO TERMINALE: Ho scelto esattamente K team
        if len(parziale) == k:
            # Calcolo la somma degli indici dei team scelti
            punteggio_attuale = sum(self.indice_sfortuna[t] for t in parziale)

            if punteggio_attuale > self._best_score:
                self._best_score = punteggio_attuale
                self._best_sfortunati = list(parziale)  # Copia profonda fondamentale!
            return

        # OTTIMIZZAZIONE (PRUNING)
        # Se i team che mancano per finire la lista non bastano ad arrivare a K, taglio il ramo.
        if len(parziale) + (len(squadre_valide) - start_index) < k:
            return

        # ESPLORAZIONE
        for i in range(start_index, len(squadre_valide)):
            parziale.append(squadre_valide[i])
            # Chiamata ricorsiva passando l'indice successivo i + 1 per evitare duplicati/permutazioni
            self._ricorsione(parziale, squadre_valide, i + 1, k)
            # Backtracking
            parziale.pop()