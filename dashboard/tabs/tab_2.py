import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import datetime
from plotly import graph_objs as go
import plotly.io as pio
import plotly.express as px

#path = "C://Users/ansaj/Desktop/AI Hobbies/Dashboards/violations_toolkit/data/"


#######################################
# Data Transform
##############################


tab_2_layout = html.Div([
  
    html.Div(id='page-2-content')
])