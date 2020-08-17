import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Covid-19 Web App")


def removeAfterComma(string):
    return string.split('/')[0].strip()

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
    


#Brasil
st.header("Dados - Brasil")


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
