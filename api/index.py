import sys
import os

# Add the backend folder to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import create_app

app = create_app()

# For local testing (optional)
if __name__ == '__main__':
    app.run()