# PIMA-Integration-Dashboard
Salesforce integration with the satellite dashboard/map.


## Run The Application

- Clone the repository

    > `git clone https://github.com/TechnoServe/PIMA-Integration-Dashboard.git`

- Change to `PIMA-Integration-Dashboard` directory and Copy `env.example.txt`  to `.env` file.

    > `cd PIMA-Integration-Dashboard/`

    > `cp env.example.txt .env`

- Modify `.env` file to match your environment

- Install the required packages.  Note: before running the command below, It is advised that you create virtual environment to isolate this application's packages from the rest of  other environments in your computer.
    > `pip install -r requirements.txt`

- Run the migrations
    > `python manage.py migrate`

- If you need to seed dummy data. If not, skip this step.
    > `python manage.py loaddata dummy_data.json`
- /!\ :Make sure Redis instance is running as you specified in `.env` file.
- Start the Celery worker
    > `celery --app PIMA_Dashboard.celery worker -l info`
- Start the Celery scheduler beat.
    > `celery --app PIMA_Dashboard.celery beat -l info`
- Start the application
    > `python manage.py runserver`