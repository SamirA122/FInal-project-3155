from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from ..models import order_details as order_detail_model
from ..models import sandwiches as sandwich_model
from ..models import recipes as recipe_model
from ..models import resources as resource_model
from ..models import promotional_codes as promo_model
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import uuid
from decimal import Decimal


def generate_tracking_number():
    """Generate a unique tracking number"""
    return f"TRK-{uuid.uuid4().hex[:8].upper()}"


def check_ingredient_availability(db: Session, sandwich_id: int, quantity: int):
    """Check if there are enough ingredients for a sandwich order"""
    # Get all recipes for this sandwich
    recipes = db.query(recipe_model.Recipe).filter(
        recipe_model.Recipe.sandwich_id == sandwich_id
    ).all()
    
    insufficient_resources = []
    for recipe in recipes:
        resource = db.query(resource_model.Resource).filter(
            resource_model.Resource.id == recipe.resource_id
        ).first()
        
        if not resource:
            insufficient_resources.append(f"Resource ID {recipe.resource_id} not found")
            continue
            
        required_amount = recipe.amount * quantity
        if resource.amount < required_amount:
            insufficient_resources.append(
                f"Insufficient {resource.item}: need {required_amount}, have {resource.amount}"
            )
    
    return insufficient_resources


def create(db: Session, request):
    # Validate promo code if provided
    promo_code_id = None
    discount_percent = Decimal('0.00')
    if request.promo_code:
        promo = db.query(promo_model.PromotionalCode).filter(
            promo_model.PromotionalCode.code == request.promo_code
        ).first()
        if not promo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid promotional code"
            )
        if not promo.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Promotional code is not active"
            )
        if promo.expiration_date and promo.expiration_date < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Promotional code has expired"
            )
        promo_code_id = promo.id
        discount_percent = promo.discount_percent
    
    # Check ingredient availability for all sandwiches in order
    total_price = Decimal('0.00')
    all_insufficient = []
    
    for order_detail in request.order_details:
        sandwich_id = order_detail.sandwich_id if hasattr(order_detail, 'sandwich_id') else order_detail['sandwich_id']
        amount = order_detail.amount if hasattr(order_detail, 'amount') else order_detail['amount']
        
        sandwich = db.query(sandwich_model.Sandwich).filter(
            sandwich_model.Sandwich.id == sandwich_id
        ).first()
        
        if not sandwich:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sandwich ID {sandwich_id} not found"
            )
        
        if not sandwich.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Sandwich '{sandwich.sandwich_name}' is not available"
            )
        
        # Check ingredients
        insufficient = check_ingredient_availability(
            db, sandwich_id, amount
        )
        if insufficient:
            all_insufficient.extend(insufficient)
        
        # Calculate price
        item_total = Decimal(str(sandwich.price)) * Decimal(str(amount))
        total_price += item_total
    
    # If insufficient ingredients, raise error
    if all_insufficient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient ingredients: " + "; ".join(all_insufficient)
        )
    
    # Apply discount
    if discount_percent > 0:
        discount_amount = total_price * (discount_percent / Decimal('100.00'))
        total_price = total_price - discount_amount
    
    # Create order
    tracking_number = generate_tracking_number()
    order_type_enum = model.OrderType(request.order_type) if request.order_type else model.OrderType.TAKEOUT
    new_item = model.Order(
        customer_name=request.customer_name,
        description=request.description,
        order_type=order_type_enum,
        tracking_number=tracking_number,
        total_price=total_price,
        promo_code_id=promo_code_id
    )

    try:
        db.add(new_item)
        db.flush()  # Get the order ID
        
        # Create order details and deduct resources
        for order_detail in request.order_details:
            sandwich_id = order_detail.sandwich_id if hasattr(order_detail, 'sandwich_id') else order_detail['sandwich_id']
            amount = order_detail.amount if hasattr(order_detail, 'amount') else order_detail['amount']
            
            # Create order detail
            od = order_detail_model.OrderDetail(
                order_id=new_item.id,
                sandwich_id=sandwich_id,
                amount=amount
            )
            db.add(od)
            
            # Deduct resources
            recipes = db.query(recipe_model.Recipe).filter(
                recipe_model.Recipe.sandwich_id == sandwich_id
            ).all()
            
            for recipe in recipes:
                resource = db.query(resource_model.Resource).filter(
                    resource_model.Resource.id == recipe.resource_id
                ).first()
                resource.amount -= recipe.amount * amount
        
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session, start_date: datetime = None, end_date: datetime = None):
    try:
        query = db.query(model.Order)
        if start_date:
            query = query.filter(model.Order.order_date >= start_date)
        if end_date:
            query = query.filter(model.Order.order_date <= end_date)
        result = query.order_by(model.Order.order_date.desc()).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_by_tracking(db: Session, tracking_number: str):
    """Get order by tracking number"""
    try:
        item = db.query(model.Order).filter(
            model.Order.tracking_number == tracking_number
        ).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tracking number not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        # Handle enum fields
        if 'order_type' in update_data:
            update_data['order_type'] = model.OrderType(update_data['order_type'])
        if 'order_status' in update_data:
            update_data['order_status'] = model.OrderStatus(update_data['order_status'])
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
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
