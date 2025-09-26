"""Fast FHIR parser using C extensions."""

import json
from typing import Dict, Any, Optional, Union

try:
    import fhir_parser_c
    HAS_C_EXTENSION = True
except ImportError:
    HAS_C_EXTENSION = False

from .parser import FHIRParser
from .foundation import FHIRResource


class FastFHIRParser(FHIRParser):
    """High-performance FHIR parser using C extensions when available."""
    
    def __init__(self):
        """Initialize the fast FHIR parser."""
        super().__init__()
        self.use_c_extensions = HAS_C_EXTENSION
        
    def parse(self, data: Union[str, Dict[str, Any]]) -> Optional[FHIRResource]:
        """
        Parse FHIR JSON data with C extension acceleration.
        
        Args:
            data: JSON string or dictionary containing FHIR resource data
            
        Returns:
            Parsed FHIR resource object
        """
        if isinstance(data, dict):
            # Convert dict to JSON string for C extension
            json_string = json.dumps(data)
        else:
            json_string = data
            
        if self.use_c_extensions:
            try:
                # Fast validation using C extension
                fhir_parser_c.validate_fhir_json(json_string)
                
                # Fast resource type extraction
                resource_type = fhir_parser_c.extract_resource_type(json_string)
                
                if not resource_type:
                    raise ValueError("Missing resourceType in FHIR data")
                
                # Use C extension for common field extraction if available
                if isinstance(data, str):
                    data = json.loads(data)
                    
            except Exception:
                # Fallback to pure Python implementation
                return super().parse(data)
        else:
            # Pure Python fallback
            if isinstance(data, str):
                data = json.loads(data)
            resource_type = data.get('resourceType')
        
        # Use parent class logic for resource creation
        resource_class = self.RESOURCE_TYPES.get(resource_type)
        if not resource_class:
            raise ValueError(f"Unsupported resource type: {resource_type}")
        
        return resource_class.from_dict(data)
    
    def parse_bundle(self, bundle_data: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Parse FHIR Bundle with C extension acceleration.
        
        Args:
            bundle_data: JSON string or dictionary containing FHIR Bundle
            
        Returns:
            Dictionary with parsed bundle information
        """
        if isinstance(bundle_data, dict):
            json_string = json.dumps(bundle_data)
        else:
            json_string = bundle_data
            bundle_data = json.loads(json_string)
        
        if bundle_data.get('resourceType') != 'Bundle':
            raise ValueError("Data is not a FHIR Bundle")
        
        # Use C extension for fast entry counting if available
        if self.use_c_extensions:
            try:
                entry_count = fhir_parser_c.count_bundle_entries(json_string)
                print(f"Bundle contains {entry_count} entries (fast count)")
            except Exception:
                pass  # Fallback to normal processing
        
        # Use parent class logic for bundle parsing
        return super().parse_bundle(bundle_data)
    
    def extract_field_fast(self, json_string: str, field_name: str) -> Any:
        """
        Fast field extraction using C extension.
        
        Args:
            json_string: JSON string
            field_name: Field name to extract
            
        Returns:
            Field value or None if not found
        """
        if not self.use_c_extensions:
            # Fallback to JSON parsing
            data = json.loads(json_string)
            return data.get(field_name)
        
        try:
            return fhir_parser_c.extract_field(json_string, field_name)
        except Exception:
            # Fallback to JSON parsing
            data = json.loads(json_string)
            return data.get(field_name)
    
    def get_performance_info(self) -> Dict[str, Any]:
        """Get information about parser performance features."""
        return {
            'c_extensions_available': HAS_C_EXTENSION,
            'c_extensions_enabled': self.use_c_extensions,
            'version': self.version,
            'features': [
                'fast_json_validation',
                'fast_resource_type_extraction',
                'fast_bundle_entry_counting',
                'fast_field_extraction'
            ] if self.use_c_extensions else ['pure_python_fallback']
        }