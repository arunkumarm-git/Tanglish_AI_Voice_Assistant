import json

def parse_commands(text: str):
    """
    Parses a JSON string from the LLM.
    It can handle either a single JSON object or a JSON array of objects.
    Always returns a list of command dictionaries for consistency.
    """
    try:
        data = json.loads(text)
        
        # If the LLM returns a single command object, wrap it in a list
        if isinstance(data, dict):
            return [data]
        
        # If it's already a list, return it as is
        if isinstance(data, list):
            return data
            
        # If it's something else, return an empty list
        return []
        
    except (json.JSONDecodeError, AttributeError):
        print("Error: Failed to decode the LLM's JSON response.")
        return []