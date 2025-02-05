# Gamo



## backend/gamelogic setup 

The following is the setup process for running the backend python without needing to install any packages to the local version of your Python.

Firstly install and create the virtual enviroment:

```bash
pip install virtualenv
python -m virtualenv venv_name
``` 

According to your operating system, activate the enviroment
```bash
Windows:
venv_name\Scripts\activate.ps1

Linux/MacOs:
source venv_name/bin/activate
```

Then install all the listed libararies using the following command:

```bash
pip install -r python_requirements.txt
```

VOILA !

now to run the django backend go to "django_backend" directory and run the following:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## frontend setup

```bash
npm install --legacy-peer-deps
npm run
```

