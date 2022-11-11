# Pull the Python 3.9 Alpine image from Dockerhub
FROM python:3.9.7-alpine3.14

# Establish the working directory for the app as src → main
WORKDIR /usr/src/app

# Copy the requirements.txt file into the working directory and install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

COPY . .

# Run the app with Python 3
CMD [ "python3", "./main.py"]