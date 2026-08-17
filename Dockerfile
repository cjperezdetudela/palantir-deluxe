FROM python:3.11-slim

# Install system dependencies including FFmpeg for real-time audio transcoding
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Render assigns dynamic PORT environment variable
ENV PORT=10000

EXPOSE ${PORT}

# Run server with uvicorn listening on 0.0.0.0 and $PORT
CMD ["sh", "-c", "python -m uvicorn server:app --host 0.0.0.0 --port ${PORT:-10000}"]
