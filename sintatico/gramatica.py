from functools import lru_cache

class Gramatica:
    """Uma gramática capaz de gerar palavras de uma linguagem formal."""
    def __init__(self, nao_terminais: set[str], terminais: set[str], producoes: dict[str, set[list[str]]], simbolo_inicial: str):
        """Inicializa a gramática.
        Args:
            nao_terminais(set[str]): Conjunto de símbolos não terminais (N)
            terminais(set[str]): Conjunto de símbolos terminais (T)
            producoes(dict[str, set[str]]): Produções da Gramática (P)
            simbolo_inicial(str): Símbolo inicial da gramática(S)
        """
        
        self.nao_terminais = nao_terminais
        self.terminais = terminais
        self.producoes = producoes
        self.simbolo_inicial = simbolo_inicial
        
    
    @classmethod
    def de_arquivo(cls, caminho_do_arquivo):
        """Método de gerar temporário (eventualmente substituir)."""
        with open(caminho_do_arquivo, 'r') as f:
            dados = f.read()
        dados = dados.split('\n')
        nao_terminais: list[str] = dados[0].split()
        terminais: list[str] = dados[1].split()
        simbolo_inicial: str = dados[2]
        producoes: dict[str, list[str]] = {}
        for linha in dados[3:]:
            linha = linha.split("->")
            producoes[linha[0].strip()] = [x.strip().split() for x in linha[1].split("|")]
        
        return cls(nao_terminais, terminais, producoes, simbolo_inicial)
    
    @lru_cache
    def first(self, simbolo: str) -> set:
        """Função que retorna o conjunto de terminais que podem aparecer no
            início de uma derivação por um dado símbolo. Caso o símbolo seja um
            terminal ou vazio(&), retorna o próprio símbolo.
        
            Args:
                simbolo(str): símbolo a ser avaliado.

            Returns:
                o conjunto de símbolos do FIRST
        """
        # Caso o símbolo seja terminao ou vazio, retorna ele mesmo
        if simbolo in self.terminais or simbolo == '&':
            return set([simbolo])
        conjunto = set()
        for producao in self.producoes[simbolo]:
            i = 0
            while i < len(producao):
                novo_simbolo = producao[i]
                conjunto.update(self.first(novo_simbolo) - {'&'})
                # Se o símbolo for anulável, também precisamos checar o próximo
                if (novo_simbolo in self.nao_terminais and ['&'] in self.producoes[novo_simbolo]) or novo_simbolo == '&':
                    # Se o último for anulável, adiciona & ao first
                    if i == len(producao) - 1:
                        conjunto.add('&')
                    i+=1
                else:
                    break

        return conjunto

    @lru_cache   
    def follow(self, simbolo: str):
        conjunto: set[str] = set()
        if simbolo == self.simbolo_inicial:
            conjunto.add('$')
        for cabeca, producoes in self.producoes.items():
            for producao in producoes:
                # Cria lista com índice de todas as ocorrências do símbolo
                indices = [i for i, x in enumerate(producao) if x == simbolo]
                while len(indices) != 0:
                    indice = indices.pop()
                    if indice == len(producao) - 1:
                        if simbolo != cabeca:
                            conjunto.update(self.follow(cabeca))
                    else:
                        proximo = producao[indice+1]
                        conjunto.update(self.first(proximo) - {'&'})
                        if (proximo in self.nao_terminais and ['&'] in self.producoes[proximo]) or proximo == '&':
                            indices.append(indice+1)
        
        return conjunto
    
    def extender(self):
        """Gera uma nova gramática extendida a partir desta."""
        nao_terminais = list(self.nao_terminais)
        nao_terminais.append("S'")
        nova_prod = {"S'": [[self.simbolo_inicial]]}
        producoes = self.producoes | nova_prod
        return Gramatica(nao_terminais, self.terminais, producoes, "S'")
                
def main():
    g = Gramatica.de_arquivo('entradas/gramaticas/aritmetica.txt')
    for gra in[g]:
        print("BORA")
        for simbolo in gra.nao_terminais:
            print(f"FIRST({simbolo}) >> {gra.first(simbolo)}")
            print(f"FOLLOW({simbolo}) >> {gra.follow(simbolo)}")
if __name__ == "__main__":
    main()