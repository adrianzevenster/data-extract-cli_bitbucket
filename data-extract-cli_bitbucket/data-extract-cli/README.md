# DATA EXTRACT COMMAND LINE INTERFACE (CLI)

This repository is home to the command line interface responsisble for extracting data from the airvantage profiler db, to s3, specifically for machine learning purposes. 

## Requirements
[AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) 

# Setup

## Setting up and activating the .venv

### Windows:
`c:\>python -m venv .venv --copies`
### Ubuntu:
`python3 -m venv .venv --copies`

If you want to, you can set your bash context so that all Python commands run in the virtual environment, by running:  

`source .venv/bin/activate`

to deactivate a virtual environment, run:  
`deactivate` 

## Installing the Required Python Modules
Install pipenv package for easier package management. 

First activate your virtual environment, then:

### Windows:
`pip install pipenv`
### Ubuntu:
`pip install pipenv`

Now use pipenv to install the production modules, by running 

### Windows:
`pipenv install`
### Ubuntu:
`pipenv install`

or install the entire dev stack by typing 

### Windows:
`pipenv install --dev`
### Ubuntu:
`pipenv install --dev`


# Running and Testing
`.venv/bin/python src/main.py  extract --input-json-path ./src/extract-request.json`  
or  
`python src/main.py  extract --input-json-path ./src/extract-request.json`  

## Test Suite
`make test`


### Required Reading
https://jinja.palletsprojects.com/en/3.1.x/  
https://click.palletsprojects.com/en/8.1.x/  
https://pandas.pydata.org/  
https://dev.mysql.com/doc/connector-python/en/  

### Signed
Henk van Zyl (Symbyte)  
Alexander Glöss (Symbyte)
