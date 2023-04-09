# Atividades XML

## Tarefas

### Aula 1
  - Tarefa 1: Quantas tags ***page*** tem no arquivo?
 
  - Tarefa 2: Imprimir o *id* e *title* de cada uma das *page* do arquivo.
 
  - Tarefa 3: O usuário informa uma string de busca. Você deve listar apenas os *id* e *title* daquelas páginas em que aparece aquela string de busca no       *title*.
 
  - Tarefa 4: Há duas opções, você deve escolher aquela que preferir:
 
    - Opção 1: Caching. Crie um loop perguntando qual a string de busca. Quando houver uma busca, você deve armazenar o resultado em uma hash table, onde devem ficar armazenadas as buscas que já foram feitas. Assim, quando se procura novamente por uma mesma palavra de busca, o resultado sai mais rápido porque já está armazenado em uma hash table.
 
    - Opção 2: Hash invertida. Para cada string encontrada no *title* de todas as páginas, você deve inserir o resultado daquela busca em uma hash invertida. É bem parecido com o cache, mas agora você insere no cache todas as strings que encontrar no *title* das páginas do arquivo. Dessa forma, antes mesmo de iniciar o loop pelas strings de busca, você já pré-computou todas as possíveis buscas que podem ser feitas.
 
