#!/usr/bin/env python3
"""Script to fix all new resource classes to implement abstract methods."""

import os
import re

# Resource files to fix
resource_files = [
    "src/fhir/resources/biologically_derived_product.py",
    "src/fhir/resources/device_metric.py", 
    "src/fhir/resources/nutrition_product.py",
    "src/fhir/resources/transport.py",
    "src/fhir/resources/appointment_response.py",
    "src/fhir/resources/verification_result.py",
    "src/fhir/resources/encounter_history.py",
    "src/fhir/resources/episode_of_care.py"
]

def fix_resource_file(filepath):
    """Fix a single resource file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Extract class name and resource type from the file
    class_match = re.search(r'class (\w+)\(FHIRResourceBase\):', content)
    if not class_match:
        print(f"Could not find class definition in {filepath}")
        return
    
    class_name = class_match.group(1)
    
    # Extract resource type from __init__ method
    resource_type_match = re.search(r'super\(\).__init__\("(\w+)"', content)
    if not resource_type_match:
        print(f"Could not find resource type in {filepath}")
        return
    
    resource_type = resource_type_match.group(1)
    
    # Convert class name to snake_case for C function names
    c_function_name = re.sub('([A-Z]+)', r'_\1', class_name).lower().strip('_')
    
    print(f"Fixing {class_name} in {filepath}")
    
    # Replace __init__ method to use _init_resource_fields
    init_pattern = r'(def __init__\(self[^:]+:\s*"""[^"]*"""\s*super\(\).__init__\("[^"]+", id, use_c_extensions\)\s*)(# \w+-specific attributes.*?)(\n\n)'
    
    def replace_init(match):
        init_part = match.group(1)
        fields_part = match.group(2)
        end_part = match.group(3)
        
        # Convert field assignments to _init_resource_fields method
        new_init = init_part + end_part
        new_method = f"""    def _init_resource_fields(self) -> None:
        \"\"\"Initialize {class_name}-specific fields.\"\"\"
        {fields_part.replace('        # ' + class_name.replace('FHIR', '') + '-specific attributes', '').strip()}
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        \"\"\"Get the C extension create function name.\"\"\"
        return "{c_function_name}_create"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        \"\"\"Get the C extension parse function name.\"\"\"
        return "{c_function_name}_parse"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        \"\"\"Static version of _get_c_extension_parse_function.\"\"\"
        return "{c_function_name}_parse"

"""
        return new_init + new_method
    
    content = re.sub(init_pattern, replace_init, content, flags=re.DOTALL)
    
    # Replace to_dict method with _add_resource_specific_fields
    to_dict_pattern = r'    def to_dict\(self\) -> Dict\[str, Any\]:\s*"""[^"]*"""\s*result = super\(\)\.to_dict\(\)\s*(.*?)\s*return result'
    
    def replace_to_dict(match):
        fields_part = match.group(1)
        return f"""    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        \"\"\"Add {class_name}-specific fields to the result dictionary.\"\"\"
{fields_part.replace('        # Add ' + class_name.replace('FHIR', '') + '-specific fields', '').strip()}"""
    
    content = re.sub(to_dict_pattern, replace_to_dict, content, flags=re.DOTALL)
    
    # Replace from_dict method with _parse_resource_specific_fields
    from_dict_pattern = r'    @classmethod\s*def from_dict\(cls, data: Dict\[str, Any\]\) -> \'[^\']+\':\s*"""[^"]*"""\s*instance = cls\(data\.get\("id"\)\)\s*instance\._populate_from_dict\(data\)\s*(.*?)\s*return instance'
    
    def replace_from_dict(match):
        fields_part = match.group(1)
        return f"""    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        \"\"\"Parse {class_name}-specific fields from data dictionary.\"\"\"
{fields_part.replace('        # Set ' + class_name.replace('FHIR', '') + '-specific fields', '').replace('instance.', 'self.').strip()}"""
    
    content = re.sub(from_dict_pattern, replace_from_dict, content, flags=re.DOTALL)
    
    # Add _validate_resource_specific method before the validate method
    validate_pattern = r'(    def validate\(self\) -> List\[str\]:\s*"""[^"]*"""\s*errors = super\(\)\.validate\(\)\s*)(.*?)(return errors)'
    
    def replace_validate(match):
        validate_start = match.group(1)
        validation_logic = match.group(2)
        validate_end = match.group(3)
        
        # Extract the validation logic for the specific method
        specific_validation = validation_logic.replace('errors = super().validate()', '').replace('errors.append(', 'return False  # ').strip()
        if not specific_validation:
            specific_validation = 'return True'
        else:
            # Convert error appends to return False
            specific_validation = re.sub(r'errors\.append\([^)]+\)', 'return False', specific_validation)
            if 'return False' not in specific_validation:
                specific_validation += '\n        return True'
        
        new_specific_method = f"""    def _validate_resource_specific(self) -> bool:
        \"\"\"Perform {class_name}-specific validation.\"\"\"
        {specific_validation}
    
    def validate(self) -> List[str]:
        \"\"\"Validate {class_name} resource and return list of errors.\"\"\"
        errors = []
        
        # Basic validation
        if not self.resource_type:
            errors.append("Resource type is required")
        
{validation_logic.strip()}
        
        {validate_end}

"""
        return new_specific_method
    
    content = re.sub(validate_pattern, replace_validate, content, flags=re.DOTALL)
    
    # Write the fixed content back
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"Fixed {filepath}")

# Fix all resource files
for filepath in resource_files:
    if os.path.exists(filepath):
        fix_resource_file(filepath)
    else:
        print(f"File not found: {filepath}")

print("All resource files have been fixed!")