from sys import argv
from lexico.analisador_lexico import AnalisadorLexico

def main():
    if len(argv) != 3:
        print("Uso: python main.py <entrada.txt> <saida.txt>")
        return
    
    if not argv[1].endswith('.txt') or not argv[2].endswith('.txt'):
        print("Os arquivos de entrada e saída devem ter a extensão .txt")
        return
    
    entrada = argv[1]
    saida = argv[2]

    analisador = AnalisadorLexico(entrada, saida)
    analisador.analisar()

if __name__ == "__main__":
    main()