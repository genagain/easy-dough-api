## Flask Starter Project

This project allows you to get up and running with Postgres, Flask, and SQLAlchemy quickly. There are a number of other packages that are also installed that may be useful in the assessment as well.

### Quick Start

Install the the Pip environment using the following command.
```
$ pipenv install
```

Open `app/config.py` and fill in the `SQLALCHEMY_DATABASE_URI`.

Open a PSQL shell by running `psql`

Run the following SQL commands in the PSQL shell to create a user and database. Be sure to replace the user, the password and the database name with the same ones you filled in the `SQLALCHEMY_DATABASE_URI`.

```
CREATE USER your_db_user WITH SUPERUSER password 'password';
CREATE DATABASE you_db_name WITH OWNER your_db_user;
```

Quit the PSQL shell using `\q`.

Get into the Pip environment shell using the following command.
```
$ pipenv shell
```

Run the flask app using the following command.
```
(flask-starter) $ flask run
```

To verify that you are set up correctly, visit `localhost:5000` in your browser.
You should see a webpage that says `It works!`
