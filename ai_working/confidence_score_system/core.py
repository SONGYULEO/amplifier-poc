"""
Core module for the Confidence Score system.
"""
from typing import List, Dict, Any

class ConfidenceCalculator:
    """
    Calculates the confidence score based on a set of heuristic rules.
    """

    BASE_SCORE = 70.0

    # Define modifiers as a dictionary for easy access and modification.
    # Format: "modifier_name": weight
    MODIFIERS = {
        # Information Source
        "used_read_file": 10.0,
        "used_codebase_investigator": 15.0,
        "used_google_search": 5.0,
        "used_internal_knowledge_only": -20.0,

        # Clarity of User Request
        "request_is_clear": 10.0,
        "request_is_vague": -15.0,

        # Task Completion
        "all_todos_completed": 10.0,
        "task_execution_error": -10.0,

        # Response Type
        "response_is_code": 5.0,
        "response_is_explanation": -5.0,
    }

    def __init__(self):
        self.score = self.BASE_SCORE
        self.applied_modifiers: List[Dict[str, Any]] = []

    def apply(self, modifier_name: str, reason: str):
        """
        Applies a modifier to the score.
        
        Args:
            modifier_name: The name of the modifier to apply.
            reason: A brief explanation of why the modifier was applied.
        """
        if modifier_name in self.MODIFIERS:
            modifier_value = self.MODIFIERS[modifier_name]
            self.score += modifier_value
            self.applied_modifiers.append({
                "modifier": modifier_name,
                "value": modifier_value,
                "reason": reason
            })
        else:
            # In a real scenario, we might want to log this as a warning.
            print(f"Warning: Modifier '{modifier_name}' not found.")

    def get_score(self) -> float:
        """
        Returns the final calculated score, clamped between 0 and 100.
        """
        return max(0.0, min(100.0, self.score))

    def get_calculation_trace(self) -> str:
        """
        Returns a human-readable trace of the score calculation.
        """
        trace = [f"Base Score: {self.BASE_SCORE}%"]
        for mod in self.applied_modifiers:
            sign = "+" if mod['value'] > 0 else ""
            trace.append(f"{sign}{mod['value']}%: {mod['reason']} ({mod['modifier']})")
        
        final_score = self.get_score()
        trace.append("---")
        trace.append(f"Final Score: {final_score}%")
        return "\n".join(trace)

if __name__ == '__main__':
    # Example Usage
    print("--- Example 1: A clear request to read a file ---")
    calc = ConfidenceCalculator()
    calc.apply("used_read_file", "Read file 'amplifier/main.py'")
    calc.apply("request_is_clear", "User provided a specific file and function name")
    calc.apply("response_is_explanation", "The response was an explanation of a function")
    
    print(calc.get_calculation_trace())
    # Expected: 70 + 10 + 10 - 5 = 85

    print("\n--- Example 2: A vague request using only internal knowledge ---")
    calc2 = ConfidenceCalculator()
    calc2.apply("used_internal_knowledge_only", "No external tools were used")
    calc2.apply("request_is_vague", "User asked to 'optimize the code'")
    
    print(calc2.get_calculation_trace())
    # Expected: 70 - 20 - 15 = 35
