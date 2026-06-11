Names: Jason Lee (34900403) and Wee Jun Zen (33524815)
Date: 11 June 2026
Applied Session: Friday 2PM-4PM

# Project/Directory Structure
```text
34900403_33524815_assignment03/
├── deployment/
│   ├── config/
│   │   └── docker-compose.yml       # Standardized multi-container orchestration config
│   └── scripts/
│       ├── start_infra_scr1.sh      # Shell script to initiate infrastructure & Kafka topics
│       └── pipeline_launch_scr2.sh  # Shell script to initiate streaming pipeline headlessly
├── src/
│   ├── app.py                       # Main standalone Dash dashboard application
│   ├── 34900403_33524815_producer_a_b_c.ipynb         # Kafka traffic stream event producer
│   └── 34900403_33524815_data_design_streaming.ipynb  # PySpark Structured Streaming engine
└── README.md                        # Deployment manual and advanced engineering brief

# Core Dependencies and Automated Setup
## System prerequisites
- Docker Desktop installed and running (Windows or MacOS)
- Apache Spark version v3.5.0 or higher
- Python 3.10 or higher with access to the pip package manager
## Local Python Environment Setup
Run the Bash command line anywhere in the terminal:
For Windows, the command line is: 
```text
pip install numpy pymongo plotly dash pandas jupyter nbconvert

For MacOS, the command line is:
```text
pip3 install numpy pymongo plotly dash pandas jupyter nbconvert

# End-to-End Operational Execution Guide
## Step 1: Provide the Infrastructure
Run the following Bash commands in the terminal to launch the containerized cluster engines and automatically initialise the require message broker topics:
```text
cd deployment/scripts
chmod +x *.sh
./start_infra_scr1.sh

Note: The first of these commands is dependent on where your terminal is in the working directory; you may need to run more cd commands to ensure you reach the scripts directory
## Step 2: Launch the Data Streaming Pipeline
Once the infrastructure outputs a successful handshake, trigger the cell-by-cell Jupyter pipeline wrapper by running:
```text
./pipeline_launch_scr2.sh

## Step 3: Launch the Dashboard
Keep the first terminal window running and open a new terminal window. Navigate to the source directory and ignite the Dash web platform:
The below line to navigate to the source directory depends on where your terminal is in the working directory
```text
cd ../../src

For Windows, the command line to ignite Dash is:
```text
python app.py

For MacOS, the command line to ignite Dash is:
```text
python3 app.py

## Step 4: Access the live visualisation
Find any browser such as Google Chrome, Microsoft Edge, Safari or etc and type "http://127.0.0.1:8050/", which would present the live visualisation in real-time
[[TBW]]
