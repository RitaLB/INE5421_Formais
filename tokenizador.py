from afd import AFD
from afnd import AFND

class Tokenizador:
    """Classe que gera a lista de tokens a partir de um texto fonte."""
    
    def __init__(self, arquivo_entrada: str) -> None:
        """Inicializa o tokenizador com o arquivo de entrada."""
        self.arquivo_entrada = arquivo_entrada
        self.tokens: list[tuple[str, str]] = []

    def gerar_tokens(self, automato: AFD) -> None:
        """Gera a lista de tokens a partir do texto fonte usando o AFD fornecido.
        
        Args:
            automato (AFD): O autômato finito determinístico usado para tokenização.
        """
        with open(self.arquivo_entrada, 'r') as arquivo:
            conteudo = arquivo.read()

        for palavra in conteudo.splitlines():
            palavra = palavra.strip()
            resultado = automato.avaliar_palavra(palavra)
            if resultado[0]:
                identificador = resultado[1]
                self.tokens.append((palavra, identificador))
        
    def imprimir_tokens(self) -> None:
        """Imprime a lista de tokens gerados."""
        with open("tokens.txt", 'w') as arquivo:
            for token, identificador in self.tokens:
                arquivo.write(f"<{token}, {identificador}>\n")
        print("Tokens gerados e salvos em 'tokens.txt'.")


def main():
    tokenizador = Tokenizador("texto_exemplo.txt")
    # Definindo AFD que aceita palavras terminadas em 'a'
    afd1 = AFD(
        nome="A",
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
        nome="B",
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
        nome="C",
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
    # Determinizando o AFND
    afd_determinizado = afnd.determinizar()
    tokenizador.gerar_tokens(afd_determinizado)
    tokenizador.imprimir_tokens()
    

if __name__ == "__main__":
    # Exemplo de uso
    main()