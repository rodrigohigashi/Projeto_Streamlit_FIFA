import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Loading data
df_data = st.session_state["data"]

# Filter per club
clubs = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Select one club", clubs)

# Filtering data for selected club
df_filtered = df_data[df_data["Club"] == club]

# Defining weekly salary range
salary_bins = [0, 5000, 10000, 15000, 20000, 30000, 50000, np.inf]
salary_labels = ['0-5k', '5k-10k', '10k-15k', '15k-20k', '20k-30k', '30k-50k', '50k+']
df_filtered['Salary Range'] = pd.cut(df_filtered['Wage(£)'], bins=salary_bins, labels=salary_labels)

# Calculating average weekly salary by nationality and salary
salary_by_nationality_and_range = df_filtered.groupby(['Nationality', 'Salary Range'])['Wage(£)'].mean().unstack()

# Set up the chart
plt.figure(figsize=(12, 8))
sns.heatmap(salary_by_nationality_and_range, cmap="YlGnBu", annot=False, fmt="d", cbar=True)

# Fit on chart
plt.title(f"Heatmap: Nationality and Salary Range - {club}", fontsize=16)
plt.xlabel('Weekly Salary Range (£)')
plt.ylabel('Nationality')

# Exhibit the chart on Streamlit
st.pyplot(plt)