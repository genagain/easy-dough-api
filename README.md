# Easy Dough API

Easy Dough is a personal finance app that enables user to manage their personal finances easily.

The frontend for this application is [here](https://github.com/genagain/easy-dough-client)

## Quickstart

Clone this repository
```
git clone https://github.com/genagain/easy-dough-api
```

Install the Python dependencies
```
pipenv install
```

Sign up for a Developer Account with Plaid [here](https://dashboard.plaid.com/signup)

Create a **.env** file based on the `.env.example` with proper settings for your development environment

Setup your PostgreSQL user, password and database and make sure it matches your .env file

Activate your pip environment
```
pipenv shell
```

Run the database migrations
```
flask db upgrade
```

Seed your database
```
python seed.py
```

Run the application
```
flask run
```

Then please be sure to follow the quickstart [here](https://github.com/genagain/easy-dough-client) to run the frontend for this application

## Running tests

Run the following command the execute the tests
```
pytest
```

## Technologies

This project uses the following technologies

[Flask](https://flask.palletsprojects.com/en/1.1.x/)

[SQLAlchemy](https://www.sqlalchemy.org/)

[Alembic](https://alembic.sqlalchemy.org/en/latest/)

[Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)

[Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/)

[Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/)

[Flask-CORS](https://flask-cors.readthedocs.io/en/latest/)

[Plaid](https://plaid.com/)

[Advanced Python Scheduler](https://apscheduler.readthedocs.io/en/stable/)

[Postgres](https://www.postgresql.org/)

[pytest](https://docs.pytest.org/en/stable/)
