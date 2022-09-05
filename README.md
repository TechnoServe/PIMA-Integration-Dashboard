# PIMA-Integration-Dashboard
Salesforce integration with the satellite dashboard/map.


## Run The Application

- Clone the repository

    > `git clone https://github.com/TechnoServe/PIMA-Integration-Dashboard.git`

- Change to `PIMA-Integration-Dashboard` directory and Copy `env.example.txt`  to `.env` file.

    > `cd PIMA-Integration-Dashboard/`

    > `cp env.example.txt .env`

- Modify `.env` file to match your environment


- Set Mysql database instance up. (for the local environment, you can use a docker container to speed up the development)
    > `docker run  --name pima-db --rm  -p 3306:3306 -e MYSQL_DATABASE=database_name -e MYSQL_USER=pima_user -e MYSQL_PASSWORD=pima_user_password -e MYSQL_ROOT_PASSWORD=root_password  mysql:8`

- Install the required packages.
- /!\ : before running the command below, It is advised that you create virtual environment to isolate the application's packages from the rest of  other environments in your computer. Here's official docs for virtual environment creation: https://docs.python.org/3/library/venv.html
    > `pip install -r requirements.txt`

- Run the migrations
    > `python manage.py migrate`

- Set redis instance up.
    > `sudo docker run --name redis-instance --rm  -p 6379:6379 redis`
- Start the Celery worker
    > `celery --app PIMA_Dashboard.celery worker -l info`
- Start the Celery scheduler beat.
    > `celery --app PIMA_Dashboard.celery beat -l info`
- Create superuser
    > `python manage.py createsuperuser`
- Run the application
    > `python manage.py runserver`