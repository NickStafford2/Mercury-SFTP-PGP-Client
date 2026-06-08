# Information Needed From Mercury

## SFTP Access

1. SFTP hostname
2. Port number
3. Username
4. Exact inbound and outbound directory paths


## SSH Key Setup

1. Preferred SSH public key format, if they have a requirement
2. Where and how they want us to send our SSH public key
3. Whether they require key rotation on a schedule

## PGP Setup

1. Mercury's PGP public key file
2. Whether they require a specific PGP algorithm, key size, or expiration policy
3. Signing
  a. Whether outbound files to Mercury should be encrypted only, or encrypted and signed
  b. Whether inbound files from Mercury will be signed


## After it works

1. Server host key fingerprint for `known_hosts` verification
2. Mercury's verified PGP key fingerprint 
