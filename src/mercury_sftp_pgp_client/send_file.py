import os
from pathlib import path

from mercury_sftp_pgp_client.config import config
from mercury_sftp_pgp_client._logger import get_logger
from mercury_sftp_pgp_client._pgp import encrypt_file
from mercury_sftp_pgp_client._sftp import upload_file

log = get_logger()


def send_file(file_path: str):
    cfg = config()

    path(cfg.work_dir).mkdir(exist_ok=true)

    filename = path(file_path).name
    encrypted_path = os.path.join(cfg.work_dir, filename + ".pgp")

    # do later once sftp works for sure
    # log.info(f"encrypting {file_path}")
    # encrypt_file(file_path, encrypted_path, cfg.pgp_public_key_path)

    remote_path = f"{cfg.remote_outbound_dir}/{path(encrypted_path).name}"

    log.info(f"uploading to {remote_path}")
    upload_file(
        # encrypted_path,
        file_path
        remote_path,
        cfg.sftp_host,
        cfg.sftp_port,
        cfg.sftp_user,
        cfg.ssh_key_path,
    )

    log.info("send complete")


if __name__ == "__main__":
    import sys
    send_file(sys.argv[1])
