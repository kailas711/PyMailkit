import pytest
from unittest.mock import patch, MagicMock
from pymailkit.receiver import EmailReceiver

@pytest.fixture
def mock_imap():
    with patch("imaplib.IMAP4_SSL") as mock_imap_class:
        mock_server = MagicMock()
        mock_imap_class.return_value = mock_server
        yield mock_server

def test_connect_sets_server(mock_imap):
    receiver = EmailReceiver("imap.example.com")
    receiver.connect("user")
    mock_imap.login.assert_called_with("user", "pass")
    mock_imap.select.assert_called_with("inbox")
    assert receiver._server is mock_imap

def test_fetch_emails_returns_empty_when_no_emails(mock_imap):
    receiver = EmailReceiver("imap.example.com")
    receiver._server = mock_imap
    mock_imap.search.return_value = ("OK", [b""])
    emails = receiver.fetch_emails()
    assert emails == []

def test_fetch_emails_parses_email(mock_imap):
    receiver = EmailReceiver("imap.example.com")
    receiver._server = mock_imap
    mock_imap.search.return_value = ("OK", [b"1"])
    from email.message import EmailMessage
    msg = EmailMessage()
    msg["Subject"] = "Test"
    msg["From"] = "sender@example.com"
    msg.set_content("Hello World")
    raw_bytes = msg.as_bytes()
    mock_imap.fetch.return_value = ("OK", [(b"1", raw_bytes)])
    emails = receiver.fetch_emails()
    assert len(emails) == 1
    assert emails[0].subject == "Test"
    assert emails[0].sender == "sender@example.com"
    assert "Hello World" in emails[0].body

def test_close_calls_logout_and_close(mock_imap):
    receiver = EmailReceiver("imap.example.com")
    receiver._server = mock_imap
    receiver.close()
    mock_imap.close.assert_called()
    mock_imap.logout.assert_called()
    assert receiver._server is None
