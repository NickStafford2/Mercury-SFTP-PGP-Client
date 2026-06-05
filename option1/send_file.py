# send_file.py

import os
import paramiko
import gnupg
from config import *

gpg = gnupg.GPG()

def encrypt_file(filepath):
    with open(filepath, "rb") as f:
        status = gpg.encrypt_file(
            f,
            recipients=[PGP_RECIPIENT_KEY],
            output=filepath + ".gpg"
        )

    if not status.ok:
        raise Exception(f"Encryption failed: {status.status}")

    return filepath + ".gpg"


def upload_file(local_file, remote_path):
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USER)

    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_file, remote_path)

    sftp.close()
    transport.close()


def process_outbox():
    for file in os.listdir(LOCAL_OUTBOX):
        full_path = os.path.join(LOCAL_OUTBOX, file)

        if os.path.isfile(full_path) and not file.endswith(".gpg"):
            encrypted = encrypt_file(full_path)

            remote_file = f"{REMOTE_INBOX}/{os.path.basename(encrypted)}"
            upload_file(encrypted, remote_file)

            print(f"Sent: {encrypted}")


if __name__ == "__main__":
    process_outbox()
