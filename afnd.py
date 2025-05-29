from afd import AFD

class AFND:
    def __init__(self, nome: str, estados: set[str], alfabeto: set[str], transicoes: dict[tuple[str, str], str], estado_inicial: str, estados_aceitacao: set[str]):
        """Inicializa o AFD com os estados, alfabeto, transições, estado inicial
        e estados de aceitação.
            
        Args:
            nome (str): Nome do AFND (importante para identificação).
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

        # Adiciona um novo estado inicial, que vai para os antigos iniciais com transições epsilon
        estados.add('s')
        estado_inicial = 's'
        transicoes[(estado_inicial, '&')] = {f"{af1.estado_inicial}_1", f"{af2.estado_inicial}_2"}

        # Retorna o novo AFND
        return cls("Unido", estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)
    
    def resetar(self) -> None:
        """Reseta os ramos do AFND para o estado inicial (e seu E-fecho)."""
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

        # Utiliza uma pilha para explorar os estados alcançáveis por transições epsilon
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
        # Para cada ramo, encontra os novos ramos possíveis com o símbolo atual
        for ramo in self.ramos:
            if (ramo, simbolo) in self.transicoes:
                # Se houver transição com o símbolo, adiciona os novos ramos
                novo = self.transicoes.get((ramo, simbolo), set())
                novos_ramos.update(novo)
                # Também adiciona os E-fechos dos novos estados
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

    def E_tabela(self) -> dict[frozenset[str], set[tuple[str, frozenset[str]]]]:
        """Gera uma tabela de transições do AFND, mas com conjuntos de estados 
        (apenas os conjuntos alcançáveis). Essa tabela é útil para determinizar
        o AFND posteriormente.

        Returns:
            dict[str, set[str]]: A tabela de transições epsilon do AFND.
        """

        # Cria uma pilha para armazenar os conjuntos de estados a serem processados
        # Inicia com o estado inicial e seus E-fechos
        pilha = [{self.estado_inicial}.union(self.E_fechos.get(self.estado_inicial, set()))]
        tabela = {}
        while len(pilha) > 0:
            # Pega o próximo conjunto de estados da pilha
            conjunto = pilha.pop()
            # Torna o conjunto imutável (conjuntos não podem ser chaves de dicionário)
            conjunto = frozenset(conjunto)
            # Se o conjunto ainda não estiver na tabela, adiciona-o
            if conjunto not in tabela:
                tabela[conjunto] = set()
                # Para cada símbolo do alfabeto, calcula o conjunto de estados para que ele transita
                for simbolo in self.alfabeto:
                    novo_conjunto = set()
                    for estado in conjunto:
                        if (estado, simbolo) in self.transicoes:
                            novo_conjunto.update(self.transicoes[(estado, simbolo)])
                            # Adiciona os E-fechos dos estados alcançados
                            fechos = [self.E_fechos.get(novo_estado, set()) for novo_estado in self.transicoes[(estado, simbolo)]]
                            novo_conjunto.update(estado_do_fecho for fecho in fechos for estado_do_fecho in fecho)

                    # Se o novo conjunto não estiver vazio, adiciona à tabela
                    # e à pilha para processamento posterior
                    if novo_conjunto:
                        tabela[conjunto].add((simbolo, frozenset(novo_conjunto)))
                        if frozenset(novo_conjunto) not in tabela:
                            pilha.append(frozenset(novo_conjunto))
        
        return tabela

    def determinizar(self) -> AFD:
        """Determiniza o AFND, convertendo-o em um AFD.

            Returns:
                O AFD resultante da determinização.
        """
        alfabeto = self.alfabeto
        # Gera a tabela de transições do AFND
        tabela = self.E_tabela()
        # Cria um mapeamento de conjuntos de estados para estados equivalentes
        equivalentes = {conjunto: f"q{i}" for i, conjunto in enumerate(tabela.keys())}
        estados = set(equivalentes.values())

        # Define o estado inicial e os estados de aceitação do AFD
        estado_inicial = equivalentes[frozenset([self.estado_inicial]).union(self.E_fechos.get(self.estado_inicial, set()))]
        estados_aceitacao = {equivalentes[conjunto] for conjunto in tabela.keys() if any(estado in self.estados_aceitacao for estado in conjunto)}
        # Cria as transições do AFD a partir da tabela de transições do AFND
        transicoes = {}
        for conjunto, novos_conjuntos in tabela.items():
            estado_atual = equivalentes[conjunto]
            for simbolo, novo_conjunto in novos_conjuntos:
                if novo_conjunto:
                    estado_proximo = equivalentes[novo_conjunto]
                    transicoes[(estado_atual, simbolo)] = estado_proximo
        
        # Retorna o AFD determinizado
        return AFD(f"{self.nome}_determinizado", estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)


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
    af1 = AFD("af1", estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)

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
    af2 = AFD("af2", estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)

    # Unindo os dois AFDs
    afnd = AFND.uniao(af1, af2)

    # Determinizando o AFND
    determinizado = afnd.determinizar()
    print("AFD Determinizado:")
    print(f"Estados: {determinizado.estados}")
    print(f"Alfabeto: {determinizado.alfabeto}")
    print(f"Estado Inicial: {determinizado.estado_inicial}")
    print(f"Estados de Aceitação: {determinizado.estados_aceitacao}")
    print("Transições:")
    for (estado, simbolo), proximo_estado in determinizado.transicoes.items():
        print(f"  {estado} --{simbolo}--> {proximo_estado}")

    # Testando o AFND com algumas palavras
    # palavras = ['0', '1', '00', '01', '10', '11', '000', '111', '010', '101',
    #             '110', '1111', '0000', '0011', '1100', '1110', '1010', '1001']
    # for palavra in palavras:
    #     resultado = determinizado.avaliar_palavra(palavra)
    #     print(f"A palavra '{palavra}' é aceita pelo AFND? {"Sim" if resultado else "Não"}")

    determinizado.escrever_arquivo()
    print(f"Definição do AFD determinizado escrita no arquivo '{determinizado.nome}.txt'.")

if __name__ == "__main__":
    main()