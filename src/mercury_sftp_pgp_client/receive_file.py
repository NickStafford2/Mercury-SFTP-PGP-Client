from __future__ import annotations

import argparse
from pathlib import Path

from mercury_sftp_pgp_client._crypto import decrypt_file
from mercury_sftp_pgp_client._logger import get_logger
from mercury_sftp_pgp_client._sftp import build_remote_path, download_file
from mercury_sftp_pgp_client.config import Config

log = get_logger()


def receive_file(remote_filename: str) -> Path:
    cfg = Config.from_env()
    cfg.work_dir.mkdir(parents=True, exist_ok=True)

    encrypted_local = cfg.work_dir / remote_filename
    if encrypted_local.suffix.lower() == ".pgp":
        decrypted_local = encrypted_local.with_suffix("")
    else:
        decrypted_local = Path(f"{encrypted_local}.decrypted")

    remote_path = build_remote_path(cfg.remote_inbound_dir, remote_filename)

    log.info("Downloading %s", remote_path)
    download_file(
        remote_path,
        encrypted_local,
        cfg.sftp_host,
        cfg.sftp_port,
        cfg.sftp_user,
        cfg.ssh_key_path,
    )

    log.info("Decrypting %s", encrypted_local)
    decrypt_file(
        encrypted_local,
        decrypted_local,
        cfg.pgp_passphrase,
    )

    log.info("Receive complete: %s", decrypted_local)
    return decrypted_local


def main() -> None:
    parser = argparse.ArgumentParser(description="Download and decrypt a file from SFTP.")
    parser.add_argument("remote_filename", help="Filename under REMOTE_INBOUND_DIR to receive.")
    args = parser.parse_args()
    receive_file(args.remote_filename)


if __name__ == "__main__":
    main()
