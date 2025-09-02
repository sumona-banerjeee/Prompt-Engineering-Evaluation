import os
import json
from src.prompt_catalog import PromptCatalog
from src.evaluator import Evaluator
from src.model_interface import ModelInterface
from src.analyzer import Analyzer

def main():

    print("Starting Prompt Evaluation Pipeline")
    
    os.makedirs("outputs", exist_ok=True)
    
    
    catalog = PromptCatalog()
    evaluator = Evaluator()
    model = ModelInterface(use_mock=True)
    analyzer = Analyzer()
    
   
    with open("data/test_cases.json", "r") as f:
        test_cases = json.load(f)
    
    results = []
    
    
    print(f"Processing {len(test_cases)} test cases...")
    
    for i, case in enumerate(test_cases):
        template_name = case["template"]
        params = case["params"]
        
        
        prompt = catalog.get_prompt(template_name, **params)
        response = model.generate(prompt)
        
        
        evaluation = evaluator.evaluate(prompt, response)
        
        result = {
            'id': i,
            'template': template_name,
            'prompt': prompt,
            'response': response,
            'scores': evaluation
        }
        
        results.append(result)
        print(f"Processed {i+1}/{len(test_cases)}: {template_name}")
    
    
    analysis = analyzer.analyze(results)
    
    
    output_data = {
        'results': results,
        'analysis': analysis
    }
    
    with open("outputs/results.json", "w") as f:
        json.dump(output_data, f, indent=2)
    
    
    report = analyzer.generate_report(analysis)
    with open("outputs/evaluation_report.md", "w") as f:
        f.write(report)
    
    
    print("\nEvaluation Complete")
    print(f"Average Score: {analysis['summary']['avg_overall_score']:.3f}")
    print(f"Best Prompt: {analysis['best_prompts'][0]['template']} ({analysis['best_prompts'][0]['overall']:.3f})")
    print(f"Worst Prompt: {analysis['worst_prompts'][0]['template']} ({analysis['worst_prompts'][0]['overall']:.3f})")
    print("\nResults saved to outputs/results.json")
    print("Report saved to outputs/evaluation_report.md")

if __name__ == "__main__":
    main()