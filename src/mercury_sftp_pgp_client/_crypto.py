import subprocess
from pathlib import Path


def encrypt_file(input_path: str, output_path: str, recipient: str):
    subprocess.run([
        "gpg",
        "--yes",
        "--batch",
        "--output", output_path,
        "--encrypt",
        "--recipient", recipient,
        input_path
    ], check=True)


def decrypt_file(input_path: str, output_path: str):
    subprocess.run([
        "gpg",
        "--yes",
        "--batch",
        "--output", output_path,
        "--decrypt",
        input_path
    ], check=True)
