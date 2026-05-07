import sys
import os

# Add src to sys.path to allow importing the cipherself package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cipherself.cli import cli

if __name__ == "__main__":
    cli()
