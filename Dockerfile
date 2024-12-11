# syntax=docker/dockerfile:1

###################################
# Stage 1: Builder
###################################
FROM python:3.11-slim AS builder

# set work directory
WORKDIR /app

# copy requirements.txt and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --target /app/deps -r requirements.txt

# copy all source code to /app/src
COPY src/ /app/src

###################################
# Stage 2: Distroless
###################################
FROM python:3.11-slim

# set work directory
WORKDIR /app

# copy dependencies and source code from builder stage
COPY --from=builder /app/deps /app/deps
COPY --from=builder /app/src /app/src

# set environment variables and PYTHONPATH
ENV PYTHONPATH=/app/deps
EXPOSE 8080

# run Flask app
CMD ["python3", "/app/src/app.py"]
