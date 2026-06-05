import os
from pathlib import Path

from mercury_sftp_pgp_client.config import Config
from mercury_sftp_pgp_client._logger import get_logger
from mercury_sftp_pgp_client._pgp import decrypt_file
from mercury_sftp_pgp_client._sftp import download_file

log = get_logger()


def receive_file(remote_filename: str):
    cfg = Config()

    Path(cfg.work_dir).mkdir(exist_ok=True)

    encrypted_local = os.path.join(cfg.work_dir, remote_filename)
    decrypted_local = os.path.join(cfg.work_dir, remote_filename.replace(".pgp", ""))

    remote_path = f"{cfg.remote_inbound_dir}/{remote_filename}"

    log.info(f"Downloading {remote_path}")
    download_file(
        remote_path,
        encrypted_local,
        cfg.sftp_host,
        cfg.sftp_port,
        cfg.sftp_user,
        cfg.ssh_key_path,
    )

    log.info("Decrypting file")
    decrypt_file(
        encrypted_local,
        decrypted_local,
        cfg.pgp_private_key_path,
        cfg.pgp_passphrase,
    )

    log.info(f"Done: {decrypted_local}")


if __name__ == "__main__":
    import sys
    receive_file(sys.argv[1])
