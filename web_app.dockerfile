# Use the official Python image from the slim variant
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git && \
    rm -rf /var/lib/apt/lists/*

RUN pip install pip-review

RUN pip-review --local --auto

# Install pipenv
RUN pip install pipenv

RUN git clone https://github.com/Institute-of-Surface-Science/CorWiz.git .

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install Python dependencies
RUN pipenv install --deploy --ignore-pipfile

## Copy the application code
COPY . .

# Create the necessary directories for certificates
RUN mkdir -p /etc/letsencrypt/live/www.corwiz.xyz

# Copy the certificate and key files
# COPY .certificates/fullchain.pem /etc/letsencrypt/live/www.corwiz.xyz/fullchain.pem
# COPY .certificates/privkey.pem /etc/letsencrypt/live/www.corwiz.xyz/privkey.pem

# Expose the port the app runs on
EXPOSE 8501 443

# Define a health check to ensure the service is running
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

WORKDIR /app/web_app

# Run the application
ENTRYPOINT ["pipenv", "run", "streamlit", "run", "website.py", "--server.port=8501", "--server.address=0.0.0.0"]
