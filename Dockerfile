# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /usr/src/app
COPY . /usr/src/app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

WORKDIR /usr/src/app/MixrAi

# Run Django server when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
