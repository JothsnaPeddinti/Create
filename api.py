import os
import psycopg2
from fastapi import FastAPI
from email.message import EmailMessage
import smtplib

app = FastAPI()

def fetch_data_from_postgres():
    conn = psycopg2.connect(
        host="192.168.100.130",
        port="5432",
        database="postgres",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")

    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def send_email(data):
    msg = EmailMessage()
    msg['Subject'] = "PostgreSQL Data Report"
    msg['From'] = "venkatakeerthana123@gmail.com"
    msg['To'] = "jothsna97@gmail.com"
    msg.set_content("Here is the data:\n\n" + str(data))

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    username = 'venkatakeerthana123@gmail.com'
    password = 'bvvj nzdd jyta syug'   

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)

@app.get("/send-report")
def send_report():
    data = fetch_data_from_postgres()
    send_email(data)
    return {"message": "Report sent successfully", "rows": len(data)}
