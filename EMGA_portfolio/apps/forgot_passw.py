import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


import dash
import dash_core_components as dcc
import dash_html_components as html


def send_email(players,receiver_email):
    print('OK')
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "emgatue@gmail.com"  # Enter your address
    # receiver_email = "address@gmail.com"  # Enter receiver address
    password = "emga_12345"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Restore user Password - EMGA"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = """\
    Dear {},
    Click on the following link to restore your password:
    Restore password
    https://emga.herokuapp.com/restore
    Please do not answer to this e-mail""".format(players[0][0])
    # write the HTML part
    html = """\
    <html>
      <body>
        <p>Dear {},<br>
           Click on the following link to restore your password:</p>
        <p><a href="https://emga.herokuapp.com/restore">Restore password</a></p>
        <p> Please do not answer to this e-mail</p>
      </body>
    </html>
    """.format(players[0][0])
    # convert both parts to MIMEText objects and add them to the MIMEMultipart message
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)


    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


