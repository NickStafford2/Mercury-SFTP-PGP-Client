import unittest

from mercury_sftp_pgp_client._sftp import build_remote_path


class BuildRemotePathTests(unittest.TestCase):
    def test_builds_posix_path(self):
        self.assertEqual(build_remote_path("/outbound", "file.csv.pgp"), "/outbound/file.csv.pgp")

    def test_rejects_absolute_filename(self):
        with self.assertRaises(ValueError):
            build_remote_path("/outbound", "/etc/passwd")

    def test_rejects_parent_traversal(self):
        with self.assertRaises(ValueError):
            build_remote_path("/outbound", "../secret.csv")


if __name__ == "__main__":
    unittest.main()
