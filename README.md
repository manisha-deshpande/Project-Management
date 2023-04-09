# ProjectManagementREADME.md
This repository contains a Flask application that allows users to manage and create new projects. It has a basic login and authentication system, and it uses TOTP (Time-based One-Time Password) authentication, which requires users to use an authentication app such as Google Authenticator to generate a code for each login.

Getting Started
Unzip the repository and navigate to the project directory

Install the required packages
    pip install -r requirements.txt
Run the application
    python app.py

Access the application at http://localhost:5000




Usage:
Authentication
The application uses TOTP authentication. When a user enters their credentials and submits the login form, a QR code is generated and displayed on the page. The user must scan the QR code with an authentication app such as Google Authenticator to get a code, which they then enter on the authentication page. If the code is valid, the user is logged in and redirected to the projects page.

Login
By default the users are: (username/password (role))
admin@admin.com/admin (admin)
manager@manager.com/manager (manager)
mdeshp10@asu.edu/mdeshp10 (member)
pmohan9@asu.edu/pmohan9 (member)
zfalah@asu.edu/zfalah (member)

Registration
A new user can register with an email and password. By default, the 'member' role is assigned.

Projects
The projects page displays a list of all projects. Users can create new projects by clicking the "New Project" button and filling out the form. Projects are stored in a JSON file located in the data directory.

Different views for different roles
The manager and admin roles can create new projects.
The admin can change other users' permissions.


License
This project is licensed under the MIT License. See LICENSE for more information.
