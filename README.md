# Title: Building a Backend API for a Simple Inventory Management System using Django Rest Framework

This project is a simple Inventory Management System backend built using Django Rest Framework (DRF), integrated with JWT-based authentication,MySQL, and Redis for caching. The project is containerized using Docker Compose for easy setup and deployment.

## Prerequisites
- [Python 3.8+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [MySQL](https://dev.mysql.com/downloads/installer/) (for local setup)

## Project Structure

## Setting Up the Project

### Option 1: Running Locally with a Virtual Environment
    
1. **Clone the repository**
    ```bash
       git clone https://github.com/Giri-www/inventory_assignment.git
       cd inventory_proj

2. **Create Virtual enviroment using below commands**
    ```bash
    *Windows*
    >> python -m venv venv
    >> venv\Scripts\activate
    *Linux*
    >> python3 -m venv venv
    >> source venv/bin/activate

3. **Install the required dependencies**
    ```bash
    >> pip install -r requirements.txt

4. **Migrations & Migrate**
    ```bash
    >> python manage.py makemigrations
    >> python manage.py migrate

5. **Run your Docker Compose**
    ```bash
    >> docker-compose up -d 
    >> docker-compose up --build 

 RUN YOUR SERVER
6. **From Project Import the request Postman json in your Postman**
    >> using sign in you can create the user




### Key Changes:
1. Updated `DATABASES` settings in `settings.py` to use `django.db.backends.mysql`.
2. Adjusted setting.py file to include MySQL settings.
3. Updated `docker-compose.yml` to use MySQL as the database service.

Let me know if you need any more changes or further customization!
