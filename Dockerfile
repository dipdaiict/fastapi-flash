# FROM python:3.12.4

# WORKDIR /usr/src/app

# COPY requirements.txt ./

# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# ## This to Deployment for the Product as Container:
FROM python:3.12.4

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements file
COPY requirements.txt ./

# Install virtualenv
RUN pip install virtualenv

# Create a virtual environment and activate it
RUN virtualenv venv

# Install dependencies into the virtual environment
RUN venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port 8080
EXPOSE 8080

# Start the application using Gunicorn within the virtual environment
CMD ["venv/bin/gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8080"]    