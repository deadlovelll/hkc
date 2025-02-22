#!/bin/bash

# First operation: Run Django tests
cd /Users/timofeyivankov/Desktop/hkc/house_zhkh_core || { echo "Failed to cd into the Django tests directory"; exit 1; }
echo "Running Django tests..."
python manage.py test base || { echo "Django tests failed"; exit 1; }

# Second operation: Run Unittest tests
cd /Users/timofeyivankov/Desktop/hkc/house_zhkh_ms/tests || { echo "Failed to cd into the Unittest tests directory"; exit 1; }
echo "Running Unittest tests..."
python -m unittest discover || { echo "Unittest tests failed"; exit 1; }

echo "All tests completed successfully"
