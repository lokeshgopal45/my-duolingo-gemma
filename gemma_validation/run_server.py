"""
Simple script to start the Django development server
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config')
    
    # Run migrations
    print("🔄 Running migrations...")
    execute_from_command_line(['manage.py', 'migrate', '--no-input'])
    
    # Load sample data
    print("📚 Loading sample exercises...")
    execute_from_command_line(['manage.py', 'load_sample_exercises'])
    
    # Start server
    print("\n🚀 Starting Django development server...")
    print("   API available at: http://localhost:8000/api/")
    print("   Admin panel at: http://localhost:8000/admin/")
    print("   Press Ctrl+C to stop")
    
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
