from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
from db import dbtool
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

# Configure Flask-Session to use server-side sessions (file-based in this example)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_KEY_PREFIX"] = "casino_"  # Prefix for session keys (optional)

# Initialize Flask-Session
Session(app)

@app.route('/')
def index():
    # Check if the user is logged in (you can use your own logic here)
    username = session.get('username') is not None
    print(session.get('username'))
    # Access user-specific data from the session (if available)
    user_balance = session.get('balance', 0)
    
    return render_template('index.html', user_balance=user_balance, username=username)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get user input from the form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        try:
            if dbtool.user_exists(username):
                error_message = "The username is already taken"
                return render_template('register/index.html', error_message=error_message)
            else: 
                dbtool.add_user(username, email, password, 0, 0)
                # Redirect to the login page after successful registration
                return redirect(url_for('login'))

        except Exception as e:
            # Handle any other exceptions gracefully
            error_message = "An error occurred during registration."
            return render_template('register/index.html', error_message=error_message)

    return render_template("register/index.html")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get user input from the form
        username = request.form['username']
        password = request.form['password']

        try:
            if dbtool.user_exists(username):
                if dbtool.check_password(username, password):
                    # Store user-specific data in the session (e.g., balance)
                    session['balance'] = dbtool.get_balance(username)
                    session['username'] = username
                    # Redirect to the main page after successful login
                    return redirect(url_for('index'))
                else:
                    error_message = "Wrong password! Try again!"
                    return render_template('login/index.html', error_message=error_message)
            else: 
                error_message = "Wrong login! Check spelling or create a new account!"
                return render_template('login/index.html', error_message=error_message)

        except Exception as e:
            # Handle any other exceptions gracefully
            error_message = str(e)
            return render_template('login/index.html', error_message=error_message)

    return render_template("login/index.html")

if __name__ == '__main__':
    app.run(debug=True)
