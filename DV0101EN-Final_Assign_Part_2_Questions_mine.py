#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    #TASK 2.1 Add title to the dashboard
    html.H1("ABC Auto - Automobile Sales Statistics Dashboard With a meaningful Title"),#May include style for title
    html.Div([#TASK 2.2: Add two dropdown menus
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Select Statistics',
            placeholder='Select a report type',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
        )
    ]),
    html.Div(dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value='Select a Year'
        )),
    html.Div([  # TASK 2.3: Add a division for output display
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),
    ])
])
#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value'))
def update_input_container(selected_statistics):
    return selected_statistics != 'Yearly Statistics' and selected_statistics != 'Recession Period Statistics'


#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'), 
     Input(component_id='dropdown-statistics', component_property='value')]
)
def update_output_container(selected_year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[(data['Recession'] == 1) & (data['Year'] == selected_year)]

    #TASK 2.5: Create and display graphs for Recession Report Statistics
    # Plot 1: Automobile sales fluctuate over Recession Period (year wise)
        # Check if recession_data is empty
        if recession_data.empty:
            return html.Div("No data available for the selected year during recession periods.")

        # Creating the plot for R_chart1
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        
        # Check if yearly_rec is empty
        if yearly_rec.empty:
            return html.Div("No aggregate data available for the selected year.")

        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                           x='Year', 
                           y='Automobile_Sales',
                           title="Average Automobile Sales Fluctuation Over Recession Period"))


        # Plot 2: Calculate the average number of vehicles sold by vehicle type       
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
        figure=px.bar(average_sales, 
                      x='Vehicle_Type',
                      y='Automobile_Sales',
                      title="Average Number of Vehicles Sold by Vehicle Type During Recessions"))
     
        # Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        # use groupby to create relevant data for plotting
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec,
                        values='Advertising_Expenditure',
                        names='Vehicle_Type',
                        title="Total Advertising Expenditure Share by Vehicle Type During Recessions"))

        # Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        unemployment_data = recession_data.groupby(['Vehicle_Type', 'unemployment_rate'])['Automobile_Sales'].sum().reset_index()
        R_chart4 = dcc.Graph(
        figure=px.bar(unemployment_data, 
                    x='unemployment_rate',
                    y='Automobile_Sales',
                    color='Vehicle_Type',
                    title="Effect of Unemployment Rate on Vehicle Type and Sales"))
# Returning the plots
        return html.Div([
            html.Div(children=[R_chart1], className='grid-item'),
            html.Div(children=[R_chart2], className='grid-item'),
            html.Div(children=[R_chart3], className='grid-item'),
            html.Div(children=[R_chart4], className='grid-item')
        ], className='grid-container', style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'grid-gap': '20px'})


# TASK 2.6: Create and display graphs for Yearly Report Statistics
 # Yearly Statistic Report Plots                             
    elif (selected_year and selected_statistics == 'Yearly Statistics'):
        yearly_data = data[data['Year'] == selected_year]
        
        # Plot 1: Yearly Automobile sales using line chart for the whole period
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales', title="Yearly Automobile Sales"))
        
        # Plot 2: Total Monthly Automobile sales using line chart for the selected year
        monthly_sales = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(monthly_sales, x='Month', y='Automobile_Sales', title="Monthly Automobile Sales in {}".format(selected_year)))
        
        # Plot 3: Bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales', title='Average Vehicles Sold by Vehicle Type in the year {}'.format(selected_year)))
        
        # Plot 4: Total Advertisement Expenditure for each vehicle using pie chart
        ad_exp = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(ad_exp, values='Advertising_Expenditure', names='Vehicle_Type', title="Total Advertising Expenditure for Each Vehicle Type in {}".format(selected_year)))
   
        # Returning the plots
        return html.Div([
            html.Div(children=[Y_chart1], className='grid-item'),
            html.Div(children=[Y_chart2], className='grid-item'),
            html.Div(children=[Y_chart3], className='grid-item'),
            html.Div(children=[Y_chart4], className='grid-item')
        ], className='grid-container', style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'grid-gap': '20px'})

                                
            
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)