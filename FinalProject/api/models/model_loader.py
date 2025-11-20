from . import orders, order_details, recipes, sandwiches, resources, reviews, promotional_codes, payments

from ..dependencies.database import engine
from sqlalchemy.exc import OperationalError
import logging

logger = logging.getLogger(__name__)


def index():
    """Create all database tables. Handles connection errors gracefully."""
    try:
        orders.Base.metadata.create_all(engine)
        order_details.Base.metadata.create_all(engine)
        recipes.Base.metadata.create_all(engine)
        sandwiches.Base.metadata.create_all(engine)
        resources.Base.metadata.create_all(engine)
        reviews.Base.metadata.create_all(engine)
        promotional_codes.Base.metadata.create_all(engine)
        payments.Base.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except OperationalError as e:
        logger.warning(f"Could not connect to database: {e}")
        logger.warning("Server will start, but database operations will fail until connection is established")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
