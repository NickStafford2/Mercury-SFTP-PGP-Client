## Secure Weekly File Exchange (PGP + SFTP)

* The partner company will be sending us a **secure file on a weekly basis**.
* They are transitioning away from password-based authentication to:

  * **SSH key authentication (for SFTP access)**
  * **PGP encryption (for file-level security)**

## Key management

* They require us to provide a **PGP public key**.

## Security onboarding process

* Their internal security team must approve the setup via a security ticket.
* Once approved:

  * We will provide:

    * Our **PGP public key**
    * Our **SSH public key**
    * Our **public IP address(es)** for whitelisting
      * We should probably use the windows server so that we can easily copy files internally. 
* After approval and configuration:

  * They will whitelist our IP address
  * They will configure access using our SSH key for SFTP connectivity

## Data exchange flow

* Files will be transferred on a weekly schedule.
* Files will be:

  1. Sent to us in encrypted form (PGP)
  2. Transferred via SFTP using SSH key authentication
* We will:

  * Decrypt incoming files using our private PGP key
  * Process data internally
  * Send back results securely (format and encryption requirements to be confirmed)

