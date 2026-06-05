from dataclasses import dataclass
import os


@dataclass
class Config:
    sftp_host: str = os.getenv("SFTP_HOST")
    sftp_port: int = int(os.getenv("SFTP_PORT", 22))
    sftp_user: str = os.getenv("SFTP_USER")
    ssh_key_path: str = os.getenv("SSH_KEY_PATH")

    remote_inbound_dir: str = os.getenv("REMOTE_INBOUND_DIR", "/inbound")
    remote_outbound_dir: str = os.getenv("REMOTE_OUTBOUND_DIR", "/outbound")

    pgp_public_key_path: str = os.getenv("PGP_PUBLIC_KEY_PATH")
    pgp_private_key_path: str = os.getenv("PGP_PRIVATE_KEY_PATH")
    pgp_private_key_passphrase: str = os.getenv("PGP_PASSPHRASE", "")
    
    local_work_dir: str = os.getenv("LOCAL_WORK_DIR", "./work")
