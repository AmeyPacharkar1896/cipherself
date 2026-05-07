import unittest
import subprocess
import os
import shutil

class TestCipherselfCLI(unittest.TestCase):
    def setUp(self):
        # Ensure outputs/ is clean for certain tests if needed, 
        # but we'll mostly check for file existence
        pass

    def run_cli(self, args):
        cmd = ["uv", "run", "cipherself.py"] + args
        return subprocess.run(cmd, capture_output=True, text=True)

    def test_demo_success(self):
        result = self.run_cli(["--demo"])
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists("outputs/demo/Alex_Mercer_exposed.pdf"))

    def test_github_only_success(self):
        # We use a known user for the test
        result = self.run_cli(["--github", "torvalds"])
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists("outputs/github/torvalds_exposed.pdf"))

    def test_name_only_success(self):
        result = self.run_cli(["--name", "Linus Torvalds"])
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists("outputs/name/Linus_Torvalds_exposed.pdf"))

    def test_reddit_only_success(self):
        result = self.run_cli(["--reddit", "spez"])
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists("outputs/reddit/spez_exposed.pdf"))

    def test_github_name_success(self):
        result = self.run_cli(["--github", "torvalds", "--name", "Linus Torvalds"])
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists("outputs/github_name/Linus_Torvalds_exposed.pdf"))

    def test_github_reddit_success(self):
        result = self.run_cli(["--github", "torvalds", "--reddit", "torvalds"])
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists("outputs/github_reddit/torvalds_exposed.pdf"))

    def test_full_intel_success(self):
        result = self.run_cli(["--github", "torvalds", "--reddit", "torvalds", "--name", "Linus Torvalds"])
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists("outputs/full/Linus_Torvalds_exposed.pdf"))

    def test_no_args_failure(self):
        result = self.run_cli([])
        self.assertEqual(result.returncode, 2) # argparse returns 2 for validation errors
        self.assertIn("Please provide at least one of: --github, --name, or --reddit", result.stderr)

    def test_unknown_flag_failure(self):
        result = self.run_cli(["--unknown"])
        self.assertEqual(result.returncode, 2)
        self.assertIn("unrecognized arguments: --unknown", result.stderr)

if __name__ == "__main__":
    unittest.main()
