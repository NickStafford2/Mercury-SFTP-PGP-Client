# Instructions for SFTP Access

## Purpose

To enable secure authentication to the partner's SFTP environment, our company will provide an SSH public key. The partner will install the public key on their SFTP server and associate it with our assigned SFTP account.


## Step 1: Generate a Dedicated SSH Key Pair

Generate a dedicated SSH key pair for the Mercury SFTP integration:

```bash
ssh-keygen -t ed25519 \
  -f ~/.ssh/mercury_sftp_ed25519 \
  -C "Mercury SFTP Integration"
```

This creates:

```text
~/.ssh/mercury_sftp_ed25519       # Private key that must remain confidential
~/.ssh/mercury_sftp_ed25519.pub   # Public key that provide to Mercury
```

## Step 2: Provide the Public Key to Mercury

Send the contents of:

```text
~/.ssh/mercury_sftp_ed25519.pub
```

to Mercury as part of the SFTP onboarding process. Do not send the private key file.

## Step 3: Partner Configures Access

The partner will install the public key on their SFTP server and associate it with the SFTP account created for our organization.

The partner will then provide:

* SFTP hostname
* Port number
* Username
* Available directories
* Any additional onboarding instructions

## Step 4: Test Connectivity

Once the partner confirms setup is complete, test the connection:

```bash
sftp -i ~/.ssh/mercury_sftp_ed25519 \
     username@sftp.partner.com
```

Successful authentication should result in an SFTP prompt:

```text
sftp>
```

Verify access by listing the available directories:

```text
sftp> ls
```

