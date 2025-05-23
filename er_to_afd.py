'''
Funcões para transformar expressões regulares em autômatos finitos determinísticos (AFDs)
'''

# Passo 1: transformar a expressão regular em uma árvore binária
def create_three( er : str):
    """
    Cria uma árvore binária a partir de uma expressão regular.
    """
    # Implementação da árvore binária

    pass

# Passo 2: transformar a árvore binária em um autômato finito determinístico (AFD)
def create_afd( three ):
    """
    Cria um autômato finito determinístico (AFD) a partir de uma árvore binária.
    """
    # Implementação do AFD

    pass


# Criação dos nodes da árvore binária, um para cada tipo de nodo (pois têm regras de lastpos e firstpos diferentes)
class Node:
    """
    Classe base para os nodos da árvore binária.
    """
    def __init__(self, value):
        self.left = None
        self.right = None
        # self.value = value ?

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
    def __init__(self, left, right):
        # super().__init__('concat') ?
        self.left = left
        self.right = right
    
    @property
    def is_nullable(self):
        return self.left.is_nullable and self.right.is_nullable
    
    @property
    def last_pos(self):
        # Implementar
        pass

    @property
    def first_pos(self):
        # Implementar
        pass

    def follow_pos(self):
        # Implementar
        pass

class OrNode(Node):
    """
    Nodo de alternância (ou) (|)
    """
    def __init__(self, left, right):
        # super().__init__('or') ?
        self.left = left
        self.right = right
    
    @property
    def is_nullable(self):
        return True # Conferir
    
    @property
    def last_pos(self):
        # Implementar
        pass

    @property
    def first_pos(self):
        # Implementar
        pass

    def follow_pos(self):
        # Implementar
        pass

class StarNode(Node):
    """
    Nodo de estrela (zero ou mais). (*)
    """
    def __init__(self, child):
        # super().__init__('star') ?
        self.child = child
    
    @property
    def is_nullable(self):
        return True # Conferir
    
    @property
    def last_pos(self):
        # Implementar
        pass

    @property
    def first_pos(self):
        # Implementar
        pass

    def follow_pos(self):
        # Implementar
        pass

class PlusNode(Node):
    """
    Nodo de mais (um ou mais). (+)
    """
    def __init__(self, child):
        # super().__init__('plus') ?
        self.child = child
    
    @property
    def is_nullable(self):
        return False # Conferir
    
    @property
    def last_pos(self):
        # Implementar
        pass

    @property
    def first_pos(self):
        # Implementar
        pass

    def follow_pos(self):
        # Implementar
        pass

class LeafNode(Node):
    """
    Nodo folha (caractere).
    """
    def __init__(self, value, nullable=False):
        # super().__init__(value) ?
        self.value = value
    
    @property
    def is_nullable(self):
        return False
    
    @property
    def last_pos(self):
        return {self.value}

    @property
    def first_pos(self):
        return {self.value}

    def follow_pos(self):
        return set()
    
