"""
Filename: send_gmail.py
Author: Lee Dillard
Created: 02/07/2024
Purpose: Send email using Gmail with Python
"""

# Library to manage communication with an SMTP server
import smtplib 

# Library to create and email message
from email.message import EmailMessage

# Import Gmail credentials and SMTP server settings
import gmail_credentials

def main():

    email_from = "enter_user_name_here <enter_email_address_here>"

    # A list containing one or more email addresses
    email_dst = [
        "email_address_to_send_to_here",
        #"and_here_if_needed",
        #"and_so_on"
    ]
    subject = "Subject_here"
    content = """
    Content_here
    """
# Create email message
    message = EmailMessage()
    message["From"] = email_from
    message.set_content(content)
    message["Subject"] = subject
    message["To"] = email_dst

    # Send email message
    try:
        # Use with context manager to create an smtp_server object
        with smtplib.SMTP(
            gmail_credentials.SMTP_SERVER,
            gmail_credentials.PORT
    ) as    SMTP_SERVER:
            # Show all communication with the server
            # This line can be commented out
            SMTP_SERVER.set_debuglevel(True)
            # Say enhanced hello to the server
            SMTP_SERVER.ehlo()
            # Request a TLS connection with the SMTP server
            SMTP_SERVER.starttls()
            #Login to the SMTP server
            SMTP_SERVER.login(
                gmail_credentials.LOGIN,
                gmail_credentials.APP_PASSWORD
        )
        # Ask smtp_server to send out message
            SMTP_SERVER.send_message(
                message
        )
        print()
        print(25*"**")
        print("      Email message successfully sent.")
        print(25*"**")
        print()
    except Exception as e:
        print(25*"**")
        print(f"Message not sent.")
        print(e)
        print(25*"**")


main()
