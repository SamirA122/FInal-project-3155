from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..controllers import payments as controller
from ..schemas import payments as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Payments'],
    prefix="/payments"
)


@router.post("/", response_model=schema.Payment)
def create(request: schema.PaymentCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Payment])
def read_all(
    payment_status: str = Query(None, description="Filter by payment status"),
    db: Session = Depends(get_db)
):
    return controller.read_all(db, payment_status=payment_status)


@router.get("/{item_id}", response_model=schema.Payment)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.get("/order/{order_id}", response_model=schema.Payment)
def read_by_order(order_id: int, db: Session = Depends(get_db)):
    result = controller.read_by_order(db, order_id=order_id)
    if not result:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found for this order")
    return result


@router.put("/{item_id}", response_model=schema.Payment)
def update(item_id: int, request: schema.PaymentUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
