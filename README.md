1.Clone the project in your local machine.

2.Set up the virtal Environment and activate it.

3.In your respective project folder perform the following steps

4.Download the requirements.txt file to get all the required packages using the command **pip install -r requirements.txt** in your shell.

5.To install rabbit mq please use the following command **sudo apt-get install rabbitmq-server** and start the rabbit mq by **sudo systemctl start rabbitmq-server**

6.Make the migrations using the command **python manage.py makemigrations**

7.Then migrate the models using the command **python manage.py migrate**

8.In a seperate terminal, activate the virtual environment and start the celery workers by **celery -A miniwallet worker -l INFO** inside the project directory.

9.Run the server using the command **python manage.py runserver**

10.Consume the API's with postman using this collection link: https://www.getpostman.com/collections/c9be561d3772e93c5dce

11.To run unit tests use the command **python manage.py test** while inside the project directory.
