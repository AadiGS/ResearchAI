import os
import json
import google.generativeai as genai
from typing import Dict, Any

class PaperSearchBackend:
    def __init__(self, api_key: str):
        """
        Initialize the backend with Gemini API key
        
        Args:
            api_key: Your Gemini API key
        """
        genai.configure(api_key=api_key)
        # Use Gemini 2.0 Flash - fast and reliable
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
    def load_format_reference(self, format_file_path: str = "format.json") -> Dict:
        """
        Load the format.json file to understand the proper terminology
        
        Args:
            format_file_path: Path to the format.json file
            
        Returns:
            Dictionary containing the format reference
        """
        try:
            with open(format_file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {format_file_path} not found. Using default format.")
            return {
                "subjectArea": "artificial Intelligence",
                "keywords": [
                    "machine learning", "deep learning", "neural networks",
                    "natural language processing", "computer vision",
                    "reinforcement learning", "generative AI", "transformer models",
                    "large language models", "artificial intelligence",
                    "supervised learning", "unsupervised learning",
                    "convolutional neural networks", "recurrent neural networks",
                    "transfer learning", "explainable AI", "AI ethics",
                    "automation", "data mining", "pattern recognition"
                ]
            }
    
    def refine_text_with_gemini(self, text: str, field_name: str, format_reference: Dict) -> str:
        """
        Use Gemini API to refine text by correcting spelling mistakes and expanding short forms
        
        Args:
            text: Input text to refine
            field_name: Name of the field (title, abstract, subjectArea)
            format_reference: Reference format from format.json
            
        Returns:
            Refined text
        """
        # Create context from format.json keywords for better refinement
        keywords_context = ", ".join(format_reference.get("keywords", []))
        subject_area = format_reference.get("subjectArea", "")
        
        prompt = f"""You are a text refinement assistant for academic paper searches. Your task is to refine the following {field_name}.

Context: This is related to {subject_area}. Common terms include: {keywords_context}

Input text: "{text}"

Instructions:
1. Fix ALL spelling mistakes (papr → paper, presants → presents, etc.)
2. Expand ALL abbreviations and short forms to their full forms:
   - ML → machine learning
   - AI → artificial intelligence
   - NLP → natural language processing
   - DL → deep learning
   - CNN → convolutional neural networks
   - RNN → recurrent neural networks
   - CV → computer vision
   - GPU → graphics processing unit
   - LLM → large language model
   - RL → reinforcement learning
   - etc.
3. IMPORTANT: Only expand abbreviations, do NOT change "AI and ML" to "Artificial Intelligence and Machine Learning" - change it to "artificial intelligence and machine learning" (lowercase, just expanded)
4. Keep the original structure and meaning intact
5. Use proper academic terminology
6. Maintain professional language
7. Do NOT add extra information or change the core content
8. Return ONLY the refined text, nothing else (no explanations, no quotes, no markdown)

Refined text:"""

        try:
            response = self.model.generate_content(prompt)
            refined_text = response.text.strip()
            # Remove any quotes that might be added
            refined_text = refined_text.strip('"').strip("'").strip('`')
            # Remove markdown code blocks if present
            if refined_text.startswith('```'):
                lines = refined_text.split('\n')
                refined_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else refined_text
            return refined_text
        except Exception as e:
            print(f"Error refining {field_name}: {e}")
            return text  # Return original text if refinement fails
    
    def extract_keywords_with_gemini(self, text: str, format_reference: Dict) -> list:
        """
        Extract relevant keywords from the title and abstract using Gemini API
        
        Args:
            text: Combined title and abstract text
            format_reference: Reference format from format.json
            
        Returns:
            List of extracted keywords
        """
        keywords_context = ", ".join(format_reference.get("keywords", []))
        
        prompt = f"""Extract the most relevant technical keywords and terms from the following academic text.

Context: Common AI/ML terms include: {keywords_context}

Text: "{text}"

Instructions:
1. Extract EXACTLY 15-20 most relevant technical keywords and phrases for maximum search precision
2. Use lowercase for all terms (e.g., "machine learning", "deep learning", "artificial intelligence")
3. Expand ALL abbreviations to full forms (AI → artificial intelligence, ML → machine learning, DL → deep learning, NLP → natural language processing, etc.)
4. Include NO abbreviations in the keywords - only full expanded terms
5. Focus on technical terms, methodologies, technologies, and research areas
6. Include variations and related terms for better search coverage
7. Return ONLY a comma-separated list of keywords, nothing else (no numbering, no explanations)

Keywords:"""

        try:
            response = self.model.generate_content(prompt)
            keywords_text = response.text.strip()
            # Remove any quotes or formatting
            keywords_text = keywords_text.strip('"').strip("'").strip('`')
            # Remove markdown formatting if present
            if keywords_text.startswith('```'):
                lines = keywords_text.split('\n')
                keywords_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else keywords_text
            # Split by comma and clean each keyword
            keywords = [k.strip() for k in keywords_text.split(',') if k.strip()]
            
            # Ensure we have at least 15 keywords
            if len(keywords) < 15:
                # Add default keywords from format reference if needed
                default_keywords = format_reference.get("keywords", [])
                for kw in default_keywords:
                    if kw not in keywords and len(keywords) < 20:
                        keywords.append(kw)
            
            # Return 15-20 keywords
            return keywords[:20]
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            # Return default keywords from format reference
            return format_reference.get("keywords", [])[:10]
    
    def validate_percentage(self, from_percent: int, to_percent: int) -> tuple:
        """
        Validate and ensure percentage values are integers between 0-100
        
        Args:
            from_percent: Starting percentage
            to_percent: Ending percentage
            
        Returns:
            Tuple of validated (from_percent, to_percent)
        """
        # Convert to int if needed
        from_percent = int(from_percent)
        to_percent = int(to_percent)
        
        # Clamp values between 0 and 100
        from_percent = max(0, min(100, from_percent))
        to_percent = max(0, min(100, to_percent))
        
        # Ensure from is less than or equal to to
        if from_percent > to_percent:
            from_percent, to_percent = to_percent, from_percent
            
        return from_percent, to_percent
    
    def convert_openaccess(self, openaccess_input: Any) -> int:
        """
        Convert open access input to 1 (yes) or 0 (no)
        
        Args:
            openaccess_input: Can be boolean, string, or int
            
        Returns:
            1 for yes/true, 0 for no/false
        """
        if isinstance(openaccess_input, bool):
            return 1 if openaccess_input else 0
        elif isinstance(openaccess_input, str):
            return 1 if openaccess_input.lower() in ['yes', 'true', '1', 'y'] else 0
        elif isinstance(openaccess_input, int):
            return 1 if openaccess_input > 0 else 0
        else:
            return 0
    
    def process_input(self, input_data: Dict, format_file_path: str = "format.json") -> Dict:
        """
        Main processing function that takes input JSON and returns refined output JSON
        
        Args:
            input_data: Dictionary with keys: subjectArea, title, abstract, accPercentFrom, accPercentTo, openAccess
            format_file_path: Path to format.json file
            
        Returns:
            Dictionary with refined inputs in the required format
        """
        print("="*60)
        print("STARTING REFINEMENT PROCESS")
        print("="*60)
        
        # Load format reference
        print("\n[1/7] Loading format reference...")
        format_reference = self.load_format_reference(format_file_path)
        
        # Refine subject area
        print("[2/7] Refining subject area...")
        refined_subject = self.refine_text_with_gemini(
            input_data.get("subjectArea", ""), 
            "subject area", 
            format_reference
        )
        
        # Refine title
        print("[3/7] Refining title...")
        refined_title = self.refine_text_with_gemini(
            input_data.get("title", ""), 
            "title", 
            format_reference
        )
        
        # Refine abstract
        print("[4/7] Refining abstract...")
        refined_abstract = self.refine_text_with_gemini(
            input_data.get("abstract", ""), 
            "abstract", 
            format_reference
        )
        
        # Extract keywords from title and abstract
        print("[5/7] Extracting keywords...")
        combined_text = f"{refined_title}. {refined_abstract}"
        keywords = self.extract_keywords_with_gemini(combined_text, format_reference)
        
        # Validate percentages
        print("[6/7] Validating acceptance percentages...")
        validated_from, validated_to = self.validate_percentage(
            input_data.get("accPercentFrom", 0),
            input_data.get("accPercentTo", 100)
        )
        
        # Convert open access
        print("[7/7] Converting open access value...")
        openaccess_value = self.convert_openaccess(input_data.get("openAccess", 0))
        
        # Build output with the required format
        result = {
            "subjectArea": refined_subject,
            "keywords": keywords,
            "openAccess": openaccess_value,
            "acceptancePercentFrom": validated_from,
            "acceptancePercentTo": validated_to
        }
        
        print("\n" + "="*60)
        print("REFINEMENT COMPLETE!")
        print("="*60)
        
        return result