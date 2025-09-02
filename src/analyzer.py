import pandas as pd
from typing import List, Dict, Any

#It is the entry point for the analysis logic that will take the result and evaluate the result(scores, prompt etc)
#It will return summary dict containing overall metrics, failure cases, and recommendations.

class Analyzer:
    def analyze(self, results: List[Dict]) -> Dict[str, Any]:
        
#It will converts the list of results into a structured DataFrame containing different individual scores like fluency,correctness,bias,clarity etc.
        df = pd.DataFrame([{
            'template': r['template'],
            **r['scores']
        } for r in results])
        
#It will calculates different avg score, count the prompts (good/poor) and return the avg for each eveluation metric.

        summary = {
            'total_prompts': len(results),
            'avg_overall_score': float(df['overall'].mean()),
            'score_distribution': {
                'excellent': int(len(df[df['overall'] > 0.8])),
                'good': int(len(df[(df['overall'] >= 0.6) & (df['overall'] <= 0.8)])),
                'poor': int(len(df[df['overall'] < 0.6]))
            },
            'metric_averages': {
                'fluency': float(df['fluency'].mean()),
                'correctness': float(df['correctness'].mean()),
                'bias_check': float(df['bias_check'].mean()),
                'clarity': float(df['clarity'].mean()),
                'age_appropriate': float(df['age_appropriate'].mean())
            }
        }
        
#It will retrun top 3 best prompt and worst prompt and will converts them to dictionary format for reporting.
        
        best_prompts = df.nlargest(3, 'overall')[['template', 'overall']].to_dict('records')
        for prompt in best_prompts:
            prompt['overall'] = float(prompt['overall'])
        
        
        worst_prompts = df.nsmallest(3, 'overall')[['template', 'overall']].to_dict('records')
        for prompt in worst_prompts:
            prompt['overall'] = float(prompt['overall'])
        
#It will identify failure modes and filter prompts that fall below thresholds in key metrics.    
        failure_modes = []
        
       
        bias_problems = df[df['bias_check'] < 0.7]
        if len(bias_problems) > 0:
            #Each group will become a failure mode entry.
            failure_modes.append({
                'type': 'bias_issues',
                'count': int(len(bias_problems)),
                'templates': bias_problems['template'].tolist(),
                'description': 'Prompts showing potential bias or non-inclusive language'
            })
        
        
        correctness_problems = df[df['correctness'] < 0.5]
        if len(correctness_problems) > 0:
            failure_modes.append({
                'type': 'accuracy_issues',
                'count': int(len(correctness_problems)),
                'templates': correctness_problems['template'].tolist(),
                'description': 'Prompts with potential accuracy or factual concerns'
            })
        
        
        age_problems = df[df['age_appropriate'] < 0.6]
        if len(age_problems) > 0:
            failure_modes.append({
                'type': 'age_appropriateness',
                'count': int(len(age_problems)),
                'templates': age_problems['template'].tolist(),
                'description': 'Prompts not well-suited for target age group'
            })
        
#It will call the helper method (generate_mitigations()) to propose strategies based on what went wrong.     
        mitigations = self._generate_mitigations(failure_modes, summary)
        
#It will filter the prompts that performed consistently well across metrics focusing on greater than 0.75.       
        robust_prompts = df[df['overall'] > 0.75]['template'].tolist()

# It will return Final result like Visualization, Reporting and Further decision-making.        
        return {
            'summary': summary,
            'best_prompts': best_prompts,
            'worst_prompts': worst_prompts,
            'failure_modes': failure_modes,
            'mitigations': mitigations,
            'robust_prompts': robust_prompts,
            'detailed_scores': df.to_dict('records')
        }

#It will Generate remedial suggestions based on failure types and metric weaknesses.    
#In short it find the problems, understand where the system is weak, and suggest ways to fix or improve them.
    def _generate_mitigations(self, failure_modes: List[Dict], summary: Dict) -> List[str]:
        """Generate mitigation strategies based on identified issues"""
        mitigations = []
        
#It will check the failure types that is it bias issue or different issues.     
        failure_types = [fm['type'] for fm in failure_modes]
        
        if 'bias_issues' in failure_types:
            mitigations.append(
                "Implement bias checking: Add explicit guidelines for inclusive language "
                "and review prompts for potential stereotypes or discriminatory content"
            )
        
        if 'accuracy_issues' in failure_types:
            mitigations.append(
                "Enhance fact verification: Include requirements for evidence-based responses "
                "and avoid absolute statements without proper qualification"
            )
        
        if 'age_appropriateness' in failure_types:
            mitigations.append(
                "Improve age targeting: Use grade-level vocabulary lists and adjust "
                "complexity based on developmental appropriateness"
            )
        
