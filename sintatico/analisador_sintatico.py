from sintatico.gramatica import Gramatica
from sintatico.canonico import Canonico

class AnalisadorSintatico:

    def __init__(self):
        pass
    
    def gerar_tabela(self, caminho_gramatica):
        g = Gramatica.de_arquivo(caminho_gramatica)
        colecao = Canonico.colecao_canonica(g)
        tabela = colecao.gerar_tabela()
        return tabela