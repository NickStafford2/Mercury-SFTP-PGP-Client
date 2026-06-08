from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc


def _expand_path(path: str | None) -> Path | None:
    if not path:
        return None
    return Path(path).expanduser()


@dataclass(frozen=True)
class Config:
    sftp_host: str
    sftp_port: int
    sftp_user: str
    ssh_key_path: Path
    ssh_key_passphrase: str | None
    sftp_timeout_seconds: int

    remote_inbound_dir: str
    remote_outbound_dir: str

    pgp_recipient: str | None
    pgp_public_key_path: Path | None
    pgp_passphrase: str | None
    gpg_home: Path | None
    work_dir: Path

    @classmethod
    def from_env(cls) -> "Config":
        ssh_key_path = _expand_path(_required_env("SSH_KEY_PATH"))
        if ssh_key_path is None:
            raise ValueError("SSH_KEY_PATH is required")

        cfg = cls(
            sftp_host=_required_env("SFTP_HOST"),
            sftp_port=_env_int("SFTP_PORT", 22),
            sftp_user=_required_env("SFTP_USER"),
            ssh_key_path=ssh_key_path,
            ssh_key_passphrase=os.getenv("SSH_KEY_PASSPHRASE") or None,
            sftp_timeout_seconds=_env_int("SFTP_TIMEOUT_SECONDS", 30),
            remote_inbound_dir=os.getenv("REMOTE_INBOUND_DIR", "/inbound"),
            remote_outbound_dir=os.getenv("REMOTE_OUTBOUND_DIR", "/outbound"),
            pgp_recipient=os.getenv("PGP_RECIPIENT") or None,
            pgp_public_key_path=_expand_path(os.getenv("PGP_PUBLIC_KEY_PATH")),
            pgp_passphrase=os.getenv("PGP_PASSPHRASE") or None,
            gpg_home=_expand_path(os.getenv("GPG_HOME")),
            work_dir=_expand_path(os.getenv("WORK_DIR", "./work")) or Path("./work"),
        )
        cfg.validate()
        return cfg

    def validate(self) -> None:
        if not self.ssh_key_path.exists():
            raise ValueError(f"SSH private key does not exist: {self.ssh_key_path}")

        if self.sftp_port < 1 or self.sftp_port > 65535:
            raise ValueError("SFTP_PORT must be between 1 and 65535")

        if not self.remote_inbound_dir.startswith("/"):
            raise ValueError("REMOTE_INBOUND_DIR must be an absolute SFTP path")

        if not self.remote_outbound_dir.startswith("/"):
            raise ValueError("REMOTE_OUTBOUND_DIR must be an absolute SFTP path")

        if self.pgp_public_key_path and not self.pgp_public_key_path.exists():
            raise ValueError(f"PGP public key file does not exist: {self.pgp_public_key_path}")

        if self.gpg_home and not self.gpg_home.exists():
            raise ValueError(f"GPG_HOME does not exist: {self.gpg_home}")

    def require_encryption_recipient(self) -> None:
        if not self.pgp_recipient and not self.pgp_public_key_path:
            raise ValueError("Set PGP_RECIPIENT or PGP_PUBLIC_KEY_PATH before sending encrypted files")
