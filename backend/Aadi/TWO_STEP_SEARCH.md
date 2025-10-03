# Two-Step Journal Search Strategy

## Overview

The new `find_top_journals()` function implements a sophisticated two-step strategy for finding the most relevant academic journals for your research.

## How It Works

### **Step 1: Find Highly-Cited Papers**
- Searches OpenAlex for the top 30 most-cited papers matching your query
- Uses the `/works` endpoint with citation-based sorting
- Filters for journal publications only

### **Step 2: Aggregate and Rank Journals**
- Extracts all unique journals from those 30 papers
- Counts how many times each journal appears (relevance)
- Fetches detailed journal metadata from `/sources` endpoint
- Calculates a comprehensive score for each journal
- Returns the top 3 highest-scoring journals

---

## Scoring Algorithm

Each journal receives a score from 0-100 based on four factors:

### 1. **Relevance Score (40 points)**
- How many times the journal appeared in the top 30 papers
- Formula: `min(relevance / 10, 1.0) × 40`
- Example: If a journal appeared 6 times → (6/10) × 40 = 24 points

### 2. **h-index Score (30 points)**
- Measures journal's impact and influence
- Formula: `min(h_index / 200, 1.0) × 30`
- Top journals have h-index of 200+
- Example: h-index of 500 → 30 points (capped)

### 3. **Citation Count Score (20 points)**
- Total number of citations received by the journal
- Formula: `min(cited_by_count / 100,000, 1.0) × 20`
- Example: 1.7M citations → 20 points (capped)

### 4. **Open Access Bonus (10 points)**
- Checks if journal supports open access
- Full 10 points if journal is in DOAJ or supports OA
- 0 points otherwise

---

## Usage

### Basic Usage

```python
from fetch_journals import OpenAlexJournalFetcher

fetcher = OpenAlexJournalFetcher()

# Search for journals
top_journals = fetcher.find_top_journals(
    search_query="deep learning neural networks",
    email="your.email@example.com"
)

# Display results
for journal in top_journals:
    print(f"{journal['journal_name']} - Score: {journal['calculated_score']}")
```

### Command Line

```bash
# Edit fetch_journals.py to uncomment test_two_step_journal_search()
cd backend/Aadi
python fetch_journals.py
```

---

## Example Output

```json
{
  "journal_name": "Nature",
  "issn": ["0028-0836", "1476-4687"],
  "publisher": "Nature Portfolio",
  "homepage_url": "https://www.nature.com/nature/",
  "h_index": 1795,
  "cited_by_count": 25578329,
  "works_count": 431710,
  "is_open_access": false,
  "is_in_doaj": false,
  "relevance_count": 6,
  "calculated_score": 74.0,
  "openalex_id": "https://openalex.org/S137773608",
  "type": "journal"
}
```

### Key Metrics Explained

- **relevance_count**: How many of the top 30 papers were published in this journal
- **calculated_score**: Overall score (0-100) based on the algorithm
- **h_index**: Journal's h-index (higher = more impactful)
- **cited_by_count**: Total citations across all journal publications
- **works_count**: Total number of papers published

---

## Advantages Over Single-Step Search

### Traditional Approach (Old)
- Searches for papers directly
- Ranks papers by individual metrics
- May miss prestigious journals with few matches

### Two-Step Approach (New)
- Finds the journals where top research is published
- Aggregates multiple papers per journal
- Weights both relevance AND prestige
- More likely to find high-impact venues

---

## Real-World Example

**Query:** `"deep learning neural networks"`

### Results:
1. **Nature** - Score: 74/100
   - Appeared 6 times in top 30 papers
   - h-index: 1795 (extremely prestigious)
   - 25M+ citations

2. **IEEE TPAMI** - Score: 74/100
   - Appeared 6 times in top 30 papers
   - h-index: 542 (highly specialized, top-tier)
   - 1.7M+ citations

3. **Neural Networks** - Score: 58/100
   - Appeared 2 times in top 30 papers
   - h-index: 244 (solid journal)
   - 436K citations

---

## When to Use This Method

✅ **Best For:**
- Finding prestigious journals in your field
- Discovering where similar work is published
- Identifying high-impact venues
- General topic searches (e.g., "machine learning", "cancer research")

❌ **Not Ideal For:**
- Very specific niche topics
- New/emerging research areas
- When you need journals with specific acceptance rates
- Ultra-specialized sub-fields with limited publications

---

## Technical Details

### API Endpoints Used

1. **Works Endpoint:**
   ```
   GET https://api.openalex.org/works
   Parameters:
   - search: query string
   - per_page: 30
   - sort: cited_by_count:desc
   - filter: primary_location.source.type:journal
   ```

2. **Sources Endpoint:**
   ```
   GET https://api.openalex.org/sources
   Parameters:
   - filter: ids.openalex:ID1|ID2|ID3
   - per_page: number of unique journals
   ```

### Performance
- **Speed:** ~3-5 seconds for typical queries
- **API Calls:** 2 (one for works, one for sources)
- **Rate Limit:** Benefits from polite pool with email

---

## Function Signatures

### `find_top_journals(search_query: str, email: str) -> List[Dict]`
Main function that executes the two-step strategy.

**Args:**
- `search_query`: Search terms (e.g., "artificial intelligence ethics")
- `email`: Your email for OpenAlex polite pool

**Returns:**
- List of 3 dictionaries with formatted journal data

### `calculate_journal_score(journal: Dict, relevance: int) -> float`
Calculates the 0-100 score for a journal.

**Args:**
- `journal`: Raw journal data from OpenAlex
- `relevance`: Number of times journal appeared in top 30

**Returns:**
- Float score between 0-100

### `format_journal_output(journal: Dict) -> Dict`
Formats journal data for clean output.

**Args:**
- `journal`: Raw journal data with score

**Returns:**
- Dictionary with standardized fields

---

## Comparison: Two-Step vs. Original Method

| Aspect | Original Method | Two-Step Method |
|--------|----------------|-----------------|
| **Search Target** | Individual papers | Journals (aggregated) |
| **Ranking** | Paper-level metrics | Journal-level prestige |
| **Relevance** | Keyword matching | Citation-based discovery |
| **Best For** | Specific paper search | Finding publication venues |
| **Output** | Top 3 papers | Top 3 journals |
| **Score Focus** | Recency + keywords | Impact + relevance |

---

## Future Enhancements

Potential improvements for this method:

1. **Acceptance Rate Integration:**
   - Add filter for journal acceptance rates
   - Weight score by acceptance difficulty

2. **Field-Specific Normalization:**
   - Adjust h-index thresholds by field
   - Different citation count expectations per discipline

3. **Author Network Analysis:**
   - Consider where similar researchers publish
   - Weight journals by author reputation

4. **Temporal Trends:**
   - Favor journals with growing citation rates
   - Identify emerging high-impact venues

---

## Troubleshooting

### No Results Returned
- Check if search query is too narrow
- Verify internet connection
- Ensure email is configured in `.env`

### Low Scores for All Journals
- Query might be too broad
- Consider more specific keywords
- Try different search terms

### Missing Journal Metadata
- Some journals may have incomplete data in OpenAlex
- Score calculation handles missing fields gracefully

---

## Credits

- **OpenAlex API:** https://openalex.org/
- **Scoring Algorithm:** Custom implementation based on bibliometric principles
- **Implementation:** Part of the ResearchAI project

---

**Last Updated:** January 3, 2025
