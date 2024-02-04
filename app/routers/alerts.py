from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import models
from ..database.database import get_db
from ..schemas import schemas
from ..controllers import JWTauth
from ..webSocket import ws
from typing import Optional
import redis
import pickle


# Initialize redis
rd = redis.Redis(host="localhost", port=6379, db=0)

# Set APIRouter class with URL prefix and swagger docs tag
router = APIRouter(
    prefix = "/alerts",
    tags = ['Alerts'],
)

# POST route to create an alert
@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_alert(alert: schemas.AlertCreate, db: Session = Depends(get_db), current_user: int = Depends(JWTauth.get_current_user)):

    new_alert = models.Alert(owner_id=current_user.id, **alert.model_dump())
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return new_alert


# POST route to change status of alert to 'deleted'
@router.post("/delete/{id}")
def delete_alert(id: int, db: Session = Depends(get_db), current_user: int = Depends(JWTauth.get_current_user)):
    
    alert_query = db.query(models.Alert).filter(models.Alert.id == id)
    alert = alert_query.first()

    # Exception for if query returns None
    if not alert_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert with id: {id} does not exist")
    
    # Exception for if alert's owner_id is not the same as logged in user's
    if alert.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    alert_query.update({"status": "deleted"}, synchronize_session=False)
    db.commit()

    return alert_query.first()


# GET route to get multiple alerts of a user
@router.get("/")
def get_alerts(db: Session = Depends(get_db), current_user: int = Depends(JWTauth.get_current_user), status: Optional[str]=""):

    # Accessing the cache and getting data using key
    cache = rd.get(str(current_user.id)+status)

    # If cache hit, return the data
    if cache:
        return pickle.loads(cache)
    
    # If cache miss, add to cache with user_id + status as the key and normally query from the database
    else:
        query = db.query(models.Alert).filter(models.Alert.owner_id == current_user.id)
        if status:
            query = query.filter(models.Alert.status == status)

        result = query.all()
        rd.set(str(current_user.id)+status, pickle.dumps(result), 600)

        return result
    

# GET route to start the alerts and run them
@router.get("/start", status_code=status.HTTP_200_OK)
def start_alerts(background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: int = Depends(JWTauth.get_current_user)):
    to_websocket = []
    data = db.query(models.Alert).filter(models.Alert.owner_id==current_user.id, models.Alert.status=="created").all()

    for dat in data:
        to_websocket.append((dat.crypto_name, dat.price_to_alert))
    
    # Adds to background tasks so response of 200 can be returned if no error
    background_tasks.add_task(ws.run_threads, data=to_websocket, email=current_user.email)
    

    return {
        "status": 200,
        "detail": "OK"
    }