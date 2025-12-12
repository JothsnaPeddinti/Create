import smtplib
from email.message import EmailMessage
msg = EmailMessage()
msg['Subject'] = "Test Email from Python"
msg['From'] = "venkatakeerthana123@gmail.com"
msg['To'] = "jothsna97@gmail.com"
msg.set_content("Hello, this is a test email sent using Python.")
smtp_server = "smtp.gmail.com"
smtp_port = 587
username = "venkatakeerthana123@gmail.com"
password = "bvjq nzzd jyta syug"
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(username, password)
    server.send_message(msg)

print("Email sent successfully!")
