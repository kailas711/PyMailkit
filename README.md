# PyMailkit

PyMailkit is a lightweight Python library designed to simplify sending and receiving emails. It provides an easy-to-use interface for interacting with email servers, making it ideal for automation, notifications, and email-based workflows.

[![PyPI Downloads](https://static.pepy.tech/badge/pymailkit)](https://pepy.tech/projects/pymailkit)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)


## Project Structure

- Send emails with attachments and custom headers
- Fetch and filter emails from your inbox
- Simple authentication using app passwords
- Minimal dependencies and easy setup

```
PyMailkit/
├── LICENSE
├── pyproject.toml
├── README.md
├── setup.py
└── src/
    └── pymailkit/
        ├── __init__.py
        ├── auth.py
        ├── receiver.py
        ├── sender.py
        └── tests/
            ├── test_receiver.py
            └── test_sender.py
```


## Installation

Install PyMailkit with pip:

```bash
pip install PyMailkit
```

## Modules

### 1. Sender Module (`pymailkit.sender`)

The sender module allows you to send emails easily, including support for attachments and custom subjects/bodies.

**Key Features:**
- Send plain text or HTML emails
- Add attachments
- Specify sender, recipients, subject, and body

**Example:**

```python
from pymailkit.sender import EmailSender

# Initialize the email sender
mail_server = EmailSender()

# Connect to your email account (prompts for app password)
mail_server.connect(username="example@gmail.com")

# Email details
from_add = "fromsomeone@gmail.com"
to_add = "tosomeone@gmail.com"
sub = "Sample Subject"
body = "Sample body for email sending example"

# Send the email
mail_server.send_email(
    to_addresses=to_add,
    from_address=from_add,
    subject=sub,
    body=body,
    attachments = "/content/sample_data/mnist_test.csv" # Provide absolute path
)

# Close the connection to the server
mail_server.close()
```


### 2. Receiver Module (`pymailkit.receiver`)

The receiver module lets you fetch emails from your inbox, with options to limit the number of emails and filter by criteria.

**Key Features:**
- Fetch emails from inbox
- Limit number of emails retrieved
- Access email metadata (subject, sender, date, body)

**Example:**

```python
from pymailkit.receiver import EmailReceiver

# Initialize the email receiver
mail_server = EmailReceiver()

# Connect to your email account (prompts for app password)
mail_server.connect(username="example@gmail.com")

# Fetch the latest 3 emails
emails = mail_server.fetch_emails(limit=3)

# Print subjects of fetched emails
for email in emails:
    print(email['subject'])

# Close the connection to the server
mail_server.close()
```


## Authors
- [@kailas711](https://github.com/kailas711)