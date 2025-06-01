'''
Funcões para transformar expressões regulares em autômatos finitos determinísticos (AFDs)
'''

from typing import Set, Dict, Tuple
from abc import ABC
from afd import AFD  # Importa a classe AFD definida em afd.py
# Passo 1: transformar a expressão regular em uma árvore binária



class Tree(ABC):
    """Classe utilitária abstrata (não instanciável) para métodos estáticos relacionados a árvores."""

    @staticmethod
    def create_tree(self,er: str) -> Node:
        er = Tree.inserir_concatenacao(er)
        postfix = Tree.to_postfix(er)
        stack = []
        pos = 1
        for c in postfix:
            if c.isalnum() or c == '#':
                stack.append(LeafNode(c, pos))
                pos += 1
            elif c == '*':
                child = stack.pop()
                stack.append(StarNode(child))
            elif c == '+':
                child = stack.pop()
                stack.append(PlusNode(child))
            elif c == '.':
                right = stack.pop()
                left = stack.pop()
                stack.append(ConcatenationNode(left, right))
            elif c == '|':
                right = stack.pop()
                left = stack.pop()
                stack.append(OrNode(left, right))
        return stack[0]


    @staticmethod
    def merge_follow(f1: Dict[int, Set[int]], f2: Dict[int, Set[int]]) -> Dict[int, Set[int]]:
        """
        Função auxiliar para unir dois dicionários de follow_pos.
        """
        merged = dict(f1)  # cópia
        for k, v in f2.items():
            if k in merged:
                merged[k] |= v
            else:
                merged[k] = set(v)
        return merged
    
    @staticmethod
    def inserir_concatenacao(er: str) -> str:
        """
            Função auxiliar adiciona concatenação explicita entre caracteres adjacentes
            na expressão regular.
            Exemplo: "ab" -> "a.b"
        """
        resultado = ""
        operadores = {'|', '*', '+', ')'}
        for i in range(len(er)):
            resultado += er[i]
            if i + 1 < len(er):
                a, b = er[i], er[i+1]
                if (a not in '(|' and b not in '|)*+.)'):
                    resultado += '.'
        return resultado
    
    @staticmethod

    def to_postfix(er: str) -> str:
        """
        Converte uma expressão regular em notação infixa para notação pós-fixa (RPN).
        Utiliza o algoritmo de Shunting Yard.
        """
        precedencia = {'*': 3, '+': 3, '.': 2, '|': 1}
        output = []
        stack = []
        for c in er:
            if c.isalnum() or c == '#':
                output.append(c)
            elif c == '(':
                stack.append(c)
            elif c == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # remove '('
            else:  # operador
                while stack and stack[-1] != '(' and precedencia.get(stack[-1], 0) >= precedencia.get(c, 0):
                    output.append(stack.pop())
                stack.append(c)
        while stack:
            output.append(stack.pop())
        return ''.join(output)


# Criação dos nodes da árvore binária, um para cada tipo de nodo (pois têm regras de lastpos e firstpos diferentes)
class Node:
    """
    Classe base para os nodos da árvore binária.
    """
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value

    @property
    def is_nullable(self):
        """
        Verifica se o nodo é nulo.
        """
        pass
    
    @property
    def last_pos(self):
        """
        Retorna o conjunto lastpos do nodo.
        """
        pass

    @property
    def first_pos(self):
        """
        Retorna o conjunto firstpos do nodo.
        """
        pass

    def follow_pos(self):
        """
        Retorna o conjunto followpos do nodo.
        """
        pass


class ConcatenationNode(Node):
    """
    Nodo de concatenação.
    """
    def __init__(self, left: Node, right: Node, nullable: bool = False):
        # super().__init__('concat') ?
        self.left = left
        self.right = right
        self.null = nullable
    
    @property
    def is_nullable(self):
        return (self.left.is_nullable and self.right.is_nullable) or self.null
    
    @property
    def last_pos(self):
        # Conferir
        if self.right.is_nullable:
            return self.left.last_pos.union(self.right.last_pos)
        return self.right.last_pos
    

    @property
    def first_pos(self):
        # Conferir
        if self.left.is_nullable:
            return self.left.first_pos.union(self.right.first_pos)
        return self.left.first_pos

    def follow_pos(self):
        """
        Retorna o conjunto followpos do nodo de concatenação.
        Regra: Para cada posição i em lastpos(left), adicionamos firstpos(right) ao followpos(i)
        Além disso, unimos com os followpos dos filhos.
        """
        follow = {}
        
        # 1. Unir os followpos dos filhos
        left_follow = self.left.follow_pos()
        right_follow = self.right.follow_pos()
        follow = Tree.merge_follow(left_follow, right_follow)
        
        # 2. Adicionar as regras específicas de concatenação
        # Para cada posição em lastpos do filho esquerdo, adicionamos firstpos do filho direito
        for pos in self.left.last_pos:
            if pos in follow:
                follow[pos].update(self.right.first_pos)
            else:
                follow[pos] = set(self.right.first_pos)
        
        return follow

