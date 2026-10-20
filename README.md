# db-app-example

A small Flask application that reads and writes actor data in the MySQL `sakila` sample database.

## Prerequisites

- Python 3
- MySQL running locally on port 3306, with the [sakila sample database](https://dev.mysql.com/doc/sakila/en/) installed

## Setup

This application must be run from inside a virtual environment, so its libraries don't conflict with anything else on your computer. The app will refuse to start if you skip this.

1. **(Recommended, one time only)** Tell pip to install packages only inside a virtual environment:

   ```
   pip3 config set global.require-virtualenv true
   ```

2. From the project folder, create the virtual environment:

   ```
   python3 -m venv venv
   ```

3. Activate it. You need to do this every time you open a new terminal.

   - macOS / Linux:
     ```
     source venv/bin/activate
     ```
   - Windows:
     ```
     venv\Scripts\activate
     ```

   Your prompt should now start with `(venv)`.

4. Install the required libraries:

   ```
   pip install -r requirements.txt
   ```

5. Create a file named `.env` in the project folder containing your MySQL root password:

   ```
   PASSWORD=your_mysql_password
   ```

   This file is ignored by git, so your password won't be committed.

## Running the app

With the virtual environment activated:

```
python app.py
```

Then open http://127.0.0.1:8000 in your browser.

When you're finished, run `deactivate` to leave the virtual environment.
