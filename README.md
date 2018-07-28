# Flask Task Queue Starter

This is a flask-based starter application that can be easily integrated with Redis Queue. Redis Queue is a queuing framework useful for performing an asynchronous task on a separate process. It uses Redis server underneath. This starter uses Docker and Docker Compose for managing flask app with Redis server.

### Prerequisites

This application requires `Docker` to be installed on the System. If you do not have Docker installed on your system, head out to this link https://docs.docker.com/install/ to get started.

### Setting up

* Clone this repository on your machine.
* Make sure you have Docker daemon running on your machine.
* Run the following command to bootstrap the application:
```
docker-compose up --build
```

This will start two docker containers, one is our flask web server and the other is a Redis server. The build argument builds an image each time the command is executed to ensure the web server container runs with the latest code. The Redis server uses the official Redis image available on DockerHub.

You can check out the whole application on `completed` branch.