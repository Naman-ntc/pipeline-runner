import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailNotifier:
    def __init__(self, smtp_host: str, smtp_port: int, sender: str) -> None:
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.sender = sender

    def validate_recipient(self, email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def build_template(self, subject: str, body: str, html: bool = False) -> MIMEMultipart:
        msg = MIMEMultipart("alternative")
        msg["From"] = self.sender
        msg["Subject"] = subject
        if html:
            msg.attach(MIMEText(body, "html"))
        else:
            msg.attach(MIMEText(body, "plain"))
        return msg

    def send(self, recipient: str, subject: str, body: str, html: bool = False) -> bool:
        if not self.validate_recipient(recipient):
            raise ValueError(f"Invalid recipient: {recipient}")
        msg = self.build_template(subject, body, html)
        msg["To"] = recipient
        conn = smtplib.SMTP(self.smtp_host, self.smtp_port)
        conn.sendmail(self.sender, [recipient], msg.as_string())
        conn.quit()
        return True
