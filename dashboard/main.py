#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##########################################
# Import s
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import sys
import tabs
from tabs import  tab_1 , tab_2 
import uuid
import os
import flask
import os.path, time 
import datetime
from datetime import datetime as tmx
import base64
import os
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


#############################################33
#System Configurations


server = Flask(__name__)
app = dash.Dash(server=server)




###################################
date_format = "%Y-%m-%d"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
sys.path.insert(0, "/Users/ansaj/Desktop/AI Hobbies/Corona_virus_DS/dashboard/tabs")
app = dash.Dash(external_stylesheets=external_stylesheets)


pathx =   "C:/Users/ansaj/Desktop/AI Hobbies/Corona_virus_DS/dashboard/data/"






###################################################
# Date Time Update : This function updates the Dates on the Dashboard
def update_date_status():

    today =  str(datetime.date.today()) 
    file_date = time.strftime(date_format, time.localtime(os.path.getmtime(pathx + 'dataset.csv')))
    start_date = tmx.strptime(today, date_format)
    end_date = tmx.strptime(file_date, date_format)

    days = abs((end_date-start_date).days)
    #print(days)

    if days < 5:

        return html.Div("Last Data Update: " +  str(time.ctime(os.path.getmtime(pathx + 'dataset.csv')))+ " (" + str(days) + " days ago)",
                                             style = {'textAlign': 'left', 'color': 'red', 'fontSize': 20})
                                            

    else:

        return html.Div("Last Data Update: " +  str(time.ctime(os.path.getmtime(pathx + 'dataset.csv'))) + " (" + str(days) + " days ago)",
                                             style = {'textAlign': 'center'})

    return days





###############################################
# APP LAYOUT  

#################################################
app.layout = html.Div([


    # let try to see if we can add a corvid Logo on the page
     
    html.H2('Corvid Research Labs: Real Time Corona Virus Dashboard', style = {'textAlign': 'left'}),

    html.Div(update_date_status(),style = {'font_size': 20, 'fontColor': 'blue'}),
    
    
    dcc.Tabs(id="tabs-example", value='tab-1-example',style = {'fontSize':25},
        children=[
      
        dcc.Tab(label='GEO MAP: OUTBREAKS IN  AFRICA', value='tab-1-example'),
        dcc.Tab(label='TRENDING NEWS', value='tab-2-example'), # Forget about this tab. Its just a plae holder
       
    ]),
    html.Div(id='tabs-content-example')
])

app.config['suppress_callback_exceptions'] = True
@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])

def render_content(tab):

    if tab == 'tab-2-example':
        return tab_2.tab_2_layout
    

    if tab == 'tab-1-example':
        return tab_1.tab_1_layout




if __name__ == '__main__':
    app.run_server(debug=False)