#It will check low metric averages        
        if summary['metric_averages']['clarity'] < 0.7:
            mitigations.append(
                "Enhance clarity: Use shorter sentences, transition words, and "
                "structured formatting to improve readability"
            )
        
        if summary['metric_averages']['fluency'] < 0.7:
            mitigations.append(
                "Improve fluency: Focus on natural language flow and vary "
                "sentence structures to enhance readability"
            )
        
#If there are no problems found (the mitigations list is empty), continue work, because everything is fine.       
        if not mitigations:
            mitigations.append(
                "Continue current approach: Prompts show good overall performance "
                "with no major issues identified"
            )
        
        return mitigations

#It will take the analysis results and turns them into a nicely formatted text report using Markdown Includes (Summary, Metric Averages, Best/Worst Prompts).
#It will store the data in outputs/evaluation_report.md.
  
    def generate_report(self, analysis: Dict[str, Any]) -> str:
        
        report = f"""# Prompt Engineering Evaluation Report

## Executive Summary

- **Total prompts tested**: {analysis['summary']['total_prompts']}
- **Average overall score**: {analysis['summary']['avg_overall_score']:.3f}/1.0
- **Performance distribution**:
  - Excellent (>0.8): {analysis['summary']['score_distribution']['excellent']} prompts
  - Good (0.6-0.8): {analysis['summary']['score_distribution']['good']} prompts
  - Poor (<0.6): {analysis['summary']['score_distribution']['poor']} prompts

## Metric Averages

- **Fluency**: {analysis['summary']['metric_averages']['fluency']:.3f}
- **Correctness**: {analysis['summary']['metric_averages']['correctness']:.3f}
- **Bias Check**: {analysis['summary']['metric_averages']['bias_check']:.3f}
- **Clarity**: {analysis['summary']['metric_averages']['clarity']:.3f}
- **Age Appropriate**: {analysis['summary']['metric_averages']['age_appropriate']:.3f}

## Top 3 Performing Prompts
"""
#Loop through top 3 prompts, add numbered lines with template names and scores (3 decimal places). 
        for i, prompt in enumerate(analysis['best_prompts'], 1):
            report += f"\n{i}. **{prompt['template']}**: {prompt['overall']:.3f}"
        

#Adds a header, then lists the bottom 3 prompts with their template names and scores numbered from 1.
        report += "\n\n## Bottom 3 Performing Prompts\n"
        
        for i, prompt in enumerate(analysis['worst_prompts'], 1):
            report += f"\n{i}. **{prompt['template']}**: {prompt['overall']:.3f}"
        

#If any prompts scored > 0.75, adds a header and lists them as bullet points using their template names.        
        if analysis['robust_prompts']:
            report += f"\n\n## Robust Prompts (Score > 0.75)\n"
            for prompt in analysis['robust_prompts']:
                report += f"- {prompt}\n"
        
#Adds a section header if any failure modes (like bias or errors) were detected in the analysis.        
        if analysis['failure_modes']:
            report += "\n\n## Identified Failure Modes\n"


#For each failure type, it formats the title nicely, shows how many prompts are affected,& lists the description plus the affected prompt templates.
            for failure in analysis['failure_modes']:
                report += f"\n### {failure['type'].replace('_', ' ').title()}\n"
                report += f"- **Count**: {failure['count']} prompts\n"
                report += f"- **Description**: {failure['description']}\n"
                report += f"- **Affected templates**: {', '.join(failure['templates'])}\n"
        

#Adds a section header for improvements, then lists each mitigation strategy as a numbered item from the suggestions.       
        report += "\n\n## Mitigation Strategies\n"
        
        for i, strategy in enumerate(analysis['mitigations'], 1):
            report += f"\n{i}. {strategy}\n"
        
#Adds another section header for top-level takeaways.        
        report += "\n\n## Key Recommendations\n"


#Summarizes prompt quality as Excellent, Good, or Needs Improvement based on the average overall score.
        if analysis['summary']['avg_overall_score'] >= 0.8:
            report += "\n- **Overall Performance**: Excellent. Current prompts are highly effective."
        elif analysis['summary']['avg_overall_score'] >= 0.6:
            report += "\n- **Overall Performance**: Good with room for improvement."
        else:
            report += "\n- **Overall Performance**: Needs significant improvement."
        

#Checks specific metric scores and adds focused recommendations if any are below set thresholds.       
        metrics = analysis['summary']['metric_averages']
        
        if metrics['bias_check'] < 0.8:
            report += "\n- **Priority**: Address potential bias issues in prompt design"
        
        if metrics['correctness'] < 0.7:
            report += "\n- **Focus Area**: Improve factual accuracy and evidence-based responses"
        
        if metrics['age_appropriate'] < 0.7:
            report += "\n- **Target**: Better age-appropriate language and concepts"


# Footer of the Report
        report += f"\n\n---\n*Report generated from {analysis['summary']['total_prompts']} prompt evaluations*"
        
        return report
    