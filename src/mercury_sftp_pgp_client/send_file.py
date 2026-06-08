from __future__ import annotations

import argparse
from pathlib import Path

from mercury_sftp_pgp_client._crypto import encrypt_file
from mercury_sftp_pgp_client._logger import get_logger
from mercury_sftp_pgp_client._sftp import build_remote_path, upload_file
from mercury_sftp_pgp_client.config import Config

log = get_logger()


def send_file(file_path: str | Path) -> Path:
    cfg = Config.from_env()
    cfg.require_encryption_recipient()

    source_path = Path(file_path).expanduser()
    if not source_path.is_file():
        raise FileNotFoundError(f"Local file does not exist: {source_path}")

    cfg.work_dir.mkdir(parents=True, exist_ok=True)
    encrypted_path = cfg.work_dir / f"{source_path.name}.pgp"
    remote_path = build_remote_path(cfg.remote_outbound_dir, encrypted_path.name)

    log.info("Encrypting %s", source_path)
    encrypt_file(
        source_path,
        encrypted_path,
        recipient=cfg.pgp_recipient,
        recipient_file=cfg.pgp_public_key_path,
        gpg_home=cfg.gpg_home,
    )

    log.info("Uploading %s", remote_path)
    upload_file(
        encrypted_path,
        remote_path,
        cfg.sftp_host,
        cfg.sftp_port,
        cfg.sftp_user,
        cfg.ssh_key_path,
        key_passphrase=cfg.ssh_key_passphrase,
        known_hosts_path=cfg.sftp_known_hosts_path,
        allow_unknown_host=cfg.sftp_allow_unknown_host,
        timeout_seconds=cfg.sftp_timeout_seconds,
    )

    log.info("Send complete")
    return encrypted_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Encrypt and upload a file over SFTP.")
    parser.add_argument("file_path", help="Path to the local file to encrypt and send.")
    args = parser.parse_args()
    send_file(args.file_path)


if __name__ == "__main__":
    main()
