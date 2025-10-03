# How to Use ResearchAI Backend (Dynamic Input)

The backend is now **fully dynamic** and can accept input from multiple sources:

## Method 1: Command Line with JSON File

Create a JSON file with your input:

```json
{
  "subjectArea": "NLP",
  "title": "Sentiment Analysis using Transformers",
  "abstract": "This research explores...",
  "accPercentFrom": 30,
  "accPercentTo": 60,
  "openAccess": "yes"
}
```

Run with:
```bash
cd backend/Vraj
python run.py custom_input.json
```

## Method 2: Python API (For Frontend Integration)

```python
from backend.Vraj.api import process_research_paper

input_data = {
    "subjectArea": "DL",
    "title": "CNN for Image Classification",
    "abstract": "We use deep learning...",
    "accPercentFrom": 40,
    "accPercentTo": 70,
    "openAccess": "yes"
}

# Process and get results
result = process_research_paper(input_data, trigger_search=True)

# Access results
print(result['refined_output'])  # Refined input
print(result['final_results'])   # Top 3 journals
```

## Method 3: Import process_user_input

```python
from backend.Vraj.run import process_user_input

result = process_user_input(input_data, trigger_search=True)
```

## Input Format

All inputs are **dynamic** and will be processed by Gemini AI:

- **subjectArea**: Can use abbreviations (DL, ML, NLP, CV, RL, etc.)
- **title**: Can have spelling mistakes and abbreviations
- **abstract**: Can have spelling mistakes and abbreviations
- **accPercentFrom/To**: 0-100 (integers)
- **openAccess**: Accepts "yes"/"no", True/False, or 1/0

## Output Format

```json
{
  "refined_output": {
    "subjectArea": "deep learning",
    "keywords": [...],
    "openAccess": 1,
    "acceptancePercentFrom": 40,
    "acceptancePercentTo": 70
  },
  "refined_output_path": "path/to/format.json",
  "final_results": [...],  // Top 3 journals
  "final_results_path": "path/to/final_result.json"
}
```

## Features

✅ **Dynamic Input**: No hardcoding - accepts any input
✅ **Spelling Correction**: AI fixes typos automatically
✅ **Abbreviation Expansion**: DL → deep learning, ML → machine learning
✅ **Keyword Extraction**: AI extracts 15-20 relevant keywords
✅ **Flexible Format**: Accepts multiple input formats for openAccess
✅ **Automated Pipeline**: Optionally triggers journal search automatically
✅ **Frontend Ready**: Can be imported and used by web/API

## Example: Different Subjects

### Computer Vision
```json
{
  "subjectArea": "CV",
  "title": "Object Detection using CNNs",
  ...
}
```

### Natural Language Processing
```json
{
  "subjectArea": "NLP",
  "title": "Chatbot using LLMs",
  ...
}
```

### Reinforcement Learning
```json
{
  "subjectArea": "RL",
  "title": "DQN for Game Playing",
  ...
}
```

All inputs are processed dynamically - no static code!
