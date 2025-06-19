class Item:
    def __init__(self, cabeca: str, corpo: list[str], ponto_pos: int):
        """"""
        self.cabeca = cabeca
        self.corpo = tuple(corpo) # Linhas são unhashable, então usamos tuplas
        self.ponto_pos = ponto_pos

    # Dunder methods hash e eq (para linhas como "if item in conjunto" funcionarem)
    
    def __hash__(self):
        """Define um hash para a classe. (Função meramente para fazer linhas
        como 'if item in conjunto' funcionarem, não se preocupe com isso.)"""
        return hash((self.cabeca, self.corpo, self.ponto_pos))
    
    def __eq__(self, item: "Item"):
        """Define os requisitos para 2 itens serem iguais. (Função meramente 
        para fazer linhas como 'if item in conjunto' funcionarem, não se 
        preocupe com isso.)"""
        if not isinstance(item, Item):
            return False
        mesma_cabeca = (self.cabeca == item.cabeca)
        mesmo_corpo = (self.corpo == item.corpo)
        mesma_pos = (self.ponto_pos == item.ponto_pos)
        return mesma_cabeca and mesmo_corpo and mesma_pos
    
    def avancar_ponto(self):
        if self.ponto_pos == len(self.corpo):
            return None
        nova_pos = self.ponto_pos + 1
        return Item(self.cabeca, self.corpo, nova_pos)
    
    def elemento_do_ponto(self):
        if self.ponto_pos == len(self.corpo):
            return None
        return self.corpo[self.ponto_pos]
    

def main():
    i1 = Item('A', ['B'], 0)
    i2 = Item('34', ['not'], 0)
    conjunto = {i1, i2}
    novo = set(conjunto)
    novo.add(Item('1', ['A'], 0))
    novo.remove(i2)
    print(conjunto)
    print(novo)

if __name__ == "__main__":
    main()