# TanX.fi Backend Engineer Task

**Name:** Rishikeshav Ravichandran
**Reg No:** 20BEC1261
**Personal email:** rishi.r1804@gmail.com
**College email:** rishikeshav.ravi2020@vitstudent.ac.in

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
## POST /alerts/create
Route to create an alert, accepted schema is 

## POST /alerts/delete/{id}
Route to change status of an alert to 'deleted'

## GET /alerts
Route to get multiple alerts of a user
query parameters are: status

## GET alerts/start
GET route to start the process of running Binance's websocket


## POST /login
Route to authenticate login and get JWT access_token

## POST /users/
Route to create a user
  

# Solution to send alerts:
Used a class based solution called PriceChecker wherein multithreading is used to run multiple websockets at the same time then send an email through Gmail SMTP, incorporated with RabbitMQ for message queuing if the given price is reached.
