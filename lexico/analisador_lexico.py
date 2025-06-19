from lexico.parser import Parser
from lexico.afd import AFD
from lexico.afnd import AFND
from lexico.tree import Tree, Node, LeafNode

class AnalisadorLexico:
    def __init__(self, arquivo_ers: str, codigo_fonte: str):
        self.arquivo_ers = arquivo_ers
        self.codigo_fonte = codigo_fonte
        self.tokens = []

    def gerar_afd(self, tree: Node, nome: str) -> AFD:
        """
        Cria um autômato finito determinístico (AFD) a partir de uma árvore binária.
        """
        # Implementação do AFD
        from collections import deque
        # 1. Mapeia cada posição para seu símbolo
        pos_to_symbol = {}
        def mapear_folhas(node):
            if isinstance(node, LeafNode):
                #print("leaf_node", node.value)
                pos_to_symbol[node.position] = node.value
            elif hasattr(node, 'left'):
                #print("left")
                mapear_folhas(node.left)
                if hasattr(node, 'right'):
                    mapear_folhas(node.right)
            elif hasattr(node, 'child'):
                #print('child')
                mapear_folhas(node.child)

        mapear_folhas(tree)

        # 2. Obter follow_pos, first_pos, last_pos
        follow_pos = tree.follow_pos()
        first_pos = tree.first_pos

        # 3. Inicializações
        estado_inicial = frozenset(first_pos)
        estados = {estado_inicial}
        fila = deque([estado_inicial])
        transicoes = {}
        alfabeto = set(pos_to_symbol.values()) - {'#'}  # remove '#' (fim da palavra)
        estados_aceitacao = set()

        # 4. Mapeamento de conjuntos de posições para nomes de estado (opcional: para salvar nomes bonitos)
        nome_estados = {estado_inicial: "S0"}
        contador_nome = 1

        while fila:
            estado = fila.popleft()
            for simbolo in alfabeto:
                destinos = set()
                for pos in estado:
                    # print("pos:", pos, "simbolo:", simbolo)
                    if pos_to_symbol[pos] == simbolo:
                        destinos.update(follow_pos.get(pos, set()))
                if destinos:
                    destino_fset = frozenset(destinos)
                    if destino_fset not in nome_estados:
                        nome_estados[destino_fset] = f"S{contador_nome}"
                        contador_nome += 1
                        fila.append(destino_fset)
                        estados.add(destino_fset)
                    transicoes[(nome_estados[estado], simbolo)] = nome_estados[destino_fset]

        # 5. Determinar estados de aceitação
        for estado in estados:
            for pos in estado:
                if pos_to_symbol[pos] == '#':
                    estados_aceitacao.add(nome_estados[estado])
                    break

        # 6. Construir o AFD
        afd = AFD(
            nome=nome,
            estados=set(nome_estados.values()),
            alfabeto=alfabeto,
            transicoes=transicoes,
            estado_inicial=nome_estados[estado_inicial],
            estados_aceitacao=estados_aceitacao
        )

        return afd
    
    def gerar_tokens(self, automato: AFD) -> None:
        """Gera a lista de tokens a partir do texto fonte usando o AFD fornecido.
        
        Args:
            automato (AFD): O autômato finito determinístico usado para tokenização.
        """
        with open(self.codigo_fonte, 'r') as arquivo:
            conteudo = arquivo.read()

        for linha in conteudo.splitlines():
            for palavra in linha.split():
                palavra = palavra.strip()
                resultado = automato.avaliar_palavra(palavra)
                if resultado[0]:
                    identificador = resultado[1]
                    self.tokens.append((palavra, identificador))
                else:
                    self.tokens.append((palavra, "erro!"))  # E para erro
        
    def imprimir_tokens(self) -> None:
        """Imprime a lista de tokens gerados."""
        with open("tokens.txt", 'w') as arquivo:
            for token, identificador in self.tokens:
                arquivo.write(f"<{token}, {identificador}>\n")

    def analisar(self):
        expressoes = Parser.process_er_file(self.arquivo_ers)
        afds = []
        print("Iniciando análise léxica...")
        print()
        for nome, expressao in expressoes.items():
            print(f"Processando ER: {nome}...")
            tree = Tree.create_tree(expressao)
            automato = self.gerar_afd(tree, nome)
            afds.append(automato)
            automato.escrever_arquivo()
            automato.gerar_tabela()
            print(f"AFD '{nome}' criado e salvo em '{automato.nome}.txt' e {automato.nome}_tabela.txt.")
            print()
        afnd = AFND.uniao(afds)
        automato_final = afnd.determinizar()
        automato_final.escrever_arquivo()
        automato_final.gerar_tabela()
        print(f"AFD final criado e salvo em '{automato_final.nome}.txt' e {automato_final.nome}_tabela.txt.")
        self.gerar_tokens(automato_final)
        self.imprimir_tokens()
        print("Tokens gerados e salvos em 'tokens.txt'.")

def main():
    analisador = AnalisadorLexico("entrada.txt", "texto_exemplo.txt")
    analisador.analisar()

if __name__ == "__main__":
    main()
