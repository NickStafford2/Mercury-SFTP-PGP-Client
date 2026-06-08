# Mercury SFTP PGP Client

Simple SFTP + OpenPGP file transfer client.

The client encrypts outbound files with `gpg`, uploads them over SFTP using SSH
key authentication, downloads inbound `.pgp` files, and decrypts them with
`gpg`.

## Install

```bash
poetry install
```

GnuPG must be installed on the machine running this client:

```bash
gpg --version
```

## Configuration

Copy `.env.example` to `.env` and set the values for the target environment.

## SSH/SFTP Notes

Use normal SSH keys. Ed25519 is the recommended default for new SSH keys.

The client always rejects unknown SFTP host keys. Add the server host key to the
normal SSH `known_hosts` file before running transfers.

## PGP/GPG Notes

Import Mercury's public key into GPG, verify the fingerprint through a secondary
channel, then set `PGP_RECIPIENT` to that verified fingerprint.

Decryption uses our secret key from the normal GPG keyring. `PGP_PASSPHRASE` is
passed to `gpg` through stdin, not as a command-line argument.

## Usage

Encrypt and upload:

```bash
poetry run send-file path/to/file.csv
```

Download and decrypt:

```bash
poetry run receive-file file.csv.pgp
```

## Checks

```bash
poetry check
poetry run python -m unittest discover
poetry run python -m compileall src tests
```
