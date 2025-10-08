#!/usr/bin/env python
"""
Production setup script for SafeOperator Pro
Run this after deploying to Railway to populate the database
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_production():
    """Set up production database with sample data"""
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'operator_training.settings')
    django.setup()
    
    print("🚀 Setting up SafeOperator Pro production database...")
    
    try:
        # Run migrations
        print("📊 Running database migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Create demo user
        print("👤 Creating demo user...")
        execute_from_command_line(['manage.py', 'create_demo_user'])
        
        # Populate sample data
        print("📚 Populating sample safety training data...")
        execute_from_command_line(['manage.py', 'populate_sample_data'])
        
        # Collect static files
        print("📁 Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        
        print("✅ Production setup complete!")
        print("🎯 Demo credentials: demo@safeoperatorpro.com / demo123")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    setup_production()
