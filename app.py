from flask import Flask, render_template, request, redirect, url_for, flash
import json
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For flashing messages

# File to store user data
DATA_FILE = 'creds.json'

# Function to load users from the JSON file
def load_users():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save users to the JSON file
def save_user(user_data):
    users = load_users()
    # Encrypt the password if needed
    user_data['password'] = user_data['password']
    users[user_data['email']] = user_data
    with open(DATA_FILE, 'w') as file:
        json.dump(users, file)

# Verify if the email is a student ID (example: checking if it ends with .edu or a specific domain)
def is_student_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.(edu|in|ac|tech)\b$', email)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if email already exists
        existing_users = load_users()
        if email in existing_users:
            flash("Email already registered!", "error")
            return redirect(url_for('signup'))

        if not is_student_email(email):
            flash("Invalid email! Please use your student email.", "error")
            return redirect(url_for('signup'))

        user_data = {
            'username': username,
            'email': email,
            'password': password
        }

        save_user(user_data)
        flash("Signup successful!", "success")
        return redirect('https://alumninetwork.tiiny.site')  # Redirect to login page after successful signup

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
