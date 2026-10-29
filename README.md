# db-app-example

A small Flask application that reads and writes actor data in the MySQL `sakila` sample database.

## Prerequisites

- Python 3.10 or newer (check with `python3 --version`, or `py --version` on Windows)
- MySQL running locally on port 3306, with the [sakila sample database](https://dev.mysql.com/doc/sakila/en/) installed

The app connects as MySQL user `root` to `127.0.0.1:3306`. These settings are not read from `.env`. If your MySQL uses a different user or port, change `db_cred` in `core/__init__.py`.

## Setup

This application must be run from inside a virtual environment, so its libraries don't conflict with anything else on your computer. The app will refuse to start if you skip this.

1. **(Recommended, one time only)** Tell pip to install packages only inside a virtual environment:

   ```
   pip3 config set global.require-virtualenv true
   ```

   This applies to every Python project on your computer, not just this one. If it gets in the way of other work, undo it with:

   ```
   pip3 config unset global.require-virtualenv
   ```

2. From the project folder, create the virtual environment:

   - macOS / Linux:
     ```
     python3 -m venv venv
     ```
   - Windows:
     ```
     py -m venv venv
     ```

3. Activate it. You need to do this every time you open a new terminal.

   - macOS / Linux:
     ```
     source venv/bin/activate
     ```
   - Windows (PowerShell, the default in Windows Terminal and VS Code):
     ```
     venv\Scripts\Activate.ps1
     ```
     If you get an error that running scripts is disabled on this system, run this once and then try again:
     ```
     Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
     ```
   - Windows (Command Prompt):
     ```
     venv\Scripts\activate.bat
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
