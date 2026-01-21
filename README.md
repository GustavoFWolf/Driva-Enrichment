#Driva-Enrichment

O projeto tem como solução utilizar um ambiente local com Docker contendo PostgreSQL, n8n, API feita com Python/FastAPI.
A API expõe um endpoint simulando a API de enriquecimento, e um endpoint da leitura de dados da camada GOLD, com os dados já enriquecidos.
O n8n cria workflows que coleta dados de enriquecimento, armazena os dados brutos na camada Bronze e processa, transformando-o na camada Gold.

Para subir o ambiente digite os comandos na terminal:
docker-compose build
docker-compose up

Para verificar se os containers estão rodando digite:
docker ps

Para testar o funcionamento da API digite no navegador http://localhost:3000/docs, no campo de Authorization coloque driva_test_key_abc123xyz789,
va em algum dos endpoints e aperte em try it out para ver o resultado em arquivo JSON.

Para testar o funcionamento do workflows via n8n, digite no navegador http://localhost:5678, crie um workflow novo e importe os arquivos JSON que estão dentro da pasta n8n, e execute eles.

