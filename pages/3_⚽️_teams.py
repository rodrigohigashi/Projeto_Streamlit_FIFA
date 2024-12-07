import streamlit as st
import pandas as pd
import datetime


# Definindo o limite para contratos próximos ao vencimento (6 meses, por exemplo)
limite_dias = 180  # 180 dias = 6 meses

st.set_page_config(
    page_title="Players",
    page_icon="🏃🏼",
    layout="wide"
)

df_data = st.session_state["data"]

clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

df_filtered = df_data[(df_data["Club"] == club)].set_index("Name")

# Ano atual
current_year = datetime.datetime.now().year

# Convertendo a data de validade para números inteiros
df_filtered['Contract Valid Until'] = pd.to_numeric(df_filtered['Contract Valid Until'], errors='coerce')

# Filtrar jogadores com contrato vencendo no ano atual
expiring_contracts = df_filtered[df_filtered['Contract Valid Until'] <= current_year]

st.image(df_filtered.iloc[0]["Club Logo"])
st.markdown(f"## {club}")

# Cálculos
total_market_value = df_filtered['Value(£)'].sum()  # Soma do valor de mercado
highest_weekly_wage = df_filtered['Wage(£)'].max()  # Maior salário semanal
highest_release_clause = df_filtered['Release Clause(£)'].max()  # Maior cláusula de rescisão
average_age = df_filtered['Age'].mean() # Média de idade do time

# Exibição de KPIs usando colunas e `st.metric`
st.markdown(f"### KPIs para o clube: {club}")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Valor Total de Mercado", value=f"£{total_market_value:,.0f}")

with col2:
    st.metric(label="Maior Salário Semanal", value=f"£{highest_weekly_wage:,.0f}")

with col3:
    st.metric(label="Maior Cláusula de Rescisão", value=f"£{highest_release_clause:,.0f}")

with col4:
    st.metric(label="Idade Média do Time", value=f"{average_age:,.0f}")

# Exibir alerta apenas para jogadores com contratos vencidos ou vencendo
if not expiring_contracts.empty:
    st.warning(f"⚠️Atenção! {len(expiring_contracts)} jogador(es) do clube {club} têm contratos vencidos ou vencendo até {current_year}.")
else:
    st.success(f"Nenhum jogador do clube {club} tem contratos vencidos ou vencendo até {current_year}.")


columns = ["Age", "Photo", "Flag", "Overall", 'Value(£)', 'Wage(£)', 'Joined', 
           'Height(cm.)', 'Weight(lbs.)',
           'Contract Valid Until', 'Release Clause(£)']

st.dataframe(df_filtered[columns],
             column_config={
                 "Overall": st.column_config.ProgressColumn(
                     "Overall", format="%d", min_value=0, max_value=100
                 ),
                 "Wage(£)": st.column_config.ProgressColumn("Weekly Wage", format="£%f", 
                                                    min_value=0, max_value=df_filtered["Wage(£)"].max()),
                "Photo": st.column_config.ImageColumn(),
                "Flag": st.column_config.ImageColumn("Country"),
             })