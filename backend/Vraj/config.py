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
OUTPUT_FILE = "refined_output.json"

# Settings
VERBOSE_OUTPUT = True  # Set to False to reduce console output
