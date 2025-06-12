#Isntall requirements
pytest
flask-testing
requests
pytest-html
pytest-cov

# Under tests folder
pytest
pytest --html=reports.html

# Shows print debug statements
pytest -s --html=reports.html

# Cov detailed html reports with backend
pytest --cov=. --cov-report=html