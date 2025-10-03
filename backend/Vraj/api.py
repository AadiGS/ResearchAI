"""
API Module for ResearchAI Backend
This module can be imported by the frontend to process research paper inputs
"""

from run import process_user_input
import json


def process_research_paper(input_data: dict, trigger_search: bool = True) -> dict:
    """
    Main API function to be called from frontend
    
    Args:
        input_data: Dictionary with keys:
            - subjectArea: str (can use abbreviations like "DL", "NLP", etc.)
            - title: str (can have spelling mistakes/abbreviations)
            - abstract: str (can have spelling mistakes/abbreviations)
            - accPercentFrom: int (0-100)
            - accPercentTo: int (0-100)
            - openAccess: str/bool/int ("yes"/"no", True/False, 1/0)
        
        trigger_search: bool (default: True)
            - True: Runs both Vraj's refinement AND Aadi's journal search
            - False: Only runs Vraj's refinement
    
    Returns:
        Dictionary containing:
            - refined_output: The refined/corrected input
            - refined_output_path: Path to saved refined output
            - final_results: Top 3 journals (if trigger_search=True)
            - final_results_path: Path to final results (if trigger_search=True)
    
    Example:
        >>> input_data = {
        ...     "subjectArea": "ML",
        ...     "title": "CNN for Image Clasification",
        ...     "abstract": "We use deep lerning for CV tasks...",
        ...     "accPercentFrom": 40,
        ...     "accPercentTo": 70,
        ...     "openAccess": "yes"
        ... }
        >>> result = process_research_paper(input_data)
        >>> print(result['refined_output']['subjectArea'])
        'machine learning'
        >>> print(len(result['final_results']))
        3
    """
    return process_user_input(input_data, trigger_search)


def process_from_json_file(filepath: str, trigger_search: bool = True) -> dict:
    """
    Process input from a JSON file
    
    Args:
        filepath: Path to JSON file containing input data
        trigger_search: Whether to trigger journal search
    
    Returns:
        Same as process_research_paper()
    """
    with open(filepath, 'r') as f:
        input_data = json.load(f)
    
    return process_user_input(input_data, trigger_search)


# For direct import usage
__all__ = ['process_research_paper', 'process_from_json_file']
