# syntax=docker/dockerfile:1

###################################
# Stage 1: Builder
###################################
# Use an official Python image for building and installing dependencies
FROM python:3.11-slim AS builder

# Set the working directory
WORKDIR /app

# Copy requirements.txt to install dependencies
COPY requirements.txt ./

# Install dependencies into a dedicated directory using --target
RUN pip install --no-cache-dir --target /app/deps -r requirements.txt

# Copy the application source code
COPY src/ src/

###################################
# Stage 2: Distroless
###################################
# Use a distroless Python image with no shell and minimal footprint
FROM gcr.io/distroless/python3

# Set working directory
WORKDIR /app

# Copy the dependencies and source code from the builder stage
COPY --from=builder /app/deps /app/deps
COPY --from=builder /app/src /app

# Set PYTHONPATH to include the deps directory
ENV PYTHONPATH=/app/deps

# Expose the port your Flask app runs on (if needed)
ENV PORT=8080

# Command to run your Flask application
CMD ["app.py"]
