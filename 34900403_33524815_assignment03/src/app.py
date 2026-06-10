#instructions for using app.py with help from Claude
#install relevant dependencies using terminal in VSCode -> pip install numpy pymongo plotly dash
#run "python app.py" using terminal in VSCode (make sure your are in src directory first)
#the following output should appear:
"""
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8050
Press CTRL+C to quit
"""
#click on the http://127.0.0.1:8050/, it will take you to the website.
#profit.

# Before running any of the code below, run this on the terminal:
# pip3 install pandas

# Additionally only run this after running the spark streaming ipynb file
# and the kafka producers file, the go to the terminal, set the working
# directory to the src folder and type in "python3 app.py" or "python app.py",
# depending on which device you're using.

# 1. Force the typing fix before doing anything
import typing
import typing_extensions
typing_extensions.Generic = typing.Generic

# 2. Base network and connection setup
from pymongo import MongoClient

# Configure Host IP
hostip = "localhost"
client = MongoClient(hostip, 27017)
db = client.a2_db
violations = db.violations_daily_summary

# 3. Now try the imports—Dash will no longer crash on typing_extensions
import plotly.express as px

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Initialize the Dash App inside the Jupyter Notebook
app = dash.Dash(__name__)

# Define the HTML Web Layout
app.layout = html.Div([
    html.H1("AWAS Real-Time Traffic Violation Dashboard",
            style={'textAlign': 'center', 'fontFamily': 'sans-serif',
                   'color': '#e84910', 'padding': '20px'}),
    
    # Dropdown for interactivity (e.g., Filtering by something specific if needed)
    html.Div([
        html.Label("Select Visual Profile:"),
        dcc.Dropdown(
            id='traffic-filter-dropdown',
            options=[
                {'label': 'All Live Violations', 'value': 'SPEED'},
                {'label': 'High-Speed Offenders (>140 km/h)', 'value': 'SPEED_HIGH'},
                {'label': 'Extreme Speed / Reckless (>160 km/h)', 'value': 'SPEED_EXTREME'},
                {'label': 'Chronic Serial Offenders (10+ Infractions)', 'value': 'CHRONIC_OFFENDERS'}
            ],
            value='SPEED',
            clearable=False
        )
    ], style={'width': '30%', 'padding': '10px'}),
    
    # The Plotly Chart Component
    dcc.Graph(id='live-traffic-graph'),
    
    # Background timer triggers every 2000 milliseconds to check MongoDB
    dcc.Interval(
        id='interval-component',
        interval=2*1000, 
        n_intervals=0
    )
], style={'backgroundColor': '#f4e0b7', 'padding': '10px'})

# Connects the Timer to the Plotly Graph Rendering Loop
@app.callback(
    Output('live-traffic-graph', 'figure'),
    [Input('interval-component', 'n_intervals'),
     Input('traffic-filter-dropdown', 'value')]
)
def update_live_graph(n, selected_filter):
    query = {}
    if selected_filter == 'SPEED_HIGH':
        query['max_speed_recorded'] = {'$gt': 140}
        
    elif selected_filter == 'SPEED_EXTREME':
        query['max_speed_recorded'] = {'$gt': 160}
        
    elif selected_filter == 'CHRONIC_OFFENDERS':
        query['total_violations_today'] = {'$gte': 10}
    
    # Fetch latest data stream from MongoDB summary collection
    cursor = violations.find(query).sort("max_speed_recorded", -1).limit(10)
    data = list(cursor)
    print(f"!!! DEBUG: Found {len(data)} documents in MongoDB !!!")
    
    if not data:
        return px.bar(title="Waiting for Spark Streaming Data Ingestion...")
        
    # Extract schema fields
    car_plates = [doc['car_plate'] for doc in data]
    max_speeds = [doc['max_speed_recorded'] for doc in data]
    total_counts = [doc['total_violations_today'] for doc in data]
    
    # Create interactive Plotly figure
    fig = px.bar(
        x=car_plates, 
        y=max_speeds,
        color=total_counts, # Color bars by how many times they've offended today
        title="Top 10 Most Critical Speeding Violations Detected",
        labels={
            'x': 'Vehicle Registration Plate', 
            'y': 'Maximum Recorded Speed (km/h)',
            'color': 'Total Infractions'
        },
        color_continuous_scale=px.colors.sequential.OrRd
    )
    
    # Add a horizontal threshold line for speed limit visibility
    fig.add_hline(y=110, line_dash="dash", line_color="red", annotation_text="Speed Limit (110km/h)")
    fig.update_layout(xaxis_tickangle=-45)
    
    return fig

# Launch the operational Dash framework server to be accessed externally

app.run(jupyter_mode='external', host='127.0.0.1', port=8050, debug=False)