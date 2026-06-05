import paramiko
from pathlib import Path


def _connect(host: str, port: int, user: str, key_path: str):
    key = paramiko.RSAKey.from_private_key_file(key_path)

    transport = paramiko.Transport((host, port))
    transport.connect(username=user, pkey=key)

    return transport, paramiko.SFTPClient.from_transport(transport)


def upload_file(local_path: str, remote_path: str, host: str, port: int, user: str, key_path: str):
    transport, sftp = _connect(host, port, user, key_path)

    try:
        tmp_remote = remote_path + ".tmp"
        sftp.put(local_path, tmp_remote)
        sftp.rename(tmp_remote, remote_path)  # atomic move
    finally:
        sftp.close()
        transport.close()


def download_file(remote_path: str, local_path: str, host: str, port: int, user: str, key_path: str):
    transport, sftp = _connect(host, port, user, key_path)

    try:
        tmp_local = local_path + ".tmp"
        sftp.get(remote_path, tmp_local)
        Path(tmp_local).replace(local_path)
    finally:
        sftp.close()
        transport.close()
