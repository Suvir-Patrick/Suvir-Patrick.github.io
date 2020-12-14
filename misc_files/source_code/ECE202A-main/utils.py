import math


import smtplib
import ssl
import mail_config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText




def send_alert2():
    port = 465

    sender = mail_config.sender
    password = mail_config.pw

    receive = mail_config.receive

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Request to enter home"
    msg['From'] = sender
    msg['To'] = receive

    # Create the body of the message
    html = """\
    <html>
      <head></head>
      <body>
        <p>Hi!<br>
           Someone has requested the front door entrance for your house should be unlocked<br>
           Here is the link to your ARENA: https://arena.andrew.cmu.edu/?scene=patrick_scene. Click the button near the door to unlock it<br>
           <br>
           Best,<br>
           - Your ARENA Home Automation System
        </p>
      </body>
    </html>
    """
    msg.attach(MIMEText(html, 'html'))

    context = ssl.create_default_context()
    print("Sending Alert")
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context = context) as server:
        server.login(sender, password)
        server.sendmail(sender, receive, msg.as_string())
        server.quit()