from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize Flask app
app = Flask(__name__)

# Path to the SQLite database
DATABASE = 'database.db'

# Function to get a connection to the database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Function to create the database table (if it doesn't exist)
def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS contact_form (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        message TEXT NOT NULL
                    )''')
        db.commit()

# Function to send an email
def send_email(name, email, message):
    try:
        sender_email = "expresssrs01@gmail.com"  # Your email address
        sender_password = "prateek123"  # Your email password
        recipient_email = "prateek09bits@gmail.com"  # The email to receive the messages

        # Create email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"New Contact Form Submission from {name}"

        # Email body
        body = f"""
        You have a new message from your contact form:

        Name: {name}
        Email: {email}
        Message: {message}
        """

        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

    except Exception as e:
        print(f"Failed to send email: {e}")

# Route to render the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the form submission
@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Get form data
    name = request.form['name']
    email = request.form['_replyto']
    message = request.form['message']

    # Check for existing entry with the same name and email
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM contact_form WHERE name = ? AND email = ?''', (name, email))
    existing_entry = cursor.fetchone()

    if not existing_entry:  # Insert data only if it's not already present
        conn.execute('''INSERT INTO contact_form (name, email, message) 
                        VALUES (?, ?, ?)''', (name, email, message))
        conn.commit()

    # Send email notification
    send_email(name, email, message)

    # Redirect to the home page with popup flag
    return redirect(url_for('index', popup=True))
if __name__ == '__main__':
    # Initialize database (create tables if they don't exist)
    init_db()
    
    # Run the Flask app
    app.run(debug=True)
