# Owls
> A survival game where your owl hunts, eats and sleeps (for now).
<hr>

# Requirements
* Python 3
* Flask, flask-sqlAlchemy, flask-migrate, python-dotenv

# Setup
*GitBash commands run from Windows*
1. Install Python 3: https://www.python.org/downloads/
1. Clone repo: `git clone https://github.com/jlyden/mair`
1. Enter folder: `cd mair`
1. Create virtual environment: `python -m venv venv`
1. Activate virtual environment: `. venv\Scripts\activate`
1. Install dependencies: `pip install flask python-dotenv flask-sqlalchemy flask-migrate`
1. Initialize & migrate db: `flask db init; flask db migrate; flask db upgrade`
1. Run application: `flask run`

