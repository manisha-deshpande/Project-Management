# ProjectManagementREADME.md
This repository contains a Flask application that allows users to manage and create new projects. It has a basic login and authentication system, and it uses TOTP (Time-based One-Time Password) authentication, which requires users to use an authentication app such as Google Authenticator to generate a code for each login.

Getting Started
<br>
1. Unzip the repository and navigate to the project directory
<br>
2. Install the required packages: <br>
    pip install -r requirements.txt
<br>
3. Install the Google Authenticator app on your phone.
<br>
4. Run the application: <br>
    python app.py <br>
    or the run button for the app.py in IntelliJ Idea
<br>
5. Access the application at http://localhost:5000
<br>

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




Usage
Authentication
The application uses TOTP authentication. When a user enters their credentials and submits the login form, a QR code is generated and displayed on the page. The user must scan the QR code with an authentication app such as Google Authenticator to get a code, which they then enter on the authentication page. If the code is valid, the user is logged in and redirected to the projects page.

App.py:
The app.py file contains the main logic for the project management application. It uses the Flask framework to handle routing and rendering of templates. The app has several functionalities including user authentication, user profile management, project creation and management, and team member management.

The app stores data in JSON files for projects, credentials, and user data. The script includes functions for loading and saving user data from/to a JSON file. There are also routes for login, authentication, registration, viewing and editing user profiles.

The app allows users to view a list of projects and create new projects. Project details include the project name, manager, team members, and details. Users can also view projects by team member.

here is a detailed overview of the usage of each route in the app.py file:

/profile: This route displays the user’s profile page. It retrieves the user’s data from the user_data.json file and displays their full name, birthday, join date, gender and experience level. The route uses the load_user_data() function to load user data from the JSON file. The route then retrieves the current user’s username from the session and uses it to retrieve the user’s data from the loaded user data. The route then passes the user’s data to the profile.html template for rendering.

/login: This route handles user login. It accepts both GET and POST requests. If the request is a GET request, it renders the login template. If the request is a POST request, it reads the username and password from the request form and verifies them against the credentials stored in the credentials.json file. If the credentials are valid, a QR code is generated for two-factor authentication using pyotp and qrcode libraries. The QR code is then displayed on the page by passing it to the authenticate.html template.

/authenticate: This route handles two-factor authentication. It accepts both GET and POST requests. If the request is a GET request, it renders the authentication template. If the request is a POST request, it reads the authentication code from the request form and verifies it using pyotp library. If the code is valid, a session variable is set to indicate that the user is authenticated and they are redirected to either admin_ui(), manager_ui() or member_ui() depending on their role.

/: This route redirects to the login page if the user is not authenticated or to the projects page if they are.

/register: This route handles user registration. It accepts both GET and POST requests. If the request is a GET request, it renders the registration template. If the request is a POST request, it reads email and password from request form and saves them to credentials.json file using json.dump(). It also adds new user to user_data.json file with default values for full name, birthday, join date, gender and experience level.

/projects: This route displays a list of all projects. It retrieves project data from projects.json file using json.load() and converts dictionary to list of projects which is passed to projects.html template for rendering.

/projects/new: This route handles project creation. It accepts both GET and POST requests. If the request is a GET request, it renders new project template with list of managers and team members which are retrieved from user_data.json file using load_user_data() function. If request method is POST, it reads project data from request form and generates new project id by incrementing maximum id in projects_data by 1. New project data is then added to projects_data dictionary with new_project_id as key and saved to projects.json file using json.dump().

/projects/details/<project_id>: This route displays details for a specific project. It retrieves project data from projects.json file using json.load() and checks if project_id exists in projects_data dictionary. If it does then project data for that id is passed to project_details.html template for rendering otherwise ‘Project not found’ message is displayed.

/members: This route displays projects by team member. It accepts both GET and POST requests. If request method is GET then all team members are retrieved from user_data.json file using load_user_data() function and passed to members.html template for rendering. If request method is POST then member_name is read from request form and all projects where member_name is part of team are retrieved from projects.json file using json.load(). These projects are then passed to member_projects.html template for rendering.

/edit-profile: This route handles editing of user profiles. It accepts both GET and POST requests. If request method is GET then current user’s profile data such as full name, birthday, gender and experience level are retrieved from session variable ‘username’ using load_user_data() function and passed to edit_profile.html template for rendering with pre-filled values in form fields. If request method is POST then updated values for full name, birthday, gender and experience level are read from request form and saved to user_data.json file using save_user_data() function.

/users/<user_id>: This route handles editing of user permissions. It accepts both GET and POST requests. If request method is GET then user data for user_id is retrieved from user_data.json file using load_user_data() function and passed to admin_permissions.html template for rendering with pre-filled values in form fields. If request method is POST then updated value for role is read from request form and saved to user_data.json file using save_user_data() function.

/users: This route displays a list of all users. It retrieves user data from user_data.json file using json.load() and converts dictionary to list of users which is passed to admin_users.html template for rendering.

/effort_log: This route handles logging of effort by team members. It accepts both GET and POST requests. If request method is GET then user data and projects data are retrieved from user_data.json and projects.json files respectively using json.load(). List of projects where current user is part of team is then passed to effortlogger.html template for rendering. If request method is POST then effort log data such as project_id, date, hours and description are read from request form and added to user_effort.json file using json.dump().

/effort_logged/<username>: This route displays effort log for a specific user. It retrieves effort log data from user_effort.json file using json.load() and filters it to include only entries for specified username. These entries are then sorted by date in descending order and passed to user_effort_log.html template for rendering.
The script includes comments indicating the author of each function or route. The app uses pyotp and qrcode libraries to handle two-factor authentication.


File Structure:
.idea: This directory contains configuration files for the IntelliJ IDEA development environment.
Backend: This directory contains backend code for the application.
data: This directory contains JSON files for storing data such as projects and user credentials.
frontend: This directory contains frontend code for the application.
static: This directory contains static files such as CSS and JavaScript files.
templates: This directory contains HTML templates for the application.
.gitignore: This file specifies which files and directories should be ignored by Git.
README.md: This file provides an overview of the project and instructions for getting started.
app.py: This file contains the main logic for the project management application.
logo.png: This file is an image of the project logo.
requirements: This file lists the required packages for the application.

Projects
The projects page displays a list of all projects. Users can create new projects by clicking the "New Project" button and filling out the form. Projects are stored in a JSON file located in the data directory.



Author: Manisha Malhar Rao Deshpande, Prateek Mohan, Zahra Falah
