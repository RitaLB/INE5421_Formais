# PArseando arquivo de entrada para identificação das ERs, criando a arvore binaria da er (grafo de nodos):
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
