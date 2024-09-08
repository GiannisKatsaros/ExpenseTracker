import imaplib
import os
import environ
import email


class MailService:
    """Service to interact with email"""

    def __init__(self):
        env = environ.Env(DEBUG=(bool, False))
        django_env = env("DJANGO_ENV", default="development")
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        environ.Env.read_env(os.path.join(base_dir, f".env.{django_env}"))
        self.imap_server = env("EMAIL_IMAP_SERVER")
        self.imap_port = env("EMAIL_IMAP_PORT")
        self.username = env("EMAIL_USERNAME")
        self.password = env("EMAIL_PASSWORD")
        self.mail = None
        # self.piraeus = env("EMAIL_PIRAEUS")

    def login(self):
        """Login to email server"""
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(self.username, self.password)
            self.mail = mail
        except Exception as e:
            print(e)

    def get_emails_from_sender(self, search):
        """Get emails from a specific sender"""
        try:
            if not self.mail:
                self.login()
            self.mail.select("inbox")
            _, messages = self.mail.search(None, f'(FROM "{search}")')
            # messages = messages[0].split()
            return messages[0].split()
        except Exception as e:
            print(e)
            return []

    def get_email_message(self, email_id):
        """Get email message"""
        try:
            if not self.mail:
                self.login()
            _, data = self.mail.fetch(email_id, "(RFC822)")
            email_message = email.message_from_bytes(data[0][1])
            return email_message
        except Exception as e:
            print(e)
            return None

    def mark_as_deleted(self, email_id):
        """Mark email as deleted"""
        try:
            if not self.mail:
                self.login()
            self.mail.store(email_id, "+FLAGS", "\\Deleted")
            # self.mail.expunge()
            return None
        except Exception as e:
            print(e)
            return None

    def delete_marked_emails(self):
        try:
            if not self.mail:
                self.login()
            self.mail.expunge()
            return None
        except Exception as e:
            print(e)
            return None

    def logout(self):
        try:
            if self.mail:
                self.mail.logout()
            return None
        except Exception as e:
            print(e)
            return None
