"""
Authentication utilities for PyMailkit.
"""
from typing import Dict, Optional
from pymailkit.sender import EmailSender
from pymailkit.receiver import EmailReceiver


def authenticate(
    email: str,
    password: str,
    smtp_host: Optional[str] = None,
    smtp_port: int = 587,
    imap_host: Optional[str] = None,
    imap_port: int = 993
) -> Dict[str, object]:
    """
    Authenticate and create both sender and receiver instances.
    
    This function provides a convenient way to set up both sending and receiving
    email capabilities with a single authentication call.
    
    Args:
        email: Email address
        password: Email password or app-specific password
        smtp_host: Optional SMTP server host 
        smtp_port: SMTP server port (default: 587)
        imap_host: Optional IMAP server host 
        imap_port: IMAP server port (default: 993)
        
    Returns:
        Dictionary containing authenticated EmailSender and EmailReceiver instances
    """
        
    if not smtp_host or not imap_host:
        smtp_host = 'smtp.gmail.com'
        imap_host = 'imap.gmail.com'
    
    # Create and authenticate sender
    sender = EmailSender(smtp_host, smtp_port)
    sender.connect(email, password)
    
    # Create and authenticate receiver
    receiver = EmailReceiver(imap_host, imap_port)
    receiver.connect(email, password)
    
    return {
        'sender': sender,
        'receiver': receiver
    }
