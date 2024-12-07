import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Carregar os dados
df_data = st.session_state["data"]

# Filtro por clube
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Selecione um clube", clubes)

# Filtrar os dados para o clube selecionado
df_filtered = df_data[df_data["Club"] == club]

# Definir faixas de idades
age_bins = [18, 25, 30, 35, 40, 45, np.inf]
age_labels = ['18-24', '25-29', '30-34', '35-39', '40-44', '45+']
df_filtered['Age Range'] = pd.cut(df_filtered['Age'], bins=age_bins, labels=age_labels)

# Definir faixas de salários semanais
salary_bins = [0, 5000, 10000, 15000, 20000, 30000, 50000, np.inf]
salary_labels = ['0-5k', '5k-10k', '10k-15k', '15k-20k', '20k-30k', '30k-50k', '50k+']
df_filtered['Salary Range'] = pd.cut(df_filtered['Wage(£)'], bins=salary_bins, labels=salary_labels)

# Calcular a média do salário semanal por faixa de idade e faixa salarial
salary_by_age_and_salary_range = df_filtered.groupby(['Age Range', 'Salary Range'])['Wage(£)'].mean().unstack()

# Configurar o gráfico
plt.figure(figsize=(12, 8))
sns.heatmap(salary_by_age_and_salary_range, cmap="YlGnBu", annot=False, fmt="d", cbar=True)

# Ajustes no gráfico
plt.title(f"Mapa de Calor: Faixa de Idade e Faixa de Salário - {club}", fontsize=16)
plt.xlabel('Faixa de Salário')
plt.ylabel('Faixa de Idade')

# Exibir o gráfico no Streamlit
st.pyplot(plt)