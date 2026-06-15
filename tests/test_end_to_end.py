import os
import shutil
import unittest
from pathlib import Path
from uuid import uuid4

from mercury_sftp_pgp_client.config import Config
from mercury_sftp_pgp_client.receive_file import receive_file
from mercury_sftp_pgp_client.send_file import send_file


class EndToEndTransferTests(unittest.TestCase):
    @unittest.skipUnless(os.getenv("RUN_E2E") == "1", "set RUN_E2E=1 to run Docker/GPG/SFTP test")
    def test_encrypt_send_move_receive_decrypt(self):
        cfg = Config.from_env()
        project_root = Path(__file__).resolve().parents[1]
        server_root = project_root.parent / "SFTPServerTest"
        server_outbound = server_root / "data" / "outbound"
        server_inbound = server_root / "data" / "inbound"

        if not server_outbound.is_dir() or not server_inbound.is_dir():
            self.skipTest("SFTPServerTest data directories were not found")

        filename = f"e2e-{uuid4().hex}.csv"
        plaintext = f"hello mercury\n{uuid4().hex}\n"
        source_path = project_root / filename
        outbound_encrypted = server_outbound / f"{filename}.pgp"
        inbound_encrypted = server_inbound / f"{filename}.pgp"
        decrypted_path = cfg.work_dir / filename

        try:
            source_path.write_text(plaintext, encoding="utf-8")

            send_file(source_path)
            self.assertTrue(outbound_encrypted.is_file(), f"Expected upload at {outbound_encrypted}")

            shutil.move(outbound_encrypted, inbound_encrypted)
            receive_file(f"{filename}.pgp")

            self.assertEqual(decrypted_path.read_text(encoding="utf-8"), plaintext)
        finally:
            source_path.unlink(missing_ok=True)
            outbound_encrypted.unlink(missing_ok=True)
            inbound_encrypted.unlink(missing_ok=True)
            (cfg.work_dir / f"{filename}.pgp").unlink(missing_ok=True)
            decrypted_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
