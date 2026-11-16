from dataclasses import dataclass
from database.prezzo_DAO import PrezzoDAO

'''
    DTO (Data Transfer Object) dell'entità Distributore
'''

@dataclass()
class Distributore:
    id: int
    nome: str
    indirizzo: str

    # RELAZIONI
    lista_prezzi: list = None

    def get_prezzi(self,id_distributore):
        """ Aggiorna e Restituisce la lista di prezzi (self.lista_prezzi) associati al distributore"""
        prezzi=PrezzoDAO().get_prezzi(id_distributore)
        d=[]
        for prezzo in prezzi:
            d.append(prezzo)
        return d

    def __eq__(self, other):
        return isinstance(other, Distributore) and self.id == other.id

    def __str__(self):
        return f"{self.id} | {self.nome} | Indirizzo: {self.indirizzo}"

    def __repr__(self):
        return f"{self.id} | {self.nome} | Indirizzo: {self.indirizzo}"
