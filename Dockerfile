FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy all contents from the "challenge" folder to the working directory in the container
COPY ./challenge /app/challenge

# Copy the requirements.txt file to the working directory
COPY requirements.txt /app/requirements.txt

# Remove the exploration.ipynb file and .pyc files (Python compiled files)
RUN rm -f /app/challenge/exploration.ipynb && \
    find /app/challenge -name '*.pyc' -delete

# Install dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose port 8080 to be accessible from outside the container
EXPOSE 8080

# Set the PYTHONPATH environment variable to the working directory
ENV PYTHONPATH="/app"

# Define the command to run the application when the container starts
CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8080"]