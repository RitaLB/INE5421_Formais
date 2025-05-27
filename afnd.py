class AFND:
    def __init__(self, estados: set[str], alfabeto: set[str], transicoes: dict[tuple[str, str], str], estado_inicial: str, estados_aceitacao: set[str]):
        """Inicializa o AFD com os estados, alfabeto, transições, estado inicial
        e estados de aceitação.
            
        Args:
            estados (set[str]): Conjunto de estados do AFD.
            alfabeto (set[str]): Conjunto de símbolos do alfabeto do AFD.
            transicoes (dict[tuple[str, str], str]): Dicionário que mapeia tuplas (estado, símbolo) para o próximo estado.
            estado_inicial (str): Estado inicial do AFD.
            estados_aceitacao (set[str]): Conjunto de estados de aceitação do AFD.
        """
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.E_transicoes = {estado: ramos for (estado, simbolo), ramos in transicoes.items() if simbolo == 'E'}
        self.E_fechos = {estado: self.E_fecho(estado) for estado in estados}
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = estados_aceitacao
        self.resetar()
    
    def resetar(self) -> None:
        """Reseta os ramos do AFND para o estado inicial."""
        self.ramos = set([self.estado_inicial])
        self.ramos = self.ramos.union(self.E_transicoes.get(self.estado_inicial, set()))
    
    def E_fecho(self, estado: str) -> set[str]:
        """Calcula o fecho epsilon de um estado, retornando todos os estados
        alcançáveis a partir do estado dado através de transições epsilon.
        
        Args:
            estado (str): O estado para o qual calcular o fecho epsilon.
        
        Returns:
            set[str]: Conjunto de estados alcançáveis através de transições epsilon.
        """
        fecho = set([estado])
        pilha = [estado]
        
        while pilha:
            atual = pilha.pop()
            for proximo in self.E_transicoes.get(atual, []):
                if proximo not in fecho:
                    fecho.add(proximo)
                    pilha.append(proximo)
        
        return fecho
    
    def transitar(self, simbolo: str) -> None:
        """Realiza uma transição com base no símbolo fornecido 
        (e nos ramos atuais), alterando os ramos do AFND.
        
        Args:
            simbolo (str): O símbolo a ser processado.
        """
        novos_ramos = set()
        for ramo in self.ramos:
            if (ramo, simbolo) in self.transicoes:
                novo = self.transicoes.get((ramo, simbolo), set())
                novos_ramos.update(novo)
                for estado in novo:
                    novos_ramos.update(self.E_fechos.get(estado, set()))
        self.ramos = novos_ramos

    def aceita(self) -> bool:
        """Verifica se algum dos ramos atuais é um estado de aceitação.
        
        Returns:
            True se algum ramo atual for um estado de aceitação, False caso contrário.
        """
        return any(ramo in self.estados_aceitacao for ramo in self.ramos)
    
    def avaliar_palavra(self, palavra: str) -> bool:
        """Avalia uma palavra no AFND, processando cada símbolo e verificando se a palavra é aceita.
        
        Args:
            palavra (str): A palavra a ser avaliada.
        
        Returns:
            True se a palavra for aceita pelo AFND, False caso contrário.
        """
        # Reseta os ramos para o estado inicial
        self.resetar()

        # Processa a palavra, símbolo a símbolo
        for simbolo in palavra:
            self.transitar(simbolo)
        
        # Determina a aceitação da palavra
        return self.aceita()
    
def main():
    # Definindo o autômato para linguagem que termina em "abb"
    estados = {'q0', 'q1', 'q2', 'q3'}
    alfabeto = {'a', 'b'}
    transicoes = {
        ('q0', 'a'): {'q0', 'q1'},
        ('q0', 'b'): {'q0'},
        ('q1', 'b'): {'q2'},
        ('q2', 'b'): {'q3'},
    }
    estado_inicial = 'q0'
    estados_aceitacao = {'q3'}

    # Criando o AFND
    afnd = AFND(estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)

    # Avaliando palavras
    palavras = ['abb', 'a', 'b', 'aab', 'abb', 'abaab', 'abbb', 'aaabb']
    for palavra in palavras:
        resultado = afnd.avaliar_palavra(palavra)
        print(f"A palavra '{palavra}' é aceita pelo AFND? {resultado}")

if __name__ == "__main__":
    main()