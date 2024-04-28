# BlogRestAPIs
Backend of a Blog application built with RESTful APIs

## Features
- The application is built on 2 different routes for 'auth' and 'posts'.
- Test cases are written in /tests folder
- to view API documentation, run the application and visit 'http://localhost:5000/swagger/' 

*Instructions to run the Application*

Clone the git repository and set up the project

-Set up virtual environment so that dependencies will not cause issues (For windows)
```bash
python -m venv venv
venv\Scripts\activate
```

- Install dependencies- 
```bash
pip install -r requirements.txt
```
- make sure that .env file is present with the information related to MONGO_URI, MONGO_TEST_URI, SECRET_KEY, FLASK_ENV
- to run the unit and integration tests, run application in TEST mode:
```bash
export FLASK_ENV=TEST
pytest tests/ 
```

- to run in DEV mode run commands:
```bash
export FLASK_ENV=DEV
export FLASK_APP=run.py
flask run
```


