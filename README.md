# Storyvord Server

This document provides instructions on how to set up and start the Storyvord server.

## Prerequisites

- Python 3.10.6
- pip
- virtualenv
- PostgreSQL

## Setup

1. **Clone the repository**

    ```bash
    git clone https://github.com/username/storyvord.git
    cd storyvord
    ```

2. **Create a virtual environment**

    ```bash
    python3 -m venv .env
    ```

3. **Activate the virtual environment**

    On Unix or MacOS:

    ```bash
    source .env/bin/activate
    ```

    On Windows:

    ```bash
    .env\Scripts\activate
    ```

4. **Install the dependencies**

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up the database**

    Create a PostgreSQL database and note down the connection details. You will need the database name, username, password, host, and port.

6. **Set the environment variables**

    Create a `.env` file in the root directory of the project and add the following lines:

    ```properties
    DATABASE_URL=postgres://username:password@localhost:5432/mydatabase
    ```

    Replace `username`, `password`, `localhost`, `5432`, and `mydatabase` with your actual PostgreSQL username, password, host, port, and database name.

## Running the server

1. **Apply the migrations**

    ```bash
    python manage.py migrate
    ```

2. **Start the server**

    ```bash
    gunicorn storyvord.wsgi:application --bind=0.0.0.0 --workers=3 --chdir storyvord/
    ```

The server should now be running at `http://0.0.0.0:8000`.

## Troubleshooting

If you encounter any issues while setting up or running the server, please check the console output for error messages. These messages can often provide clues about what's going wrong.