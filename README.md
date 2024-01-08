# Dashboard com informações sobre ações

## Objetivo:
Criar uma aplicação web monstrando um painel contendo duas seções:
    1. Um gráfico de *candlestick* com os valores de abertura, fechamento, mínimo e máximo de uma ação;
    2. Alguns links das últimas notícias sobre a ação escolhida.

## Funcionamento:
Ao selecionar uma ação, dentre as disponíveis, o painel atualiza a cotação e faz uma busca pelas últimas notícias no site https://braziljournal.com/.

## Ferramentas utilizadas:
    - API **Yahoo Finance** para aquisição das cotações
    - **Beautifulsoup** para a coleta das notícias ( *web scrapping* )
    - **Plotly** para graficar
    - Framework **Dash Plotly** para a construção da aplicação em Python
    - Servidor em núvem *Render* para disponibilizar a aplicação

## Acesso:
O dashboard pode ser acessado através do link https://stock-info-dashboard-app.onrender.com/