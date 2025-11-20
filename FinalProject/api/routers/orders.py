from fastapi import APIRouter, Depends, FastAPI, status, Response, Query
from sqlalchemy.orm import Session
from datetime import datetime
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Order])
def read_all(
    start_date: datetime = Query(None, description="Filter orders from this date"),
    end_date: datetime = Query(None, description="Filter orders until this date"),
    db: Session = Depends(get_db)
):
    return controller.read_all(db, start_date=start_date, end_date=end_date)


@router.get("/tracking/{tracking_number}", response_model=schema.Order)
def read_by_tracking(tracking_number: str, db: Session = Depends(get_db)):
    return controller.read_by_tracking(db, tracking_number=tracking_number)


@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
