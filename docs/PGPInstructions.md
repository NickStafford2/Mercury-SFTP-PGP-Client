# Instructions for PGP Key Exchange Process

## Purpose

To securely exchange encrypted files, each party will provide its PGP public key to the other party. Public keys are used for encryption only and may be shared openly. Private keys must never be shared.

## Step 1: Generate a PGP Key Pair

Generate a dedicated PGP key for the Mercury file exchange:

```bash
gpg --full-generate-key
```

When prompted, use a descriptive name such as:

```
Key Type: RSA and RSA
Key Size: 4096
Expiration: 2 years
User ID: Foundations Mercury File Exchange
Passphrase: Strong passphrase
Email: someEmail@foundations.com
```

After creation, verify the key:

```bash
gpg --list-keys
```

Example output:

```
pub   rsa4096 2026-06-08 [SC]
      ABCD1234EFGH5678IJKL9012MNOP3456QRST7890
uid   Foundations Mercury File Exchange <sftp@foundations.com>
```

## Step 2: Export the Public Key

Export the public key using the key name or email address:

```bash
gpg --armor \
    --export "Foundations Mercury File Exchange" \
    > foundations-mercury-public-key.asc
```

This creates:

```
foundations-mercury-public-key.asc
```

The file contents will begin with:

```
-----BEGIN PGP PUBLIC KEY BLOCK-----
```

## Step 3: Exchange Public Keys

Each party will send its ASCII-armored public key (`.asc` file) to the other party.

Example:

* Foundations sends: `foundations-mercury-public-key.asc`
* Mercury sends: `mercury-public-key.asc`

No private keys should ever be transmitted.

## Step 4: Import the Partner's Public Key

After receiving Mercury's public key:

```bash
gpg --import mercury-public-key.asc
```

Verify that the key has been imported successfully:

```bash
gpg --list-keys
```

## Step 5: Verify Key Fingerprints

Before using the exchanged keys, both parties should verify key fingerprints through a secondary communication channel (for example, a phone call or secure messaging platform).

View a key fingerprint:

```bash
gpg --fingerprint "Foundations Mercury File Exchange"
```

Provide that fingerprint to Mercury and request theirs as well. 
Confirm that the fingerprint exactly matches the fingerprint provided by the partner.
