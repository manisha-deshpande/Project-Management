from flask import Flask, jsonify, request, render_template, redirect, url_for, session
import os
import json
import pyotp
import qrcode
import io
import base64
import datetime

# Initialize Flask app
app = Flask(__name__)



# Set up the path to the projects.json file
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
PROJECTS_FILE = os.path.join(data_dir, 'projects.json')
CREDENTIALS_FILE = os.path.join(data_dir, 'credentials.json')
# Define a global variable to store user data
USER_DATA_FILE = os.path.join(data_dir,'user_data.json')

try:
    with open("secret_key.txt", "r") as f:
        secret = f.read().strip()
# If the file doesn't exist, generate a new secret key and save it to the file
except FileNotFoundError:
    secret = pyotp.random_base32()
    with open("secret_key.txt", "w") as f:
        f.write(secret)

totp = pyotp.TOTP(secret)


# Define a function to load user data from a JSON file
def load_user_data():
    with open(USER_DATA_FILE, 'r') as f:
        user_data = json.load(f)
    return user_data

# Define a function to save user data to a JSON file
def save_user_data(user_data):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(user_data, f)

# Define a route for the user profile page
@app.route('/profile')
def profile():
    # Load the user data from the JSON file
    user_data = load_user_data()

    # Get the current user's username from the session
    username = session['username']
    user = user_data[username]


    # Get the user's full name
    full_name = user_data[username]['full_name']

    # Get the user's birthday
    birthday = user_data[username]['birthday']

    # Get the user's join date
    join_date = user_data[username]['join_date']

    # Render the user profile template with the user data
    return render_template('profile.html', username=username, full_name=full_name, birthday=birthday, join_date=join_date)











# Define routes for login and authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Read the login data from the request form
        username = request.form['username']
        password = request.form['password']

        # Verify the login credentials
        with open(CREDENTIALS_FILE, 'r') as f:
            credentials_data = json.load(f)
        if username in credentials_data and credentials_data[username] == password:
            print("WE ARE IN/n/n/n/n")
            session['authenticated'] = True
            session['username'] = username
            provisioning_uri = totp.provisioning_uri(username, issuer_name="MyApp")
            qr = qrcode.QRCode(version=None, box_size=10, border=4)
            qr.add_data(provisioning_uri)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # Convert the image to a base64 encoded string
            buffered = io.BytesIO()
            img.save("static/1.png")
            img_str = base64.b64encode(buffered.getvalue()).decode("ascii")

            return render_template('authenticate.html', qr_code=img_str, username=username)

        else:
            return render_template('login.html', error=True)
    else:
        return render_template('login.html', error=False)

@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    if request.method == 'POST':
        # Read the authentication data from the request form

        code = request.form['code']

        # Verify the authentication code
        if totp.verify(code):
            # Set a session variable to indicate that the user is authenticated
            session['authenticated'] = True

            # Redirect to the projects page
            return redirect(url_for('new_project'))
        else:
            return render_template('authenticate.html', error=True)
    else:
        return render_template('authenticate.html', error=False)

# Define routes for getting and creating projects
@app.route('/')
def index():
    if 'authenticated' not in session or not session['authenticated']:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Read the registration data from the request form
        email = request.form['email']
        password = request.form['password']

        # Update the credentials JSON with the new user's email and password
        with open(CREDENTIALS_FILE, 'r+') as f:
            credentials_data = json.load(f)
            credentials_data[email] = password
            f.seek(0)
            json.dump(credentials_data, f)
            f.truncate()

        # Redirect to the login page
        return redirect(url_for('login'))
    else:
        return render_template('register.html')



@app.route('/projects')
def get_projects():
    # Check if the user is authenticated
    ##    return redirect(url_for('login'))
    # Read the project data from the projects.json file
    if 'authenticated' not in session or not session['authenticated']:
        return redirect(url_for('login'))
    with open(PROJECTS_FILE, 'r') as f:
        projects_data = json.load(f)
    # Convert the dictionary to a list of projects and pass to the template
    projects = [{'id': id, 'project': projects_data[id]} for id in projects_data]
    return render_template('projects.html', projects=projects)



@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    if 'authenticated' not in session or not session['authenticated']:
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Read the project data from the request form
        new_project = {
            'name': request.form['name'],
            'manager': request.form['manager'],
            'team': request.form['team'].split(','),
            'details':request.form['details']
        }
        # Generate a new project ID
        with open(PROJECTS_FILE, 'r') as f:
            projects_data = json.load(f)
        new_project_id = str(max([int(id) for id in projects_data.keys()]) + 1)
        # Write the new project data to the projects.json file
        with open(PROJECTS_FILE, 'w') as f:
            projects_data[new_project_id] = new_project
            json.dump(projects_data, f)
        # Redirect to the list of projects
        return get_projects()
    else:
        # Read the existing projects data from the projects.json file
        with open(PROJECTS_FILE, 'r') as f:
            projects_data = json.load(f)
        # Convert the dictionary to a list of projects and pass to the template
        projects = [projects_data[id] for id in projects_data]
        return render_template('new_project.html', projects=projects)

@app.route('/projects/details/<project_id>')
def get_project_details(project_id):
    if 'authenticated' not in session or not session['authenticated']:
        return redirect(url_for('login'))
    # Read the project data from the projects.json file
    with open(PROJECTS_FILE, 'r') as f:
        projects_data = json.load(f)
    # Check if the project ID exists in the projects data
    if project_id in projects_data:
        project = projects_data[project_id]
        return render_template('project_details.html', project=project)
    else:
        return 'Project not found'





@app.route('/members', methods=['GET', 'POST'])
def get_member_projects():
    if 'authenticated' not in session or not session['authenticated']:
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Get the member name from the form data
        member_name = request.form['member_name']
        # Read the project data from the projects.json file
        with open(PROJECTS_FILE, 'r') as f:
            projects_data = json.load(f)
        # Find all projects where the member is a part of the team
        member_projects = []
        for project_id, project_data in projects_data.items():
            if member_name in project_data['team']:
                member_projects.append(project_data)
        return render_template('member_projects.html', member_name=member_name, projects=member_projects)
    else:
        # Read the existing projects data from the projects.json file
        with open(PROJECTS_FILE, 'r') as f:
            projects_data = json.load(f)
        # Get all team members
        team_members = set()
        for project_id, project_data in projects_data.items():
            for member in project_data['team']:
                team_members.add(member)
        return render_template('members.html', team_members=team_members)

# Run the Flask application
if __name__ == '__main__':
    app.secret_key =  '8yS#Jw7?_ZPQ:dYq~+e^2fcH!L@KbTn'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
