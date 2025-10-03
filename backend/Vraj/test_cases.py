"""
Comprehensive Test Cases for Paper Search Backend
Run this file to test various input scenarios and verify the refinement functionality
"""

import json
from main import PaperSearchBackend
from config import GEMINI_API_KEY, FORMAT_REFERENCE_FILE, OUTPUT_FILE


class TestCases:
    def __init__(self):
        """Initialize the test suite"""
        self.backend = PaperSearchBackend(GEMINI_API_KEY)
        self.test_results = []
        
    def print_test_header(self, test_number: int, test_name: str):
        """Print formatted test header"""
        print("\n" + "="*80)
        print(f"TEST CASE #{test_number}: {test_name}")
        print("="*80)
    
    def print_comparison(self, input_data: dict, output_data: dict):
        """Print side-by-side comparison of input and output"""
        print("\n" + "-"*80)
        print("INPUT (with errors/abbreviations):")
        print("-"*80)
        print(json.dumps(input_data, indent=2))
        
        print("\n" + "-"*80)
        print("OUTPUT (refined - in required format):")
        print("-"*80)
        print(json.dumps(output_data, indent=2))
        
        # Show what was refined
        print("\n" + "-"*80)
        print("CHANGES MADE:")
        print("-"*80)
        if "subjectArea" in input_data:
            print(f"Subject Area:")
            print(f"  Before: {input_data.get('subjectArea')}")
            print(f"  After:  {output_data.get('subjectArea')}")
        if "keywords" in output_data:
            print(f"Keywords Extracted: {len(output_data.get('keywords', []))} keywords")
            print(f"  {', '.join(output_data.get('keywords', [])[:5])}...")
        print("-"*80)
    
    def run_test(self, test_number: int, test_name: str, input_data: dict):
        """Run a single test case"""
        self.print_test_header(test_number, test_name)
        
        try:
            output_data = self.backend.process_input(input_data, FORMAT_REFERENCE_FILE)
            self.print_comparison(input_data, output_data)
            
            # Store result
            self.test_results.append({
                "test_number": test_number,
                "test_name": test_name,
                "status": "PASSED",
                "input": input_data,
                "output": output_data
            })
            
            print(f"\n✓ Test #{test_number} PASSED")
            return output_data
            
        except Exception as e:
            print(f"\n✗ Test #{test_number} FAILED")
            print(f"Error: {str(e)}")
            
            self.test_results.append({
                "test_number": test_number,
                "test_name": test_name,
                "status": "FAILED",
                "error": str(e),
                "input": input_data
            })
            return None
    
    def test_1_typical_errors(self):
        """Test Case 1: Typical spelling errors and abbreviations"""
        input_data = {
            "subjectArea": "AI and ML",
            "title": "DL Aproaches for Enhanced NLP Understanding in LLMs",
            "abstract": "This papr presants a comprehensive investigaton into advanced DL architectures for improving NLP capabilities in modern LLMs. We propose a novel transfomer-based framwork that integrates atention mechanisms with contextual embedings to achive superior performence in semantic comprehension taskz.",
            "accPercentFrom": 15,
            "accPercentTo": 25,
            "openAccess": "yes"
        }
        return self.run_test(1, "Typical Spelling Errors & Abbreviations", input_data)
    
    def test_2_multiple_abbreviations(self):
        """Test Case 2: Multiple technical abbreviations"""
        input_data = {
            "subjectArea": "CV and DL",
            "title": "CNN and RNN Approaches for Real-Time Object Detection",
            "abstract": "We explore CNN architectures combined with RNN for CV tasks. Our aproach uses GPU accelaration for real-time procesing. The model achievs sota results on standard benchmarks using transfer learing techniques.",
            "accPercentFrom": 30,
            "accPercentTo": 50,
            "openAccess": True  # Boolean input
        }
        return self.run_test(2, "Multiple Technical Abbreviations", input_data)
    
    def test_3_minimal_errors(self):
        """Test Case 3: Minimal errors, mostly correct input"""
        input_data = {
            "subjectArea": "Natural Language Processing",
            "title": "Advanced Transformer Models for Sentiment Analisys",
            "abstract": "This research presents state-of-the-art transformer models specifically designed for sentiment analysis tasks. We demonstrate significant improvements in accuracy and processing speed compared to traditional methods.",
            "accPercentFrom": 40,
            "accPercentTo": 60,
            "openAccess": 1  # Integer input
        }
        return self.run_test(3, "Minimal Errors (Mostly Correct)", input_data)
    
    def test_4_extensive_errors(self):
        """Test Case 4: Extensive spelling and grammatical errors"""
        input_data = {
            "subjectArea": "Artifical Inteligence and Data Sciance",
            "title": "Machene Lerning Algorthms for Predective Analystics",
            "abstract": "This studie investigates varios ML algorthms for predective analystics in big data enviroments. We prpose a hybid aproach that combins supervized and unsupervized learing techniqes to achive beter accuarcy and efficency in data procesing tasks.",
            "accPercentFrom": 10,
            "accPercentTo": 30,
            "openAccess": "no"
        }
        return self.run_test(4, "Extensive Spelling Errors", input_data)
    
    def test_5_edge_case_percentages(self):
        """Test Case 5: Edge cases for percentage validation"""
        input_data = {
            "subjectArea": "Reinforcement Learning",
            "title": "RL Agents for Complex Task Planning",
            "abstract": "We develop RL agents capable of complex task planning using deep Q-networks and policy gradient methods. Our agents demonstrate superior performance in multi-agent environments.",
            "accPercentFrom": 150,  # Invalid: > 100
            "accPercentTo": -10,    # Invalid: < 0
            "openAccess": "maybe"  # Invalid string
        }
        return self.run_test(5, "Edge Cases - Invalid Percentages", input_data)
    
    def test_6_reversed_percentages(self):
        """Test Case 6: Reversed percentage values"""
        input_data = {
            "subjectArea": "Computer Vision",
            "title": "Image Segmentation using Deep Neural Networks",
            "abstract": "This paper explores advanced image segmentation techniques using deep neural networks. We achieve state-of-the-art results on multiple benchmark datasets.",
            "accPercentFrom": 80,  # Higher than 'to'
            "accPercentTo": 20,    # Lower than 'from'
            "openAccess": 0
        }
        return self.run_test(6, "Reversed Percentage Values", input_data)
    
    def test_7_empty_fields(self):
        """Test Case 7: Empty or minimal text fields"""
        input_data = {
            "subjectArea": "ML",
            "title": "AI Research",
            "abstract": "Study of AI.",
            "accPercentFrom": 0,
            "accPercentTo": 100,
            "openAccess": "yes"
        }
        return self.run_test(7, "Empty/Minimal Text Fields", input_data)
    
    def test_8_real_world_example(self):
        """Test Case 8: Real-world example with common mistakes"""
        input_data = {
            "subjectArea": "NLP and AI",
            "title": "Enhancing Chatbot Performence Through Advanced NLU Techniques",
            "abstract": "This reasearch focusses on improving chatbot performence by implementing advanced Natural Language Understanding techniqes. We utilize transformr models, specifically BERT and GPT variants, to enhance the conversational AI's ability to understand context and intent. Our experimental results show a 35% improvment in user satisfaction scores compared to baseline chatbots.",
            "accPercentFrom": 25,
            "accPercentTo": 45,
            "openAccess": "Yes"  # Capitalized
        }
        return self.run_test(8, "Real-World Chatbot Research Example", input_data)
    
    def test_9_academic_paper(self):
        """Test Case 9: Academic paper with complex terminology"""
        input_data = {
            "subjectArea": "Deep Learning and Computer Vision",
            "title": "Multi-Modal Fusion for Enhanced Image Captioning using CNN-RNN Architectures",
            "abstract": "This papr introduces a novel multi-modal fusion framwork for image captioning that combines CNN for image feature extraction and RNN for sequence generation. Our aproach incorporates atention mechanisms to focuse on relevent image regions during caption generation. Extensive experimants on COCO and Flickr30k datasets demonstrate that our method outperforms exisitng state-of-the-art techniques by 12% in BLEU score.",
            "accPercentFrom": 35,
            "accPercentTo": 55,
            "openAccess": True
        }
        return self.run_test(9, "Academic Paper - Complex Terminology", input_data)
    
    def test_10_mixed_case_sensitivity(self):
        """Test Case 10: Mixed case sensitivity issues"""
        input_data = {
            "subjectArea": "ai AND ml",
            "title": "dl approaches FOR nlp TASKS in modern LLMs",
            "abstract": "this PAPER explores DL techniques for NLP. we USE transformer MODELS including bert AND gpt FOR various nlp TASKS such AS sentiment analysis, NAMED entity recognition, AND question ANSWERING.",
            "accPercentFrom": 20,
            "accPercentTo": 40,
            "openAccess": "YES"
        }
        return self.run_test(10, "Mixed Case Sensitivity Issues", input_data)
    
    def print_summary(self):
        """Print summary of all test results"""
        print("\n\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["status"] == "PASSED")
        failed_tests = total_tests - passed_tests
        
        print(f"\nTotal Tests Run: {total_tests}")
        print(f"✓ Passed: {passed_tests}")
        print(f"✗ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print("\n" + "-"*80)
            print("FAILED TESTS:")
            print("-"*80)
            for result in self.test_results:
                if result["status"] == "FAILED":
                    print(f"  Test #{result['test_number']}: {result['test_name']}")
                    print(f"    Error: {result.get('error', 'Unknown error')}")
        
        # Save all results to file
        with open("test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)
        
        print("\n" + "="*80)
        print("Detailed test results saved to: test_results.json")
        print("="*80)
    
    def run_all_tests(self):
        """Run all test cases"""
        print("\n" + "█"*80)
        print("█" + " "*78 + "█")
        print("█" + " "*20 + "PAPER SEARCH BACKEND TEST SUITE" + " "*27 + "█")
        print("█" + " "*78 + "█")
        print("█"*80)
        
        # Run all tests
        self.test_1_typical_errors()
        self.test_2_multiple_abbreviations()
        self.test_3_minimal_errors()
        self.test_4_extensive_errors()
        self.test_5_edge_case_percentages()
        self.test_6_reversed_percentages()
        self.test_7_empty_fields()
        self.test_8_real_world_example()
        self.test_9_academic_paper()
        self.test_10_mixed_case_sensitivity()
        
        # Print summary
        self.print_summary()


def run_single_test(test_number: int):
    """Run a specific test by number"""
    tests = TestCases()
    test_methods = {
        1: tests.test_1_typical_errors,
        2: tests.test_2_multiple_abbreviations,
        3: tests.test_3_minimal_errors,
        4: tests.test_4_extensive_errors,
        5: tests.test_5_edge_case_percentages,
        6: tests.test_6_reversed_percentages,
        7: tests.test_7_empty_fields,
        8: tests.test_8_real_world_example,
        9: tests.test_9_academic_paper,
        10: tests.test_10_mixed_case_sensitivity
    }
    
    if test_number in test_methods:
        test_methods[test_number]()
        tests.print_summary()
    else:
        print(f"Error: Test #{test_number} does not exist. Available tests: 1-10")


def run_custom_test(custom_input: dict):
    """Run a test with custom input"""
    tests = TestCases()
    tests.run_test(0, "Custom Test", custom_input)


if __name__ == "__main__":
    # Run all tests
    test_suite = TestCases()
    test_suite.run_all_tests()
    
    # Uncomment below to run a single specific test:
    # run_single_test(1)
    
    # Uncomment below to run a custom test:
    # custom_input = {
    #     "subjectArea": "Your Subject",
    #     "title": "Your Title",
    #     "abstract": "Your Abstract",
    #     "accPercentFrom": 10,
    #     "accPercentTo": 50,
    #     "openAccess": "yes"
    # }
    # run_custom_test(custom_input)
