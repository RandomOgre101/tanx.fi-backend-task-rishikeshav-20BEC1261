# TanX.fi Backend Engineer Task

## Techstack:

- Python (FastAPI)
- Postgres
- Redis (caching)
- RabbitMQ (message queuing)
- Docker
- Docker Compose

## Initial Setup :

- First clone the repository .
```
git clone https://github.com/RandomOgre101/tanx.fi-backend-task-rishikeshav-20BEC1261
```
- Now go to the `app` folder .
```
cd app
```

# Docker
Build the Docker image:
```
docker build -t fastapi-task .
```

Run the Docker container:
```
docker run -p 8000:8000 fastapi-task
```

# Docker Compose Setup :

- There is file called `docker-compose.yml`.
- To run the compose file below command:

```
docker compose up
```
- This will automatically build and run the containers

## Note 
- If there is an error in your Docker compose build, please try the below command:
```
docker compose build --no-cache
```


# Endpoints:
## POST
