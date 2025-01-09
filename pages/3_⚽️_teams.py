import streamlit as st
import pandas as pd
import datetime


# Setting the limit for contracts close to maturity (6 months, for example)
limit_days = 180  # 180 days = 6 months

st.set_page_config(
    page_title="Players",
    page_icon="🏃🏼",
    layout="wide"
)

df_data = st.session_state["data"]

clubs = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Club", clubs)

df_filtered = df_data[(df_data["Club"] == club)].set_index("Name")

# Current year
current_year = datetime.datetime.now().year

# Converting date to int
df_filtered['Contract Valid Until'] = pd.to_numeric(df_filtered['Contract Valid Until'], errors='coerce')

# Filter players with contract finishing on current year
expiring_contracts = df_filtered[df_filtered['Contract Valid Until'] <= current_year]

st.image(df_filtered.iloc[0]["Club Logo"])
st.markdown(f"## {club}")

# Calculation
total_market_value = df_filtered['Value(£)'].sum()  # Market value 
highest_weekly_wage = df_filtered['Wage(£)'].max()  # Highest weekly salary
highest_release_clause = df_filtered['Release Clause(£)'].max()  # Highest release clause
average_age = df_filtered['Age'].mean() # Average team age

# Displaying KPIs using columns and `st.metric`
st.markdown(f"### KPIs by club: {club}")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Market Value", value=f"£{total_market_value:,.0f}")

with col2:
    st.metric(label="Highest Weekly Salary", value=f"£{highest_weekly_wage:,.0f}")

with col3:
    st.metric(label="Highest Release Clause", value=f"£{highest_release_clause:,.0f}")

with col4:
    st.metric(label="Average Age", value=f"{average_age:,.0f}")

# Display alert only for players which contracts are due or expiring by
if not expiring_contracts.empty:
    st.warning(f"⚠️Watch out! {len(expiring_contracts)} player(s) from {club} have contracts due or expiring by  {current_year}.")
else:
    st.success(f"None of the club's players {club} have contracts that have expired or will expire by {current_year}.")


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