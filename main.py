import streamlit as st
import warnings
warnings.filterwarnings("ignore")
import requests
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import pycountry
import base64
raw_df = pd.read_csv("population.csv")


st.sidebar.title("Silahkan pilih menu dibawah")
option = st.sidebar.selectbox(
        '',
    ('Home','WebScrapping','Visualisasi','GIS')
)
dict = {'year': raw_df['Year'], 'country':raw_df['Country'], 'population':raw_df['Population'], 'yearly%change':raw_df['Yearly%Change']}
sub_df = pd.DataFrame(dict)
if option == 'Home' or option == '':
    st.title('Mengulas tentang Perkembangan Populasi di dunia dari tahun 1955 sampai dengan 2020')
    st.header('Data Perkembangan populasi 1995-2020')
    raw_df = pd.read_csv("population.csv")
    st.write(raw_df)
        

    df = pd.read_csv("population.csv")

    def download_csv():
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # encode to base64
        return f'data:file/csv;base64,{b64}'

    if st.button("Download CSV"):
        csv_url = download_csv()
        st.markdown(f'<a href="{csv_url}" download="population.csv">Download CSV File</a>', unsafe_allow_html=True)

elif option == 'Visualisasi':
    wrld_pop=pd.read_csv('population.csv')
    st.title("Perubahan Populasi negara dari tahun 1955-2020")

    fig = px.line(wrld_pop, x="Year", y="YearlyChange", color='Country',
              labels={
                     "YearlyChange": "perubahan populasi",
                 })

    st.plotly_chart(fig)

    
    st.header("20 negara teratas dengan tingkat persentase perubahan terbanyak di tahun 2020")
    data = sub_df[sub_df['year'] == 2020].sort_values(by=['yearly%change'], ascending=False)[:20]
    fig, ax = plt.subplots(figsize=(12,5))
    sns.barplot(data=data, x="country", y="yearly%change", ax=ax)
    plt.setp(ax.get_xticklabels(), rotation=90)
    st.pyplot(fig)

    
    Median_filtered=wrld_pop[wrld_pop['MedianAge']!=0]
    Median_col=Median_filtered.loc[:,['Continent','Year','MedianAge']]
    Median_group=Median_col.groupby(['Year','Continent']).agg('mean').reset_index()

    st.title("Rata - rata umur per Negara")

    fig = px.bar(Median_group, x="Year", y= "MedianAge", facet_col="Continent",facet_col_wrap = 3,
         labels={
                 "MedianAge": "Age",
             },
        title="Rata - rata umur negara per tahun")

    st.plotly_chart(fig)

elif option == 'WebScrapping':
    
    url = "https://www.worldometers.info/world-population/population-by-country/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"id": "example2"})
    rows = table.tbody.find_all("tr")
    data = []

    for row in rows:
        cols = row.find_all("td")
        name = cols[1].text.strip()
        population = cols[2].text.strip()
        data.append((name, population))

    st.text("Web Scrapping Populasi dari web https://www.worldometers.info/world-population/population-by-country/")
    st.markdown(f'<a href="https://www.worldometers.info/world-population/population-by-country/">Lihat website</a>', unsafe_allow_html=True)
    st.write(data)
    st.title('Table Web Scrapping')
    st.table(data)

elif option == 'GIS':
    import pycountry

    def do_fuzzy_search(country):
        try:
            result = pycountry.countries.search_fuzzy(country)
            return result[0].alpha_3
        except:
            return np.nan

    wrld_pop=pd.read_csv('population.csv')
    wrld_pop["Country_code"] = wrld_pop["Country"].apply(lambda country: do_fuzzy_search(country))
    

    st.title("Tingkat Kesuburan Global")

    fig = px.choropleth(wrld_pop, locations='Country_code', color='FertilityRate', hover_name='Country', animation_frame='Year',
                 color_continuous_scale=px.colors.sequential.Reds, projection='natural earth',
                 title='Tingkat Kesuburan Global')

    st.plotly_chart(fig)

    fig = px.choropleth(wrld_pop, locations='Country_code', color='Migrants(net)', hover_name='Country', animation_frame='Year',
                 color_continuous_scale=px.colors.sequential.Greens, projection='natural earth',
                 title='Migrasi Global')

    st.plotly_chart(fig)

    








