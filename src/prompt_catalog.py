from typing import Dict

class PromptCatalog:
    def __init__(self):
        self.templates = {
            
            "science_basic": "Explain {concept} to a {grade} student in simple terms.",
            
            "science_stepwise": "Break down {concept} into 3 simple steps for {grade} students: Step 1: Step 2: Step 3:",
            
            "science_analogy": "Explain {concept} using a simple analogy that {grade} students would understand.",
            
            "science_qa": "Answer this {grade} student's question about {concept}: {question}",
            
            "science_experiment": "Describe a simple experiment to demonstrate {concept} for {grade} students.",
            
            # English Prompts
            "grammar_rule": "Explain the grammar rule for {topic} to {grade} students with examples.",
            
            "writing_feedback": "Give constructive feedback on this {grade} student's writing: {text}",
            
            "reading_guide": "Help a {grade} student understand this passage: {passage}",
            
            "vocabulary": "Define {word} for {grade} students and use it in a sentence.",
            
            "story_analysis": "Help a {grade} student analyze the main idea of this story: {story}",
            
            # General Learning Prompts
            "concept_compare": "Compare {concept1} and {concept2} for {grade} students.",
            
            "problem_solve": "Guide a {grade} student through solving: {problem}",
            
            "study_tip": "Give study tips for {subject} to {grade} students.",
            
            "mistake_correct": "A {grade} student thinks {misconception}. Correct this gently.",
            
            "real_world": "Show how {concept} applies in real life for {grade} students."
        }
    
    def get_prompt(self, template_name: str, **kwargs) -> str:
    #Generate a prompt using the specified template and parameters
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        return self.templates[template_name].format(**kwargs)
    
    def get_all_templates(self) -> Dict[str, str]:
        #Return all available templates
        return self.templates.copy()
    
    def list_templates(self) -> list:
        #Return list of template names
        return list(self.templates.keys())
    
    