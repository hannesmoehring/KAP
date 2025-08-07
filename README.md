# Klinisches Anwendungsprojekt - Neurologiedaten

## How to run

### 1. Create a virtual environment

`python3 -m venv .venv`

### 2. Activate virtual environment

On Linux/MacOS:
`source .venv/bin/activate`

On Windows:
`.venv/bin/activate`

### 3. Install dependencies

`pip install -r requirements.txt`

### 4. Start program

### 4.1 Create a config

if no config is available, it is possible to create a config template for a specific csv using

`python3 util.py -p path/to/<file>.csv `

### 4.2 Run Checks

`python3 main.py /path/to/<file>.csv`

path to csv is an optional argument, if nothing is passed, a test dataframe is created.
