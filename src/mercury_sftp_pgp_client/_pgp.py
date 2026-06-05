from pgpy import PGPKey, PGPMessage
from pathlib import Path


def _load_public_key(path: str):
    key, _ = PGPKey.from_file(path)
    return key


def _load_private_key(path: str):
    key, _ = PGPKey.from_file(path)
    return key


def encrypt_file(input_path: str, output_path: str, public_key_path: str):
    public_key = _load_public_key(public_key_path)

    data = Path(input_path).read_bytes()
    msg = PGPMessage.new(data, file=True)

    encrypted = public_key.encrypt(msg)

    Path(output_path).write_text(str(encrypted))


def decrypt_file(input_path: str, output_path: str, private_key_path: str, passphrase: str):
    private_key = _load_private_key(private_key_path)

    msg = PGPMessage.from_blob(Path(input_path).read_text())

    with private_key.unlock(passphrase):
        decrypted = private_key.decrypt(msg)

    Path(output_path).write_bytes(decrypted.message)
