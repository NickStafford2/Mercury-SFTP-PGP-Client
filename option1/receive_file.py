# receive_file.py

import os
import paramiko
import gnupg
from config import *

gpg = gnupg.GPG()


def download_files():
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USER)

    sftp = paramiko.SFTPClient.from_transport(transport)

    files = sftp.listdir(REMOTE_OUTBOX)

    downloaded = []

    for file in files:
        remote_file = f"{REMOTE_OUTBOX}/{file}"
        local_file = os.path.join(LOCAL_INBOX, file)

        sftp.get(remote_file, local_file)
        downloaded.append(local_file)

    sftp.close()
    transport.close()

    return downloaded


def decrypt_file(filepath):
    with open(filepath, "rb") as f:
        result = gpg.decrypt_file(f, output=filepath.replace(".gpg", ""))

    if not result.ok:
        raise Exception(f"Decryption failed: {result.status}")

    return filepath.replace(".gpg", "")


def process_inbox():
    files = download_files()

    for file in files:
        if file.endswith(".gpg"):
            decrypted = decrypt_file(file)
            print(f"Decrypted: {decrypted}")


if __name__ == "__main__":
    process_inbox()
