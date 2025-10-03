
import requests
import json
import os
from dotenv import load_dotenv
from typing import List, Dict, Any
import time

# Load environment variables
load_dotenv()

class OpenAlexJournalFetcher:
    """Fetch research journals from OpenAlex API based on input criteria."""
    
    def __init__(self):
        self.api_key = os.getenv('OPENALEX_API_KEY', '')
        self.email = os.getenv('OPENALEX_EMAIL', '')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY', '')
        self.base_url = "https://api.openalex.org/works"
        # Use gemini-2.0-flash for reliable text generation
        self.gemini_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
    def load_search_criteria(self, format_file: str = 'format.json') -> Dict[str, Any]:
        """Load search criteria from format.json file."""
        with open(format_file, 'r') as f:
            return json.load(f)
    
    def build_query_params(self, criteria: Dict[str, Any]) -> Dict[str, str]:
        """
        Build OpenAlex API query parameters based on input criteria.
        
        Args:
            criteria: Dictionary containing search criteria from format.json
                - subjectArea: Subject area for filtering
                - keywords: List of 15-20 keywords
                - openAccess: 1 for open access, 0 for non-open access
                - acceptancePercentFrom: Lower bound of acceptance percentage
                - acceptancePercentTo: Upper bound of acceptance percentage
        
        Returns:
            Dictionary of query parameters for the API
        """
        params = {}
        
        # Add email for polite pool (better rate limits)
        if self.email:
            params['mailto'] = self.email
        
        # Build filter string
        filters = []
        
        # Open Access filter
        if criteria.get('openAccess') == 1:
            filters.append('is_oa:true')
        elif criteria.get('openAccess') == 0:
            filters.append('is_oa:false')
        
        # Filter by primary location source type (journal)
        filters.append('primary_location.source.type:journal')
        
        # Combine all filters
        if filters:
            params['filter'] = ','.join(filters)
        
        # Search query - combine subject area and keywords
        search_terms = []
        
        if criteria.get('subjectArea'):
            search_terms.append(criteria['subjectArea'])
        
        if criteria.get('keywords'):
            # Use first 10 keywords to avoid overly long query
            keywords_str = ' OR '.join(criteria['keywords'][:10])
            search_terms.append(f"({keywords_str})")
        
        if search_terms:
            params['search'] = ' '.join(search_terms)
        
        # Sort by relevance and citation count
        params['sort'] = 'cited_by_count:desc'
        
        # Limit results to get top 15 most relevant
        params['per_page'] = '15'
        
        return params
    
    def fetch_journals(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Fetch research journals from OpenAlex API.
        
        Args:
            criteria: Search criteria from format.json
        
        Returns:
            List of journal works matching the criteria
        """
        params = self.build_query_params(criteria)
        
        # Add API key if available
        if self.api_key:
            params['api_key'] = self.api_key
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            results = data.get('results', [])
            
            # Extract relevant information from each work
            journals = []
            for work in results:
                journal_info = {
                    'id': work.get('id'),
                    'title': work.get('display_name'),
                    'doi': work.get('doi'),
                    'publication_year': work.get('publication_year'),
                    'cited_by_count': work.get('cited_by_count'),
                    'is_open_access': work.get('open_access', {}).get('is_oa'),
                    'oa_status': work.get('open_access', {}).get('oa_status'),
                    'journal_name': work.get('primary_location', {}).get('source', {}).get('display_name'),
                    'journal_issn': work.get('primary_location', {}).get('source', {}).get('issn'),
                    'abstract': work.get('abstract_inverted_index'),
                    'topics': [topic.get('display_name') for topic in work.get('topics', [])],
                    'keywords': [kw.get('keyword') for kw in work.get('keywords', [])],
                    'url': work.get('primary_location', {}).get('landing_page_url'),
                }
                journals.append(journal_info)
            
            return journals
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from OpenAlex API: {e}")
            return []
    
    def calculate_aptness_score(self, work: Dict[str, Any], criteria: Dict[str, Any]) -> float:
        """
        Calculate aptness score based on keyword matching, recency, and criteria.
        
        Scoring breakdown:
        - Keyword/Topic matching: 60% (0-60 points)
        - Recency: 25% (0-25 points) - Papers from last 5 years get full points
        - Open access match: 15% (0-15 points)
        
        Args:
            work: Individual work/journal data
            criteria: Search criteria
        
        Returns:
            Aptness score (0-100)
        """
        score = 0.0
        input_keywords = set(kw.lower() for kw in criteria.get('keywords', []) if kw)
        
        # 1. Keyword and Topic Matching (60 points max)
        work_keywords = set(kw.lower() for kw in work.get('keywords', []) if kw)
        keyword_matches = len(input_keywords.intersection(work_keywords))
        
        work_topics = set(topic.lower() for topic in work.get('topics', []) if topic)
        topic_keywords = ' '.join(work_topics)
        topic_matches = sum(1 for kw in input_keywords if kw in topic_keywords)
        
        total_matches = keyword_matches + topic_matches
        max_possible = len(input_keywords)
        
        if max_possible > 0:
            relevance_score = (total_matches / max_possible) * 60
            score += relevance_score
        
        # 2. Recency Score (25 points max)
        # Papers from last 5 years get full points, older papers get diminishing scores
        current_year = 2025
        pub_year = work.get('publication_year')
        
        if pub_year:
            years_old = current_year - pub_year
            if years_old <= 5:
                # Recent papers (0-5 years): Full 25 points
                recency_score = 25
            elif years_old <= 10:
                # 6-10 years old: Linear decay from 25 to 15 points
                recency_score = 25 - ((years_old - 5) * 2)
            elif years_old <= 20:
                # 11-20 years old: Linear decay from 15 to 5 points
                recency_score = 15 - ((years_old - 10) * 1)
            else:
                # Older than 20 years: 5 points minimum
                recency_score = 5
            
            score += recency_score
        
        # 3. Open Access Match (15 points)
        if work.get('is_open_access') == bool(criteria.get('openAccess')):
            score += 15
        
        return min(score, 100)  # Cap at 100
    
    def rank_and_filter_journals(self, journals: List[Dict[str, Any]], 
                                 criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Rank journals by aptness score and return top 15.
        
        Args:
            journals: List of journal data
            criteria: Search criteria
        
        Returns:
            Top 15 most apt journals with aptness scores
        """
        # Calculate aptness score for each journal
        for journal in journals:
            journal['aptness_score'] = self.calculate_aptness_score(journal, criteria)
        
        # Sort by aptness score descending
        ranked_journals = sorted(journals, key=lambda x: x['aptness_score'], reverse=True)
        
        # Return top 15
        return ranked_journals[:15]
    
    def save_results(self, journals: List[Dict[str, Any]], output_file: str = 'results.json'):
        """Save fetched journals to a JSON file (overwrites existing file)."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(journals, f, indent=2, ensure_ascii=False)
        print(f"Results saved to {output_file}")
    
    def reconstruct_abstract(self, inverted_index: Dict[str, List[int]]) -> str:
        """
        Reconstruct abstract from inverted index format.
        
        Args:
            inverted_index: Dictionary mapping words to their positions
        
        Returns:
            Reconstructed abstract text
        """
        if not inverted_index:
            return None
        
        try:
            # Create a list to hold words at each position
            word_positions = []
            for word, positions in inverted_index.items():
                for pos in positions:
                    word_positions.append((pos, word))
            
            # Sort by position and join words
            word_positions.sort(key=lambda x: x[0])
            abstract = ' '.join([word for _, word in word_positions])
            
            return abstract if abstract else None
        except Exception as e:
            print(f"Error reconstructing abstract: {e}")
            return None
    
    def generate_abstract_with_gemini(self, title: str, journal_name: str, 
                                     year: int, topics: List[str]) -> str:
        """
        Generate abstract using Gemini API REST endpoint when abstract is not available.
        
        Args:
            title: Paper title
            journal_name: Journal name
            year: Publication year
            topics: List of topics
        
        Returns:
            Generated abstract
        """
        if not self.gemini_api_key:
            return "Abstract not available. Please configure GEMINI_API_KEY in .env file."
        
        try:
            # Create prompt for Gemini
            topics_str = ", ".join(topics[:3]) if topics else "research"
            prompt = f"""Write a concise academic abstract (100-150 words) for a research paper with the following details:

Title: {title}
Journal: {journal_name}
Year: {year}
Topics: {topics_str}

The abstract should:
- Summarize the main research objective
- Mention key methodology or approach
- Highlight main findings or contributions
- Use formal academic language
- Be concise and informative

Generate only the abstract text, without any additional commentary."""

            # Use REST API instead of gRPC for better reliability
            headers = {
                'Content-Type': 'application/json',
            }
            
            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 250,
                }
            }
            
            url = f"{self.gemini_api_url}?key={self.gemini_api_key}"
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            # Extract text from response
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0].get('content', {})
                parts = content.get('parts', [])
                if parts and 'text' in parts[0]:
                    abstract = parts[0]['text'].strip()
                    return abstract if abstract else "Abstract not available."
            
            return "Abstract not available."
            
        except requests.exceptions.Timeout:
            print(f"  Timeout generating abstract")
            return "Abstract generation timed out."
        except Exception as e:
            print(f"  Error generating abstract: {str(e)[:100]}")
            return "Abstract generation failed."
    
    def save_final_results(self, journals: List[Dict[str, Any]], criteria: Dict[str, Any], 
                          output_file: str = 'final_result.json'):
        """
        Save top 3 most apt journals to final_result.json with required fields.
        
        Args:
            journals: List of ranked journals
            criteria: Original search criteria
            output_file: Output filename
        """
        # Take top 3 journals
        top_3 = journals[:3]
        
        final_results = []
        for i, journal in enumerate(top_3, 1):
            title = journal.get('title') or 'Untitled'
            print(f"\nProcessing journal {i}/3: {title[:60]}...")
            
            # Try to get abstract from OpenAlex
            abstract = self.reconstruct_abstract(journal.get('abstract'))
            
            # If no abstract available, generate using Gemini
            if not abstract:
                print(f"  No abstract found from OpenAlex")
                # Use Gemini REST API for generation
                if self.gemini_api_key:
                    print(f"  Generating with Gemini...")
                    abstract = self.generate_abstract_with_gemini(
                        title=journal.get('title', 'Untitled'),
                        journal_name=journal.get('journal_name', 'Unknown Journal'),
                        year=journal.get('publication_year', 'Unknown'),
                        topics=journal.get('topics', [])
                    )
                    # Add small delay to avoid rate limiting
                    time.sleep(1)
                else:
                    abstract = "Abstract not available. Configure GEMINI_API_KEY for automatic generation."
            else:
                print(f"  Abstract found from OpenAlex")
            
            result = {
                "title": journal.get('title', 'N/A'),
                "abstract": abstract,
                "publishedYear": journal.get('publication_year', 'N/A'),
                "publishedBy": journal.get('journal_name', 'N/A'),
                "acceptancePercent": {
                    "from": criteria.get('acceptancePercentFrom', 0),
                    "to": criteria.get('acceptancePercentTo', 100)
                },
                "subjectArea": criteria.get('subjectArea', 'N/A'),
                "openAccess": journal.get('oa_status', 'N/A'),
                "citedByCount": journal.get('cited_by_count', 0),
                "doi": journal.get('doi', 'N/A'),
                "url": journal.get('url', 'N/A'),
                "aptnessScore": journal.get('aptness_score', 0),
                "journalISSN": journal.get('journal_issn', []),
                "topics": journal.get('topics', [])
            }
            final_results.append(result)
        
        # Overwrite final_result.json
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Top 3 most apt journals saved to {output_file}")


def main():
    """Main function to fetch and display research journals."""
    fetcher = OpenAlexJournalFetcher()
    
    # Load search criteria from format.json
    print("Loading search criteria from format.json...")
    criteria = fetcher.load_search_criteria()
    
    print(f"\nSearch Criteria:")
    print(f"Subject Area: {criteria.get('subjectArea')}")
    print(f"Keywords: {len(criteria.get('keywords', []))} keywords")
    print(f"Open Access: {'Yes' if criteria.get('openAccess') == 1 else 'No'}")
    print(f"Acceptance %: {criteria.get('acceptancePercentFrom')}-{criteria.get('acceptancePercentTo')}")
    
    # Fetch journals
    print("\nFetching journals from OpenAlex API...")
    journals = fetcher.fetch_journals(criteria)
    
    if not journals:
        print("No journals found matching the criteria.")
        return
    
    # Rank and filter journals
    print(f"\nRanking {len(journals)} journals by aptness...")
    top_journals = fetcher.rank_and_filter_journals(journals, criteria)
    
    # Display results
    print(f"\n{'='*80}")
    print(f"Top {len(top_journals)} Most Apt Research Journals")
    print(f"{'='*80}\n")
    
    for i, journal in enumerate(top_journals, 1):
        print(f"{i}. {journal['title']}")
        print(f"   Journal: {journal.get('journal_name', 'N/A')}")
        print(f"   Year: {journal.get('publication_year', 'N/A')}")
        print(f"   Citations: {journal.get('cited_by_count', 0)}")
        print(f"   Open Access: {journal.get('oa_status', 'N/A')}")
        print(f"   Aptness Score: {journal['aptness_score']:.2f}%")
        print(f"   URL: {journal.get('url', 'N/A')}")
        print()
    
    # Save all results to results.json (overwrites each time)
    fetcher.save_results(top_journals)
    
    # Save top 3 most apt journals to final_result.json
    fetcher.save_final_results(top_journals, criteria)


if __name__ == "__main__":
    main()
