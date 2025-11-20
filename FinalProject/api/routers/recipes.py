from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..controllers import recipes as controller
from ..schemas import recipes as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Recipes'],
    prefix="/recipes"
)


@router.post("/", response_model=schema.Recipe)
def create(request: schema.RecipeCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Recipe])
def read_all(
    sandwich_id: int = Query(None, description="Filter by sandwich ID"),
    resource_id: int = Query(None, description="Filter by resource ID"),
    db: Session = Depends(get_db)
):
    return controller.read_all(db, sandwich_id=sandwich_id, resource_id=resource_id)


@router.get("/{item_id}", response_model=schema.Recipe)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Recipe)
def update(item_id: int, request: schema.RecipeUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
