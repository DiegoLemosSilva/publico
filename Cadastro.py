import streamlit as st
import psycopg2
import pandas as pd



# Função para conectar ao banco de dados
schema="br_addidas"
def conectar_banco():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='DocDk4yiUfITsrVq',
            host='remotely-valued-pangolin.data-1.use1.tembo.io',  # ou o IP do seu servidor
            port='5432',        # ou a porta que você está usando
            
        )
        return conn
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")

# Função para buscar nomes no banco de dados
def busca_campo(conn,campo,base,filtro="Padrao"):
    campo = campo
    base = base
    filtro = filtro
    if filtro == "Padrao":
        query = f"select distinct {campo} from {schema}.{base} order by 1 asc"
    else:
        query = f"select distinct {campo} from {schema}.{base} where {filtro} order by 1 asc"

    return pd.read_sql_query(query, conn)[campo].tolist()


# Conectar ao banco de dados
conn = conectar_banco()


# Cria um container para agrupar os componentes
with st.container():
    col1, col2 = st.columns([1, 2])  # Ajuste os pesos conforme necessário

    # Adiciona os componentes nas colunas
    with col1:
        data_selecionada = st.date_input("Escolha uma data:")

    with col2:
        opcao_selecionada = st.selectbox("Selecione uma opção:", ("Instalação", "Desinstalação")) 

# Cria um container para agrupar os componentes
with st.container():
    # Cria colunas para alinhar os componentes
    col1, col2,col3,col4 = st.columns([1, 2,2,2])  # Ajuste os pesos conforme necessário

    # Adiciona os componentes nas colunas
    with col1:
        uf = busca_campo(conn,"uf","store")
        st.session_state.uf_selecionada = st.selectbox("Estado", uf)
        up_uf_selecionada = st.session_state.uf_selecionada

    with col2:
        cidade  = busca_campo(conn,"cidade","store",f"uf = '{st.session_state.uf_selecionada}'")
        st.session_state.cidade_selecionada = st.selectbox("Cidade:", cidade)
        up_cidade_selecionada = st.session_state.cidade_selecionada

    with col3:
        empresa  = busca_campo(conn,"store_name","store",f"uf = '{st.session_state.uf_selecionada}' and cidade = '{st.session_state.cidade_selecionada}'")
        st.session_state.empresa = st.selectbox("Empresa:", empresa) 
        up_empresa = st.session_state.empresa

    with col4:
        st.session_state.tipo_loja = st.selectbox("Selecione uma opção:", ("Franquias", "Lojas Propias","WHS"))
        
# Cria um container para agrupar os componentes

with st.container():
    # Cria colunas para alinhar os componentes
    col1, col2 = st.columns([3, 1])  # Ajuste os pesos conforme necessário
    with col1:
        produto = st.text_input("Digite o nome do Produto:")
    with col2:
        qtd = st.number_input("Quantidade:", min_value=1, value=1)

st.write("totas as medidas devem ser realizadas em cm: ")
with st.container():
    # Cria colunas para alinhar os componentes
    col1, col2,col3 = st.columns([2, 2,2])  # Ajuste os pesos conforme necessário
    
    with col1:
        altura = st.number_input("Altura:")
        
    with col2:
        largura = st.number_input("Largura:")
    with col3:
        comprimento = st.number_input("Comprimento:")
   



# Botão para limpar o carrinho
if st.button("Comfirmar"):
    #st.session_state.carrinho.clear()  # Limpa o carrinho corretamente
    st.success("Campanha Gerada com sucesso")

conn.close() 
   

