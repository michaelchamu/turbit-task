# Alternative using Alpine Linux (smaller, sometimes more reliable)
FROM python:3.11-alpine as base

# Set working directory
WORKDIR /app/turbit-apis

# Install system dependencies for Alpine
RUN apk add --no-cache \
    gcc \
    musl-dev \
    curl

# Copy project files
COPY . .

# Install the shared mongo connector package
RUN cd mongoconnector && pip install . --no-cache-dir

# Install requirements for both applications
RUN pip install --no-cache-dir --upgrade pip && \
    if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi && \
    if [ -f task-1/app/requirements.txt ]; then pip install --no-cache-dir -r task-1/app/requirements.txt; fi && \
    if [ -f task-2/api/requirements.txt ]; then pip install --no-cache-dir -r task-2/api/requirements.txt; fi

# Stage for Task 1
FROM base as task1
WORKDIR /app/turbit-apis/task-1
EXPOSE 6000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "6060"]

# Stage for Task 2
FROM base as task2
WORKDIR /app/turbit-apis/task-2
EXPOSE 7000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7070"]