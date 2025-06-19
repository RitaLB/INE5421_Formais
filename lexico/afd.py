class AFD:
    """Classe que representa um Autômato Finito Determinístico (AFD)."""

    def __init__(self, nome:str, estados: set[str], alfabeto: set[str], transicoes: dict[tuple[str, str], str], estado_inicial: str, estados_aceitacao: set[str], mapeamento: dict[str, str] = None):
        """Inicializa o AFD com os estados, alfabeto, transições, estado inicial
           e estados de aceitação.
        
            Args:
                nome (str): Nome do AFD (importante para identificação).
                estados (set[str]): Conjunto de estados do AFD.
                alfabeto (set[str]): Conjunto de símbolos do alfabeto do AFD.
                transicoes (dict[tuple[str, str], str]): Dicionário que mapeia tuplas (estado, símbolo) para o próximo estado.
                estado_inicial (str): Estado inicial do AFD.
                estados_aceitacao (set[str]): Conjunto de estados de aceitação do AFD.
                mapeamento (dict[str, str], opcional): Mapeamento de estados de aceitação para identificadores (se None, usa o nome do AFD).
        """
        self.nome = nome
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = estados_aceitacao
        self.estado_atual = estado_inicial
        self.mapeamento = mapeamento if mapeamento is not None else {nome: estados_aceitacao}
        
    
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
    
    def avaliar_palavra(self, palavra: str) -> tuple[bool, str]:
        """Avalia uma palavra no AFD, processando cada símbolo e verificando se a palavra é aceita.
        Se for aceita, também retorna o identificador do estado de aceitação.
        
        Args:
            palavra (str): A palavra a ser avaliada.

        Returns:
            (bool, str): Uma tupla contendo um booleano que indica se a palavra é aceita e o identificador do estado de aceitação (ou None se não for aceita).
        """
        # Reseta o estado atual para o estado inicial
        self.resetar()

        # Processa a palavra, símbolo a símbolo
        for simbolo in palavra:
            self.transitar(simbolo)
        
        # Determina a aceitação da palavra
        if self.aceita():
            # Procura o identificador do estado de aceitação
            for identificador, estados in self.mapeamento.items():
                if self.estado_atual in estados:
                    return True, identificador
                
        return False, None
    
    def escrever_arquivo(self):
        """Escreve a definição do AFD em um arquivo de texto."""
        with open(f"automatos/{self.nome}.txt", 'w') as f:
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
    
    def gerar_tabela(self) -> str:
        """Gera uma representação em string da tabela de transições do AFD.
        
        Returns:
            str: A tabela de transições formatada como string.
        """
        tabela = "Tabela de Transições:\n"
        tabela += f"{'Estado':<10} "
        for simbolo in sorted(self.alfabeto):
            tabela += f"{simbolo:<10} "
        tabela += "Aceitação\n"
        tabela += "-" * (10 + 11 * len(self.alfabeto)) + "\n"
        for estado in self.estados:
            tabela += f"{estado:<10} "
            for simbolo in sorted(self.alfabeto):
                novo_estado = self.transicoes.get((estado, simbolo), "ERRO")
                tabela += f"{novo_estado:<10} "
            tabela += f"{'Sim' if estado in self.estados_aceitacao else 'Não':<10}\n"
        
        with open(f"tabelas/{self.nome}_tabela.txt", 'w') as f:
            f.write(tabela)

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

    # Testando o AFD com algumas palavras
    palavras = ['ab', 'a', 'b', 'aab', 'abb','abaab']
    for palavra in palavras:
        resultado = afd.avaliar_palavra(palavra)
        print(f"A palavra '{palavra}' é aceita? {"Sim" if resultado[0] else "Não"}")
        if resultado[0]:
            print(f"Identificador do estado de aceitação: {resultado[1]}")

    afd.escrever_arquivo()
    print(f"Definição do AFD escrita no arquivo '{afd.nome}.txt'.")

if __name__ == "__main__":
    main()

