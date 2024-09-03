# Reserve Shop - Auth Service

The `auth` service is a crucial part of the Reserve Shop project, responsible for handling user authentication and management. This service is built using FastAPI and follows a microservice architecture.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Running the Service](#running-the-service)
  - [Step 1: Run Docker Compose](#step-1-run-docker-compose)
  - [Step 2: Install Python Dependencies](#step-2-install-python-dependencies)
  - [Step 3: Start the Auth Service](#step-3-start-the-auth-service)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [License](#license)

## Prerequisites

Before you start, ensure you have the following installed on your system:

- Docker
- Docker Compose
- Python 3.8+
- pip

## Running the Service

Follow the steps below to run the `auth` service.

### Step 1: Run Docker Compose

To set up the necessary infrastructure (such as the database), navigate to the root directory of the project where the `docker-compose.yml` file is located and run the following command:

```bash
docker-compose up -d
```

This will pull and start all the necessary Docker containers in the background.

### Step 2: Install Python Dependencies

Before starting the service, you need to install the required Python packages. Navigate to the `auth` service directory and run:

```bash
pip install -r requirements.txt
```

This command will install all the dependencies listed in the `requirements.txt` file.

### Step 3: Start the Auth Service

Once the dependencies are installed, you can start the `auth` service. Run the FastAPI application using `uvicorn`:

```bash
cd app/
python3 main.py
```

This will start the `auth` service on `http://localhost:8000`.

## Environment Variables

The `auth` service requires certain environment variables to be set. You can configure these in a `.env` file located in the `auth` service directory or set them directly in your environment. The most common environment variables include:

- `DATABASE_URL`: The connection string for your database.
- `SECRET_KEY`: A secret key used for JWT token encoding.
- `DEBUG`: Set to `True` for development and `False` for production.

## API Endpoints

The `auth` service exposes the following API endpoints:

- `POST /register`: Register a new user.
- `POST /login`: Authenticate a user and issue a JWT.
- `GET /users/me`: Get the authenticated user's information.
- `POST /refresh-token`: Refresh the JWT token.

Refer to the API documentation at `http://localhost:8000/docs` for more detailed information on each endpoint.

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for more details.
