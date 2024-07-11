# Use an official Python runtime as a parent image
FROM python:3.10.6
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1  # Prevent Python from writing .pyc files to disk
ENV PYTHONUNBUFFERED 1         # Ensure that Python output is not buffered
# Set the working directory in the container
WORKDIR /code
# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*
# Copy the requirements file into the container at /code/
COPY requirements.txt /code/
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the current directory contents into the container at /code/
COPY . /code/
# Copy the JSON credentials file into the container
COPY apis-gcp-storyvord.json /code/apis-gcp-storyvord.json
# Set the environment variable for Google Cloud credentials
ENV GOOGLE_APPLICATION_CREDENTIALS=/code/apis-gcp-storyvord.json
# Collect static files
RUN python manage.py collectstatic --noinput
# Expose the port specified by the PORT environment variable
EXPOSE 8000
# Set the PORT environment variable
ENV PORT=8000
# Debugging: Print environment variables and list files
RUN echo "Environment Variables:" && env && echo "Directory Structure:" && ls -l /code
# Run the application using the PORT environment variable
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "storyvord.wsgi:application"]