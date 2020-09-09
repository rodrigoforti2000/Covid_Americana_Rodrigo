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

regiao_names = {"SP":"Sudeste",
                      "RJ":"Sudeste",
                      "MG":"Sudeste",
                      "ES":"Sudeste",
                      "CE":"Nordeste",
                      "BA":"Nordeste",
                      "PE":"Nordeste",
                      "PB":"Nordeste",
                      "RN":"Nordeste",
                      "MA":"Nordeste",
                      "AL":"Nordeste",
                      "PI":"Nordeste",
                      "SE":"Nordeste",
                      "RS":"Sul",
                      "PR":"Sul",
                      "SC":"Sul",
                      "DF":"DF",
                      "MS":"Centro-Oeste",
                      "GO":"Centro-Oeste",
                      "MT":"Centro-Oeste",
                      "AC":"Norte",
                      "AM":"Norte",
                      "PA":"Norte",
                      "RO":"Norte",
                      "RR":"Norte",
                      "TO":"Norte",
                      "AP":"Norte"}

def get_reg(estado):
  return regiao_names[estado]

@st.cache
def load_data():
        covid = pd.read_csv("https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities-time.csv")
        covid = covid.loc[:, ["date", "state", "city", "totalCases", "deaths", "newDeaths", "newCases"]]
        covid.columns = ["Ult_atualização", "Estado", "Cidade", "Total de Casos", "Mortes", "Novas Mortes", "Novos Casos"]
        covid = covid[covid.Estado != "TOTAL"]
        covid["Cidade"] = covid["Cidade"].apply(removeAfterComma)
        covid["Cidade"] = covid["Cidade"].apply(str.upper)
        covid["Estado"] = covid["Estado"].apply(str.upper)
        covid["Regiao"] = covid.Estado.apply(get_reg)
        return covid


covid = load_data()

#--------------------------------------------------------------------------------------
if add_selectbox == "Bem Vindo":
     #Brasil
    st.header("Bem vindo!")
    st.write("Essa aplicação web foi criada com o objetivo de facilitar a visualização e a análise dos dados da COVID-19 no Brasil. É possível escolher a área desejada no menu à esquerda.")
    st.write("Essa aplicação web foi criada por Rodrigo Forti. Os dados usados para a construção das análises são provenientes do Github.")
    st.write("Dados Brasil: https://raw.githubusercontent.com/peixebabel/COVID-19/master/data/casos-br-total.csv")
    st.write("Dados Estados e Cidades: https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities-time.csv")

#--------------------------------------------------------------------------------------
if add_selectbox == "Brasil":
     #Brasil
    st.header("Dados - Brasil")
    
    @st.cache
    def load_brasil(): 
        covid = pd.read_csv("https://raw.githubusercontent.com/peixebabel/COVID-19/master/data/casos-br-total.csv")
        covid.Mortes[covid.Mortes == "#REF!"] = ['64330.5','64330.5']
        covid.Mortes = covid["Mortes"].astype(float)
        m_diarias = np.array(covid["Mortes"]) - np.array(covid["Mortes"].shift())
        covid["mortes_diarias"] = m_diarias
        mm = []
        for i in range(7,len(covid)):
           mm.append(covid.mortes_diarias.iloc[range(i-7, i)].mean())
        covid["media_movel"] = [np.nan for __ in range(7)] + mm
        covid["media_movel"] = covid.media_movel.round()
        return covid

    brasil = load_brasil()

    st.write("Última atualização em: ")
    st.write(brasil.Data.tail(1))
    

    fig, ax = plt.subplots(figsize = (10,5))
    ax.plot(range(len(brasil)), brasil.mortes_diarias, label='Mortes Diárias \nHoje = ' + str(round(brasil.mortes_diarias.values[-1],0)))
    ax.plot(range(len(brasil)), brasil.media_movel, label= 'Média Móvel de Mortes Diárias \nHoje = ' + str(round(brasil.media_movel.values[-1],0)))
    plt.title("Mortes por COVID-19 no Brasil", loc = "left")
    plt.xlabel("Dias")
    plt.ylabel("Mortes")
    ax.legend(loc='upper left', shadow=True)
    st.pyplot()

#---------------------------------------------------------------------------------------
if add_selectbox == "Estados":
    #Estados
    st.header("Dados - Estados")

    st.write("Última atualização em:")
    st.write(covid["Ult_atualização"].tail(1))
    
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

    #Grafico2
    regiao_box = st.selectbox(
    'Selecione uma região', np.unique(covid.Regiao))

    regiao = covid[covid.Regiao == regiao_box]
    regiao_mortes = regiao.groupby(["Ult_atualização","Estado"]).sum()["Novas Mortes"]
    regiao_mortes = regiao_mortes.reset_index()

    regiao_semanal = []
    est = []
    count_sem = []
    for i in np.unique(regiao_mortes.Estado):
      k = 1
      for j in range(1, (len(regiao_mortes[regiao_mortes.Estado == i]) - 7), 7):
        x = regiao_mortes[regiao_mortes.Estado == i][j:j+7].sum()["Novas Mortes"]
        regiao_semanal.append(x)
        est.append(i)
        count_sem.append(k)
        k += 1
        
    mse = pd.DataFrame({"Estado":est,"Mortes":regiao_semanal, "Semana":count_sem})

    st.write("Mortes por Semana em cada Estado")
    g = sns.FacetGrid(mse, col = "Estado", col_wrap= 3)
    g = g.map_dataframe(sns.lineplot,
                 x = "Semana",
                 y = "Mortes")
    plt.xlabel("Semana")
    plt.ylabel("Mortes")
    st.pyplot()


#-------------------------------------------------------------------------------------
if add_selectbox == "Cidades":
    #CIdade
    st.header("Dados - Cidade")
    covid_table = covid.loc[:,["Ult_atualização", "Estado", "Cidade", "Total de Casos", "Mortes"]]
    cidade1 = st.selectbox(options = ["AMERICANA","SANTA BÁRBARA D'OESTE"], label = "Selecione a Cidade: ")
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
