from __future__ import annotations

import subprocess
from pathlib import Path


def _run_gpg(args: list[str], *, passphrase: str | None = None) -> None:
    input_text = None
    if passphrase is not None:
        args = args[:1] + ["--pinentry-mode", "loopback", "--passphrase-fd", "0"] + args[1:]
        input_text = f"{passphrase}\n"

    result = subprocess.run(
        args,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "gpg failed"
        raise RuntimeError(detail)


def encrypt_file(input_path: Path, output_path: Path, recipient: str) -> None:
    input_path = input_path.expanduser()
    output_path = output_path.expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    _run_gpg([
        "gpg",
        "--batch",
        "--yes",
        "--no-tty",
        "--trust-model",
        "always",
        "--output",
        str(output_path),
        "--encrypt",
        "--recipient",
        recipient,
        str(input_path),
    ])


def decrypt_file(input_path: Path, output_path: Path, passphrase: str | None = None) -> None:
    input_path = input_path.expanduser()
    output_path = output_path.expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    _run_gpg([
        "gpg",
        "--batch",
        "--yes",
        "--no-tty",
        "--output",
        str(output_path),
        "--decrypt",
        str(input_path),
    ], passphrase=passphrase)
