from sintatico.gramatica import Gramatica
from sintatico.item import Item

class Canonico:

    def __init__(self):
        # Armazena os itens de cada conjunto de itens {I0: S'->·S, S->·A, ...}
        self.itens: dict[str, set[Item]] = {}
        # Armazena desvios entre conjuntos de itens  {(I0, A): I2}
        self.desvios: dict[tuple[str, str], str] = {}
    
    @classmethod
    def colecao_canonica(cls, gram: Gramatica) -> "Canonico":
        """Gera coleção de itens canônicos (I0, I1, I2...)"""
        g_ext = gram.extender()
        
        itens: dict[str, set[Item]] = {}

        simbolo_inicial = g_ext.simbolo_inicial
        corpo_inicial = list(g_ext.producoes[simbolo_inicial])[0]
        item_inicial = Item(simbolo_inicial, corpo_inicial, 0)
        itens["I0"] = Canonico.closure({item_inicial})
        fila = []
        # Falta bastante coisa aqui ainda

    
    @staticmethod
    def closure(i: set[Item], producoes: dict[str, set[list[str]]]):
        """Implementa CLOSURE(I)"""
        j = set(i)
        pilha = list(i)
        while len(pilha) != 0:
            item_atual = pilha.pop()
            elemento = item_atual.elemento_do_ponto()
            for corpo in producoes.get(elemento, []):
                novo_item = Item(elemento, corpo, 0)
                if novo_item not in j:
                    j.add(novo_item)
                    pilha.add(novo_item)
        return j

    @staticmethod
    def go_to(self, i: set[Item], producoes: dict[str, set[list[str]]], elemento: str):
        """IMPLEMENTA GOTO(Y)"""
        j = {item for item in i if item.elemento_do_ponto() == elemento}
        return Canonico.closure(j, producoes)

    def gerar_tabela():
        """Gera tabela de shifts, reduces e desvios baseados na coleção de itens
        e desvios."""
        pass
