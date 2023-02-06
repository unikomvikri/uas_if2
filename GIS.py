import pycountry
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

raw_df = pd.read_csv("population.csv")




df = px.data.gapminder()
fig = px.scatter_geo(raw_df, locations="Country_code", color="Continent",
                     hover_name="Country", size="Population",
                     animation_frame="Year",
                     projection="natural earth",
                     title="Global Population")
fig.show()