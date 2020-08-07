import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Covid-19")

# Dados Americana
#cidade = pd.read_csv("https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities-time.csv")
#americana = cidade[cidade["city"].str.startswith('Americana')]

#ameri_res = americana[["date", "city", "totalCases", "deaths", "newDeaths"]]
#ame_total_deaths = ameri_res.iloc[-1].deaths
#ame_total_cases = ameri_res.iloc[-1].totalCases
#ame_date_final = ameri_res.iloc[-1].date

#tabela = pd.DataFrame(np.array([[ame_date_final, ame_total_cases, ame_total_deaths]]),
#                      columns=["Data", "Total Casos", "Total Mortes"])

# Dados Brasil
#covid = pd.read_csv("https://raw.githubusercontent.com/peixebabel/COVID-19/master/data/casos-br-total.csv")

#m_diarias = np.array(covid["Mortes"]) - covid["Mortes"].shift()
#covid["mortes_diarias"] = m_diarias

#tabela_br = pd.DataFrame(
#    np.array([[covid.iloc[-1].Data, covid.iloc[-1].Confirmados, int(covid.iloc[-1].Mortes), int(m_diarias.iloc[-1])]]),
#    columns=["Data", "Total Casos", "Total Mortes", "Ult. 24h"])

#seq = range(len(covid))
#sns.relplot(y="mortes_diarias", x=seq, data=covid, kind="line")
#plt.title("Mortes Diárias por Covid-19 no Brasil", loc="left")
#plt.xlabel("Dias")
#plt.ylabel("Mortes Diárias")
#plt.xticks(
#    rotation=90,
#    fontweight='light',
#    horizontalalignment='right'
#)
#st.pyplot()

#st.subheader('Dados - Brasil')
#st.write(tabela_br)

#st.subheader('Dados - Americana')
#st.write(tabela)
