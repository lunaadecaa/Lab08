from Tools.scripts.var_access_benchmark import B

from database.distributore_DAO import DistributoreDAO
from database.prezzo_DAO import PrezzoDAO
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
        dao=PrezzoDAO()
        prezzi_totali=dao.prezzi_per_mese(mese)
        A=[]
        B=[]
        prezzi_medi=[]
        for prezzo in prezzi_totali:
            if prezzo.id_distributore==1:
                A.append(prezzo.prezzo_litro)

            else:
                B.append(prezzo.prezzo_litro)

        media_A=sum(A)/len(A)
        media_B=sum(B)/len(B)
        prezzi_medi.append(("Distributore A", media_A))
        prezzi_medi.append(("Distributore B", media_B))
        return prezzi_medi

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di rifornimenti nei primi 7 giorni
        :return: sequenza di nomi distributore ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        prezzi_settimana = self.__get_prezzi_prima_settimana_mese(mese)
        print(prezzi_settimana)

        self.__ricorsione([], 1, None, 0, prezzi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {distributore.id: distributore.nome for distributore in self._distributori}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, round(self.__costo_ottimo, 2)

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana):
        """ Implementa la ricorsione """

        if giorno > 7:
            # Controlliamo se è la prima soluzione trovata o se ha un costo minore della precedente
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = list(sequenza_parziale)  # Salviamo la sequenza vincente
            return

        prezzo_1 = prezzi_settimana[1][giorno - 1] * 100
        prezzo_2 = prezzi_settimana[2][giorno - 1] * 100

        if ultimo_distributore is None:

            self.__ricorsione(sequenza_parziale + [1], giorno + 1, 1, costo_corrente + prezzo_1, prezzi_settimana)

            self.__ricorsione(sequenza_parziale + [2], giorno + 1, 2, costo_corrente + prezzo_2, prezzi_settimana)

        else:

            if ultimo_distributore == 1:

                self.__ricorsione(sequenza_parziale + [1], giorno + 1, 1, costo_corrente + prezzo_1,
                                  prezzi_settimana)

                self.__ricorsione(sequenza_parziale + [2], giorno + 1, 2, costo_corrente + prezzo_2 + 5,
                                  prezzi_settimana)


            elif ultimo_distributore == 2:

                self.__ricorsione(sequenza_parziale + [1], giorno + 1, 1, costo_corrente + prezzo_1 + 5,
                                  prezzi_settimana)

                self.__ricorsione(sequenza_parziale + [2], giorno + 1, 2, costo_corrente + prezzo_2,
                                  prezzi_settimana)



    def __get_prezzi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """
        dao=PrezzoDAO()
        prezzi_totali=dao.prezzi_per_mese(mese)
        A=[]
        B=[]
        for prezzo in prezzi_totali:
            if prezzo.id_distributore==1:
                A.append(prezzo.prezzo_litro)
            else:
                B.append(prezzo.prezzo_litro)
        a_n=A[:7]
        b_n=B[:7]
        prezzi_7gg={1: a_n, 2: b_n}
        #print(prezzi_7gg)
        return prezzi_7gg
