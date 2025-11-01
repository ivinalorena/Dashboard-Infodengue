import streamlit as st
import pandas as pd
import numpy as np
#from streamlit_elements import dashboard, elements, mui,nivo
import toml

# Titulo da página (header)
st.set_page_config("DashBoard InfoDengue", layout="wide")
st.title("Dashboard - InfoDengue")

geocode_cidades = {
    "Redenção": 2311603,
    "Acarape": 2300150,
    "Fortaleza": 2304400,
}

# Use selectbox para escolher apenas uma cidade
cidade_selecionada = st.selectbox("Selecione a cidade", options=list(geocode_cidades.keys()))

data_selecionada= st.date_input("selecione o ano que quer analisar", format="DD/MM/YYYY")
ano_selecionado_ano = data_selecionada.year  # retorna int, ex: 2024

#Comandos para acessar os dados da API
url = "https://info.dengue.mat.br/api/alertcity"
disease = "dengue"
format = "csv"
geocode = geocode_cidades[cidade_selecionada]
ew_start = 1
ew_end = 53
ey_start = ano_selecionado_ano
ey_end = ano_selecionado_ano
params =(
    "&disease="
    + f"{disease}"
    + "&geocode="
    + f"{geocode}"
    + "&disease="
    + f"{disease}"
    + "&format="
    + f"{format}"
    + "&ew_start="
    + f"{ew_start}"
    + "&ew_end="
    + f"{ew_end}"
    + "&ey_start=" 
    + f"{ey_start}"
    + "&ey_end="
    + f"{ey_end}"    
)

url_resp = "?".join([url, params])
dados = pd.read_csv(url_resp, index_col='SE')

# separação dos dados
dados['data_iniSE'] = pd.to_datetime(dados['data_iniSE']).dt.date 
dados_data= dados[["data_iniSE","casos"]].sort_values(by='data_iniSE')


#st.sidebar()
col1, col2 = st.columns([50,50])
with col1:
    with st.expander("Dados Brutos"):
        with st.container(border=True,horizontal_alignment = "center"):
            st.text(f"Dados brutos dos anos de {ano_selecionado_ano}, 1° semana até a 53° semana")
        #st.markdown("st.dataframe(): Ordena, destaque de linhas e células, permite filtragem, parecida com planilha interativa", width="content")
        st.dataframe(dados)

    with st.expander("Dados - Casos"):
        with st.container(border=True,horizontal_alignment = "left",gap="small"):
            st.text("DataFrame organizado e divido por semana e casos - Datas organizadas do mais antigo para o mais atual")
            st.dataframe(dados_data)

with col2:
    st.line_chart(dados_data,x = 'data_iniSE', x_label=f"1° a 53° semana de {ano_selecionado_ano}", y_label="N° de casos",color="#ea220487")
    # casos por ano?
    #fig = px.line(dados_data, x = 'data_iniSE', y = 'casos', title="Série temporal")
    #st.plotly_chart(fig)

st.caption("Dashboard desenvolvido por Ivina Lorena")