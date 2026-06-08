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

```env
SFTP_HOST=sftp.example.com
SFTP_PORT=22
SFTP_USER=username
SSH_KEY_PATH=~/.ssh/id_ed25519
SSH_KEY_PASSPHRASE=
SFTP_KNOWN_HOSTS_PATH=
SFTP_ALLOW_UNKNOWN_HOST=false
SFTP_TIMEOUT_SECONDS=30

REMOTE_INBOUND_DIR=/inbound
REMOTE_OUTBOUND_DIR=/outbound

PGP_RECIPIENT=
PGP_PUBLIC_KEY_PATH=keys/public.asc
PGP_PASSPHRASE=secret
GPG_HOME=

WORK_DIR=work
```

## SSH/SFTP Notes

Use normal SSH keys. Ed25519 is the recommended default for new SSH keys.

Production defaults reject unknown SFTP host keys. Either make sure the server
host key is already in the system `known_hosts` file, or set
`SFTP_KNOWN_HOSTS_PATH` to a known-hosts file provisioned for this transfer.

For local Docker testing only, you can set:

```env
SFTP_ALLOW_UNKNOWN_HOST=true
```

## PGP/GPG Notes

For production, prefer `PGP_RECIPIENT` set to a verified key fingerprint or key
ID. `PGP_PUBLIC_KEY_PATH` is also supported for file-based recipient keys.

Decryption uses the secret key available in the configured GPG keyring. If
`GPG_HOME` is set, that GPG home directory is used. `PGP_PASSPHRASE` is passed
to `gpg` through stdin, not as a command-line argument.

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
