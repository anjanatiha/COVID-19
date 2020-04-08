# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

####
import numpy as np
import pandas as pd

import os

from datetime import datetime
from pytz import timezone

import matplotlib.pyplot as plt
# import seaborn as sns
import plotly.express as px

#####


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

######

def print_time():
    fmt = "%a, %d %B %Y %H:%M:%S %Z%z"
    
    pacific = timezone('US/Pacific')
    
    loc_dt = datetime.now(pacific)
    
    time_str = loc_dt.strftime(fmt)
    
    print("Pacific Time" + " : " + time_str)
    
    return time_str
    


def format_date_columns(data_cols):
	data_cols_new_format = []
	data_cols_map = {}

	for d in data_cols:
	    new_d = datetime.strftime(datetime.strptime(d, '%m/%d/%y'),'%b %d')
	    data_cols_map[d] = new_d
	    data_cols_new_format.append(new_d)

	return data_cols_new_format, data_cols_map


url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'

input_dir = url

time_series_covid19_confirmed_global = pd.read_csv(input_dir + "time_series_covid19_confirmed_global.csv", error_bad_lines=False)
time_series_covid19_recovered_global = pd.read_csv(input_dir + "time_series_covid19_recovered_global.csv", error_bad_lines=False)
time_series_covid19_deaths_global    = pd.read_csv(input_dir + "time_series_covid19_deaths_global.csv", error_bad_lines=False)

# time_series_covid19_confirmed_US = pd.read_csv(input_dir + "time_series_covid19_confirmed_US.csv", error_bad_lines=False)
# # time_series_covid19_recovered_global = pd.read_csv(input_dir + "time_series_covid19_recovered_global.csv")
# time_series_covid19_deaths_US    = pd.read_csv(input_dir + "time_series_covid19_deaths_US.csv", error_bad_lines=False)

columns = time_series_covid19_confirmed_global.columns.tolist()
location_columns = ['Province/State', 'Country/Region', 'Lat', 'Long']
location_long_lat_columns = ['Lat', 'Long']
location_name_cols = ['Country/Region', 'Province/State']

data_cols = [c for c in columns if c not in location_columns]

count_days = len(data_cols)

############

data_cols_new_format, data_cols_map = format_date_columns(data_cols)
####
data_cols_new_format = data_cols

last_day = data_cols_new_format[-1]
prev_day = data_cols_new_format[-2]

new_cols = location_name_cols + [last_day]

###############

#################

total_confirmed_global = time_series_covid19_confirmed_global[last_day].sum()
total_death_global = time_series_covid19_deaths_global[last_day].sum()
total_recovered_global = time_series_covid19_recovered_global[last_day].sum()

# print("Total Confirmed Cases     : %s" % ("{:,}".format(total_confirmed_global)))
# print("Total Recovered Cases     : %s" % ("{:,}".format(total_recovered_global)))
# print("Total Deaths Cases        : %s" % ("{:,}".format(total_death_global)))


# data = [total_confirmed_global, total_recovered_global, total_death_global]

# fig = px.line(df, x="index", y=0, title="Total Global Count till + " + last_day)
# fig.show()

################

   
###########

app.layout = html.Div(children=[
    html.H1(children='Covid-19 Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': ["Total Confirmed", "Total Recovered", "Total Death"], 'y': [total_confirmed_global, total_recovered_global, total_death_global], 'type': 'bar', 'name': 'Total Count (Global)'},
                ],
            'layout': {
                'title': 'Total Count (Global)'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)