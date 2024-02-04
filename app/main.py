from fastapi import FastAPI
from .routers import alerts, users, auth


app = FastAPI()


app.include_router(alerts.router)
app.include_router(users.router)
app.include_router(auth.router)