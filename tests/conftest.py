import os
import sys
from dotenv import load_dotenv

# Load .env from project root so tests and app code see the same environment variables
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
dotenv_path = os.path.join(ROOT_DIR, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Ensure the project root is on sys.path so tests can import the `app` package.
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
