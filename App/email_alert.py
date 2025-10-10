import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

my_email = os.getenv("MY_EMAIL")
password = os.getenv("EMAIL_PASSWORD")
to_email = os.getenv("TO_EMAIL")

def send_email(number_of_errors):
    subject = "Critical Errors detected for app "
    body = f"Average Error rate's value {number_of_errors} was greater than the threshold value of 10 in 1 hour "
    message = f"Subject:{subject}\n{body}"
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=to_email,
                            msg=message.encode("utf-8"))
