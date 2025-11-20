from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime
from ..dependencies.database import get_db
from ..models import orders as order_model
from ..models import order_details as order_detail_model
from ..models import sandwiches as sandwich_model
from ..models import reviews as review_model
from decimal import Decimal

router = APIRouter(
    tags=['Analytics'],
    prefix="/analytics"
)


@router.get("/revenue")
def get_revenue(
    date: datetime = Query(None, description="Get revenue for specific date (YYYY-MM-DD)"),
    start_date: datetime = Query(None, description="Start date for revenue range"),
    end_date: datetime = Query(None, description="End date for revenue range"),
    db: Session = Depends(get_db)
):
    """Get total revenue for a specific date or date range"""
    try:
        query = db.query(func.sum(order_model.Order.total_price))
        
        if date:
            # Get revenue for a specific date
            start = datetime.combine(date.date(), datetime.min.time())
            end = datetime.combine(date.date(), datetime.max.time())
            query = query.filter(
                order_model.Order.order_date >= start,
                order_model.Order.order_date <= end
            )
        elif start_date or end_date:
            if start_date:
                query = query.filter(order_model.Order.order_date >= start_date)
            if end_date:
                query = query.filter(order_model.Order.order_date <= end_date)
        
        total_revenue = query.scalar() or Decimal('0.00')
        
        return {
            "total_revenue": float(total_revenue),
            "date": date.isoformat() if date else None,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/popular-dishes")
def get_popular_dishes(
    limit: int = Query(10, description="Number of dishes to return"),
    db: Session = Depends(get_db)
):
    """Get most popular dishes based on order count"""
    try:
        result = db.query(
            sandwich_model.Sandwich,
            func.count(order_detail_model.OrderDetail.id).label('order_count'),
            func.sum(order_detail_model.OrderDetail.amount).label('total_quantity')
        ).join(
            order_detail_model.OrderDetail,
            sandwich_model.Sandwich.id == order_detail_model.OrderDetail.sandwich_id
        ).group_by(
            sandwich_model.Sandwich.id
        ).order_by(
            desc('order_count')
        ).limit(limit).all()
        
        return [
            {
                "sandwich_id": sandwich.id,
                "sandwich_name": sandwich.sandwich_name,
                "order_count": count,
                "total_quantity": int(quantity) if quantity else 0
            }
            for sandwich, count, quantity in result
        ]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/complaints")
def get_complaints(
    min_rating: int = Query(2, description="Maximum rating to consider as complaint (default: 2)"),
    db: Session = Depends(get_db)
):
    """Get dishes with low ratings (complaints)"""
    try:
        from ..controllers import reviews as review_controller
        result = review_controller.get_complaints(db, min_rating=min_rating)
        
        return [
            {
                "sandwich_id": sandwich.id,
                "sandwich_name": sandwich.sandwich_name,
                "average_rating": float(avg_rating),
                "review_count": review_count
            }
            for sandwich, avg_rating, review_count in result
        ]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/dish-ratings/{sandwich_id}")
def get_dish_ratings(
    sandwich_id: int,
    db: Session = Depends(get_db)
):
    """Get rating statistics for a specific dish"""
    try:
        sandwich = db.query(sandwich_model.Sandwich).filter(
            sandwich_model.Sandwich.id == sandwich_id
        ).first()
        
        if not sandwich:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")
        
        ratings = db.query(
            func.avg(review_model.Review.rating).label('avg_rating'),
            func.count(review_model.Review.id).label('review_count'),
            func.min(review_model.Review.rating).label('min_rating'),
            func.max(review_model.Review.rating).label('max_rating')
        ).filter(
            review_model.Review.sandwich_id == sandwich_id
        ).first()
        
        return {
            "sandwich_id": sandwich_id,
            "sandwich_name": sandwich.sandwich_name,
            "average_rating": float(ratings.avg_rating) if ratings.avg_rating else None,
            "review_count": ratings.review_count,
            "min_rating": ratings.min_rating,
            "max_rating": ratings.max_rating
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
