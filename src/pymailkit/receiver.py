"""
Email fetching functionality for PyMailkit.
"""
import imaplib
import email
import re
import string
import getpass
from typing import List
from email.header import decode_header
from dataclasses import dataclass

@dataclass
class Email:
    """Data class representing a received email."""
    subject: str
    sender: str
    body: str


class EmailReceiver:
    """A class to handle fetching emails from the Inbox operations with IMAP."""
    
    def __init__(self, host: str = "imap.gmail.com", port: int = 993):
        """
        Initialize the EmailReceiver.
        
        Args:
            host: IMAP server hostname default is imap.gmail.com
            port: IMAP server port (default: 993 for SSL)
        """
        self.host = host
        self.port = port
        self._server = None
        
    def connect(self, username:str) -> None:
        """
        Function to connect to the IMAP server, the server by default is imap.gmail.com

        Args:
            username: Email username/address
        """
        password = getpass.getpass(prompt="Enter your password : ")

        self._server = imaplib.IMAP4_SSL(self.host, self.port)
        try:
            self._server.login(username, password)
            self._server.select("inbox")
            print(f"The connection established sucessfully!!")
        except Exception as e:
            print(f"The connection failed! Check the password and username \n\n {e}")
        
    def fetch_emails(
        self,
        limit: int = 10,
    ) -> List[Email]:
        """
        Function to fetch emails from the INBOX folder of the given hostname. 

        Args:
            limit: Maximum number of emails to fetch.

        Returns:
            List of Email objects.
        """
        status, messages = self._server.search(None, "ALL")
        email_ids = messages[0].split()
        if not email_ids or not email_ids[0]:
            return []
        
        email_messages = []

        for email_id in email_ids[-limit:]:
            status, msg_data = self._server.fetch(email_id, '(RFC822)')
            if not msg_data or not msg_data[0] or not msg_data[0][1]:
                continue
            try:
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        # Parse the message into an email object
                        msg = email.message_from_bytes(response_part[1])
                        body = ''

                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8")
                        from_ = msg.get("From") or ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                if "attachment" not in content_disposition:
                                    # Get the email body
                                    if content_type == "text/plain":
                                        try:
                                            body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                                        except Exception:
                                            body = ""
                        else:
                            try:
                                body = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8')
                            except Exception:
                                body = ""
                        # Ensure body is a string
                        body = str(body)
                        # Remove tabs, newlines, carriage returns
                        body = re.sub(r'[\r\n\t]', ' ', body)
                        
                        # Remove zero-width and invisible unicode chars: ZWSP, ZWNJ, ZWJ, BOM, etc.
                        body = re.sub(r'[\u200B-\u200D\uFEFF]', '', body)
                        
                        # Remove all other non-printable/control characters except standard spaces
                        body = ''.join(ch for ch in body if ch in string.printable)
                        
                        # Normalize multiple spaces to single space
                        body = re.sub(r' +', ' ', body)
                        body = body.strip()
                        email_obj = Email(
                            subject=subject,
                            sender=from_,
                            body=body
                        )
                        email_messages.append(email_obj)
            
            except Exception:
                continue
        print("\n")
        print("Fetched emails from inbox sucessfully !!")
        return email_messages
        
    def close(self) -> None:
        """Close the IMAP connection."""
        if self._server:
            try:
                self._server.close()
            except:
                pass
            self._server.logout()
            self._server = None
            
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()