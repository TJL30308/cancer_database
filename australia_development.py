#!/usr/bin/env python
# coding: utf-8

# ### Import data for Australia

# In[ ]:


import pandas as pd
import math

print('reading data')
print('------------')

incidence_data = pd.read_excel('../raw_data/australia/aihw-can-122-cancer_incidence.xlsx')
population_data = pd.read_csv('../population_data/USCB_Australia.csv', header=1, sep=r'\s*,\s*', engine='python')


# In[ ]:


incidence_data.head()


# In[ ]:


population_data.head()


# ### Filtering Data - Removing Projected Values

# In[ ]:


actual_incidence = incidence_data[incidence_data['Data type'] == 'Actual'].reset_index(drop = True)
actual_incidence


# ### Data Check - What's available?

# In[ ]:


icd_10_codes = incidence_data['ICD10 codes'].unique()
icd_10_codes


# In[ ]:


population_data['Year'].unique()


# In[ ]:


population_data['Age'].unique()


# In[ ]:


actual_incidence['Age group (years)'].unique()


# In[ ]:


actual_incidence['Year'].unique()


# ### Filtering Data - By ICD Code

# In[ ]:


code = 'C71' #malignant neoplasm of brain
#code = 'C53' #cervical cancer
code_df = actual_incidence[actual_incidence['ICD10 codes'] == code]
code_df


# ### Filtering Data - Incidence by Gender, Age

# In[ ]:


gender = 'Males'
#gender = 'Females'
population_gender = 'Male'
#population_gender = 'Female'
age_group = 'All ages' #can plug in any available age-grouping
population_ages = 'Total' #can plug in any available age-grouping

gender_incidence = code_df[code_df['Sex'] == gender]
gender_age_incidence_df = gender_incidence[gender_incidence['Age group (years)'] == age_group] #can select other age groups
gender_age_incidence_df.head() 


# ### Calculating Historical Cases - Incident Cases in Men, All Ages, Select Years

# In[ ]:


select_years_rates = gender_age_incidence_df.iloc[27:].reset_index(drop = True)
rates = select_years_rates['Age-specific rate\n(per 100,000)']
gender_population_select_years = population_data.loc[population_data['Age'] == population_ages].iloc[0:8][f'{population_gender} Population'].reset_index(drop = True)
cases = [math.floor(rates[i] / 100000 * gender_population_select_years[i]) for i in range(len(gender_population_select_years))]

i = 0 

while i < 8:
    for case in cases: 
        print(f'{case} diagnosed incident cases of {code} in {gender}, {age_group} years, ' + str(int(select_years_rates['Year'][i])))
        i += 1


# ### Python Plotly and ScipyStats for Plotting and Analysis

# In[ ]:


import numpy as np
import scipy.stats as stats
import plotly as py
import plotly.graph_objs as go
import plotly.express as px


# In[ ]:


rates = np.array(gender_age_incidence_df['Age-specific rate\n(per 100,000)']).astype(float) #all years available, can adjust for specific years
years = np.array(gender_age_incidence_df['Year']).astype(float) #all years available, can adjust for specific years


# In[ ]:


slope, intercept, r_value, p_value, std_err = stats.linregress(years,rates)
print('Linear Trend Analysis: Historical Rates')
print(f'slope: {slope}')
print(f'intercept: {intercept}')
print(f'r_value: {r_value}')
print('r-squared:', r_value**2)
print(f'p_value: {p_value}')
print(f'std_err: {std_err}')
print('-------------------')


# In[ ]:


fig = px.line(x=years, y=rates, title=f'Australia, {code} Incidence, {gender}, {age_group}')

fig.update_layout(yaxis=dict(range=[0,max(rates)]))

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Incidence (Cases per 100,000)",
    plot_bgcolor='rgba(0,0,0,0)',
    autosize=False,
        width=800,
        height=600,)


fig.show()


# In[ ]:


forecast_years = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029]
forecast_rates = []

for year in forecast_years:
    forecast_rate = slope * year + intercept
    forecast_rates.append(forecast_rate)
    print(f'{year} forecast rate for {code}: {forecast_rate}')


# In[ ]:


all_rates = np.concatenate((rates, forecast_rates), axis=None)
all_years = np.concatenate((years, forecast_years), axis=None)


# In[ ]:


fig = px.line(x=all_years, y=all_rates, title=f'Australia, {code} Incidence, {gender}, {age_group}')

fig.update_layout(yaxis=dict(range=[0,max(all_rates)]))

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Incidence (Cases per 100,000)",
    plot_bgcolor='rgba(0,0,0,0)',
    autosize=False,
        width=800,
        height=600,)


fig.show()


# In[ ]:


forecast_population = population_data.loc[population_data['Age'] == population_ages].iloc[8:][f'{population_gender} Population'].reset_index(drop = True)


# In[ ]:


forecast_cases = [math.floor(forecast_rates[i] / 100000 * forecast_population[i]) for i in range(len(forecast_population))]
forecast_cases


# In[ ]:


all_cases = cases + forecast_cases


# In[ ]:


fig = px.line(x=all_years[27:], y=all_cases, title=f'Australia, {code} Incident Cases, {gender}, {age_group}')

fig.update_layout(yaxis=dict(range=[0,max(all_cases)]))

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Incident Cases (N)",
    plot_bgcolor='rgba(0,0,0,0)',
    autosize=False,
        width=800,
        height=600,)


fig.show()


# In[ ]:





# In[ ]:




