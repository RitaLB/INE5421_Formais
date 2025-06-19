'''
Funcões para transformar expressões regulares em autômatos finitos determinísticos (AFDs)
'''

from typing import Set, Dict
from abc import ABC
# Passo 1: transformar a expressão regular em uma árvore binária

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

class Tree(ABC):
    """Classe utilitária abstrata (não instanciável) para métodos estáticos relacionados a árvores."""

    @staticmethod
    def create_tree(er: str) -> Node:
        '''
        er = er + '#'  # Adiciona o símbolo de fim de palavra
        er = Tree.inserir_concatenacao(er)
        er_list = list(er)
        stack = []
        pos = 1
        position = len(er_list)
        tree = ConcatenationNode(None, None)
        stack.append(tree)

        for c in reversed(er_list):
            if c.isalnum() or c == '#':
                tree = 
            if c == ".":
            
        '''

        er = '(' + er + ')' + '#'  # Adiciona o símbolo de fim de palavra
        er = Tree.inserir_concatenacao(er)
        postfix = Tree.to_postfix(er)
        print("postfix =", postfix)
        stack = []
        pos = 1
        operadores = set('*+.|?')  # Conjunto de operadores válidos
        for c in postfix:
            if c not in operadores:
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
            elif c == '?':
                child = stack.pop()
                child.question_mark = True  # Marca o nodo como opcional
                stack.append(child)
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
        for i in range(len(er)):
            resultado += er[i]
            if i + 1 < len(er):
                a, b = er[i], er[i+1]
                if (a not in '(|' and b not in '|)*+.)?'):
                    resultado += '.'
        
        return resultado
    
    @staticmethod

    def to_postfix(er: str) -> str:
        """
        Converte uma expressão regular em notação infixa para notação pós-fixa (RPN).
        Utiliza o algoritmo de Shunting Yard.
        """
        precedencia = {'?': 3, '*': 3, '+': 3, '.': 2, '|': 1}
        output = []
        stack = []
        operadores = set(precedencia.keys())
        for c in er:
            if c not in operadores and c != '(' and c != ')':
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

class ConcatenationNode(Node):
    """
    Nodo de concatenação.
    """
    def __init__(self, left: Node, right: Node, nullable: bool = False):
        # super().__init__('concat') ?
        self.left = left
        self.right = right
        self.null = nullable
        self.question_mark = False  # Para indicar se é opcional (usado em ERs como a? ou b?)
    
    @property
    def is_nullable(self):
        return (self.left.is_nullable and self.right.is_nullable) or self.question_mark
    
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
        self.question_mark = False  # Para indicar se é opcional (usado em ERs como a? ou b?)
    
    @property
    def is_nullable(self):
        return self.left.is_nullable or self.right.is_nullable or self.question_mark
    
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
        self.question_mark = False  # Para indicar se é opcional (usado em ERs como a? ou b?)
    
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
        self.question_mark = False  # Para indicar se é opcional (usado em ERs como a? ou b?)
    
    @property
    def is_nullable(self):
        return self.question_mark # Conferir
    
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
    def __init__(self, value, position, nullable=False):
        # super().__init__(value) ?
        self.value = value
        self.null = nullable
        self.position = position
        self.question_mark = False

    @property
    def is_nullable(self):
        return self.question_mark
    
    @property
    def last_pos(self):
        return {self.position}

    @property
    def first_pos(self):
        return {self.position}

    def follow_pos(self):
        return {}   

# Passo 2: transformar a árvore binária em um autômato finito determinístico (AFD)
