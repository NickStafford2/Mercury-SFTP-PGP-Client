## GPG Key Generation Summary (PGP File Transfer System)

A new OpenPGP key pair was generated using **GnuPG (GPG) 2.5.20** on macOS.

### Key Configuration

* **Algorithm:** RSA and RSA
* **Key size:** 4096-bit
* **Purpose:** File encryption/decryption for SFTP-based transfer testing

---

## Usage Guidelines

### Testing / Development

* RSA 4096-bit key pair
* Single key pair per developer or test environment
* Passphrase optional (can be disabled for automation)
* Keys may be regenerated as needed

### Production

* RSA 4096-bit (or ECC if fully supported across all systems)
* Private key must always be passphrase-protected
* Store private keys in a secure secret manager (not on disk or in repo)
* Rotate keys periodically and on any suspected compromise
* Use a name such as: Foundations Mercury File Transfer

---

## Summary

* Use RSA 4096 for compatibility and simplicity in testing
* Use hardened key storage + passphrase protection in production
* Never reuse production private keys across environments
