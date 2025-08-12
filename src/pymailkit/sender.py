"""
Email sending functionality for PyMailkit.
"""
import getpass
import smtplib, ssl
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from typing import List, Optional, Union
from pathlib import Path

class EmailSender:
    """A class to handle email sending operations with SMTP."""
    
    def __init__(self, host: str = "smtp.gmail.com", port = 587):
        """
        Initialize the EmailSender.
        
        Args:
            host: SMTP server hostname by default smtp.gmail.com will be selected.
            port: SMTP server port (default: 587 for TLS) 
        """
        self.host = host
        self.port = port
        self.context = ssl.create_default_context()
        self._server = None
        
    def connect(self, username: str) -> None:
        """
        Function to connect to the SMTP server for sending emails, by defualt smtp.gmail.com is used.
        
        Args:
            username: Email username/address
        """
        password = getpass.getpass(prompt="Enter your password : ")
        self._server = smtplib.SMTP(self.host, self.port)

        try: 
            self._server.starttls(context=self.context)
            self._server.login(username, password)
            print(f"The connection established sucessfully!!")
        except Exception as e:
            print(f"The connection failed! Check the password and username \n\n {e}")
        
    def send_email(
        self,
        from_address: str,
        to_addresses: Union[str, List[str]],
        subject: str,
        body: str,
        attachments: Optional[Union[str, Path]] = None,
        cc: Optional[Union[str, List[str]]] = None,
    ) -> None:
        """
        Function to Send an email.
        
        Args:
            to_addresses: Single email address or list of addresses
            subject: Email subject
            body: Email body content
            attachments: Optional file path or list of file paths to attach
            cc: Optional CC recipients
        """
        if isinstance(to_addresses, str):
            to_addresses = [to_addresses]
            
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg["From"] = from_address
        msg['To'] = ', '.join(to_addresses)
        
        if cc:
            if isinstance(cc, str):
                cc = [cc]
            msg['Cc'] = ', '.join(cc)
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Handle attachments as list or single file
        if attachments:
            if isinstance(attachments, (str, Path)):
                with open(attachments, "rb") as file:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(file.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {Path(attachments).name}")
                    msg.attach(part)

        msg = msg.as_string()  
        recipients = to_addresses
        if cc:
            recipients.extend(cc)
            
        self._server.sendmail(from_address,recipients,msg)

        print("\n")
        print(f"Email send to {to_addresses} sucessfully !!")
        
    def close(self) -> None:
        """Close the SMTP connection."""
        if self._server:
            self._server.quit()
            self._server = None
            
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
