class AFD:
    """Classe que representa um Autômato Finito Determinístico (AFD)."""

    def __init__(self, nome:str, estados: set[str], alfabeto: set[str], transicoes: dict[tuple[str, str], str], estado_inicial: str, estados_aceitacao: set[str]):
        """Inicializa o AFD com os estados, alfabeto, transições, estado inicial
           e estados de aceitação.
        
            Args:
                nome (str): Nome do AFD (importante para identificação).
                estados (set[str]): Conjunto de estados do AFD.
                alfabeto (set[str]): Conjunto de símbolos do alfabeto do AFD.
                transicoes (dict[tuple[str, str], str]): Dicionário que mapeia tuplas (estado, símbolo) para o próximo estado.
                estado_inicial (str): Estado inicial do AFD.
                estados_aceitacao (set[str]): Conjunto de estados de aceitação do AFD.
        """
        self.nome = nome
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = estados_aceitacao
        self.estado_atual = estado_inicial
    
    def resetar(self) -> None:
        """Reseta o estado atual do AFD para o estado inicial."""
        self.estado_atual = self.estado_inicial
    
    def transitar(self, simbolo: str) -> None:
        """Realiza uma transição com base no símbolo fornecido 
            (e no estado atual), alterando o estado atual do AFD.
        
            Args:
                simbolo (str): O símbolo a ser processado.
        """
        # Altera o estado com base na transição definida (None se não houver)
        self.estado_atual = self.transicoes.get((self.estado_atual, simbolo))
    
    def aceita(self) -> bool:
        """Verifica se o estado atual é um estado de aceitação.
        
        Returns:
            True se o estado atual for um estado de aceitação, False caso contrário.
        """
        return self.estado_atual in self.estados_aceitacao
    
    def avaliar_palavra(self, palavra: str) -> bool:
        """Avalia uma palavra no AFD, processando cada símbolo e verificando se a palavra é aceita.
        
        Args:
            palavra (str): A palavra a ser avaliada.
        
        Returns:
            True se a palavra for aceita pelo AFD, False caso contrário.
        """
        # Reseta o estado atual para o estado inicial
        self.resetar()

        # Processa a palavra, símbolo a símbolo
        for simbolo in palavra:
            self.transitar(simbolo)
        
        # Determina a aceitação da palavra
        return self.aceita()
    
    def escrever_arquivo(self):
        """Escreve a definição do AFD em um arquivo de texto."""
        with open(f"{self.nome}.txt", 'w') as f:
            # Imprime número de estados
            f.write(f"{len(self.estados)}\n")
            # Imprime estado inicial
            f.write(f"{self.estado_inicial}\n")
            # Imprime estados de aceitação
            f.write(f"{','.join(self.estados_aceitacao)}\n")
            # Imprime alfabeto
            f.write(f"{','.join(self.alfabeto)}\n")
            # Imprime transições
            for (estado, simbolo), novo_estado in self.transicoes.items():
                f.write(f"{estado},{simbolo},{novo_estado}\n")

# Exemplo de uso da classe AFD (para rodar: python3 afd.py)
def main():
    # Definindo os estados, alfabeto, transições, estado inicial e estados de aceitação
    estados = {'q0', 'q1', 'q2'}
    alfabeto = {'a', 'b'}
    transicoes = {
        ('q0', 'a'): 'q1',
        ('q1', 'b'): 'q2',
        ('q2', 'a'): 'q0'
    }
    estado_inicial = 'q0'
    estados_aceitacao = {'q2'}

    # Criando o AFD
    afd = AFD("meu_afd", estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)

    # # Testando o AFD com algumas palavras
    # palavras = ['ab', 'a', 'b', 'aab', 'abb','abaab']
    # for palavra in palavras:
    #     resultado = afd.avaliar_palavra(palavra)
    #     print(f"A palavra '{palavra}' é aceita? {"Sim" if resultado else "Não"}")

    afd.escrever_arquivo()
    print(f"Definição do AFD escrita no arquivo '{afd.nome}.txt'.")

if __name__ == "__main__":
    main()

