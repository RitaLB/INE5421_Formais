# Parseando arquivo de entrada para identificação das ERs, criandodicionario com o nome dos padrões e 
# a ER. Posteriormente, transformo as ERs em arvore binaria (grafo de nodos):
"""
Os arquivos com ER devem seguir o padrão:
def-reg1: ER1
def-reg2: ER2
. . .
def-regn: ERn
As ER devem aceitar grupos como [a-zA-Z] e [0-9] e os operadores usuais de * (fecho), +
(fecho positivo), ? (0 ou 1) e | (ou).
• Exemplo1:
id: [a-zA-Z]([a-zA-Z] | [0-9])*
num: [1-9]([0-9])* | 0
• Exemplo 2:
er1: a?(a | b)+
er2: b?(a | b)+
"""

from abc import ABC

class Parser(ABC):
    # Função para expandir os padrões de ERs no caso de existirem grupos.
    # ex: [a-zA-Z] -> (a|b|c|...|z|A|B|C|...|Z)
    # faz z - a e itera por todos os caracteres entre a e z, adicionando-os na lista
    # depois faz Z - A e itera por todos os caracteres entre A e Z, adicionando-os na lista

    @staticmethod
    def find_bracket_groups(expr_str: str) -> list[str]:
        """
        Encontra todos os grupos de colchetes (como [a-z], [0-9]) em uma string de expressão.
        Substitui a funcionalidade de re.findall(r'\[[^\]]+\]', expr_str).

        Args:
            expr_str: A string da expressão regular a ser parseada.

        Returns:
            Uma lista de strings, onde cada string é um grupo encontrado (e.g., ["[a-zA-Z]", "[0-9]"]).
        """
        groups_found = []
        i = 0
        n = len(expr_str)
        while i < n:
            if expr_str[i] == '[':
                start_bracket_pos = i
                j = i + 1  # Ponteiro para encontrar o colchete de fechamento ']'
                
                end_bracket_pos = -1 # Inicializa como não encontrado
                # Procura pelo colchete de fechamento ']'
                while j < n:
                    if expr_str[j] == ']':
                        end_bracket_pos = j
                        break
                    j += 1
                
                if end_bracket_pos != -1: # Se encontrou um ']'
                    # Verifica se o conteúdo entre colchetes não está vazio
                    # Ex: "[abc]" é válido, "[]" não é (pois [^\]]+ requer ao menos um caractere)
                    if end_bracket_pos > start_bracket_pos + 1: # Se tem conteúdo
                        groups_found.append(expr_str[start_bracket_pos : end_bracket_pos + 1])
                        i = end_bracket_pos + 1  # Continua a busca após o grupo encontrado
                    else:
                        # É um grupo vazio como "[]", que não corresponde a r'\[[^\]]+\]'
                        # Avança para depois do ']' encontrado para evitar reprocessamento indevido
                        i = end_bracket_pos + 1
                else:
                    # Não encontrou colchete de fechamento para o '[' em start_bracket_pos
                    # Avança para o próximo caractere após o '[' inicial para continuar a busca
                    i = start_bracket_pos + 1
            else:
                # Caractere atual não é '[', apenas avança
                i += 1
                
        return groups_found

    @staticmethod
    def expand_group(group_str):
        """
        Expande uma string de grupo como [a-zA-Z0-9] para (a|b|...|z|A|...|Z|0|...|9)
        """
        chars = []
        i = 1  # começa após o [
        while i < len(group_str) - 1:
            if i+2 < len(group_str) - 1 and group_str[i+1] == '-':
                start = group_str[i]
                end = group_str[i+2]
                for c in range(ord(start), ord(end) + 1):
                    chars.append(chr(c))
                i += 3  # pula o intervalo
            else:
                chars.append(group_str[i])
                i += 1
        return '(' + '|'.join(chars) + ')'

    @staticmethod
    def expand_regex_expression(expr):
        # Encontra todos os grupos como [a-z], [a-zA-Z], etc.
        matches = Parser.find_bracket_groups(expr)
        for m in matches:
            expanded = Parser.expand_group(m)
            expr = expr.replace(m, expanded)
        return expr
    
    @staticmethod
    def process_er_file(filename):
        result = {}
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or ':' not in line:
                    continue
                name, expr = line.split(':', 1)
                name = name.strip()
                expr = expr.strip()
                expanded_expr = Parser.expand_regex_expression(expr)
                result[name] = expanded_expr.replace(" ", "")
        return result

# teste
if __name__ == "__main__":
    er_dict = Parser.process_er_file("entrada.txt")
    er_dict = Parser.process_er_file("entrada.txt")
    for name, expr in er_dict.items():
        print(f"{name}: {expr}")