from database.distributore_DAO import DistributoreDAO
from model.distributore_DTO import Distributore
from model.prezzo_DTO import Prezzo

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._distributori = None
        self.load_distributori()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_distributori(self):
        """ Carica tutti i distributori e li setta nella variabile self._distributori """
        self._distributori = DistributoreDAO.get_distributori()

    def get_prezzo_medio(self, mese:int):
        """
        Calcola, per ogni distributore, il prezzo medio al litro per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome del distributore, media), es. (Distributore A, 1.789)
        """
        result = []

        for distributore in self._distributori:
            # lista di tutti i prezzi di un singolo distributore
            prezzi = distributore.get_prezzi()
            # lista dei prezzi del mese che viene aggiornata se si verifica la condizione
            lista_prezzi = []
            # condizione sui prezzi
            for prezzo in prezzi:
                if prezzo.data.month == mese: # verifica del mese
                    lista_prezzi.append(prezzo.prezzo_litro)
            media = sum(lista_prezzi) / len(lista_prezzi)
            result.append((distributore.nome, media))

        return result

        # TODO

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di rifornimenti nei primi 7 giorni
        :return: sequenza di nomi distributore ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        prezzi_settimana = self.__get_prezzi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, prezzi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {distributore.id: distributore.nome for distributore in self._distributori}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, round(self.__costo_ottimo, 2)

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana):
        """ Implementa la ricorsione """
        # 🟤 E - istruzioni che dovrebbero essere sempre eseguite (raramente necessarie)
        #do_always(...)
        # --> in questo caso non ci sono azioni da fare sempre

        # 🟢 A - if terminal_condition:
                    # do_something(...)
                # return...
        if giorno > 7:
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                # '-1' indica che non ho ancora trovato una soluzione (caso iniziale)
                self.__costo_ottimo = costo_corrente
                # salvo una copia della sequenza migliore, perché quella parziale verrà modificata dal backtracking
                self.__sequenza_ottima = sequenza_parziale.copy()
            return

        # for ...: (un loop, se necessario)
        # ciclo sui distributori
        for distributore in self._distributori:
            # 🔵 B - compute_partial()
            prezzo_litro = prezzi_settimana[distributore.id][giorno - 1]
            # calcolo il costo giornaliero di 100 litri
            costo_giornaliero = prezzo_litro * 100
            #  aggiungo 5 € se cambio distributore
            if ultimo_distributore is not None and distributore.id != ultimo_distributore:
                costo_giornaliero += 5
            # aggiorno il costo totale e aggiungo alla sequenza il distributore scelto per il giorno corrente
            # calcolo il costo del ramo corrente senza modificare il costo degli altri rami
            nuovo_costo = costo_corrente + costo_giornaliero
            sequenza_parziale.append(distributore.id)

            # if filter: 🟡 C - Se necessario filtrare prima di procedere con la ricorsione
                # recursion(..., level + 1)
            # continuo solo se il ramo può ancora migliorare la soluzione ottima
            if self.__costo_ottimo == -1 or nuovo_costo < self.__costo_ottimo:
                self.__ricorsione(sequenza_parziale, giorno + 1, distributore.id, nuovo_costo, prezzi_settimana)

            # 🟣 D - back_tracking()
            # rimuovo l'ultima scelta per poter provare l'altro distributore
            # eseguito anche quando il ramo viene scartato
            sequenza_parziale.pop()



        # TODO

    def __get_prezzi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """
        prezzi_primi_gg_mese = {}
        for distributore in self._distributori:
            # lista di tutti i prezzi di un singolo distributore
            prezzi = distributore.get_prezzi()
            prezzi.sort(key=lambda prezzo: prezzo.data)
            # lista dei prezzi del mese che viene aggiornata se si verifica la condizione
            lista_prezzi = []
            for prezzo in prezzi:
                if prezzo.data.month == mese and 1 <= prezzo.data.day <= 7: # verifica del mese
                    lista_prezzi.append(prezzo.prezzo_litro) #aggiungo ogni prezzo alla lista
            prezzi_primi_gg_mese[distributore.id] = lista_prezzi # prezzi_primi_gg_mese = {id: [lista dei primi 7 prezzi]}
        return prezzi_primi_gg_mese
        # TODO