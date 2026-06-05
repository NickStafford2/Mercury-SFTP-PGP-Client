# config.py

SFTP_HOST = "sftp.partner.com"
SFTP_PORT = 22
SFTP_USER = "your_sftp_user"

PRIVATE_KEY_PATH = "/secure/path/your_private_key.asc"
PUBLIC_KEY_PATH = "/secure/path/your_public_key.asc"

LOCAL_OUTBOX = "./outbox"
LOCAL_INBOX = "./inbox"

REMOTE_INBOX = "/incoming"
REMOTE_OUTBOX = "/outgoing"

PGP_RECIPIENT_KEY = "partner@example.com"
