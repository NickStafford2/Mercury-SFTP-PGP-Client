# PGP Key Exchange Process

## Purpose

To securely exchange encrypted files, each party will provide its PGP public key to the other party. Public keys are used for encryption only and may be shared openly. Private keys must never be shared.

## Step 1: Generate a PGP Key Pair

If a PGP key pair does not already exist, generate one using GPG:

```bash
gpg --full-generate-key
```

Record the email address associated with the key, as it will be used as the key identifier.

## Step 2: Export the Public Key

Export the public key in ASCII-armored format:

```bash
gpg --armor --export you@foundations.com > company-public-key.asc
```

This creates a file similar to:

```
company-public-key.asc
```

The file contents will begin with:

```
-----BEGIN PGP PUBLIC KEY BLOCK-----
```

## Step 3: Exchange Public Keys

Each party will send its ASCII-armored public key (`.asc` file) to the other party via email or another agreed-upon communication channel.

Example:

* Our Company sends: `our-public-key.asc`
* Partner sends: `partner-public-key.asc`

No private keys should ever be transmitted.

## Step 4: Import the Partner's Public Key

After receiving the partner's public key:

```bash
gpg --import partner-public-key.asc
```

Verify that the key has been imported successfully:

```bash
gpg --list-keys
```

## Step 5: Verify Key Fingerprints

Before using the exchanged keys, both parties should verify key fingerprints through a secondary communication channel (for example, a phone call or secure messaging platform).

View a key fingerprint:

```bash
gpg --fingerprint partner@example.com
```

Confirm that the fingerprint exactly matches the fingerprint provided by the partner.

## Step 6: Encrypt Files for Transmission

Before uploading a file to the SFTP server, encrypt it using the partner's public key:

```bash
gpg --encrypt \
    --recipient partner@example.com \
    filename.csv
```

This produces an encrypted file, for example:

```
filename.csv.gpg
```

Only the partner, using their private key, can decrypt the file.

## Step 7: Upload Encrypted Files via SFTP

Upload only encrypted files to the designated SFTP directory.

Example workflow:

1. Generate file
2. Encrypt file using partner's public key
3. Upload encrypted file to SFTP
4. Partner downloads encrypted file
5. Partner decrypts using their private key

## Security Requirements

* Share only public keys (`.asc` files).
* Never share private keys.
* Verify fingerprints before first use.
* Store private keys securely.
* Use passphrase-protected private keys whenever possible.
* Upload only encrypted files to the SFTP environment.
