# Use the official Python 3 base image
FROM python:3.11-slim

# Install uv for python3
RUN pip install uv
RUN apt-get update && apt-get install -y ffmpeg

# Set working directory
WORKDIR /app

# Install dependencies
COPY pyproject.toml /app/
COPY uv.lock /app/
RUN uv sync

# Copy application code
COPY . /app

# Expose port
EXPOSE 8000

CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "main:get_app"]