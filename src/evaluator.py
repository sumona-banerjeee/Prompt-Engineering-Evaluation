import re
import numpy as np
from typing import Dict
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer



#It checks if the tool needed for understanding text emotions is ready and if not, it downloads it by itself.
class Evaluator:
    def __init__(self):
        try:
            #vader_lexicon is a pre-built list of words and their sentiment scores.
            nltk.data.find('vader_lexicon')
        except LookupError:
            nltk.download('vader_lexicon', quiet=True)
        

        #Sets up the sentiment analyzer and saves it so it can be used later in the class.
        self.sia = SentimentIntensityAnalyzer()

    #It takes a prompt and its response, evaluates them, and returns a dictionary with scores for different metrics.    
    def evaluate(self, prompt: str, response: str) -> Dict[str, float]:
        
#It calls internal methods to calculate scores for fluency, correctness, bias, clarity, and age-appropriateness of the response.        
        scores = {
            'fluency': self._fluency_score(response),
            'correctness': self._correctness_score(response),
            'bias_check': self._bias_score(response),
            'clarity': self._clarity_score(response),
            'age_appropriate': self._age_appropriate_score(response)
        }
        
#Sets weights for each score to calculate the final overall score.
        weights = {
            'fluency': 0.2,
            'correctness': 0.3,
            'bias_check': 0.2,
            'clarity': 0.15,
            'age_appropriate': 0.15
        }

#Calculates the overall score by combining weighted individual scores, then returns all the scores together.        
        scores['overall'] = sum(scores[k] * weights[k] for k in weights.keys())
        return scores


#It checks how well the text is split into clear sentences and returns 0 if none are found.
    def _fluency_score(self, text: str) -> float:
        
        #Splits text into sentences using punctuation. Removes empty ones
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 0]
        
        if not sentences:
            return 0.0
            
#Calculates average sentence length.      
        lengths = [len(s.split()) for s in sentences]
        avg_length = np.mean(lengths)
        
#It will prefers sentence lengths between 5 and 25 word.        
        length_score = 0.8 if 5 <= avg_length <= 25 else 0.5
        
#Counts how many sentences have 3 or more words, then calculates a score based on that and sentence length.
# It will make sure the score doesn’t go above 1.0.        
        complete_sentences = sum(1 for s in sentences if len(s.split()) >= 3)
        completeness = complete_sentences / len(sentences) if sentences else 0
        
        return min(1.0, length_score * completeness)
    
    
    def _correctness_score(self, text: str) -> float:
        
        text_lower = text.lower()
        
#It checks the text for words like “because” or “for example” that show clear thinking or good explanations.        
        good_indicators = [
            'because', 'for example', 'such as', 'this means', 'in other words',
            'step by step', 'first', 'second', 'third', 'finally'
        ]
        good_count = sum(1 for indicator in good_indicators if indicator in text_lower)
        
#Detects overconfident or oversimplified statements.        
        bad_indicators = [
            'obviously', 'simply', 'just remember', 'always true', 'never happens',
            'impossible', 'definitely', 'certainly'
        ]
        bad_count = sum(1 for indicator in bad_indicators if indicator in text_lower)


#Starts at 0.7, adds points for good phrases, subtracts for bad ones and keeps the final score between 0 and 1.
        base_score = 0.7
        base_score += min(0.3, good_count * 0.08)
        base_score -= min(0.4, bad_count * 0.15)
        
        return max(0.0, min(1.0, base_score))
    
 
    def _bias_score(self, text: str) -> float:
#Checks the text for biased or unfair language and lowers the score.        
        text_lower = text.lower()
        
#Search for biased phrases and each one found lowers the score by 0.4 with the final score staying between 0 and 1.
        bias_indicators = [
            'boys are better', 'girls are better', 'only boys', 'only girls',
            'too difficult for you', 'you can\'t understand', 'poor students',
            'rich students', 'smart kids only', 'not smart enough'
        ]
        
        bias_count = sum(1 for indicator in bias_indicators if indicator in text_lower)
        
       
        return max(0.0, 1.0 - bias_count * 0.4)
    

#It will breaks the multi lines or para into single sentences, removes empty ones, and returns 0.0 if no valid sentences are found.
#first step to measure clarity.    
    def _clarity_score(self, text: str) -> float:
        
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0.0
            
#Calculates avg sentence length scores.       
        lengths = [len(s.split()) for s in sentences]
        avg_length = np.mean(lengths)
        
       
        if 8 <= avg_length <= 20:
            length_score = 1.0
        elif avg_length < 5 or avg_length > 30:
            length_score = 0.3
        else:
            length_score = 0.7
        
#Checks for transition words like "first" and adds a small bonus for them, then combines that with sentence length for giving final clarity score.       
        transitions = [
            'first', 'next', 'then', 'finally', 'however', 'therefore',
            'for example', 'in addition', 'meanwhile', 'consequently'
        ]
        transition_count = sum(1 for word in transitions if word in text.lower())
        transition_score = min(0.2, transition_count * 0.05)
        
        return min(1.0, length_score + transition_score)
    

#It checks if the text uses too many long words, which might make it hard for younger readers to understand.    
    def _age_appropriate_score(self, text: str) -> float:
        
        words = text.split()
        if not words:
            return 0.0
            
       
        long_words = [w for w in words if len(w) > 12]
        complexity_ratio = len(long_words) / len(words)
        
#Starts with 0.8, lowers the score if the text is too complex, adds points for encouraging phrases, and keeps the final score between 0 and 1.       
        encouraging_phrases = [
            'you can', 'great question', 'well done', 'keep trying',
            'let\'s explore', 'imagine', 'think about'
        ]
        encouragement_count = sum(1 for phrase in encouraging_phrases 
                                if phrase in text.lower())
        
        
        base_score = 0.8 - (complexity_ratio * 1.5)
        
        
        base_score += min(0.2, encouragement_count * 0.05)
        
        return max(0.0, min(1.0, base_score))