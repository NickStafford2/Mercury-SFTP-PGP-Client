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


def _path_env(name: str, default: str | None = None) -> Path:
    value = os.getenv(name, default)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return Path(value).expanduser()


@dataclass(frozen=True)
class Config:
    sftp_host: str
    sftp_port: int
    sftp_user: str
    ssh_key_path: Path
    remote_inbound_dir: str
    remote_outbound_dir: str
    pgp_recipient: str | None
    pgp_passphrase: str | None
    work_dir: Path

    @classmethod
    def from_env(cls) -> "Config":
        cfg = cls(
            sftp_host=_required_env("SFTP_HOST"),
            sftp_port=_env_int("SFTP_PORT", 22),
            sftp_user=_required_env("SFTP_USER"),
            ssh_key_path=_path_env("SSH_KEY_PATH"),
            remote_inbound_dir=os.getenv("REMOTE_INBOUND_DIR", "/inbound"),
            remote_outbound_dir=os.getenv("REMOTE_OUTBOUND_DIR", "/outbound"),
            pgp_recipient=os.getenv("PGP_RECIPIENT") or None,
            pgp_passphrase=os.getenv("PGP_PASSPHRASE") or None,
            work_dir=_path_env("WORK_DIR", "./work"),
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
