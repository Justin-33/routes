# Use a base image with Python pre-installed
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN pip uninstall decouple && \
    pip install python-decouple pymysql && \
    pip install sqlalchemy_utils

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variables
ENV DATABASE_USER=root
ENV DATABASE_PASSWORD=examplepassword
ENV DATABASE_HOST=db
ENV DATABASE_PORT=3306
ENV DATABASE_NAME=your_database_name
ENV SERVER_PORT=5013

# Expose the Flask server port
EXPOSE $SERVER_PORT

# Copy the application code to the container
COPY . .

# Run the application
CMD ["python3", "app.py"]
