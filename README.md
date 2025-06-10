# Análise Léxica

Nesse projeto, criamos um Analisador léxico, capaz de gerar tokens, contendo lexeme e padrão, para um dado código fonte, dado um arquivo contendo as expressões regulares que definem cada padrão de lexemas.

Para mais informações sobre o modelo de entradas e fluxo de execução, veja o arquivo "Trabalho20251.pdf"

## Como rodar

Estando na pasta do repositório, rode o arquivo main, informando o caminho para o arquivo onde estão contidas as Expressões Regulares e para o arquivo contendo o texto fonte a ser analisado.

```cmd
python3 main.py caminho/para/ers.txt caminho/para/texto-fonte.txt
```

## Estrutura do projeto
- afd.py: define a classe para Autômatos Finitos Determinísticos (AFDs)
- afnd.py: define a classe para Autômatos Finitos Não-Determinísticos (AFNDs)
- analisador_lexico: define a classe para Analisador Léxico (classe principal do código)
- main.py: arquivo de execução principal (executa a aplicação)
- parser.py: define a classe Parser (classe que lê ERS do arquivo de entrada e expande seus intervalos)
- tree.py: define as classes Tree, Node e filhos de Node (implementam uma análise léxica)