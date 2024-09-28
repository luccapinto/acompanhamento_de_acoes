Descrição:

Este aplicativo permite que você selecione ações para visualizar seus preços de fechamento ao longo do tempo, com a possibilidade de escolher o intervalo de datas. Além disso, ele exibe um ranking dos retornos percentuais das ações selecionadas.

Funcionalidades:

- Seleção de múltiplas ações de uma lista pré-definida.
- Escolha personalizada do intervalo de datas.
- Exibição de gráficos interativos com rótulos de dados.
- Ranking das ações com base nos retornos percentuais, exibido na barra lateral.
- Formatação dos retornos com uma casa decimal e símbolo %.
- Índice do ranking correspondente à posição das ações.

Como Executar:

1. Pré-requisitos:

   - Python 3 instalado.
   - Bibliotecas necessárias instaladas:

     ```
     pip install streamlit yfinance pandas altair
     ```

2. Execução:

   Salve o código em um arquivo chamado `app.py` e execute:

   ```
   streamlit run app.py
   ```

3. Uso:

   - No navegador, selecione as ações que deseja analisar.
   - Escolha as datas de início e fim.
   - Visualize os gráficos e o ranking de retornos na barra lateral.

Notas:

- Ações Brasileiras:

  - Para ações que terminam com `.SA`, é importante usar os parâmetros corretos no `yf.download()`.
  - Certifique-se de que o `yfinance` está atualizado para evitar problemas ao baixar dados de ações brasileiras.

- Rótulos de Dados nos Gráficos:

  - A cor dos rótulos é definida como 'black' para melhor visibilidade no tema claro.
  - Se estiver usando o tema escuro, você pode alterar `color='white'` nos parâmetros de `mark_text()`.

Personalizações Futuras:

- Adicionar a detecção automática do tema do Streamlit para ajustar a cor dos rótulos.
- Permitir que o usuário escolha a cor dos rótulos e do gráfico.
- Incluir mais indicadores financeiros e métricas.

