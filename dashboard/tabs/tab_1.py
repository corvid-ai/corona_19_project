import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import dash_table
from dateutil.relativedelta import relativedelta
import dash_bootstrap_components as dbc
import uuid
import os
import flask
import plotly.express as px
import os.path, time 
import pandas as pd
import numpy as np
import pycountry as pc
import pycountry_convert as pc1


######################3
#Get Data from John Hopkins in Real Time
url = 'https://raw.githubusercontent.com/corvid-ai/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-15-2020.csv'
#
try: 
  df = pd.read_csv(url,  encoding ='latin',  index_col=0) 
  df.to_csv("C:/Users/ansaj/Desktop/AI Hobbies/Corona_virus_DS/dashboard/data/dataset.csv")

except:
  df = pd.read_csv("C:/Users/ansaj/Desktop/AI Hobbies/Corona_virus_DS/dashboard/data/dataset.csv", encoding ='latin')
  

###################################
#DATA PROCESSING
standard_names = {'US': 'United States', 'Iran': 'Iran, Islamic Republic of',
                  'Bolivia': 'Bolivia, Plurinational State of',
                  'Korea, South':  'Korea, Republic of',
                  'Russia': 'Russian Federation', 'Brunei': 'Brunei Darussalam',
                  'Moldova': 'Moldova, Republic of', 'Vietnam': 'Viet Nam',
                  'Taiwan':'Taiwan, Province of China'
                   }
continent_code_to_name = {'AS': 'ASIA',
                  'NA': 'NORTH AMERICA',
                  'OC':  'OCEANA',
                  'EU': 'EUROPE',
                  'AF':'AFRICA',
                  'SA': 'SOUTH AMERICA'
                   }
def get_data_from_repo(df):

  global africa_standardized_data
  df['Country/Region']=  df['Country/Region'].str.replace('*', '')
  name = []
  common_name = []
  official_name = []
  alpha_2 = []
  for i in list(pc.countries):
    name.append(i.name)
    alpha_2.append(i.alpha_3)
    if hasattr(i, "common_name"):
        common_name.append(i.common_name)
    else:
        common_name.append('No Common Name')
        
    if hasattr(i, "offical_name"):
        official_name.append(i.official_name)
    else:
        official_name.append('No Official Name')

    iso_alpha_dict = dict(zip(name, alpha_2))
    df['Country/Region'] = df['Country/Region'].replace(standard_names)
    df['iso_alpha'] = df['Country/Region'].replace(iso_alpha_dict)
    df['Validation'] = df['Country/Region'].apply(lambda x: 'Yes' if x in name else 'No')
    standardized_data= df[df['Validation']=='Yes']

    continent_code_to_name = {'AS': 'ASIA','NA': 'NORTH AMERICA', 'OC':  'OCEANA',
          'EU': 'EUROPE','AF':'AFRICA','SA': 'SOUTH AMERICA'
                   }
  codes = []
  for (i, row) in standardized_data.iterrows():
    country_code = pc1.country_name_to_country_alpha2(row['Country/Region'], cn_name_format="default")
    continent_name = pc1.country_alpha2_to_continent_code(country_code)
    codes.append(continent_name)  
  standardized_data['continent_codes']= codes
  standardized_data['continent_codes'] = standardized_data['continent_codes'].replace(continent_code_to_name)
  africa_standardized_data= standardized_data[standardized_data['continent_codes']=='AFRICA']
  africa_standardized_data.groupby(['Country/Region','Latitude','Longitude', 'Recovered','Deaths',  'iso_alpha'])['Confirmed'].value_counts().reset_index(name="")
  return africa_standardized_data

get_data_from_repo(df)
###############333


#MAP FIGURE
map_fig = px.scatter_geo(africa_standardized_data, locations="iso_alpha",  #color="continent",
                     hover_name='Country/Region',
                     hover_data= ['Confirmed', 'Recovered', 'Deaths'],
                     color = 'Country/Region',
                     size='Confirmed',
                     projection="mercator"
                     )

map_fig.update_geos( 
                     resolution=110,
                     showocean=True, oceancolor="slategray",
                     #showlakes=True, lakecolor="Blue",
                     #showrivers=True, rivercolor="Blue"
                     showcountries=True, countrycolor="grey",
                     showframe = True,
    
   
)
map_fig.update_layout(
           title = 'Corona Virus cases reported in Africa So Far<br> Source: <a href="https://data.hdx.rwlabs.org/dataset/rowca-ebola-cases">\HDX</a>',
           geo_scope="africa",
           height= 600, width= 900, showlegend = True
          )

################################################33333
#BAR FIG
bar_fig = px.bar(africa_standardized_data, x='Country/Region', y='Confirmed',  
            # barmode='group',
              color = 'Country/Region',
            # facet_col= 'Fiscal Year',
             height=600,

             title = 'Cases Reported')

###################333333333333333333333333
### Layout of the Tab
##########################################
tab_1_layout = html.Div([


    html.Div(
        [

           html.Div(
           	    [

                    dcc.Graph(id="geo_graph_1",
                              figure=map_fig,
                              style={'margin-top': '-10'})

                 ], className = "six columns"
            ),

           html.Div(
                [


                dcc.Graph(id="bar_graph_1",
                              figure=bar_fig,
                              style={'margin-top': '-10'})


                 ], className = "five columns"
            ),
 
         ], className="row"
),
html.Div(id='page-1-content')

])