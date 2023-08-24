# -*- coding: utf-8 -*-
"""
You are a data scientist and would like to know where the top 5 places in the 
world (country or city) where your salary will go the farthest with respect to 
each individual index within the cost_of_living.csv file. Provide a simple 
statistical analysis in a Jupyter Notebook file and provide visualizations 
to support your analysis (I am looking for data wrangling more than anything). 
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

cost_of_living_data = pd.read_csv("cost_of_living.csv")
ds_salaries = pd.read_csv("ds_salaries.csv")
levels_fyi_salaray_data = pd.read_csv("Levels_Fyi_Salary_Data.csv")
country_codes_data = pd.read_excel("country_codes.xlsx")
