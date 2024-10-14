# Tempo App

## Description

**A simple API built with FastAPI that efficiently retrieves user data from a MongoDB database**

## Features

- **User Management**: Register User and Login to system.
- **Manage Friends**: Can send friend requests and retrieve friends.
- **Caching Mechanism**: Redis is used to respond rapidly for repeated requests.
- **Tests Cases**: Test cases are written to ensure reliability(100% coverage).


### Technologies Used

| Python | FastAPI | MongoDB | Redis |
|--------|---------|---------|-------|
| <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" width="50"> | <img src="https://cdn.worldvectorlogo.com/logos/fastapi.svg" width="50"> | <img src="https://www.svgrepo.com/show/331488/mongodb.svg" width="50"> | <img src="https://www.svgrepo.com/show/303460/redis-logo.svg" width="50"> |



## Setup Locally
- **Pre-Requisite**  
  - Make sure you have python-3.12 on your system  
  - Make sure you have [MongoDB](https://www.mongodb.com/) installed on your system and initial development and test databases
  - Make sure you have [redis](https://redis.io/) installed on your system 

- **Install Dependencies**  
  First make sure virtual environment is activated i.e `conda activate tempoenv`  
  `pip install -r requirements.txt`

- **Setup env**  
  Create .env file according to .env.example  

- **Run Tests**  
  To make sure everything is setup correctly run tests  
  `pytest`

- **Run Server**  
  `uvicorn main:app --reload`  

## Test Performance
- **Seed Database**  
  Make sure you seed database before testing performance.This has to be done only once so that performance is checked correctly.  
  `python seeder.py`  

- **Run Locust**  
  Make sure your server is up and running.  
  `locust -f locustfile.py --host=http://localhost:8000`  
  After that visit `http://0.0.0.0:8089` to test performance

