# run.py
import sys
import os

print("Python Path:", sys.path)
print("Current Working Directory:", os.getcwd())

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
