# -----Instructions to run this file-----
# 1. Ensure the Kafka Producer and PySpark Streaming jobs are already running
# 2. Open a terminal in VS Code and navigate to the 'src' directory
# 3. Run "pip install numpy pymongo plotly dash pandas"
# 4. Run "python3 app.py" or "python app.py", depending on your environment
# 5. To know that the command from Step 4 is working, the terminal should output:
"""
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8050
Press CTRL+C to quit
"""
# 6. Open your browser and navigate to: http://127.0.0.1:8050/

# Import the typing and typing_extension modules
import typing
import typing_extensions

# Force the typing fix before doing anything
typing_extensions.Generic = typing.Generic

# Import MongoClient from pymongo library
from pymongo import MongoClient

# Configure the Host IP to the local host
hostip = "localhost"
client = MongoClient(hostip, 27017)

# Obtain the database and the collection to use for live visualisation
db = client.a2_db
violations = db.violations_daily_summary

# Import the plotly express module
import plotly.express as px

# Import the dash module, as well as the dcc and html functions for the UI
import dash
from dash import dcc
from dash import html

# Import modules to build interactive callback functions
from dash.dependencies import Input, Output

# Initialize the Dash Application
app = dash.Dash(__name__)

# Define the HTML Web Layout
app.layout = html.Div([

    # Header
    html.H1("AWAS Real-Time Traffic Violation Dashboard",
            style={'textAlign': 'center', 'fontFamily': 'sans-serif',
                   'color': '#e84910', 'padding': '20px'}),
    
    # Container for Dropdowns
    html.Div([
        
        # Dropdown for severity profiles
        html.Div([
            html.Label("Select Visual Profile:", style={'fontWeight': 'bold', 'fontFamily': 'sans-serif'}),
            dcc.Dropdown(
                id='traffic-filter-dropdown',
                options=[
                    {'label': 'All Live Violations', 'value': 'ALL'},
                    {'label': 'High-Speed Offenders (>140 km/h)', 'value': 'SPEED_HIGH'},
                    {'label': 'Extreme Speed / Reckless (>160 km/h)', 'value': 'SPEED_EXTREME'},
                    {'label': 'Chronic Serial Offenders (10+ Infractions)', 'value': 'CHRONIC_OFFENDERS'}
                ],
                value='ALL',
                clearable=False
            )
        ], style={'width': '45%', 'display': 'inline-block', 'marginRight': '5%'}),
        
        # Dropdown for end camera checkpoint
        html.Div([
            html.Label("Select Camera Checkpoint:", style={'fontWeight': 'bold', 'fontFamily': 'sans-serif'}),
            dcc.Dropdown(
                id='end-camera-filter-dropdown',
                options=[
                    {'label': 'All End Camera Checkpoints', 'value': 'ALL'},
                    {'label': 'End Camera Checkpoint B (110 km/h Zone)', 'value': 'Camera B'},
                    {'label': 'End Camera Checkpoint C (90 km/h Zone)', 'value': 'Camera C'}
                ],
                value='ALL',
                clearable=False
            )
        ], style={'width': '45%', 'display': 'inline-block'})

    ], style={'width': '60%', 'margin': '0 auto', 'padding': '10px'}),
    
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
     Input('traffic-filter-dropdown', 'value'),
     Input('end-camera-filter-dropdown', 'value')]
)

# Update live graph based on the selected filter
def update_live_graph(n, selected_filter, selected_camera):
    # Depending on the selected filter, queries are set differently
    query = {} # No filter

    if selected_camera == 'Camera B':
        query['violations_today.camera_id_end'] = 2  # Camera B is ID 2
    elif selected_camera == 'Camera C':
        query['violations_today.camera_id_end'] = 3  # Camera C is ID 3

    if selected_filter == 'SPEED_HIGH':
        query['max_speed_recorded'] = {'$gt': 140} # Max speed > 140km/h
    elif selected_filter == 'SPEED_EXTREME':
        query['max_speed_recorded'] = {'$gt': 160} # Max speed > 160km/h   
    elif selected_filter == 'CHRONIC_OFFENDERS':
        query['total_violations_today'] = {'$gte': 10} # Total violations today >= 10
    
    # Fetch latest data stream from MongoDB summary collection
    # and take only the 10 highest max speeds recorded
    cursor = violations.find(query).sort("max_speed_recorded", -1).limit(10)
    data = list(cursor)

    # Debugging line
    print(f"DEBUG: Found {len(data)} documents in MongoDB")
    
    # If no data is ingested yet, display a message
    if not data:
        return px.bar(title="No Active Stream Records Found")
        
    # Extract the structural array data for rendering
    car_plates = [doc['car_plate'] for doc in data]
    max_speeds = [doc['max_speed_recorded'] for doc in data]
    total_counts = [doc['total_violations_today'] for doc in data]
    
    # Create interactive Plotly bar chart
    fig = px.bar(
        x=car_plates, 
        y=max_speeds,
        color=total_counts, 
        title="Top 10 Most Critical Speeding Violations Detected",
        labels={
            'x': 'Vehicle Registration Plate', 
            'y': 'Maximum Recorded Speed (km/h)',
            'color': 'Total Infractions'
        },
        color_continuous_scale=px.colors.sequential.OrRd
    )
    
    # Dynamically position operational speed limit
    if selected_camera == "Camera C":
        speed_limit = 90
        annotation = "Speed Limit (90km/h)"
    else:
        # Default to 110km/h for Camera B or if "All Cameras" is selected
        speed_limit = 110
        annotation = "Speed Limit (110km/h)"

    # Add a horizontal threshold line for speed limit visibility
    fig.add_hline(y=speed_limit, line_dash="dash", line_color="red", annotation_text=annotation)
    fig.update_layout(xaxis_tickangle=-45)
    
    return fig

# Launch the operational Dash framework server to be accessed externally
app.run(jupyter_mode='external', host='127.0.0.1', port=8050, debug=False)