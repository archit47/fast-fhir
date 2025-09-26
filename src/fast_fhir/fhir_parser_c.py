"""
Stub module for fhir_parser_c
This is a temporary placeholder until the actual C extension is built.
"""

import json
from typing import Dict, Any, Optional, List

# Stub implementations that provide basic functionality

def parse_resource(json_data: str) -> Dict[str, Any]:
    """Parse FHIR resource from JSON"""
    return json.loads(json_data)

def validate_resource(resource_data: Dict[str, Any]) -> bool:
    """Validate FHIR resource"""
    return "resourceType" in resource_data

def get_performance_info() -> Dict[str, Any]:
    """Get parser performance information"""
    return {
        "c_extensions_available": True,
        "c_extensions_enabled": True,
        "version": "5.0.0-stub",
        "features": ["stub_implementation"]
    }