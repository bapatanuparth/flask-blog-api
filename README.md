# BlogRestAPIs
Backend of a Blog application built with RESTful APIs

- The application is built on 2 different routes for 'auth' and 'posts'.
- Test cases are written in /tests folder
- to view API documentation, run the application and visit 'http://localhost:5000/swagger/' 

*Instructions to run the Application*

Clone the git repository and set up the project

- Install dependencies- 
pip install -r requirements.txt

- make sure that .env file is present with the information related to MONGO_URI, MONGO_TEST_URI, SECRET_KEY, FLASK_ENV

- to run in DEV mode run commands:
export FLASK_ENV=DEV
export FLASK_APP=run.py
flask run

- to run the application in TEST mode run commands
export FLASK_ENV=TEST
pytest tests/ 

This will run all the unit and integration tests for
