import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt
from datetime import datetime

st.title('📈 Análise de Ações')

# Lista de ações disponíveis para seleção
acoes = [
    'AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA', 'META', 'NFLX', 'NVDA', 'AMD', 'INTC'
]

# Permitir que o usuário selecione as ações
acoes_selecionadas = st.multiselect('Selecione as ações que deseja visualizar:', acoes)

if acoes_selecionadas:
    # Adicionar seleção de datas
    start_date = st.date_input('Data de Início', value=datetime(2024, 1, 1))
    end_date = st.date_input('Data de Fim', value=datetime.today())

    if start_date > end_date:
        st.error('A data de início não pode ser posterior à data de fim.')
    else:
        # Obter dados das ações selecionadas
        try:
            dados = yf.download(
                tickers=acoes_selecionadas,
                start=start_date,
                end=end_date,
                interval='1d',
                threads=True,
                auto_adjust=True
            )
        except Exception as e:
            st.error(f"Ocorreu um erro ao baixar os dados: {e}")
            dados = None

        if dados is not None and not dados.empty:
            # Garantir que 'dados['Close']' seja sempre um DataFrame
            if isinstance(dados['Close'], pd.Series):
                dados_close = dados[['Close']].rename(columns={'Close': acoes_selecionadas[0]})
            else:
                dados_close = dados['Close']

            # Calcular o retorno percentual no período
            retornos = {}
            for acao in acoes_selecionadas:
                if acao in dados_close.columns:
                    preco_inicio = dados_close[acao].dropna().iloc[0]
                    preco_fim = dados_close[acao].dropna().iloc[-1]
                    retorno = ((preco_fim - preco_inicio) / preco_inicio) * 100
                    retornos[acao] = retorno
                else:
                    retornos[acao] = None

            # Criar o ranking das ações
            ranking = pd.DataFrame(list(retornos.items()), columns=['Ação', 'Retorno (%)'])
            ranking = ranking.dropna().sort_values(by='Retorno (%)', ascending=False)

            # Redefinir o índice e começar em 1
            ranking.reset_index(drop=True, inplace=True)
            ranking.index += 1  # Iniciar em 1
            ranking.index.name = 'Posição'

            # Formatar a porcentagem
            ranking['Retorno (%)'] = ranking['Retorno (%)'].map('{:.1f}%'.format)

            # Exibir o ranking na barra lateral
            st.sidebar.title('🏆 Ranking de Retornos')
            st.sidebar.dataframe(ranking)

            # Exibir o gráfico para cada ação selecionada
            for acao in acoes_selecionadas:
                if acao in dados_close.columns:
                    st.subheader(f'Preço de Fechamento - {acao}')

                    # Preparar os dados para o Altair
                    df = dados_close[acao].reset_index()
                    df['Data'] = pd.to_datetime(df['Date']).dt.date

                    # Criar o gráfico com Altair
                    chart = alt.Chart(df).mark_line(color='blue').encode(
                        x='Data:T',
                        y=alt.Y(f'{acao}:Q', title='Preço de Fechamento')
                    )

                    # Adicionar rótulos de dados a cada N pontos
                    intervalo_rotulos = max(1, len(df) // 10)  # Mostrar rótulos a cada 10% dos dados

                    pontos = alt.Chart(df[::intervalo_rotulos]).mark_text(
                        align='left',
                        dx=5,
                        dy=-5,
                        color='black'  # Cor dos rótulos
                    ).encode(
                        x='Data:T',
                        y=f'{acao}:Q',
                        text=alt.Text(f'{acao}:Q', format='.2f')
                    )

                    # Exibir o gráfico com rótulos
                    st.altair_chart((chart + pontos).interactive(), use_container_width=True)
                else:
                    st.warning(f'Dados não disponíveis para {acao}.')
        else:
            st.error('Não foi possível obter os dados das ações selecionadas.')
else:
    st.write('Selecione ao menos uma ação para visualizar os dados.')