class OrNode(Node):
    """
    Nodo de alternância (ou) (|)
    """
    def __init__(self, left: Node, right: Node):
        # super().__init__('or') ?
        self.left = left
        self.right = right
    
    @property
    def is_nullable(self):
        return self.left.is_nullable or self.right.is_nullable# Conferir
    
    @property
    def last_pos(self):
        # Conferir
        return self.left.last_pos.union(self.right.last_pos)

    @property
    def first_pos(self):
        # Conferir
        return self.left.first_pos.union(self.right.first_pos)
    
    def follow_pos(self):
        """
        Retorna o conjunto followpos do nodo de alternância.
        """
        return Tree.merge_follow(self.left.follow_pos(), self.right.follow_pos())


class StarNode(Node):
    """
    Nodo de estrela (zero ou mais). (*)
    """
    def __init__(self, child: Node):
        # super().__init__('star') ?
        self.child = child
    
    @property
    def is_nullable(self):
        return True # Conferir
    
    @property
    def last_pos(self):
        # Conferir
        return self.child.last_pos
    @property
    def first_pos(self):
        # Conferir
        return self.child.first_pos

    def follow_pos(self):
        """
        Retorna o conjunto followpos do nodo de estrela.
        Regra: Para cada posição i em lastpos(child), adicionamos firstpos(child) ao followpos(i).
        Além disso, herdamos os followpos do nó filho.
        """
        follow = self.child.follow_pos()  # Herda os followpos do filho
        
        # Adiciona a regra do operador *: lastpos(child) -> firstpos(child)
        for pos in self.child.last_pos:
            if pos in follow:
                follow[pos].update(self.child.first_pos)  # Adiciona firstpos(child) ao followpos(pos)
            else:
                follow[pos] = set(self.child.first_pos)  # Cria novo mapeamento
        
        return follow

class PlusNode(Node):
    """
    Nodo de mais (um ou mais). (+)
    """
    def __init__(self, child: Node):
        # super().__init__('plus') ?
        self.child = child
    
    @property
    def is_nullable(self):
        return False # Conferir
    
    @property
    def last_pos(self):
        # Implementar
        return self.child.last_pos

    @property
    def first_pos(self):
        # Implementar
        return self.child.first_pos

    def follow_pos(self):
        """
        Retorna o conjunto followpos do nodo de estrela.
        Regra: Para cada posição i em lastpos(child), adicionamos firstpos(child) ao followpos(i).
        Além disso, herdamos os followpos do nó filho.
        """
        follow = self.child.follow_pos()  # Herda os followpos do filho
        
        # Adiciona a regra do operador *: lastpos(child) -> firstpos(child)
        for pos in self.child.last_pos:
            if pos in follow:
                follow[pos].update(self.child.first_pos)  # Adiciona firstpos(child) ao followpos(pos)
            else:
                follow[pos] = set(self.child.first_pos)  # Cria novo mapeamento
        
        return follow

class LeafNode(Node):
    """
    Nodo folha (caractere).
    """
    def __init__(self, value, pos, nullable=False):
        # super().__init__(value) ?
        self.value = value
        self.null = nullable
        self.pos = pos
    
    @property
    def is_nullable(self):
        return self.null
    
    @property
    def last_pos(self):
        return {self.value}

    @property
    def first_pos(self):
        return {self.value}

    def follow_pos(self):
        return {}
    

# Passo 2: transformar a árvore binária em um autômato finito determinístico (AFD)
def create_afd(tree: Node) -> AFD:
    """
    Cria um autômato finito determinístico (AFD) a partir de uma árvore binária.
    """
    # Implementação do AFD
    from collections import deque

    # 1. Mapeia cada posição para seu símbolo
    pos_to_symbol = {}
    def mapear_folhas(node):
        if isinstance(node, LeafNode):
            pos_to_symbol[node.position] = node.value
        elif hasattr(node, 'left'):
            mapear_folhas(node.left)
            if hasattr(node, 'right'):
                mapear_folhas(node.right)
        elif hasattr(node, 'child'):
            mapear_folhas(node.child)

    mapear_folhas(tree)

    # 2. Obter follow_pos, first_pos, last_pos
    follow_pos = tree.follow_pos()
    first_pos = tree.first_pos
    last_pos = tree.last_pos

    # 3. Inicializações
    estado_inicial = frozenset(first_pos)
    estados = {estado_inicial}
    fila = deque([estado_inicial])
    transicoes = {}
    alfabeto = set(pos_to_symbol.values()) - {'#'}  # remove '#' (fim da palavra)
    estados_aceitacao = set()
    nome = "afd_da_er"

    # 4. Mapeamento de conjuntos de posições para nomes de estado (opcional: para salvar nomes bonitos)
    nome_estados = {estado_inicial: "S0"}
    contador_nome = 1

    while fila:
        estado = fila.popleft()
        for simbolo in alfabeto:
            destinos = set()
            for pos in estado:
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



