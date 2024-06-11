# Step 1 select default OS image
FROM python:3.12

# # Step 3 Configure a software
# # Defining working directory
WORKDIR /app

# # Copy everything which is present in my docker directory to working (/app)
COPY requirements.txt /app

RUN pip3 install -r requirements.txt

COPY . /app

# Exposing an internal port
EXPOSE 8000

# These are permanent commands i.e even if user will provide come commands those will be considered as argunemts of this command
ENTRYPOINT [ "python3" ]

# Define environment variable
ENV NAME World

# Set the entry point to run the start.sh script
CMD ["server.py"]


