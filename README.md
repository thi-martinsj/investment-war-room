# investment-war-room

This is a project for Inoa's selection process.

## Overview

The purpose of this project is to assist an investor in his active of buying and selling assets on B3.

The investor can define the assets to be monitored and configurate the price tunnels and frequency for each asset.

It uses the free API `api-cotacao-b3` to get all companies and tickers values. I used this API only for the purpose of simulating how to get B3 assets prices.

It also uses `python smtpd` to simulate a SMTP server to send emails.

## Main technologies used

- Python 3.10.0
- Django 4.0.6

## How to run
### Install Python and dependencies

First of all, you need to have Python installed on your computer. If you don't have it, you can download Python [here](https://www.python.org/downloads/).

With Python installed, create a Python virtual environment with the following command:
```
python -m venv .venv
```

Now, active the virtual environment:
- Linux
    ```
    source .venv/bin/activate
    ```
- Windows
    ```
    source .venv/Scripts/activate
    ```

Then, install de requirements.txt dependencies:
```
pip install -r requirements.txt
```

### Run Python SMTPD

To simulate an SMTP server to send emails, run the following command in terminal:
```
python -m smtpd -n -c DebuggingServer localhost:1025 
```

The terminal will be running the server simulation.

### Run the Migrations


So, execute the following command to run the migrations:
```
python manage.py migrate
```
### Run the Application
It uses the `DB SQLite` database. It is already installed with Django and it has the `db.sqlite3` file with all configurations ready to be used.

Finally, to run the application execute the command:
```
python manage.py runserver
```

If everything has been configured correctly, you can enjoy the application. ;)

## Note

Changes and suggestions are accepted