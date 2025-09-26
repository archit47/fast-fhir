"""FHIR R5 Parser - Main parsing functionality."""

import json
from typing import Dict, Any, Optional, Union
from .foundation import FHIRResource
from .resources.patient import Patient
from .resources.observation import Observation
from .resources.medication import Medication


class FHIRParser:
    """Main FHIR R5 parser class."""
    
    # Resource type mapping
    RESOURCE_TYPES = {
        'Patient': Patient,
        'Observation': Observation,
        'Medication': Medication,
    }
    
    def __init__(self):
        """Initialize the FHIR parser."""
        self.version = "5.0.0"
    
    def parse(self, data: Union[str, Dict[str, Any]]) -> Optional[FHIRResource]:
        """
        Parse FHIR JSON data into a resource object.
        
        Args:
            data: JSON string or dictionary containing FHIR resource data
            
        Returns:
            Parsed FHIR resource object or None if parsing fails
        """
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON: {e}")
        
        if not isinstance(data, dict):
            raise ValueError("Data must be a JSON string or dictionary")
        
        resource_type = data.get('resourceType')
        if not resource_type:
            raise ValueError("Missing resourceType in FHIR data")
        
        resource_class = self.RESOURCE_TYPES.get(resource_type)
        if not resource_class:
            raise ValueError(f"Unsupported resource type: {resource_type}")
        
        return resource_class.from_dict(data)
    
    def parse_bundle(self, bundle_data: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Parse a FHIR Bundle resource.
        
        Args:
            bundle_data: JSON string or dictionary containing FHIR Bundle
            
        Returns:
            Dictionary with parsed bundle information
        """
        if isinstance(bundle_data, str):
            bundle_data = json.loads(bundle_data)
        
        if bundle_data.get('resourceType') != 'Bundle':
            raise ValueError("Data is not a FHIR Bundle")
        
        entries = bundle_data.get('entry', [])
        parsed_resources = []
        
        for entry in entries:
            resource_data = entry.get('resource')
            if resource_data:
                try:
                    parsed_resource = self.parse(resource_data)
                    if parsed_resource:
                        parsed_resources.append(parsed_resource)
                except ValueError:
                    # Skip unsupported resources in bundle
                    continue
        
        return {
            'resourceType': 'Bundle',
            'id': bundle_data.get('id'),
            'type': bundle_data.get('type'),
            'total': bundle_data.get('total'),
            'entry': parsed_resources
        }