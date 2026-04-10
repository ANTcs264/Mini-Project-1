import sys
import os

# Add the backend folder to Python's module search path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Now import the Flask app factory
from app import create_app

app = create_app()

# Optional: for local testing with `python api/index.py`
if __name__ == '__main__':
    app.run()