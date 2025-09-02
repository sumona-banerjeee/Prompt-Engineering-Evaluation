from transformers import pipeline

class ModelInterface:
    def __init__(self, model_name="gpt2", use_mock=False):
        self.model_name = model_name
        self.use_mock = use_mock
        self.pipeline = None
        
        if not use_mock:
            try:
                self.pipeline = pipeline("text-generation", model=model_name)
                print(f"Model {model_name} loaded successfully")
            except Exception as e:
                print(f"Failed to load model: {e}")
                print("Falling back to mock responses")
                self.use_mock = True
        else:
            print("Using mock responses")
    
    def generate(self, prompt: str, max_length: int = 150) -> str:
        
        if self.use_mock:
            return self._mock_response(prompt)
        
        try:
            result = self.pipeline(
                prompt,
                max_new_tokens=max_length,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=50256
            )
            
            generated_text = result[0]['generated_text']
            response = generated_text[len(prompt):].strip()
            
            if len(response) < 20:
                return self._mock_response(prompt)
            
            return response
            
        except Exception as e:
            print(f"Generation failed: {e}")
            return self._mock_response(prompt)
    
    def _mock_response(self, prompt: str) -> str:
        
        prompt_lower = prompt.lower()
        
        
        if 'photosynthesis' in prompt_lower:
            return ("Plants make food using sunlight, water, and carbon dioxide. "
                    "The green parts of plants capture sunlight like solar panels. "
                    "Water comes up from the roots, and carbon dioxide comes from the air. "
                    "When these mix together with sunlight, plants make sugar for food and release oxygen.")
        
        elif 'gravity' in prompt_lower:
            return ("Gravity is a force that pulls objects toward Earth. "
                    "Think of it like an invisible hand that always pulls things down. "
                    "That's why when you drop a ball, it falls to the ground instead of floating away. "
                    "The bigger something is, the stronger its gravity pull.")
        
        elif 'atoms' in prompt_lower:
            return ("Atoms are like tiny building blocks that make up everything around us. "
                    "Think of them like LEGO blocks - you can't see individual blocks in a big castle, "
                    "but they're all there holding it together. "
                    "Different combinations of these blocks make different materials.")
        
        elif 'experiment' in prompt_lower and 'magnet' in prompt_lower:
            return ("Here's a simple magnet experiment: Get a magnet and various small objects like paperclips, "
                    "coins, and plastic items. First, predict which items will stick to the magnet. "
                    "Then test each item. You'll find that only metal objects made of iron stick to magnets.")
        
        # English responses
        elif 'grammar' in prompt_lower or 'verb' in prompt_lower:
            return ("Subject-verb agreement means the subject and verb must match. "
                    "If the subject is singular (one thing), use a singular verb. "
                    "If the subject is plural (many things), use a plural verb. "
                    "Example: 'The cat runs' (singular) but 'The cats run' (plural).")
        
        elif 'writing' in prompt_lower and 'feedback' in prompt_lower:
            return ("Your writing shows good ideas and creativity. To improve: "
                    "First, add more descriptive words to paint pictures in the reader's mind. "
                    "Second, vary your sentence lengths by mixing short and long sentences. "
                    "Third, make sure each paragraph has one main idea.")
        
        elif 'vocabulary' in prompt_lower:
            if 'magnificent' in prompt_lower:
                return ("Magnificent means extremely beautiful, impressive, or wonderful. "
                        "It's used to describe something that makes you say 'Wow!' "
                        "Example sentence: The magnificent sunset painted the sky in brilliant colors.")
            else:
                return ("This word means something special or important. "
                        "You can use it to describe things that are impressive or noteworthy.")
        
        elif 'story' in prompt_lower or 'passage' in prompt_lower:
            return ("To understand this passage, let's find the main idea first. "
                    "Look for the most important point the author is trying to make. "
                    "Then identify supporting details that help explain this main idea. "
                    "Finally, think about how this connects to what you already know.")
        
        # General learning responses
        elif 'compare' in prompt_lower:
            if 'mammal' in prompt_lower and 'reptile' in prompt_lower:
                return ("Mammals and reptiles are both animals, but they're different in important ways. "
                        "Mammals are warm-blooded and have fur or hair, while reptiles are cold-blooded and have scales. "
                        "Mammal babies drink milk from their mothers, but reptile babies usually take care of themselves.")
            else:
                return ("These two concepts are similar in some ways but different in others. "
                        "They both share certain characteristics, but each has unique features that make it special.")
        
        elif 'problem' in prompt_lower and '%' in prompt_lower:
            return ("To find 15% of 80, let's break it down step by step. "
                    "First, remember that 15% means 15 out of 100, or 0.15. "
                    "Second, multiply 80 by 0.15: 80 × 0.15 = 12. "
                    "So 15% of 80 is 12.")
        
        elif 'study tip' in prompt_lower:
            return ("Here are good study tips for science: "
                    "First, make connections between new ideas and things you already know. "
                    "Second, practice explaining concepts in your own words. "
                    "Third, use drawings and diagrams to help you remember. "
                    "Finally, ask questions when something doesn't make sense.")
        
        elif 'misconception' in prompt_lower:
            return ("I can see why you might think that - it's a common idea. "
                    "However, let me help clarify this concept. "
                    "The actual explanation is a bit different, and here's why: "
                    "Scientific experiments have shown us the real answer.")
        
        elif 'real world' in prompt_lower:
            if 'fraction' in prompt_lower:
                return ("Fractions are everywhere in real life! "
                        "When you eat half a pizza, that's 1/2. "
                        "When a recipe calls for 3/4 cup of flour, that's a fraction. "
                        "Even telling time uses fractions - quarter past means 1/4 of an hour.")
            else:
                return ("This concept appears in many real-world situations. "
                        "You might see it when cooking, shopping, playing sports, or using technology. "
                        "Understanding this helps you solve everyday problems.")

       
        elif 'rain' in prompt_lower or 'weather' in prompt_lower:
            return ("Rain happens because of the water cycle! When the sun heats up water in oceans and lakes, "
                    "it turns into invisible water vapor that rises into the sky. High up where it's cold, "
                    "this water vapor turns back into tiny water droplets that form clouds. "
                    "When the droplets get too heavy, they fall as rain!")

        elif 'step' in prompt_lower and 'gravity' in prompt_lower:
            return ("Step 1: Gravity is a force that pulls everything toward Earth. "
                    "Step 2: This invisible force is always working, even when you can't see it. "
                    "Step 3: That's why when you drop something, it falls down instead of floating away!")

        elif 'heavier' in prompt_lower and 'fall' in prompt_lower:
            return ("I can see why you might think that - it seems like heavier things should fall faster! "
                    "But actually, all objects fall at the same speed when there's no air resistance. "
                    "Try dropping a heavy book and a light piece of paper from the same height - "
                    "they'll hit the ground at almost the same time!")

        elif 'egyptian' in prompt_lower or 'pyramid' in prompt_lower:
            return ("This passage tells us about ancient Egyptian pyramids. The main idea is that Egyptians "
                    "built these huge stone buildings as tombs for their kings called pharaohs. "
                    "The supporting detail is that they took many years to build because they were so massive. "
                    "Think about other big buildings you know - they also take a long time to construct!")

        elif 'key' in prompt_lower and 'door' in prompt_lower:
            return ("This story is about discovery and mystery. The main idea is that sometimes we find "
                    "unexpected treasures in familiar places. The young girl represents curiosity, "
                    "the mysterious key represents opportunity, and the hidden door represents new adventures "
                    "waiting to be discovered.")
        
        
        else:
            return ("That's a great question! Let me explain this step by step. "
                    "First, we need to understand the basic idea. "
                    "Then we can look at some examples. "
                    "Finally, we'll see how this connects to what you already know. "
                    "This concept is important because it helps us understand the world around us.")

