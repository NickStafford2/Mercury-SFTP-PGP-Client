# Providing an SSH Public Key for SFTP Access

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
~/.ssh/mercury_sftp_ed25519
~/.ssh/mercury_sftp_ed25519.pub
```

* `mercury_sftp_ed25519` is the private key and must remain confidential.
* `mercury_sftp_ed25519.pub` is the public key and will be provided to Mercury.

## Step 2: Provide the Public Key to Mercury

Send the contents of:

```text
~/.ssh/mercury_sftp_ed25519.pub
```

to Mercury as part of the SFTP onboarding process.

Do not send the private key file.

## Step 3: Send the Public Key to the Partner

Provide the contents of the public key file or attach the `.pub` file to a secure email.

Example file:

```text
mercury_sftp_ed25519.pub
```

Only the public key should be transmitted.

Do not send:

* `mercury_sftp_ed25519`
* any private key file
* any passphrase associated with the private key

## Step 4: Partner Configures Access

The partner will install the public key on their SFTP server and associate it with the SFTP account created for our organization.

The partner will then provide:

* SFTP hostname
* Port number
* Username
* Available directories
* Any additional onboarding instructions

## Step 5: Test Connectivity

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

## Security Requirements

* Share only the SSH public key (`.pub` file).
* Never share the SSH private key.
* Store private keys securely and restrict access to authorized personnel.
* Protect private keys with a passphrase whenever possible.
* Rotate keys according to company security policies.
* Notify the partner immediately if a private key is suspected to be compromised.
