# ase-backend
This is a shared code repository for Group 3's Applied Software Engineering (ASE) project

[For instructors & testers - how to run our program]

# For Phase-Three of project
# Setting up dependencies for Codio (if you're testing on any of own existing Codio environments that are already set up and working, you can skip this step and move to Starting our application step)
1. pip3.11 install flask
2. pip3.11 install pipenv
3. pip3.11 install --upgrade urllib3
4. pip3.11 install --upgrade urllib3 chardet
5. pip3.11 install requests==2.26.0
6. pip3.11 install geopy
7. pip3.11 install folium
8. pip3.11 install numpy --upgrade
9. pip3.11 install --upgrade requests

# Initializing the Database
10. flask --app flaskr init-db
    
# How to run Unit Testing for our application
11. python3.11 -m pytest tests

# Re-Initializing the Database to clear test data
12. flask --app flaskr init-db

# Starting our application
13. Go to root folder directory --> cd ase-backend
14. flask --app flaskr init-db
15. flask --app flaskr run --debug --host=0.0.0.0 --port=8080
