from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import promotional_codes as model
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


def create(db: Session, request):
    new_item = model.PromotionalCode(
        code=request.code,
        discount_percent=request.discount_percent,
        expiration_date=request.expiration_date,
        is_active=request.is_active if request.is_active is not None else True
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session, is_active: bool = None):
    try:
        query = db.query(model.PromotionalCode)
        if is_active is not None:
            query = query.filter(model.PromotionalCode.is_active == is_active)
        result = query.all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.PromotionalCode).filter(model.PromotionalCode.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def read_by_code(db: Session, code: str):
    """Get promotional code by code string"""
    try:
        item = db.query(model.PromotionalCode).filter(model.PromotionalCode.code == code).first()
        if not item:
            return None
        # Check if expired
        if item.expiration_date and item.expiration_date < datetime.now():
            return None
        if not item.is_active:
            return None
        return item
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def update(db: Session, item_id, request):
    try:
        item = db.query(model.PromotionalCode).filter(model.PromotionalCode.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.PromotionalCode).filter(model.PromotionalCode.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
