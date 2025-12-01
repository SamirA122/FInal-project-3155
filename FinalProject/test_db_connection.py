#!/usr/bin/env python3
"""
Quick script to test MySQL database connection
"""

from api.dependencies.database import engine, get_db
from sqlalchemy import text
import sys

def test_connection():
    """Test database connection"""
    try:
        print("🔍 Testing MySQL connection...")
        print(f"   Host: localhost")
        print(f"   Database: sandwich_maker_api")
        print()
        
        # Try to connect
        with engine.connect() as connection:
            # Test query
            result = connection.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            
            if row and row[0] == 1:
                print("✅ Database connection successful!")
                
                # Get database version
                result = connection.execute(text("SELECT VERSION()"))
                version = result.fetchone()[0]
                print(f"✅ MySQL Version: {version}")
                
                # Check if database exists
                result = connection.execute(text("SELECT DATABASE()"))
                db_name = result.fetchone()[0]
                print(f"✅ Connected to database: {db_name}")
                
                return True
            else:
                print("❌ Connection test failed")
                return False
                
    except Exception as e:
        print(f"❌ Database connection failed!")
        print(f"   Error: {str(e)}")
        print()
        print("💡 Troubleshooting:")
        print("   1. Make sure MySQL is running")
        print("   2. Check credentials in api/dependencies/config.py")
        print("   3. Verify database 'sandwich_maker_api' exists")
        print("   4. Check MySQL user permissions")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)





