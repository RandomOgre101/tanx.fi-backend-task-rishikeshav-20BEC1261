import pika
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate
import json
from dotenv import load_dotenv
import os

load_dotenv()

SMTP_USER = os.environ.get("GMAIL_SMTP_EMAIL")
SMTP_PWD = os.environ.get("GMAIL_SMTP_PWD")
SMTP_PORT = os.environ.get("GMAIL_SMTP_PORT")


def send_email(body):

    to_address = body.get('to_address')
    subject = body.get('subject')
    message = body.get('message')

    smtp_host = 'smtp.gmail.com'
    smtp_port = SMTP_PORT
    smtp_user = SMTP_USER
    smtp_password = SMTP_PWD

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)

    server.sendmail(smtp_user, to_address, msg.as_string())

    server.quit()

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    
    try:
        # Decode JSON message
        decoded_body = json.loads(body.decode('utf-8'))
        
        # Extract email-related information from the task body
        to_address = decoded_body.get('to_address')
        subject = decoded_body.get('subject')
        message = decoded_body.get('message')
        attachment_path = decoded_body.get('attachment_path')

        # Send the email
        send_email(to_address, subject, message, attachment_path)
    
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    
    except Exception as e:
        print(f"Error sending email: {e}")



def enqueue_email_task(body):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='email_queue')
    channel.basic_publish(exchange='', routing_key='email_queue', body=body)

    print(" [x] Sent message to email_queue")

    connection.close()