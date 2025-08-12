import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from pymailkit.sender import EmailSender

@pytest.fixture
def mock_smtp():
    with patch("smtplib.SMTP") as mock_smtp_class:
        mock_server = MagicMock()
        mock_smtp_class.return_value = mock_server
        yield mock_server

@pytest.fixture
def sender():
    return EmailSender("smtp.example.com")

def test_sender_initialization(sender):
    """Test EmailSender initialization with default port"""
    assert sender.host == "smtp.example.com"
    assert sender.port == 587
    assert sender._server is None

def test_connect(mock_smtp, sender):
    """Test connection to SMTP server"""
    sender.connect("user@example.com")
    
    mock_smtp.starttls.assert_called_once()
    mock_smtp.login.assert_called_once_with("user@example.com","pass")
    assert sender._server is not None

def test_send_email_single_recipient(mock_smtp, sender):
    """Test sending email to a single recipient"""
    sender._server = mock_smtp
    
    sender.send_email(
        from_address="from@example.com",
        to_addresses="to@example.com",
        subject="Test Subject",
        body="Test Body"
    )
    
    mock_smtp.sendmail.assert_called_once()
    args = mock_smtp.sendmail.call_args[0]
    assert args[0] == "from@example.com"
    assert args[1] == ["to@example.com"]

def test_send_email_multiple_recipients(mock_smtp, sender):
    """Test sending email to multiple recipients"""
    sender._server = mock_smtp
    recipients = ["to1@example.com", "to2@example.com"]
    
    sender.send_email(
        from_address="from@example.com",
        to_addresses=recipients,
        subject="Test Subject",
        body="Test Body"
    )
    
    mock_smtp.sendmail.assert_called_once()
    args = mock_smtp.sendmail.call_args[0]
    assert args[0] == "from@example.com"
    assert args[1] == recipients

@pytest.fixture
def mock_attachment():
    with patch("builtins.open") as mock_open:
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        mock_file.read.return_value = b"test content"
        yield mock_open

def test_send_email_with_attachment(mock_smtp, mock_attachment, sender):
    """Test sending email with attachment"""
    sender._server = mock_smtp
    
    sender.send_email(
        from_address="from@example.com",
        to_addresses="to@example.com",
        subject="Test Subject",
        body="Test Body",
        attachments="test.txt"
    )
    
    mock_attachment.assert_called_once_with("test.txt", "rb")
    mock_smtp.sendmail.assert_called_once()

def test_close_connection(mock_smtp, sender):
    """Test closing SMTP connection"""
    sender._server = mock_smtp
    sender.close()
    
    mock_smtp.quit.assert_called_once()
    assert sender._server is None

def test_context_manager(mock_smtp):
    """Test EmailSender as context manager"""
    with EmailSender("smtp.example.com") as sender:
        assert isinstance(sender, EmailSender)
    
    # Should be closed after context
    assert sender._server is None