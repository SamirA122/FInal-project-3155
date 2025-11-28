# Import all models to ensure relationships are properly resolved
from . import orders, order_details, recipes, sandwiches, resources, reviews, promotional_codes, payments

from ..dependencies.database import engine, Base
from sqlalchemy.exc import OperationalError
import logging

logger = logging.getLogger(__name__)


def index():
    """Create all database tables. Handles connection errors gracefully."""
    try:
        # Import all models first to ensure relationships are resolved
        # All models are already imported at the top, but we need to ensure
        # they're all loaded before creating tables
        _ = [orders, order_details, recipes, sandwiches, resources, reviews, promotional_codes, payments]
        
        # Use Base.metadata.create_all to create all tables at once
        # This ensures all relationships are properly resolved
        Base.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except OperationalError as e:
        logger.warning(f"Could not connect to database: {e}")
        logger.warning("Server will start, but database operations will fail until connection is established")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        import traceback
        logger.error(traceback.format_exc())
