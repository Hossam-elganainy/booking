FROM python:3.11-slim

# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
    git \
    gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Create application directory
RUN mkdir /islamic_chatbot
WORKDIR /islamic_chatbot

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .


# RUN django-admin compilemessages

# Clean up pip cache
RUN pip cache purge
