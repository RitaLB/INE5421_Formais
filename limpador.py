from pathlib import Path

class Limpador:

    @staticmethod
    def limpar():
        """Limpa o diretório, removendo todos os autômatos, tabelas e o arquivo
        de tokens."""

        # Caminho das pastas e arquivos a serem limpos
        caminho_automatos = Path("automatos")
        caminho_tabelas = Path("tabelas")
        caminho_tokens = Path("tokens.txt")

        # Remove todos os arquivos da pasta de autômatos
        for arquivo in caminho_automatos.iterdir():
            if arquivo.is_file():
                arquivo.unlink()

        # Remove todos os arquivos da pasa de tabelas
        for arquivo in caminho_tabelas.iterdir():
            if arquivo.is_file():
                arquivo.unlink()
        

        # Remove o arquivo de tokens
        try:
            caminho_tokens.unlink()
        except FileNotFoundError:
            pass # O arquivo nem existia, apenas seguimos

        print("Limpeza concluída! 🧹🗑️")
    
def main():
    pasta_atual = Path.cwd()
    if pasta_atual.name == "INE5421_Formais":
        Limpador.limpar()
    else:
        print("Calma lá! Você precisa estar na pasta INE5421_Formais para executar este arquivo!")

if __name__ == "__main__":
    main()