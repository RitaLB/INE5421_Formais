# Análise Léxica

Nesse projeto, criamos um Analisador léxico, capaz de gerar tokens, contendo lexeme e padrão, para um dado código fonte, dado um arquivo contendo as expressões regulares que definem cada padrão de lexemas.

Para mais informações sobre o modelo de entradas e fluxo de execução, veja o arquivo "Trabalho20251.pdf"

## Como rodar

Estando na pasta do repositório, rode o arquivo main, informando o caminho para o arquivo onde estão contidas as Expressões Regulares e para o arquivo contendo o texto fonte a ser analisado.

```sh
python3 main.py caminho/para/ers.txt caminho/para/texto-fonte.txt
```
## Arquivos de Teste

Vários arquivos de teste se encontram na pasta 'testes' do diretório. Use-os para demonstrar a execução do projeto.

## Limpando o Diretório

Caso a quantidade de saídas fique muito poluída, você pode executar o arquivo limpador.py para limpar o diretório.
Sua execução retira todos os arquivos da pasta de autômatos e tabelas, e deleta o arquivo de tokens de saída (você precisa estar na pasta principal do projeto).
```sh
python3 limpador.py
```


## Estrutura do projeto
- afd.py: define a classe para Autômatos Finitos Determinísticos (AFDs)
- afnd.py: define a classe para Autômatos Finitos Não-Determinísticos (AFNDs)
- analisador_lexico: define a classe para Analisador Léxico (classe principal do código)
- main.py: arquivo de execução principal (executa a aplicação)
- parser.py: define a classe Parser (classe que lê ERS do arquivo de entrada e expande seus intervalos)
- tree.py: define as classes Tree, Node e filhos de Node (implementam uma análise léxica)
- limpador.py: define a classe Limpador, que retira os arquivos saídas do diretório