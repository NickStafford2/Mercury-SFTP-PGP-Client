from __future__ import annotations

import subprocess
from pathlib import Path


def _gpg_base_args(gpg_home: Path | None = None) -> list[str]:
    args = ["gpg", "--batch", "--yes", "--no-tty"]
    if gpg_home:
        args.extend(["--homedir", str(gpg_home)])
    return args


def _run_gpg(args: list[str], *, passphrase: str | None = None) -> None:
    input_text = None
    if passphrase is not None:
        args.extend(["--pinentry-mode", "loopback", "--passphrase-fd", "0"])
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


def encrypt_file(
    input_path: Path,
    output_path: Path,
    *,
    recipient: str | None = None,
    recipient_file: Path | None = None,
    gpg_home: Path | None = None,
) -> None:
    if not recipient and not recipient_file:
        raise ValueError("recipient or recipient_file is required")

    input_path = input_path.expanduser()
    output_path = output_path.expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    args = _gpg_base_args(gpg_home)
    args.extend(["--trust-model", "always", "--output", str(output_path), "--encrypt"])

    if recipient:
        args.extend(["--recipient", recipient])
    if recipient_file:
        args.extend(["--recipient-file", str(recipient_file.expanduser())])

    args.append(str(input_path))
    _run_gpg(args)


def decrypt_file(
    input_path: Path,
    output_path: Path,
    *,
    passphrase: str | None = None,
    gpg_home: Path | None = None,
) -> None:
    input_path = input_path.expanduser()
    output_path = output_path.expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    args = _gpg_base_args(gpg_home)
    args.extend(["--output", str(output_path), "--decrypt", str(input_path)])
    _run_gpg(args, passphrase=passphrase)
