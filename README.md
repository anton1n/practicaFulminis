# Fulminis Practice 

## Introduction

This project aims to create a modbus tcp controler for ATV630.

## Commands

* `python -m venv .venv` - Create a python virtual environment.
* `pip install -r requirements.txt` - Install requirements.
* `python3 ATV630Controller.py` - Run program.

## Documentation

* `mkdocs serve` - Start MkDocs built-in dev-server to preview documentation.
*  Open up http://127.0.0.1:8000/ in your browser

## Project layout
    
        ├── ATV630Controller.py # Console app 
        ├── docs 
        │   ├── ATV600_Communication_parameters_EAV64332_V3.7.xlsx
        │   ├── index.md # The documentation homepage.
        │   ├── journal.md # Progress tracker
        │   ├── modbustcp.md
        │   ├── parameters.md
        │   └── registers.md
        ├── mkdocs.yml # The documentation configuration file.
        ├── README.md
        ├── requirements.txt
        └── webapp
            ├── controller
            │   └── atv_controller.py
            ├── handler
            │   └── handlers.py
            ├── main.py
            ├── model
            │   └── atv_model.py
            ├── routes
            │   └── main.py
            ├── server.py
            └── templates
                ├── index.html
                └── style.css

## Must Have
    - [x] Working modbus communication
    - [x] Basic webapp with:
            - [x] Connect/Disconect
            - [x] Start/Stop Motor
            - [x] Set Frequency
            - [x] Read Frequency, Current
            
## Nice to have
    - [] Read Motor Power

