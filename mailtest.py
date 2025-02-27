import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_email():
    try:
        # Email account credentials
        sender_email = "expresssrs01@gmail.com"  # Replace with your email address
        sender_password = "prateek123"  # Replace with your email password
        recipient_email = "prateek09bits@gmail.com"  # Replace with the recipient email address

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "Test Email from Python Script"

        # Email body
        body = "This is a simple test email sent from a Python script."
        msg.attach(MIMEText(body, 'plain'))

        # Send the email using SMTP
        with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Use Gmail's SMTP server
            server.starttls()  # Upgrade the connection to secure
            server.login(sender_email, sender_password)  # Login to the email account
            server.sendmail(sender_email, recipient_email, msg.as_string())  # Send the email
        
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

# Run the test email function
if __name__ == "__main__":
    test_email()
