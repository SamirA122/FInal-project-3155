from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from sqlalchemy.orm import Session
from ..models import resources as resource_model
from ..models import recipes as recipe_model

# Create a test client for the app
client = TestClient(app)


def test_check_ingredient_availability_sufficient(mocker):
    """Test ingredient checking when resources are sufficient"""
    db = mocker.Mock(spec=Session)
    
    # Mock recipe
    mock_recipe = mocker.Mock()
    mock_recipe.resource_id = 1
    mock_recipe.amount = 2
    
    # Mock resource with sufficient amount
    mock_resource = mocker.Mock()
    mock_resource.item = "Bread"
    mock_resource.amount = 10
    
    # Mock query
    db.query.return_value.filter.return_value.all.return_value = [mock_recipe]
    db.query.return_value.filter.return_value.first.return_value = mock_resource
    
    insufficient = controller.check_ingredient_availability(db, sandwich_id=1, quantity=2)
    
    assert len(insufficient) == 0


def test_check_ingredient_availability_insufficient(mocker):
    """Test ingredient checking when resources are insufficient"""
    db = mocker.Mock(spec=Session)
    
    # Mock recipe
    mock_recipe = mocker.Mock()
    mock_recipe.resource_id = 1
    mock_recipe.amount = 5
    
    # Mock resource with insufficient amount
    mock_resource = mocker.Mock()
    mock_resource.item = "Bread"
    mock_resource.amount = 2
    
    # Mock query
    db.query.return_value.filter.return_value.all.return_value = [mock_recipe]
    db.query.return_value.filter.return_value.first.return_value = mock_resource
    
    insufficient = controller.check_ingredient_availability(db, sandwich_id=1, quantity=2)
    
    assert len(insufficient) > 0
    assert "Insufficient" in insufficient[0]
