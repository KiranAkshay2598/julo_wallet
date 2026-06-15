# Julo Wallet API

A robust, fully-grounded backend transaction system built with Django and Python. This project was originally developed back in 2022 as part of an interview process to showcase clean software engineering practices, strict coding standards, and correct transaction flow design. Rather than a sprawling enterprise application, it is designed as a focused, core reference project to demonstrate strong backend fundamentals in transaction handling and state management.

It serves as a reference backend project for core financial and banking logic, featuring token-based authentication and strict database-level ACID transaction integrity. It is an excellent resource for learning core backend API design and asynchronous worker architectures.

---

## Key Features

*   **Account Initialization**: Create user accounts and authenticate using Token Authentication.
*   **Wallet Management**: Enable, disable, and view wallet details.
*   **ACID Compliance**: Ensures strict database integrity during financial operations (deposits and withdrawals).
*   **Asynchronous Processing**: Offloads wallet balance updates to background worker tasks using Celery and RabbitMQ.
*   **Unit Tested**: Includes comprehensive unit tests verifying success and failure transaction states.

---

## Tech Stack

*   **Backend Framework**: Django & Django REST Framework (DRF)
*   **Asynchronous Task Queue**: Celery
*   **Message Broker**: RabbitMQ
*   **Database**: SQLite (Default local development)

---

## Project Setup

Follow these steps to set up and run the project locally on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com/KiranAkshay2598/julo_wallet.git
cd julo_wallet
```

### 2. Set Up the Virtual Environment
Create a virtual environment and activate it:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
Install all required Python packages:
```bash
pip install -r requirements.txt
```

### 4. Install and Start RabbitMQ (Celery Message Broker)
On Ubuntu/Debian-based systems, run:
```bash
sudo apt-get update
sudo apt-get install rabbitmq-server
sudo systemctl start rabbitmq-server
```

### 5. Run Database Migrations
Initialize your local database schema:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Running the Application

To run the application, you need to start two processes in separate terminals:

### Terminal 1: Celery Worker
Start the Celery worker process to handle background transactions:
```bash
celery -A miniwallet worker -l info
```

### Terminal 2: Django Development Server
Start the local web server:
```bash
python manage.py runserver 0.0.0.0:8000
```
The server will be up and running at `http://127.0.0.1:8000/`.

---

## Testing the APIs

### Automated Tests
Run the unit test suite:
```bash
python manage.py test
```

### Manual API Testing (Postman)
You can find the raw Postman collection JSON file in the project directory at:
```
/postman/Julo_Wallet.postman_collection.json
```
To use it:
1. Open **Postman**.
2. Click the **Import** button.
3. Drag and drop the `Julo_Wallet.postman_collection.json` file from your project folder to start testing the transaction endpoints.
