# Import required libraries
import numpy as np
import pandas as pd
import dash
import dash_html_components as html
from dash import dcc
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                 dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                        {'label': 'All Sites', 'value': 'ALL'},
                                                        {'label': 'CCAFS LC-40', 'value': 'site1'},
                                                        {'label': 'CCAFS SLC-40', 'value': 'site2'},
                                                        {'label': 'KSC LC-39A', 'value': 'site3'},
                                                        {'label': 'VAFB SLC-4E', 'value': 'site4'}
                                                        ],
                                                         value='ALL',
                                                         placeholder="Select a Launch Site here",
                                                         searchable=True
                                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       2500: '2500',
                                                       5000: '5000',
                                                       7500: '7500',
                                                       10000: '10000'},
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    
    if entered_site == 'ALL':
        fig1 = px.pie(spacex_df, values='class', names='Launch Site',  
        title='Total Successful Launches by Site')
        return fig1
    elif entered_site == 'site1':
        site1 = spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']
        s1f = site1['class'].value_counts().to_frame()
        fig2 = px.pie(s1f, values=s1f['class'], names=s1f.index,  
        title='Total Successful Launches for site CCAFS LC-40')
        return fig2
    elif entered_site == 'site2':
        site2 = spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
        s2f = site2['class'].value_counts().to_frame()
        fig3 = px.pie(s2f, values=s2f['class'], names=s2f.index, 
        title='Total Successful Launches for site CCAFS SLC-40')
        return fig3
    elif entered_site == 'site3':
        site3 = spacex_df[spacex_df['Launch Site']=='KSC LC-39A']
        s3f = site3['class'].value_counts().to_frame()
        fig4 = px.pie(s3f, values=s3f['class'], names=s3f.index,
        title='Total Successful Launches for site KSC LC-39A')
        return fig4
    elif entered_site == 'site4':
        site4 = spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']
        s4f = site4['class'].value_counts().to_frame()
        fig5 = px.pie(s4f, values=s4f['class'], names=s4f.index, 
        title='Total Successful Launches for site VAFB SLC-4E')
        return fig5
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'), 
                Input(component_id="payload-slider", component_property="value")])
def get_scatter(entered_site,mass_range):
    sp = spacex_df
    if entered_site == 'ALL':
        sp = sp[np.logical_and(sp['Payload Mass (kg)']>=mass_range[0],sp['Payload Mass (kg)']<=mass_range[1])]
        fig1 = px.scatter(sp, x = 'Payload Mass (kg)' , y = 'class', color='Booster Version Category',
        opacity = 0.5,range_x=([0,10000]),range_y=([-0.05,1.05]), 
        title='Correlation between Payload and Success for All Sites')
        return fig1
    elif entered_site == 'site1':
        site1 = sp[sp['Launch Site']=='CCAFS LC-40']
        s1f = site1[np.logical_and(site1['Payload Mass (kg)']>=mass_range[0],site1['Payload Mass (kg)']<=mass_range[1])]
        fig2 = px.scatter(s1f, x = 'Payload Mass (kg)' , y = 'class', color='Booster Version Category',
        opacity = 0.5,range_x=([0,10000]),range_y=([-0.05,1.05]),  
        title='Correlation between Payload and Success for site CCAFS LC-40')
        return fig2
    elif entered_site == 'site2':
        site2 = sp[sp['Launch Site']=='CCAFS SLC-40']
        s2f = site2[np.logical_and(site2['Payload Mass (kg)']>=mass_range[0],site2['Payload Mass (kg)']<=mass_range[1])]
        fig3 = px.scatter(s2f,x ='Payload Mass (kg)',y = 'class',color='Booster Version Category',
        opacity = 0.5,range_x=([0,10000]),range_y=([-0.05,1.05]), 
        title='Correlation between Payload and Success for site CCAFS SLC-40')
        return fig3
    elif entered_site == 'site3':
        site3 = sp[sp['Launch Site']=='KSC LC-39A']
        s3f = site3[np.logical_and(site3['Payload Mass (kg)']>=mass_range[0],site3['Payload Mass (kg)']<=mass_range[1])]
        fig4 = px.scatter(s3f,x ='Payload Mass (kg)',y = 'class',color='Booster Version Category',
        opacity = 0.5,range_x=([0,10000]),range_y=([-0.05,1.05]),
        title='Correlation between Payload and Success for site KSC LC-39A')
        return fig4
    elif entered_site == 'site4':
        site4 = sp[sp['Launch Site']=='VAFB SLC-4E']
        s4f = site4[np.logical_and(site4['Payload Mass (kg)']>=mass_range[0],site4['Payload Mass (kg)']<=mass_range[1])]
        fig5 = px.scatter(s4f,x='Payload Mass (kg)',y ='class',color='Booster Version Category',
        opacity = 0.5,range_x=([0,10000]),range_y=([-0.05,1.05]),
        title='Correlation between Payload and Success for site VAFB SLC-4E')
        return fig5
        
        
        
        

# Run the app
if __name__ == '__main__':
    app.run_server()
