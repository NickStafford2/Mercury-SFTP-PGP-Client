
We are setting up a secure weekly file exchange with a partner using SFTP and PGP encryption. The partner will provide files over SFTP using SSH key authentication and encrypt files using PGP. We will provide them with our SSH public key, PGP public key, and static IP address for whitelisting. Once their internal security approval is complete, the connection will be enabled and we will process incoming encrypted CSV files on a weekly schedule and return processed outputs securely.

# Mercury SFTP PGP Client

Simple, explicit SFTP + PGP file transfer tool.

No classes. No framework. Just functions.

---

## Install

```bash
poetry install
