import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_confirmation_email(email: str):
    sender_email = "druk3s.official@gmail.com"  # Replace with your email address
    sender_name = "FastAPI"
    subject = "Registration Successful"
    body = f"Dear user,\n\nThank you for registering.\n\nBest regards,\n{
        sender_name}"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        # Replace with your SMTP server details
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            # Replace with your email password
            server.login("fyponline2024@gmail.com", "acig njis raie japt")
            server.sendmail(sender_email, email, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")
