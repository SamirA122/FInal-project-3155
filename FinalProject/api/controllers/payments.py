from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import payments as model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_item = model.Payment(
        order_id=request.order_id,
        amount=request.amount,
        payment_method=model.PaymentMethod(request.payment_method),
        payment_status=model.PaymentStatus(request.payment_status) if request.payment_status else model.PaymentStatus.PENDING
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session, payment_status: str = None):
    try:
        query = db.query(model.Payment)
        if payment_status:
            query = query.filter(model.Payment.payment_status == model.PaymentStatus(payment_status))
        result = query.all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid payment status: {str(e)}")
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Payment).filter(model.Payment.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def read_by_order(db: Session, order_id: int):
    """Get payment by order_id"""
    try:
        item = db.query(model.Payment).filter(model.Payment.order_id == order_id).first()
        return item
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Payment).filter(model.Payment.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        # Handle enum fields
        if 'payment_status' in update_data:
            update_data['payment_status'] = model.PaymentStatus(update_data['payment_status'])
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid enum value: {str(e)}")
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Payment).filter(model.Payment.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
