from afd import AFD

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
        self.E_transicoes = {estado: ramos for (estado, simbolo), ramos in transicoes.items() if simbolo == '&'}
        self.E_fechos = {estado: self.E_fecho(estado) for estado in estados}
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = estados_aceitacao
        self.resetar()
    
    @classmethod
    def uniao(cls, af1: AFD, af2: AFD) -> 'AFND':
        """Cria um AFND que representa a união de dois AFDs.
        
        Args:
            af1 (AFD): Primeiro AFD.
            af2 (AFD): Segundo AFD.
        
        Returns:
            AFND: Um novo AFND representando a união dos dois AFDs.
        """
        # União dos estados, alfabeto, transiçõesestados de aceitação (com ajustes no nome dos estados, para evitar conflitos)
        estados: set[str] = {f"{estado}_1" for estado in af1.estados}|({f"{estado}_2" for estado in af2.estados})
        alfabeto: set[str] = af1.alfabeto.union(af2.alfabeto)
        estados_aceitacao: set[str] = {f"{estado}_1" for estado in af1.estados_aceitacao}|{f"{estado}_2" for estado in af2.estados_aceitacao}
        transicoes: dict[tuple[str, str], set[str]] = {(f"{estado}_1", simbolo): set([f"{novo_estado}_1"]) for (estado, simbolo), novo_estado in af1.transicoes.items()}
        transicoes.update({(f"{estado}_2", simbolo): set([f"{novo_estado}_2"]) for (estado, simbolo), novo_estado in af2.transicoes.items()})

        estados.add('s')
        estado_inicial = 's'
        transicoes[(estado_inicial, '&')] = {f"{af1.estado_inicial}_1", f"{af2.estado_inicial}_2"}

        return cls(estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)
    
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
        #print(f"Transitando com o símbolo: {simbolo}")
        novos_ramos = set()
        for ramo in self.ramos:
            if (ramo, simbolo) in self.transicoes:
                novo = self.transicoes.get((ramo, simbolo), set())
                novos_ramos.update(novo)
                for estado in novo:
                    novos_ramos.update(self.E_fechos.get(estado, set()))
        self.ramos = novos_ramos
        #print(f"Ramos após a transição: {self.ramos}")

    def aceita(self) -> bool:
        """Verifica se algum dos ramos atuais é um estado de aceitação.
        
        Returns:
            True se algum ramo atual for um estado de aceitação, False caso contrário.
        """
        #print(f"Verificando aceitação nos ramos: {self.ramos}")
        #print(f"Estados de aceitação: {self.estados_aceitacao}")
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
    # Definindo AFD em que binário mod 3 = 0
    estados = {'q0', 'q1', 'q2'}
    alfabeto = {'0', '1'}
    estado_inicial = 'q0'
    estados_aceitacao = {'q0'}
    transicoes = {('q0', '0'): 'q0',
                  ('q0', '1'): 'q1',
                  ('q1', '0'): 'q2',
                  ('q1', '1'): 'q0',
                  ('q2', '0'): 'q1',
                  ('q2', '1'): 'q2'
    }
    af1 = AFD(estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)

    # Definind AFD que aceita binários pares
    estados = {'q0', 'q1'}
    alfabeto = {'0', '1'}
    estado_inicial = 'q0'
    estados_aceitacao = {'q0'}
    transicoes = {('q0', '0'): 'q0',
                  ('q0', '1'): 'q1',
                  ('q1', '0'): 'q0',
                  ('q1', '1'): 'q1'
    }
    af2 = AFD(estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)

    # Unindo os dois AFDs
    afnd = AFND.uniao(af1, af2)

    # Testando o AFND com algumas palavras
    palavras = ['0', '1', '00', '01', '10', '11', '000', '111', '010', '101', 
                '110', '1111', '0000', '0011', '1100', '1110', '1010', '1001']
    for palavra in palavras:
        resultado = afnd.avaliar_palavra(palavra)
        print(f"A palavra '{palavra}' é aceita pelo AFND? {"Sim" if resultado else "Não"}")

if __name__ == "__main__":
    main()