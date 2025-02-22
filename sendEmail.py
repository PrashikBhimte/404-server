import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from os import getenv

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = getenv("SENDER_EMAIL")
SENDER_PASSWORD = getenv("SENDER_PASSWORD")  
RECEIVER_EMAIL = "prashikbhimte29@gmail.com"

subject = "Test Email from Python"
body = "Hello, this is a test email sent using Python!"

message = MIMEMultipart()
message["From"] = SENDER_EMAIL
message["To"] = RECEIVER_EMAIL
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
    
    server.quit()
    print("✅ Email sent successfully!")

except Exception as e:
    print(f"❌ Error: {e}")
