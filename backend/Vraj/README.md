# Paper Search Backend - Vraj

AI-powered paper search backend using Google Gemini AI for text refinement and keyword extraction.

## 📁 Project Structure

```
Demo_Backend/
├── main.py              # Core backend logic
├── config.py            # Configuration (loads from .env)
├── run.py               # Single input processor
├── test_cases.py        # Test suite with 10 test cases
├── format.json          # Reference keywords for AI
├── sample_input.json    # Sample input format
├── .env                 # API keys (DO NOT COMMIT!)
├── .env.example         # Template for .env
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## 🎯 Features

- **AI-Powered Refinement**: Uses Gemini 2.0 Flash for intelligent text processing
- **15-20 Keywords**: Guaranteed minimum 15 keywords, maximum 20
- **No Abbreviations**: All abbreviations expanded in subject area and keywords
- **Spelling Correction**: Automatically fixes spelling mistakes
- **Percentage Validation**: Ensures acceptance percentages are valid (0-100)
- **Open Access Conversion**: Handles boolean, string, and integer inputs
- **Secure**: API keys stored in .env file, never committed to Git
- **10 Test Cases**: Comprehensive testing suite included

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the root directory:

```bash
GEMINI_API_KEY=your-actual-api-key-here
```

You can copy `.env.example` as a template:
```bash
cp .env.example .env
```

### 3. Run a Single Input

Edit `run.py` to modify the input data, then run:

```bash
python run.py
```

### 4. Run All Test Cases

```bash
python test_cases.py
```

## 📋 Usage Examples

### Option 1: Using run.py (Single Input)

Edit the `input_data` in `run.py`:

```python
input_data = {
    "subjectArea": "AI and ML",
    "title": "DL Aproaches for Enhanced NLP",
    "abstract": "This papr presants...",
    "accPercentFrom": 15,
    "accPercentTo": 25,
    "openAccess": "yes"
}
```

Then run:
```bash
python run.py
```

### Option 2: Using test_cases.py (Multiple Tests)

**Run all tests:**
```bash
python test_cases.py
```

**Run a specific test:**

Edit `test_cases.py` and uncomment:
```python
run_single_test(1)  # Runs test case #1
```

**Run a custom test:**

Edit `test_cases.py` and uncomment:
```python
custom_input = {
    "subjectArea": "Your Subject",
    "title": "Your Title",
    "abstract": "Your Abstract",
    "accPercentFrom": 10,
    "accPercentTo": 50,
    "openAccess": "yes"
}
run_custom_test(custom_input)
```

### Option 3: Import as a Module

```python
from main import PaperSearchBackend
from config import GEMINI_API_KEY

backend = PaperSearchBackend(GEMINI_API_KEY)

input_data = {
    "subjectArea": "ML",
    "title": "DL for NLP",
    "abstract": "This papr...",
    "accPercentFrom": 20,
    "accPercentTo": 40,
    "openAccess": True
}

output = backend.process_input(input_data)
print(output)
```

## 🧪 Test Cases Overview

The test suite includes 10 comprehensive test cases:

1. **Typical Errors** - Common spelling mistakes and abbreviations
2. **Multiple Abbreviations** - Heavy use of technical abbreviations
3. **Minimal Errors** - Mostly correct input
4. **Extensive Errors** - Severe spelling and grammar issues
5. **Edge Cases** - Invalid percentage values
6. **Reversed Percentages** - From > To values
7. **Empty Fields** - Minimal text content
8. **Real-World Example** - Chatbot research paper
9. **Academic Paper** - Complex terminology
10. **Mixed Case** - Case sensitivity issues

## 📊 Input/Output Format

### Input Format

```json
{
  "subjectArea": "AI and ML",
  "title": "DL Aproaches for NLP",
  "abstract": "This papr presants...",
  "accPercentFrom": 15,
  "accPercentTo": 25,
  "openAccess": "yes"
}
```

### Output Format

```json
{
  "subjectArea": "Artificial Intelligence and Machine Learning",
  "title": "Deep Learning Approaches for Natural Language Processing",
  "abstract": "This paper presents...",
  "accPercentFrom": 15,
  "accPercentTo": 25,
  "openAccess": 1
}
```

## 🔧 Configuration Options

Edit `config.py` to customize:

```python
GEMINI_API_KEY = "your-api-key"          # Your Gemini API key
FORMAT_REFERENCE_FILE = "format.json"    # Reference format file
OUTPUT_FILE = "refined_output.json"      # Output filename
VERBOSE_OUTPUT = True                    # Console verbosity
```

## 📝 Files Explained

### main.py
Contains the `PaperSearchBackend` class with core functionality:
- Text refinement using Gemini API
- Percentage validation
- Open access conversion
- Format reference loading

### config.py
Central configuration file for:
- API keys
- File paths
- Settings

### format.json
Reference format containing:
- Subject area terminology
- Technical keywords
- Common abbreviations

### run.py
Main entry point for processing single inputs:
- Modify `input_data` to test different scenarios
- Includes example functions
- Can load from JSON files

### test_cases.py
Comprehensive test suite:
- 10 predefined test cases
- Side-by-side input/output comparison
- Test result tracking
- Summary reports

## 🎨 Customization

### Add New Test Cases

Edit `test_cases.py` and add a new method:

```python
def test_11_your_test(self):
    """Test Case 11: Your description"""
    input_data = {
        # Your test data
    }
    return self.run_test(11, "Your Test Name", input_data)
```

Then add it to `run_all_tests()`:
```python
self.test_11_your_test()
```

### Modify Format Reference

Edit `format.json` to add domain-specific keywords:

```json
{
  "subjectArea": "Your Domain",
  "keywords": [
    "your keywords",
    "domain terms"
  ]
}
```

## 🔍 Troubleshooting

**API Key Error:**
- Ensure `GEMINI_API_KEY` is set correctly in `config.py`

**Import Error:**
- Install: `pip install google-generativeai`

**File Not Found:**
- Ensure `format.json` exists in the same directory

**Test Failures:**
- Check `test_results.json` for detailed error messages
- Verify internet connection (API calls require network)

## 📄 License

This project is for educational and development purposes.

## 🤝 Contributing

Feel free to modify and extend the test cases or add new functionality!

---

**Happy Testing! 🚀**
