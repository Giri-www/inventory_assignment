# Title: Building a Backend API for a Simple Inventory Management System using Django Rest Framework

This project is a simple Inventory Management System backend built using Django Rest Framework (DRF), integrated with JWT-based authentication,MySQL, and Redis for caching. The project is containerized using Docker Compose for easy setup and deployment.

## Prerequisites
- [Python 3.8+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [MySQL](https://dev.mysql.com/downloads/installer/) (for local setup)

## Project Structure

inventory_proj/ │ ├── Dockerfile ├── docker-compose.yml ├── inventory/ │ ├── migrations/ │ ├── init.py │ ├── admin.py │ ├── apps.py │ ├── models.py │ ├── serializers.py │ ├── tests.py │ ├── urls.py │ ├── views.py │ ├── manage.py ├── requirements.txt ├── README.md └── .env