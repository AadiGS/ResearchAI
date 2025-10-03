"""
Configuration file for Paper Search Backend
Store your API keys and settings here
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# File Paths
FORMAT_REFERENCE_FILE = "format.json"
# Get absolute path to Aadi folder
VRAJ_DIR = os.path.dirname(os.path.abspath(__file__))
AADI_DIR = os.path.join(os.path.dirname(VRAJ_DIR), "Aadi")
OUTPUT_FILE = os.path.join(AADI_DIR, "format.json")  # Save to Aadi folder

# Settings
VERBOSE_OUTPUT = True  # Set to False to reduce console output
