from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..controllers import promotional_codes as controller
from ..schemas import promotional_codes as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Promotional Codes'],
    prefix="/promotional-codes"
)


@router.post("/", response_model=schema.PromotionalCode)
def create(request: schema.PromotionalCodeCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.PromotionalCode])
def read_all(
    is_active: bool = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    return controller.read_all(db, is_active=is_active)


@router.get("/{item_id}", response_model=schema.PromotionalCode)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.get("/code/{code}", response_model=schema.PromotionalCode)
def read_by_code(code: str, db: Session = Depends(get_db)):
    result = controller.read_by_code(db, code=code)
    if not result:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotional code not found or expired")
    return result


@router.put("/{item_id}", response_model=schema.PromotionalCode)
def update(item_id: int, request: schema.PromotionalCodeUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
