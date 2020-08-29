import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Covid-19 Web App")


def removeAfterComma(string):
    return string.split('/')[0].strip()

add_selectbox = st.sidebar.selectbox(
    'Selecione uma opção',
    ('Bem Vindo','Brasil', 'Estados', 'Cidades')
)

@st.cache
def load_data():
        covid = pd.read_csv("https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities-time.csv")
        covid = covid.loc[:, ["last_info_date", "state", "city", "totalCases", "deaths", "newDeaths", "newCases"]]
        covid.columns = ["Ult_atualização", "Estado", "Cidade", "Total de Casos", "Mortes", "Novas Mortes", "Novos Casos"]
        covid = covid[covid.Estado != "TOTAL"]
        covid["Cidade"] = covid["Cidade"].apply(removeAfterComma)
        covid["Cidade"] = covid["Cidade"].apply(str.upper)
        covid["Estado"] = covid["Estado"].apply(str.upper)
        return covid


covid = load_data()

#--------------------------------------------------------------------------------------
if add_selectbox == "Bem Vindo":
     #Brasil
    st.header("Bem vindo!")
    st.text("Essa aplicação web foi criada com o objetivo de facilitar a visualizção e a análise dos dados da COVID-19 no Brasil. É possível escolher a área desejada no menu à esquerda.")
    st.text("Essa aplicação web foi criada por Rodrigo Forti. Os dados usados para a construção das análises são provenientes do Github.")

#--------------------------------------------------------------------------------------
if add_selectbox == "Brasil":
     #Brasil
    st.header("Dados - Brasil")
    
    @st.cache
    def load_brasil():
        covid = pd.read_csv("https://raw.githubusercontent.com/peixebabel/COVID-19/master/data/casos-br-total.csv")
        m_diarias = np.array(covid["Mortes"]) - covid["Mortes"].shift()
        covid["mortes_diarias"] = m_diarias
        mm = []
        for i in range(7,len(covid)):
           mm.append(covid.loc[range(i-7,i), "mortes_diarias"].mean())
        covid["media_movel"] = [np.nan for __ in range(7)] + mm
        covid["media_movel"] = covid.media_movel.round()
        return covid

    brasil = load_brasil()
    

    fig, ax = plt.subplots(figsize = (10,5))
    ax.plot(range(len(brasil)), brasil.mortes_diarias, label='Mortes Diárias \nHoje = ' + str(round(brasil.mortes_diarias.values[-1],0)))
    ax.plot(range(len(brasil)), brasil.media_movel, label= 'Média Móvel de Mortes Diárias \nHoje = ' + str(round(brasil.media_movel.values[-1],0)))
    plt.title("Dados de Mortes Brasil", loc = "left")
    plt.xlabel("Dias")
    plt.ylabel("Mortes")
    ax.legend(loc='upper left', shadow=True)
    st.pyplot()

#---------------------------------------------------------------------------------------
if add_selectbox == "Estados":
    #Estados
    st.header("Dados - Estados")  
    
    #Gráfico
    deathstate = covid.groupby("Estado").sum()["Novas Mortes"].reset_index()
    deathstate.columns = ["Estado","Mortes"]
    sns.set(rc={'figure.figsize':(8,5)})
    sns.barplot(x = "Estado",
                y = "Mortes",
                data = deathstate,
                color = "#1F77B4",
                order = deathstate.sort_values("Mortes",ascending=False).Estado)
    plt.xticks(rotation=90)
    plt.xlabel("Estados")
    plt.ylabel("Mortes")
    plt.title('Mortes por COVID-19\nem cada estado', loc = "left", fontsize = 16)
    st.pyplot()


#-------------------------------------------------------------------------------------
if add_selectbox == "Cidades":
    #CIdade
    st.header("Dados - Cidade")
    covid_table = covid.loc[:,["Ult_atualização", "Estado", "Cidade", "Total de Casos", "Mortes"]]
    cidade1 = st.selectbox(options = ["AMERICANA","SANTA BÁRBARA D'OESTE","PIRACICABA"], label = "Selecione a Cidade: ")
    estado1 = st.selectbox(options = ["SP"], label = "Selecione o Estado: ")

    if cidade1 and estado1:
        st.table(covid_table[np.logical_and(covid.Estado == estado1, covid.Cidade == cidade1)].tail(1))

    st.text("Caso não tenha o local desejado, escolha digitando abaixo")
    cidade2 = st.text_input('Cidade: ')
    estado2 = st.text_input('Estado: ')

    if cidade2 and estado2:
        cidade = str.upper(cidade2)
        estado = str.upper(estado2)
        st.table(covid_table[np.logical_and(covid.Estado == estado, covid.Cidade == cidade)].tail(1))
