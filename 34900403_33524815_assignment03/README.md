Names: Jason Lee (34900403) and Wee Jun Zen (33524815)
Date: 11 June 2026
Applied Session: Friday 2PM-4PM

# Project/Directory Structure
```text
34900403_33524815_assignment03/
├── deployment/
│   ├── config/
│   │   └── docker-compose.yml       # Standardized multi-container orchestration config
|   |   └── Dockerfile.jupyter
|   |   └── fix_kafka3.py
│   └── scripts/
│       ├── start_infra_scr1.sh      # Shell script to initiate infrastructure & Kafka topics
│       └── pipeline_launch_scr2.sh  # Shell script to initiate streaming pipeline headlessly
├── src/
│   ├── app.py                       # Main standalone Dash dashboard application
│   ├── 34900403_33524815_producer_a_b_c.ipynb         # Kafka traffic stream event producer
│   └── 34900403_33524815_data_design_streaming.ipynb  # PySpark Structured Streaming engine
└── README.md                        # Deployment manual and advanced engineering brief
```
# Added files
### Files from A2
- 34900403_33524815_data_design_streaming.ipynb 
- 34900403_33524815_producer_a_b_c.ipynb
### Files from A3
- docker-compose.yml
- Dockerfile.jupyter
- fix_kafka3.py
- start_infra_scr1.sh
- pipeline_launch_scr2.sh
- app.py

# Core Dependencies and Automated Setup
### System prerequisites
- Docker Desktop installed and running (Windows or MacOS)
- Apache Spark version v3.5.0 or higher
- Python 3.10 or higher with access to the pip package manager
### Local Python Environment Setup
Run the Bash command line anywhere in the terminal:
For Windows, the command line is: 
```bash
pip install numpy pymongo plotly dash pandas jupyter
```
For MacOS, the command line is:
```bash
pip3 install numpy pymongo plotly dash pandas jupyter
```
# End-to-End Operational Execution Guide
### Ensuring a Clean State for Ingestion Testing
If you wish to wipe out historical records from previous development runs and test the real-time pipeline from a completely empty database slate, execute the following command at the project root directory(folder where deployment folder is in, 34900403_33524815_assignment03) *before* starting Step 1:
```bash
docker compose -f deployment/config/docker-compose.yml down -v
```

### step 0: if you are running for the first time:
Run this following command in bash shell:
```bash
docker-compose -f deployment/config/docker-compose.yml build
```
According to Claude AI, this is to build the custom jupyter image. It may take some time, mine took almost 3 minutes(179.9s)

### Step 1: Provide the Infrastructure
Ensure docker desktop is running in background first.

Run the following Bash commands in the terminal to launch the containerized cluster engines and automatically initialise the required message broker topics:
```bash
cd ./deployment/scripts
chmod +x *.sh
./start_infra_scr1.sh
```
Note: The first of these commands is dependent on where your terminal is in the working directory; you may need to run more cd commands to ensure you reach the scripts directory

Troubleshooting tip:
if you get an error like this:
" -bash: ./start_infra_scr1.sh: /bin/bash^M: bad interpreter: No such file or directory"
Chage the CRLF at the bottom right of both .sh files to LF. That should resolve the issue due to how the files end lines.

### Step 2: Launch the Data Streaming Pipeline
Once the infrastructure outputs a successful handshake, trigger the cell-by-cell Jupyter pipeline wrapper by running:
```bash
./pipeline_launch_scr2.sh

debugging tip: if errors mentioning query or batches missing appears, delete the checkpoints folder
```
### Step 3: Launch the Dashboard
Keep the first terminal window running and open a new terminal window. Navigate to the source directory and ignite the Dash web platform:
The below line to navigate to the source directory depends on where your terminal is in the working directory
```bash
cd ../../src
```
For Windows, the command line to ignite Dash is:
```bash
python app.py
```
For MacOS, the command line to ignite Dash is:
```bash
python3 app.py
```
troubleshooting tip: if python app.py does not work in bash on windows, try python3 app.py
### Step 4: Access the live visualisation
Find any browser such as Google Chrome, Microsoft Edge, Safari or etc and type "http://127.0.0.1:8050/", which would present the live visualisation in real-time

# Advanced Engineering Brief
### Extension and Implementation
Based off the structural paradigms established in energy-scenario model architectures, such as the Open MASTER Energy Model by Martín (2025), the Dash visualization platform uses highly reactive, in-memory callbacks. Filtering parameters are captured and applied dynamically by updating the underlying Plotly graphical elements inside localized layout containers. This eliminates the massive layout rendering overhead and state loss associated with monolithic browser page-refreshes on every client interaction, preserving full state reproducibility without altering the structural backend execution pipeline.

The system conforms to the four-layer architectural design pattern (Data Ingestion, Data Processing, Visualization, and User Interaction) evaluated by Yaganti (2020). Utilizing a decoupled data pipeline between layers allows changes in the streaming ingestion (Kafka) and transformation (Spark) layers to pass smoothly into the user interface (Dash) via a standalone database buffer layer (MongoDB), isolating streaming ingestion cycles from front-end layout rendering latency.

### Innovation and Technical Complexity
Traditional streaming visualizations often rely on hardcoded thresholds and flat, static layouts that fail to reflect the shifting rules of multi-zone operational environments. Our implementation achieves a highly dynamic and context-aware system by leveraging structured dot-notation indexing to directly query nested document schemas within the MongoDB collection (violations_today.camera_id_end).

Instead of executing generic, uniform data fetches, the dashboard's visualization loop dynamically maps client dropdown selections onto physical traffic zones. The rendering engine isolates real-time speeding infractions and dynamically recalculates and draws the contextual horizontal speed limit boundaries (90km/h for Camera C and 110km/h for Camera B) directly onto the graph canvas via the add_hline routing pattern. This produces an interactive framework where layout rules alter themselves on-the-fly to match the live state of the query viewport.

### Performance Analysis

Yaganti (2020) demonstrated that processing datasets exceeding 100,000 records using an in-memory DataFrame architecture yields a highly efficient processing latency of approximately 1.8 seconds. However, scaling this layout within a continuous real-time streaming environment would expose a critical architecture bottleneck when coupled with an embedded document schema. Appending multi-source logs natively into nested arrays within a single master vehicle documents forces MongoDB's storage engine to repeatedly resize and reallocate split data fragments on disk, generating severe processing overhead as operational tracking logs grow over time.

To eliminate this long-term latency degradation, a production deployment should transition to an Inverted, Event-Driven Outbox Collection Schema instead of relying on monolithic nested documents. Isolating every individual speeding infraction as its own unique atomic document tagged with a indexed foreign key keeps write operations bounded at a highly efficient constant-time complexity, optimising horizontal scaling throughput to an enterprise standard.