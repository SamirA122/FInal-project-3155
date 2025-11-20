from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import reviews as model
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func


def create(db: Session, request):
    new_item = model.Review(
        order_id=request.order_id,
        sandwich_id=request.sandwich_id,
        rating=request.rating,
        review_text=request.review_text
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session, sandwich_id: int = None, order_id: int = None):
    try:
        query = db.query(model.Review)
        if sandwich_id:
            query = query.filter(model.Review.sandwich_id == sandwich_id)
        if order_id:
            query = query.filter(model.Review.order_id == order_id)
        result = query.all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Review).filter(model.Review.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Review).filter(model.Review.id == item_id)
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
        item = db.query(model.Review).filter(model.Review.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def get_complaints(db: Session, min_rating: int = 2):
    """Get sandwiches with low ratings (complaints)"""
    try:
        from ..models import sandwiches as sandwich_model
        result = db.query(
            sandwich_model.Sandwich,
            func.avg(model.Review.rating).label('avg_rating'),
            func.count(model.Review.id).label('review_count')
        ).join(
            model.Review, sandwich_model.Sandwich.id == model.Review.sandwich_id
        ).group_by(
            sandwich_model.Sandwich.id
        ).having(
            func.avg(model.Review.rating) <= min_rating
        ).all()
        return result
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
