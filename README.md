# Django Store Assessment

A project to show REST API usage

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Set Up For Local Development
### Set Up Database
- Install PostgreSQL using `brew install postgresql`
- Create a database cluster using `initdb /usr/local/var/postgres`
- Start Postgres service using `brew services start postgresql`
- To configure Postgres, use `psql`
  - Create a new user using: `CREATE USER username WITH PASSWORD ‘password’;`
  - Create a new database using: `CREATE DATABASE dbname;`
  - Grant privileges to the user using: `GRANT ALL PRIVILEGES ON DATABASE dbname TO username;`
  - Exit using `\q`

### Set Up Virtual Environment
- Create a virtual environment using `python-m venv .venv`
- Activate the virtual environment using `source .venv/bin/activate`
- Install dependencies using `pip install -r requirements/local.txt`

### Set Up Environment Variables
- Create a `.env` file in the root directory
- Create an environment variable for the database `DATABASE_URL=postgres://username:password@localhost:5432/dbname`

### Migrations
- Make migrations using `python manage.py makemigrations`
- Migrate using `python manage.py migrate`

### Superuser
- Create a superuser using `python manage.py createsuperuser`

### Run Server
- Run the server using `python manage.py runserver`
- The API endpoint for Store should be available at `http://127.0.0.1:8000/api/stores/`

## Sending Requests
- Send a POST request to the endpoint `http://127.0.0.1:8000/auth-token/` to get an authentication token
- The body of the request should contain the username and password like this:
```
{
    "username": "admin@example.com",
    "password": "password123"
}
```
- Use this token to perform CRUD via `http://127.0.0.1:8000/api/stores/` endpoint
- The token should be sent in the header of the request like this: `--header 'Authorization: Token token_value'`



#### Running tests with pytest

    $ pytest
