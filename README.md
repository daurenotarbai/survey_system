# Simple questionannaire
* API CRUD for surveys and questions of survey
* API to answer questions

## Run  
Install requirements for this project
```
pip install -r requirementa.txt
```
Navigate to the project directory (where manage.py is located) and run
```
python manage.py makemigrations
python manage.py migrate
```
Create superuser for django admin panel
```
python manage.py createsuperuser
```
Run the project
```
python manage.py runserver
```
After running the above command, the survey application will be available at http://localhost:8000/survey 

The admin portal can be accessed at http://localhost:8000/admin

The swagger documentation of the project API you can find at http://localhost:8000/api/v1/documentation

## Features:
##### There are 3 types of questions
* * Free text questions
* * Single-choice questions
* * Multiple-choice questions

## Resources Used
* python3
* django 2.2
* Django Rest Framework (DRF)
