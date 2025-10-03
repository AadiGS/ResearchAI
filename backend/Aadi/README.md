# Research Journal Fetcher - Backend

This backend application fetches research journals from the OpenAlex API based on specified criteria.

## Features

- Fetches research journals from OpenAlex API
- Filters by:
  - Subject area
  - Keywords (15-20 related keywords)
  - Open Access status
  - Acceptance percentage range (with ±5% flexibility)
- Ranks journals by aptness score
- Returns top 15 most relevant journals

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   OPENALEX_API_KEY=your_api_key_here
   OPENALEX_EMAIL=your_email@example.com
   ```

   **Note:** 
   - API key is optional but recommended for better rate limits
   - Email is used for the "polite pool" which gets better performance
   - Get your API key from: https://openalex.org/

### 3. Prepare Input File

The application reads from `format.json` which should contain:

```json
{
  "subjectArea": "artificial Intelligence",
  "keywords": [
    "machine learning",
    "deep learning",
    "neural networks",
    // ... 15-20 keywords total
  ],
  "openAccess": 1,
  "acceptancePercentFrom": 0,
  "acceptancePercentTo": 100
}
```

## Usage

Run the fetcher:

```bash
python fetch_journals.py
```

## Output

The script will:
1. Load search criteria from `format.json`
2. Query the OpenAlex API
3. Rank journals by aptness score
4. Display top 15 journals in the console
5. Save results to `results.json`

### Sample Output

```
Top 15 Most Apt Research Journals
================================================================================

1. Deep Learning Approaches for Enhanced Natural Language Understanding
   Journal: Nature Machine Intelligence
   Year: 2023
   Citations: 245
   Open Access: gold
   Aptness Score: 85.50%
   URL: https://doi.org/...
```

## How Aptness is Calculated

The aptness score (0-100%) is calculated based on:
- Keyword matches between input and work keywords
- Topic matches with input keywords
- Open access status matching criteria
- Relevance to subject area

## API Documentation

For more information about OpenAlex API:
- [OpenAlex Works Documentation](https://docs.openalex.org/api-entities/works)
- [Filter Works](https://docs.openalex.org/api-entities/works/filter-works)
- [Search Works](https://docs.openalex.org/api-entities/works/search-works)

## Files

- `fetch_journals.py` - Main script
- `format.json` - Input criteria
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (not tracked by git)
- `.env.example` - Example environment file
- `.gitignore` - Git ignore rules
- `results.json` - Output file (generated after running)

## Notes

- The acceptance percentage range allows ±5% flexibility in searches
- OpenAlex API is free but rate-limited
- Using an API key and email improves rate limits
- Results are sorted by citation count and relevance
