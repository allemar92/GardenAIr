# src/utils/parse_agent_output.py

import json
import re
from typing import TypeVar, Type
from pydantic import BaseModel, ValidationError

T = TypeVar('T', bound=BaseModel)

def parse_agent_output(raw_output: str, model_class: Type[T]) -> T:
    """
    Parse LLM output into a Pydantic model, handling common formatting issues.
    
    This function attempts multiple strategies to extract and validate JSON from
    LLM responses that may include markdown formatting, Python-style syntax, or
    extra text.
    
    Supported patterns:
    - Markdown code blocks: ```json {...} ```
    - Python-style quotes: ['item'] -> ["item"]
    - Naked arrays: ["a", "b"] -> {"field_name": ["a", "b"]}
    - Embedded JSON in text
    
    Args:
        raw_output: Raw string output from the LLM
        model_class: Pydantic model class to parse into (e.g., PlantSelectorOutput)
        
    Returns:
        Validated Pydantic model instance
        
    Raises:
        ValueError: If parsing fails after all attempts, with detailed error info
        
    Examples:
        >>> # Case 1: Clean JSON object
        >>> raw = '{"plant_list": ["tomato", "basil"]}'
        >>> result = parse_agent_output(raw, PlantSelectorOutput)
        >>> result.plant_list
        ['tomato', 'basil']
        
        >>> # Case 2: Markdown wrapped
        >>> raw = '```json\\n{"plant_list": ["tomato"]}\\n```'
        >>> result = parse_agent_output(raw, PlantSelectorOutput)
        
        >>> # Case 3: Naked array (auto-wrapped)
        >>> raw = '["tomato", "basil", "lettuce"]'
        >>> result = parse_agent_output(raw, PlantSelectorOutput)
        >>> result.plant_list
        ['tomato', 'basil', 'lettuce']
    """
    
    # Step 1: Clean markdown code blocks and whitespace
    cleaned = raw_output.strip()
    
    # Remove ```json or ``` at the start
    cleaned = re.sub(r'^```(?:json)?\s*\n?', '', cleaned)
    # Remove ``` at the end
    cleaned = re.sub(r'\n?\s*```\s*$', '', cleaned)
    cleaned = cleaned.strip()
    
    # Step 2: Convert Python-style string quotes to JSON
    # Handle cases like: ['item1', 'item2'] -> ["item1", "item2"]
    if cleaned.startswith("['") and cleaned.endswith("']"):
        cleaned = cleaned.replace("'", '"')
    
    # Step 3: Try to extract JSON from text
    # Use non-greedy matching for nested structures
    json_pattern = r'(\{.*?\}(?=\s*$)|\{.*\}|\[.*?\](?=\s*$)|\[.*\])'
    match = re.search(json_pattern, cleaned, re.DOTALL)
    
    json_str = match.group(1) if match else cleaned
    
    # Step 4: Handle naked arrays (LLM returns array but model expects object)
    # E.g., ["tomato", "basil"] but we need {"plant_list": ["tomato", "basil"]}
    if json_str.strip().startswith('['):
        if hasattr(model_class, 'model_fields') and model_class.model_fields:
            # Get the first (and usually only) field name
            field_name = next(iter(model_class.model_fields.keys()))
            
            # Wrap the array in an object with the correct field name
            json_str = f'{{"{field_name}": {json_str}}}'
    
    # Step 5: Attempt to parse with Pydantic
    try:
        return model_class.model_validate_json(json_str)
    
    except ValidationError as e:
        # Pydantic validation failed - field types don't match
        error_details = '\n'.join([f"  - {err['loc']}: {err['msg']}" for err in e.errors()])
        raise ValueError(
            f"Pydantic validation failed for {model_class.__name__}\n"
            f"Validation errors:\n{error_details}\n"
            f"Extracted JSON (first 500 chars):\n{json_str[:500]}"
        )
    
    except json.JSONDecodeError as e:
        # Invalid JSON syntax
        raise ValueError(
            f"Invalid JSON syntax for {model_class.__name__}\n"
            f"JSON decode error: {e.msg} at position {e.pos}\n"
            f"Extracted string (first 500 chars):\n{json_str[:500]}"
        )
    
    except Exception as e:
        # Any other unexpected error
        raise ValueError(
            f"Unexpected error parsing output into {model_class.__name__}\n"
            f"Error type: {type(e).__name__}\n"
            f"Error message: {str(e)}\n"
            f"Raw output (first 500 chars):\n{raw_output[:500]}\n"
            f"Cleaned output (first 500 chars):\n{cleaned[:500]}"
        )


def parse_agent_output_safe(raw_output: str, model_class: Type[T], 
                            fallback_value=None) -> T:
    """
    Safe version of parse_agent_output that returns a fallback instead of raising.
    
    Useful when you want the pipeline to continue even if one agent fails.
    
    Args:
        raw_output: Raw string output from the LLM
        model_class: Pydantic model class to parse into
        fallback_value: Optional fallback value if parsing fails
        
    Returns:
        Validated Pydantic model instance or fallback
        
    Examples:
        >>> result = parse_agent_output_safe(
        ...     raw_output,
        ...     PlantSelectorOutput,
        ...     fallback_value=PlantSelectorOutput(plant_list=["tomato"])
        ... )
    """
    try:
        return parse_agent_output(raw_output, model_class)
    except ValueError as e:
        print(f" Warning: {e}")
        if fallback_value is not None:
            return fallback_value
        raise