# Stomble Assignment

## Technology Stack

* Python3 - Flask Restplus
* MongoDB 

## Installation (Linux)

Create a python virtual environment

```bash
python3 -m virtualenv venv 
```
Activate the virtual environment

```bash
source venv/bin/activate
```
Then run the command

```bash
make install
```

## Start the server

Before starting the API server, make sure mongoDB server is up and running on localhost, PORT 27017

```bash
make run
-- or --
cd stomble_assignment/src
python3 api.py 
```

## Tests

Before running the tests, make sure the API server is up and running. 

```bash
make tests
-- or -- 
pytest
```
