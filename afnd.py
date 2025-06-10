from afd import AFD

class AFND:
    def __init__(self, nome: str, estados: set[str], alfabeto: set[str], transicoes: dict[tuple[str, str], str], estado_inicial: str, estados_aceitacao: set[str], mapeamento: dict[str, set[str]] = None):
        """Inicializa o AFD com os estados, alfabeto, transições, estado inicial
        e estados de aceitação.
            
        Args:
            nome (str): Nome do AFND (importante para identificação).
            estados (set[str]): Conjunto de estados do AFD.
            alfabeto (set[str]): Conjunto de símbolos do alfabeto do AFD.
            transicoes (dict[tuple[str, str], str]): Dicionário que mapeia tuplas (estado, símbolo) para o próximo estado.
            estado_inicial (str): Estado inicial do AFD.
            estados_aceitacao (set[str]): Conjunto de estados de aceitação do AFD.
            mapeamento (dict[str, str], opcional): Mapeamento de estados de aceitação para identificadores (se None, usa o nome do AFND).
        """
        self.nome = nome
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.E_transicoes = {estado: ramos for (estado, simbolo), ramos in transicoes.items() if simbolo == '&'}
        self.E_fechos = {estado: self.E_fecho(estado) for estado in estados}
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = estados_aceitacao
        self.mapeamento = mapeamento if mapeamento is not None else {nome: estados_aceitacao}
        self.resetar()
    
    @classmethod
    def uniao(cls, automatos: list[AFD]):
        """Cria um AFND que representa a união de múltiplos (2 ou +) AFDs.
           Estados são renomeados para evitar conflitos, e um novo estado 
           inicial é criado que transita por ε para os estados iniciais 
           de cada AFD.
        
        Args:
            automatos (list[AFD]): Lista de AFDs a serem unidos.
            
        Returns:
            Um novo AFND representando a união dos dois AFDs.
        """
        # União dos estados, alfabeto, transiçõesestados de aceitação (com ajustes no nome dos estados, para evitar conflitos)
        estados: set[str] = set()
        alfabeto: set[str] = set()
        estados_aceitacao: set[str] = set()
        transicoes: dict[tuple[str, str], set[str]] = {}
        mapeamento: dict[str, str] = {} # Mapeamento de estados de aceitação para identificadores (nome dos AFDs)


        # Estado inicial do novo AFND (transita por ε para os estados iniciais de cada AFD)
        estado_inicial = 'S'
        estados.add(estado_inicial)
        transicoes[(estado_inicial, '&')] = set()
        for af in automatos:
            # Cria um prefixo único para cada AFD para evitar conflitos de nomes
            prefixo = f"{af.nome}_"
            # Une estados, alfabeto, transições e estados de aceitação de cada AFD
            estados.update(f"{prefixo}{estado}" for estado in af.estados)
            alfabeto.update(af.alfabeto)
            estados_aceitacao.update(f"{prefixo}{estado}" for estado in af.estados_aceitacao)
            transicoes.update({(f"{prefixo}{estado}", simbolo): {f"{prefixo}{proximo_estado}"}
                               for (estado, simbolo), proximo_estado in af.transicoes.items()})
            # Adiciona transições epsilon do estado inicial do novo AFND para o antigo inicial de cada AFD
            transicoes[(estado_inicial, '&')].add(f"{prefixo}{af.estado_inicial}")
            # Mapeia os estados de aceitação para seus identificadores (AFDs antigos)
            mapeamento.update({af.nome: {f"{prefixo}{estado}" for estado in af.estados_aceitacao}})

        return cls("união", estados, alfabeto, transicoes, estado_inicial, estados_aceitacao, mapeamento)

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
        for identificador, estados in self.mapeamento.items():
            if any(estado in estados for estado in self.ramos):
                return True, identificador
        return False, None
    
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
        mapeamento = {nome: set() for nome in self.mapeamento.keys()}
        for conjunto, novo_estado in equivalentes.items():
            for identificador, estados_afd in self.mapeamento.items():
                if any(estado in conjunto for estado in estados_afd):
                    mapeamento[identificador].add(novo_estado)
        # Retorna o AFD determinizado
        return AFD("AFD_FINAL", estados, alfabeto, transicoes, estado_inicial, estados_aceitacao, mapeamento)


def main():
    # Definindo AFD que aceita palavras terminadas em 'a'
    afd1 = AFD(
        nome="afd1",
        estados={"q0", "q1"},
        alfabeto={"a", "b", "c", "d"},
        transicoes={
            ("q0", "a"): "q1",
            ("q0", "b"): "q0",
            ("q0", "c"): "q0",
            ("q0", "d"): "q0",
            ("q1", "a"): "q1",
            ("q1", "b"): "q0",
            ("q1", "c"): "q0",
            ("q1", "d"): "q0"
        },
        estado_inicial="q0",
        estados_aceitacao={"q1"}
    )
    # Definindo AFD que aceita palavras terminadas em 'b'
    afd2 = AFD(
        nome="afd2",
        estados={"q0", "q1"},
        alfabeto={"a", "b", "c", "d"},
        transicoes={
            ("q0", "a"): "q0",
            ("q0", "b"): "q1",
            ("q0", "c"): "q0",
            ("q0", "d"): "q0",
            ("q1", "a"): "q0",
            ("q1", "b"): "q1",
            ("q1", "c"): "q0",
            ("q1", "d"): "q0"
        },
        estado_inicial="q0",
        estados_aceitacao={"q1"}
    )
    # Definindo AFD que aceita palavras terminadas em 'c'
    afd3 = AFD(
        nome="afd3",
        estados={"q0", "q1"},
        alfabeto={"a", "b", "c", "d"},
        transicoes={
            ("q0", "a"): "q0",
            ("q0", "b"): "q0",
            ("q0", "c"): "q1",
            ("q0", "d"): "q0",
            ("q1", "a"): "q0",
            ("q1", "b"): "q0",
            ("q1", "c"): "q1",
            ("q1", "d"): "q0"
        },
        estado_inicial="q0",
        estados_aceitacao={"q1"}
    )
    # Criando AFND que aceita a união dos três AFDs
    afnd = AFND.uniao([afd1, afd2, afd3])

    # Testando o AFND com algumas palavras
    # palavras = ["a", "b", "c", "ab", "ac", "bc", "abc", "abcd", "aab", "bbd"]
    # for palavra in palavras:
    #     resultado = afnd.avaliar_palavra(palavra)
    #     print(f"A palavra '{palavra}' é aceita pelo AFND: {resultado[0]}")
    #     if resultado[0]:
    #         print(f"Identificador: {resultado[1]}")
    # Determinizando o AFND
    afd_determinizado = afnd.determinizar()
    # Testando o AFD determinizado com algumas palavras
    print("Mapeamento de estados de aceitação:")
    for identificador, estados in afd_determinizado.mapeamento.items():
        print(f"{identificador}: {', '.join(estados)}")
    palavras = ["a", "b", "c", "ab", "ac", "bc", "abc", "abcd", "aab", "bbd"]
    for palavra in palavras:
        resultado = afd_determinizado.avaliar_palavra(palavra)
        print(f"A palavra '{palavra}' é aceita pelo AFD determinizado: {resultado[0]}")
        if resultado[0]:
            print(f"Identificador do estado de aceitação: {resultado[1]}")
    
    # # Escreve arquivo do AFD determinizado
    # afd_determinizado.escrever_arquivo()
    # print(f"AFD determinizado '{afd_determinizado.nome}' escrito no arquivo.")

if __name__ == "__main__":
    main()