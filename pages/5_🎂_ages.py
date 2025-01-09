import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load data
df_data = st.session_state["data"]

# Filter per club
clubs = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Select one club", clubs)

# Filter data for selected club
df_filtered = df_data[df_data["Club"] == club]

# Defining age range
age_bins = [18, 25, 30, 35, 40, 45, np.inf]
age_labels = ['18-24', '25-29', '30-34', '35-39', '40-44', '45+']
df_filtered['Age Range'] = pd.cut(df_filtered['Age'], bins=age_bins, labels=age_labels)

# Defining salary range
salary_bins = [0, 5000, 10000, 15000, 20000, 30000, 50000, np.inf]
salary_labels = ['0-5k', '5k-10k', '10k-15k', '15k-20k', '20k-30k', '30k-50k', '50k+']
df_filtered['Salary Range'] = pd.cut(df_filtered['Wage(£)'], bins=salary_bins, labels=salary_labels)

# Calculate weekly salary average by age range and salary range
salary_by_age_and_salary_range = df_filtered.groupby(['Age Range', 'Salary Range'])['Wage(£)'].mean().unstack()

# Set up the chart
plt.figure(figsize=(12, 8))
sns.heatmap(salary_by_age_and_salary_range, cmap="YlGnBu", annot=False, fmt="d", cbar=True)

# Fit on the chart
plt.title(f"Heatmap: Age Range and Salary Range - {club}", fontsize=16)
plt.xlabel('Salary Range')
plt.ylabel('Age Range')

# Exhibit the chart on Streamlit
st.pyplot(plt)