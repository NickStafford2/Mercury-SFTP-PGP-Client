from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path, PurePosixPath
from typing import Iterator
from uuid import uuid4

import paramiko


def _remote_join(directory: str, filename: str) -> str:
    if filename in {"", ".", ".."}:
        raise ValueError("Remote filename must not be empty")
    name = PurePosixPath(filename)
    if name.is_absolute() or ".." in name.parts:
        raise ValueError(f"Unsafe remote filename: {filename}")
    return str(PurePosixPath(directory) / name)


def build_remote_path(directory: str, filename: str) -> str:
    return _remote_join(directory, filename)


@contextmanager
def _connect(
    host: str,
    port: int,
    user: str,
    key_path: Path,
    *,
    key_passphrase: str | None = None,
    timeout_seconds: int = 30,
) -> Iterator[paramiko.SFTPClient]:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.RejectPolicy())

    client.connect(
        hostname=host,
        port=port,
        username=user,
        key_filename=str(key_path),
        passphrase=key_passphrase,
        look_for_keys=False,
        allow_agent=False,
        timeout=timeout_seconds,
        banner_timeout=timeout_seconds,
        auth_timeout=timeout_seconds,
    )

    sftp = client.open_sftp()
    try:
        yield sftp
    finally:
        sftp.close()
        client.close()


def upload_file(
    local_path: Path,
    remote_path: str,
    host: str,
    port: int,
    user: str,
    key_path: Path,
    *,
    key_passphrase: str | None = None,
    timeout_seconds: int = 30,
) -> None:
    local_path = local_path.expanduser()
    if not local_path.is_file():
        raise FileNotFoundError(f"Local file does not exist: {local_path}")

    tmp_remote = f"{remote_path}.tmp-{uuid4().hex}"
    with _connect(
        host,
        port,
        user,
        key_path,
        key_passphrase=key_passphrase,
        timeout_seconds=timeout_seconds,
    ) as sftp:
        try:
            sftp.put(str(local_path), tmp_remote, confirm=True)
            if hasattr(sftp, "posix_rename"):
                sftp.posix_rename(tmp_remote, remote_path)
            else:
                sftp.rename(tmp_remote, remote_path)
        except Exception:
            try:
                sftp.remove(tmp_remote)
            except OSError:
                pass
            raise


def download_file(
    remote_path: str,
    local_path: Path,
    host: str,
    port: int,
    user: str,
    key_path: Path,
    *,
    key_passphrase: str | None = None,
    timeout_seconds: int = 30,
) -> None:
    local_path = local_path.expanduser()
    local_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_local = local_path.with_name(f"{local_path.name}.tmp-{uuid4().hex}")

    with _connect(
        host,
        port,
        user,
        key_path,
        key_passphrase=key_passphrase,
        timeout_seconds=timeout_seconds,
    ) as sftp:
        try:
            sftp.get(remote_path, str(tmp_local))
            tmp_local.replace(local_path)
        except Exception:
            tmp_local.unlink(missing_ok=True)
            raise
