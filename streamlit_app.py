import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Estatísticas",
    page_icon="📊",
    layout="wide"
)

# URL base da API
API_BASE_URL = "http://localhost:8000"

# Título principal
st.title("📊 Dashboard de Estatísticas de Vendas")
st.markdown("---")

# ========== SEÇÃO 1: Estatísticas Gerais ==========
st.header("📈 Estatísticas Gerais")

try:
    # Chama a API /stats
    response = requests.get(f"{API_BASE_URL}/stats")

    if response.status_code == 200:
        stats = response.json()

        # Exibe as métricas em colunas
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="Quantidade Total",
                value=f"{stats['total_qtd']:,}",
                help="Total de itens vendidos"
            )

        with col2:
            st.metric(
                label="Receita Total",
                value=f"R$ {stats['total_revenue']:,.2f}",
                help="Receita total de vendas"
            )

        with col3:
            st.metric(
                label="Preço Médio",
                value=f"R$ {stats['avg_price']:.2f}",
                help="Preço médio dos produtos"
            )

        with col4:
            # Análise FP
            fp_stats = stats.get('fp_analysis', {})
            acima = fp_stats.get('acima_limite', 0)
            abaixo = fp_stats.get('abaixo_limite', 0)
            st.metric(
                label="Análise FP",
                value=f"{acima} acima / {abaixo} abaixo",
                help=f"Produtos acima/abaixo do limite {stats.get('fp_limit', 'N/A')}"
            )

        st.success("✅ Dados carregados com sucesso!")

    else:
        st.error(f"❌ Erro ao carregar dados: Status {response.status_code}")

except requests.exceptions.ConnectionError:
    st.error("❌ Não foi possível conectar à API. Certifique-se de que ela está rodando em http://localhost:8000")
except Exception as e:
    st.error(f"❌ Erro inesperado: {str(e)}")

st.markdown("---")

# ========== SEÇÃO 2: Gráficos ==========
st.header("📊 Visualizações")

# Abas para diferentes gráficos
tab1, tab2 = st.tabs(["Histograma de Preços", "Histograma de Receita"])

try:
    # Busca os dados brutos para fazer os gráficos
    df = pd.read_csv('data/dados.csv')
    df['receita'] = df['preco'] * df['qtd']

    with tab1:
        # Histograma de Preços
        fig_preco = px.histogram(
            df,
            x='preco',
            nbins=20,
            title='Distribuição de Preços',
            labels={'preco': 'Preço (R$)', 'count': 'Quantidade'},
            color_discrete_sequence=['#1f77b4']
        )
        fig_preco.update_layout(
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig_preco, use_container_width=True)

        # Estatísticas do preço
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Preço Mínimo", f"R$ {df['preco'].min():.2f}")
        with col2:
            st.metric("Preço Máximo", f"R$ {df['preco'].max():.2f}")
        with col3:
            st.metric("Mediana", f"R$ {df['preco'].median():.2f}")

    with tab2:
        # Histograma de Receita
        fig_receita = px.histogram(
            df,
            x='receita',
            nbins=20,
            title='Distribuição de Receita',
            labels={'receita': 'Receita (R$)', 'count': 'Quantidade'},
            color_discrete_sequence=['#2ca02c']
        )
        fig_receita.update_layout(
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig_receita, use_container_width=True)

        # Estatísticas da receita
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Receita Mínima", f"R$ {df['receita'].min():.2f}")
        with col2:
            st.metric("Receita Máxima", f"R$ {df['receita'].max():.2f}")
        with col3:
            st.metric("Mediana", f"R$ {df['receita'].median():.2f}")

except FileNotFoundError:
    st.warning("⚠️ Arquivo de dados não encontrado em 'data/dados.csv'")
except Exception as e:
    st.error(f"❌ Erro ao carregar gráficos: {str(e)}")

st.markdown("---")

# ========== SEÇÃO 3: Teste do Endpoint /soma ==========
st.header("🧮 Testar Endpoint /soma")

with st.form("soma_form"):
    st.write("Digite dois números para somar:")

    col1, col2 = st.columns(2)

    with col1:
        num1 = st.number_input("Primeiro número", value=0, step=1)

    with col2:
        num2 = st.number_input("Segundo número", value=0, step=1)

    submitted = st.form_submit_button("Calcular Soma", type="primary")

    if submitted:
        try:
            response = requests.get(
                f"{API_BASE_URL}/soma",
                params={"a": num1, "b": num2}
            )

            if response.status_code == 200:
                result = response.json()
                st.success(f"✅ Resultado: {num1} + {num2} = **{result['resultado']}**")
            else:
                st.error(f"❌ Erro na API: Status {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error("❌ Não foi possível conectar à API")
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")

st.markdown("---")

# ========== RODAPÉ ==========
st.caption("💡 Certifique-se de que a API está rodando em http://localhost:8000")
st.caption("🔄 Os dados são atualizados em tempo real a cada interação")