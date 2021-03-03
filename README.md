# Getting Started with RabbitMQ

- [RabbitMQ](https://www.rabbitmq.com/) is an open source message broker. 
- It accepts and translates messages from a producer (the message sender) and holds it in a queue so that a consumer (the message receiver) can retrieve it.
- It excels at is doing this at scale while staying lightweight and easy to deploy.

## Before You Begin

Here are few tools you need
1. Docker :  RabbitMQ server will run in a container to ease the setup
2. Python 
3. [Pipenv](https://pipenv.pypa.io/en/latest/) is used to set up a working environment

## Run RabbitMQ server

To ease the setup of our RabbitMQ node, we’ll run the RabbitMQ container image from Docker Hub.
For this example, w’ll just need a simple single-node RabbitMQ server, so we won’t need to change any of the default settings. Run the container image with the following 

    docker run -it --rm -p 5672:5672 -p 15672:15672 rabbitmq:3-management

Here, we run `3-management tag` of the RabbitMQ container image. This image ships with the management plug-in, which will provide an HTTP API and web-based UI for your RabbitMQ server. Docker run in interactive shell with the -it option, as well as  automatically remove the container when it exits with the -rm option. We forward a couple of ports (5672 for the RabbitMQ server and 15672 for the HTTP API and web UI) from our local machine to the container, which means that w can connect to it on localhost.

To access the web UI, go to http://localhost:15672. The username and password are both `guest`. Here w can change settings, add and remove users, as well as view diagnostic information from the server.

## Running RabbitMQ server using docker-compose

1. From the root of the project directory run `docker-compose up`
2. If you want to run the service in the background,  pass the -d flag `docker-compose up -d`
3. To see what is running `docker-compose ps`
4. To stop, if Compose started with `docker-compose up -d` run `docker-compose stop`
5. To bring everything down, removing the containers entirely run `docker-compose down`

## Run emitter and consumer

1. `emitter.py` emit messages to Rabbit MQ. Run the code `pipenv run python3 app/emitter.py`
2. `consumer.py` code consume emitted messages. Run the code `pipenv run python3 app/consumer.py`

Make sure RabbitMQ server is running

## Links and info

1. [Experimenting with RabbitMQ on our workstation](https://www.rabbitmq.com/download.html)
2. [Pipenv](https://pipenv.pypa.io/en/latest/)
3. [Docker](https://docs.docker.com/desktop/)
4. [Docker-Compose](https://docs.docker.com/compose/gettingstarted/)



