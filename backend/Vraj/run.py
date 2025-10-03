"""
Main Runner Script for Paper Search Backend
This is the entry point for using the backend with your own input
"""

import json
import subprocess
import os
from main import PaperSearchBackend
from config import GEMINI_API_KEY, FORMAT_REFERENCE_FILE, OUTPUT_FILE


def process_single_input(input_data: dict):
    """
    Process a single input and display results
    
    Args:
        input_data: Dictionary containing the paper search input
    """
    print("\n" + "="*80)
    print("PROCESSING INPUT")
    print("="*80)
    
    # Initialize backend
    backend = PaperSearchBackend(GEMINI_API_KEY)
    
    # Display input
    print("\nINPUT DATA:")
    print("-"*80)
    print(json.dumps(input_data, indent=2))
    
    # Process input
    refined_output = backend.process_input(input_data, FORMAT_REFERENCE_FILE)
    
    # Display output
    print("\n" + "="*80)
    print("REFINED OUTPUT (in required format)")
    print("="*80)
    print(json.dumps(refined_output, indent=2))
    
    # Show changes
    print("\n" + "="*80)
    print("CHANGES SUMMARY")
    print("="*80)
    print(f"Subject Area: {input_data.get('subjectArea')} -> {refined_output.get('subjectArea')}")
    print(f"Keywords Extracted: {len(refined_output.get('keywords', []))} keywords")
    print(f"Open Access: {input_data.get('openAccess')} -> {refined_output.get('openAccess')}")
    
    # Save output
    with open(OUTPUT_FILE, "w") as f:
        json.dump(refined_output, f, indent=2)
    
    print("\n" + "="*80)
    print(f"[SUCCESS] Output saved to: {OUTPUT_FILE}")
    print("="*80)
    
    # Automatically run Aadi's fetch_journals.py
    print("\n" + "="*80)
    print("TRIGGERING JOURNAL SEARCH (Aadi's Backend)")
    print("="*80)
    
    aadi_script_path = os.path.join(os.path.dirname(__file__), "..", "Aadi", "fetch_journals.py")
    aadi_dir = os.path.join(os.path.dirname(__file__), "..", "Aadi")
    
    try:
        # Run fetch_journals.py from Aadi directory
        result = subprocess.run(
            ["python", "fetch_journals.py"],
            cwd=aadi_dir,
            capture_output=True,
            text=True
        )
        
        # Display output from Aadi's script
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("Errors/Warnings:", result.stderr)
        
        if result.returncode == 0:
            print("\n" + "="*80)
            print("[SUCCESS] Journal search completed!")
            print("="*80)
        else:
            print("\n" + "="*80)
            print(f"[ERROR] Journal search failed with code {result.returncode}")
            print("="*80)
            
    except Exception as e:
        print(f"\n[ERROR] Failed to run fetch_journals.py: {e}")
    
    return refined_output


def main():
    """
    Main function - Modify the input_data here to test different scenarios
    """
    
    # ==================== CONFIGURE YOUR INPUT HERE ====================
    # You can modify this dictionary to test different inputs
    
    input_data = {
        "subjectArea": "DL",
        "title": "A Graph-Attention-Based Deep Learning Network for Predicting Biotech–Small-Molecule Drug Interactions",
        "abstract": "The increasing demand for effective drug combinations has made drug-drug interaction (DDI) prediction a critical task in modern pharmacology. While most existing research focuses on small-molecule drugs, the role of biotech drugs in complex disease treatments remains relatively unexplored. Biotech drugs, derived from biological sources, have unique molecular structures that differ significantly from those of small molecules, making their interactions more challenging to predict. This study introduces BSI-Net, a novel graph attention network-based deep learning framework that improves interaction prediction between biotech and small-molecule drugs. Experimental results demonstrate that BSI-Net outperforms existing methods in multi-class DDI prediction, achieving superior performance across various evaluation types, including micro, macro, and weighted assessments. These findings highlight the potential of deep learning and graph-based models in uncovering novel interactions between biotech and small-molecule drugs, paving the way for more effective combination therapies in drug discovery.",
        "accPercentFrom": 65,
        "accPercentTo": 95,
        "openAccess": "yes"
    }
    
    # ===================================================================
    
    # Process the input
    process_single_input(input_data)


# Example alternative inputs (uncomment to use):

def example_1():
    """Computer Vision Example"""
    input_data = {
        "subjectArea": "CV and DL",
        "title": "CNN Architectures for Real-Time Object Detection",
        "abstract": "We explore CNN and RNN for CV tasks with GPU accelaration for real-time procesing.",
        "accPercentFrom": 30,
        "accPercentTo": 50,
        "openAccess": True
    }
    process_single_input(input_data)


def example_2():
    """NLP Chatbot Example"""
    input_data = {
        "subjectArea": "NLP and AI",
        "title": "Enhancing Chatbot Performence Through Advanced NLU",
        "abstract": "This reasearch focusses on improving chatbot performence using transformr models like BERT and GPT.",
        "accPercentFrom": 25,
        "accPercentTo": 45,
        "openAccess": "yes"
    }
    process_single_input(input_data)


def example_3():
    """Reinforcement Learning Example"""
    input_data = {
        "subjectArea": "RL and AI",
        "title": "RL Agents for Complex Task Planning",
        "abstract": "We develop RL agents using deep Q-networks and policy gradient methods for multi-agent environments.",
        "accPercentFrom": 40,
        "accPercentTo": 60,
        "openAccess": 1
    }
    process_single_input(input_data)


def load_from_json_file(filepath: str):
    """
    Load input from a JSON file and process it
    
    Args:
        filepath: Path to the JSON file containing input data
    """
    try:
        with open(filepath, 'r') as f:
            input_data = json.load(f)
        process_single_input(input_data)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file '{filepath}'")


if __name__ == "__main__":
    # Run the main function with the configured input
    main()
    
    # Uncomment any of these to run specific examples:
    # example_1()
    # example_2()
    # example_3()
    
    # Uncomment to load from a JSON file:
    # load_from_json_file("my_input.json")
