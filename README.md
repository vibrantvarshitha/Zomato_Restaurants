# Zomato_Restaurant

<img src="/images/readme_image.jpg" alt="Alt text" title="Optional title">

## Problema de Negócio

Zomato é uma plataforma de MarketPlace popular na India de agregação de restaurantes e entrega de alimentos que permite aos usuários navegar por menus, fotos e avaliações de restaurantes, bem como pedir comida online para entrega ou retirada.

O objetivo deste projeto é gerar um Dashboard interativo para a empresa, a fim de fornecer insights sobre as métricas de negócios para auxiliar o direcionamento estratégico da empresa. 

Para disso, serão utilizadas técnicas avançadas de análise de dados, como a mineração de dados e modelagem estatística, para fornecer insights mais profundos e precisos. O painel será projetado para ser altamente interativo, permitindo que os usuários explorem as métricas de negócios em diferentes níveis de detalhe.

Os dados utilizados são de domínio público e podem ser encontrados nesse site do [kaggle](https://www.kaggle.com/code/bibekrai44/zomato-restaurant-analysis):

| Coluna | Descrição |
| --- | --- |
| index | Número do índice da linha no conjunto de dados |
| restaurant_id | ID único do restaurante |
| restaurant_name | Nome do restaurante |
| country_code | Código ISO de dois caracteres do país onde o restaurante está localizado |
| city | Nome da cidade onde o restaurante está localizado |
| address | Endereço físico do restaurante |
| locality | Nome da área onde o restaurante está localizado |
| locality_verbose | Nome detalhado da área onde o restaurante está localizado |
| longitude | Coordenada de longitude do restaurante |
| latitude | Coordenada de latitude do restaurante |
| cuisines | Tipos de culinária oferecidos pelo restaurante |
| average_cost_for_two | Preço médio para duas pessoas comerem no restaurante |
| currency | Moeda na qual os preços do restaurante são exibidos |
| has_table_booking | Indica se o restaurante aceita reservas de mesa |
| has_online_delivery | Indica se o restaurante oferece entregas online |
| is_delivering_now | Indica se o restaurante está entregando no momento |
| switch_to_order_menu | Indica se o restaurante permite a mudança para um menu de pedido especial |
| price_range | Faixa de preço do restaurante |
| aggregate_rating | Média das avaliações de clientes (em uma escala de 0 a 5) |
| rating_color | Cor que representa a avaliação do restaurante |
| rating_text | Texto que representa a avaliação do restaurante |
| votes | Número total de avaliações de clientes para o restaurante |

## Estratégia:

1. **Extração de dados:** Coletar dados do kaggle
2. **Limpeza de dados**: Limpeza geral dos dados como remoção de valores nulos, tratar outliers, criação de novas colunas como continente e classificação dos preços, remoção de outliers 
3. A**nálise exploratória dos dados:** Agrupamento dos dados em diferentes níveis, criação de gráficos e mapas.
4. **Dashboard em Nuvem:** Permitirá a interação dos usuários com os dados e insights gerados durante as etapas anteriores.
