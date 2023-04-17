# 1. Problema de negócio
A empresa Food Place é uma marketplace de restaurantes. Ou seja, seu core
business é facilitar o encontro e negociações de clientes e restaurantes. Os
restaurantes fazem o cadastro dentro da plataforma da Food Place, que disponibiliza
informações como endereço, tipo de culinária servida, se possui reservas, se faz
entregas e também uma nota de avaliação dos serviços e produtos do restaurante,
dentre outras informações.

O CEO precisa entender melhor o negócio
para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a
Food Place, e para isso, ele precisa que seja feita uma análise nos dados da
empresa e que sejam gerados dashboards, a partir dessas análises, para responder algumas perguntas, tais como:

## Geral
1. Quantos restaurantes únicos estão registrados?
2. Quantos países únicos estão registrados?
3. Quantas cidades únicas estão registradas?

## País
1. Qual o nome do país que possui mais cidades registradas?
2. Qual o nome do país que possui mais restaurantes registrados?
3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?

## Cidade
1. Qual o nome da cidade que possui mais restaurantes registrados?
2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?
3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?

## Restaurantes
1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
2. Qual o nome do restaurante com a maior nota média?
3. Qual o nome do restaurante que possui o maior valor de uma prato para duas pessoas?

## Tipos de Culinária
1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?
2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?
3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação?

O CEO também pediu que fosse gerado um dashboard que permitisse que ele
visualizasse as principais informações das perguntas que ele fez. 
O CEO precisa dessas informações o mais rápido possível, uma vez que ele também é novo na
empresa e irá utilizá-las para entender melhor a empresa Food Place para conseguir
tomar decisões mais assertivas.
O objetivo deste projeto é utilizar os dados que a empresa Food Place possui e responder as
perguntas feitas do CEO e criar o dashboard solicitado.

# 2. Premissas do negócio
1. O dataset possui 7527 registros.
2. Marketplace foi o modelo de negócio assumido.
3. Cada registro é de um restaurante único, porém pode ocorrer de ter mais de um restaurante com o mesmo nome (franquias)

# 3. Estratégia da solução
O dashboard foi desenvolvido de forma que apresente 3 tipos de visões sobre os dados.
Sendo estas visões divididas em: Countries, Cities e Cuisines
A página Home é possui um mapa interativo com a localização de cada restaurante cadastrado,
possui também as métricas gerais, como quantidade de restaurantes cadastrados, países, cidades, etc.

Cada visão é representada pelo seguinte conjunto de métricas.
1. Countries
    1. Quantidade de restaurantes registrados por país
    2. Quantidade de cidades registrados por país
    3. Média de avaliações feitas por país
    4. Média preço de um prato para duas pessoas por país

2. Cities
    1. Cidades com mais restaurantes cadastrados
    2. Cidades com mais restaurantes de avaliação média acima de 4
    3. Cidades com mais restaurantes de avaliação média abaixo de 2.5
    4. Cidades com mais restaurantes com tipos culinários distintos

3. Cuisines
    1. Melhores Restaurantes dos principais tipos culinários
    2. Top 10 Restaurantes
    3. Top 10 melhores tipos culinários
    4. Top 10 piores tipos culinários

# 4. Top 3 Insights de dados
1. O país India possui a maior quantidade de restaurantes registrados
2. A cidade com a maior quantidade de restaurantes com nota acima de 4 é a de Londres
3. A cidade com a maior diversidade culinária é a de Birmingham, com 32 tipos culinários diferentes

# 5. O produto final do projeto
Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet.

O painel pode ser acessado através desse link: https://food-place.streamlit.app/

# 6. Conclusão
O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.

# 7. Próximos passos
1. Tentar adicionar restaurantes de outros países
2. Criar novos filtros no dashboard
3. Adicionar novas visões de negócio