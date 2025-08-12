"""
PyMailkit - A modern Python library for sending and receiving emails.
"""
from .sender import EmailSender
from .receiver import EmailReceiver
from .auth import authenticate

__version__ = "2.0.0"
__author__ = "Kailas P S"
__email__ = "kailaspsudheer@gmail.com"

__all__ = ['EmailSender', 'EmailReceiver', 'authenticate']