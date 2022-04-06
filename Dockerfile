# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9.10-slim-bullseye 

# Use /usr/src/app as our workdir. The following instructions will be executed in this location.
WORKDIR /usr/src/app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

COPY install-packages.sh .

RUN chmod +x /usr/src/app/install-packages.sh && ./install-packages.sh

# # Install pip requirements
COPY requirements.txt /usr/src/app/requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt


COPY app/ /usr/src/app/app 


# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /usr/src/app
USER appuser

CMD ["sleep", "infinity"]

