# PlayList API
A playlist management API build with FastAPI. The app follows a restful design while making use of
the clean architecture and repository design patterns. A code-first approach has been followed to manage the database
structure by using alembic's auto-generate migrations.


## Requirements

### Python 3
Ensure that python 3 is installed in your environment. See the following [link](https://www.python.org/downloads/) on 
how to get started.

### .env
Ensure that a .env file is created with the following environment variable included:
"DATABASE_URL". This can be an sqlite URI for the development environment.

e.g ``sqlite:///storage/development.db``

### Virtual Environment
Create a virtual environment for the project and activate it.


### Python Path
Ensure that the app folder is added to the PYTHONPATH variable


## Getting Started
1. Install dependencies
```zsh
pip install -r requirements.txt
```

2. Run migrations
```zsh
alembic upgrade head
```

3. Seed Database
```zsh 
python load_data_script.py
```

4. Start FastAPI process
```zsh
uvicorn app.main:app --host 0.0.0.0 --port 80
```
5. Open local API docs [http://localhost:8000/docs](http://localhost:8000/docs)
