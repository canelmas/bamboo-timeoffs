import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SMTPConfig:

    def __init__(self, host, mail_from, port=0) -> None:
        self.host = host
        self.port = port
        self.mail_from = mail_from


class EmailUtil:

    @staticmethod
    def send(data, smtp_config: SMTPConfig):
        # print("subject={}\nfrom={}\nto={}\ncontent={}\n".format(data[0], smtp_config.mail_from, data[1], data[2]))
        msg = MIMEMultipart('alternative')
        msg['Subject'] = data[0]
        msg['To'] = ', '.join(data[1])
        msg['From'] = smtp_config.mail_from

        msg.attach(MIMEText(data[2], 'html'))

        s = smtplib.SMTP(host=smtp_config.host, port=smtp_config.port)
        s.sendmail(smtp_config.mail_from, data[1], msg.as_string())
        s.quit()
