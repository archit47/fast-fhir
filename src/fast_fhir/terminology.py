"""Python wrapper for FHIR R5 Terminology resources implemented in C."""

from typing import Any, Dict, List, Optional, Union
import json

try:
    import fhir_foundation_c
    HAS_C_FOUNDATION = True
except ImportError:
    HAS_C_FOUNDATION = False

from .foundation import FHIRFoundationResource


class FHIRCodeSystem(FHIRFoundationResource):
    """FHIR CodeSystem resource."""
    
    def __init__(self, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize FHIR CodeSystem."""
        super().__init__("CodeSystem", id, use_c_extensions)
        self.url = None
        self.identifier = []
        self.version = None
        self.name = None
        self.title = None
        self.status = None
        self.experimental = None
        self.date = None
        self.publisher = None
        self.contact = []
        self.description = None
        self.use_context = []
        self.jurisdiction = []
        self.purpose = None
        self.copyright = None
        self.case_sensitive = None
        self.value_set = None
        self.hierarchy_meaning = None
        self.compositional = None
        self.version_needed = None
        self.content = None
        self.supplements = None
        self.count = None
        self.filter = []
        self.property = []
        self.concept = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        if self.use_c_extensions:
            try:
                return fhir_foundation_c.create_code_system(self.id)
            except:
                pass
        
        # Python fallback
        result = {"resourceType": "CodeSystem"}
        if self.id:
            result["id"] = self.id
        if self.url:
            result["url"] = self.url
        if self.version:
            result["version"] = self.version
        if self.name:
            result["name"] = self.name
        if self.title:
            result["title"] = self.title
        if self.status:
            result["status"] = self.status
        if self.content:
            result["content"] = self.content
        if self.concept:
            result["concept"] = self.concept
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRCodeSystem':
        """Create from dictionary."""
        code_system = cls(data.get("id"))
        code_system.url = data.get("url")
        code_system.version = data.get("version")
        code_system.name = data.get("name")
        code_system.title = data.get("title")
        code_system.status = data.get("status")
        code_system.content = data.get("content")
        code_system.concept = data.get("concept", [])
        return code_system
    
    @classmethod
    def from_json(cls, json_string: str) -> 'FHIRCodeSystem':
        """Create from JSON string using C extension if available."""
        if HAS_C_FOUNDATION:
            try:
                data = fhir_foundation_c.parse_code_system(json_string)
                return cls.from_dict(data)
            except:
                pass
        
        # Fallback to Python JSON parsing
        data = json.loads(json_string)
        return cls.from_dict(data)
    
    def lookup_display(self, code: str) -> Optional[str]:
        """Look up display name for a code."""
        if not self.concept:
            return None
        
        for concept in self.concept:
            if isinstance(concept, dict) and concept.get("code") == code:
                return concept.get("display")
        
        return None


class FHIRValueSet(FHIRFoundationResource):
    """FHIR ValueSet resource."""
    
    def __init__(self, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize FHIR ValueSet."""
        super().__init__("ValueSet", id, use_c_extensions)
        self.url = None
        self.identifier = []
        self.version = None
        self.name = None
        self.title = None
        self.status = None
        self.experimental = None
        self.date = None
        self.publisher = None
        self.contact = []
        self.description = None
        self.use_context = []
        self.jurisdiction = []
        self.immutable = None
        self.purpose = None
        self.copyright = None
        self.compose = None
        self.expansion = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        if self.use_c_extensions:
            try:
                return fhir_foundation_c.create_value_set(self.id)
            except:
                pass
        
        # Python fallback
        result = {"resourceType": "ValueSet"}
        if self.id:
            result["id"] = self.id
        if self.url:
            result["url"] = self.url
        if self.version:
            result["version"] = self.version
        if self.name:
            result["name"] = self.name
        if self.title:
            result["title"] = self.title
        if self.status:
            result["status"] = self.status
        if self.compose:
            result["compose"] = self.compose
        if self.expansion:
            result["expansion"] = self.expansion
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRValueSet':
        """Create from dictionary."""
        value_set = cls(data.get("id"))
        value_set.url = data.get("url")
        value_set.version = data.get("version")
        value_set.name = data.get("name")
        value_set.title = data.get("title")
        value_set.status = data.get("status")
        value_set.compose = data.get("compose")
        value_set.expansion = data.get("expansion")
        return value_set
    
    def contains_code(self, system: str, code: str) -> bool:
        """Check if ValueSet contains a specific code."""
        if not self.compose or not self.compose.get("include"):
            return False
        
        for include in self.compose["include"]:
            if include.get("system") == system:
                if "concept" in include:
                    for concept in include["concept"]:
                        if concept.get("code") == code:
                            return True
        
        return False


class FHIRConceptMap(FHIRFoundationResource):
    """FHIR ConceptMap resource."""
    
    def __init__(self, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize FHIR ConceptMap."""
        super().__init__("ConceptMap", id, use_c_extensions)
        self.url = None
        self.identifier = []
        self.version = None
        self.name = None
        self.title = None
        self.status = None
        self.experimental = None
        self.date = None
        self.publisher = None
        self.contact = []
        self.description = None
        self.use_context = []
        self.jurisdiction = []
        self.purpose = None
        self.copyright = None
        self.source_uri = None
        self.source_canonical = None
        self.target_uri = None
        self.target_canonical = None
        self.group = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        # Python implementation (C extension can be added later)
        result = {"resourceType": "ConceptMap"}
        if self.id:
            result["id"] = self.id
        if self.url:
            result["url"] = self.url
        if self.version:
            result["version"] = self.version
        if self.name:
            result["name"] = self.name
        if self.title:
            result["title"] = self.title
        if self.status:
            result["status"] = self.status
        if self.source_uri:
            result["sourceUri"] = self.source_uri
        if self.target_uri:
            result["targetUri"] = self.target_uri
        if self.group:
            result["group"] = self.group
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRConceptMap':
        """Create from dictionary."""
        concept_map = cls(data.get("id"))
        concept_map.url = data.get("url")
        concept_map.version = data.get("version")
        concept_map.name = data.get("name")
        concept_map.title = data.get("title")
        concept_map.status = data.get("status")
        concept_map.source_uri = data.get("sourceUri")
        concept_map.target_uri = data.get("targetUri")
        concept_map.group = data.get("group", [])
        return concept_map
    
    def translate(self, source_system: str, code: str) -> Optional[str]:
        """Translate a code from source to target system."""
        if not self.group:
            return None
        
        for group in self.group:
            if group.get("source") == source_system:
                for element in group.get("element", []):
                    if element.get("code") == code:
                        targets = element.get("target", [])
                        if targets:
                            return targets[0].get("code")
        
        return None


class FHIRBinary(FHIRFoundationResource):
    """FHIR Binary resource."""
    
    def __init__(self, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize FHIR Binary."""
        super().__init__("Binary", id, use_c_extensions)
        self.content_type = None
        self.security_context = None
        self.data = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        if self.use_c_extensions:
            try:
                return fhir_foundation_c.create_binary(self.id)
            except:
                pass
        
        # Python fallback
        result = {"resourceType": "Binary"}
        if self.id:
            result["id"] = self.id
        if self.content_type:
            result["contentType"] = self.content_type
        if self.data:
            result["data"] = self.data
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRBinary':
        """Create from dictionary."""
        binary = cls(data.get("id"))
        binary.content_type = data.get("contentType")
        binary.data = data.get("data")
        return binary


class FHIRBundle(FHIRFoundationResource):
    """FHIR Bundle resource."""
    
    def __init__(self, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize FHIR Bundle."""
        super().__init__("Bundle", id, use_c_extensions)
        self.identifier = None
        self.type = None
        self.timestamp = None
        self.total = None
        self.link = []
        self.entry = []
        self.signature = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        if self.use_c_extensions:
            try:
                return fhir_foundation_c.create_bundle(self.id)
            except:
                pass
        
        # Python fallback
        result = {"resourceType": "Bundle"}
        if self.id:
            result["id"] = self.id
        if self.type:
            result["type"] = self.type
        if self.timestamp:
            result["timestamp"] = self.timestamp
        if self.total is not None:
            result["total"] = self.total
        if self.entry:
            result["entry"] = self.entry
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRBundle':
        """Create from dictionary."""
        bundle = cls(data.get("id"))
        bundle.type = data.get("type")
        bundle.timestamp = data.get("timestamp")
        bundle.total = data.get("total")
        bundle.entry = data.get("entry", [])
        return bundle
    
    @classmethod
    def from_json(cls, json_string: str) -> 'FHIRBundle':
        """Create from JSON string using C extension if available."""
        if HAS_C_FOUNDATION:
            try:
                data = fhir_foundation_c.parse_bundle(json_string)
                return cls.from_dict(data)
            except:
                pass
        
        # Fallback to Python JSON parsing
        data = json.loads(json_string)
        return cls.from_dict(data)
    
    def get_entry_count(self) -> int:
        """Get number of entries in bundle."""
        if self.use_c_extensions:
            try:
                json_string = json.dumps(self.to_dict())
                return fhir_foundation_c.bundle_get_entry_count(json_string)
            except:
                pass
        
        # Python fallback
        return len(self.entry)
    
    def add_entry(self, resource: Dict[str, Any], full_url: Optional[str] = None) -> None:
        """Add an entry to the bundle."""
        entry = {"resource": resource}
        if full_url:
            entry["fullUrl"] = full_url
        
        self.entry.append(entry)
        self.total = len(self.entry)
    
    def get_resources_by_type(self, resource_type: str) -> List[Dict[str, Any]]:
        """Get all resources of a specific type from the bundle."""
        resources = []
        for entry in self.entry:
            resource = entry.get("resource", {})
            if resource.get("resourceType") == resource_type:
                resources.append(resource)
        return resources


# Utility functions
def is_terminology_resource(resource_type: str) -> bool:
    """Check if resource type is a Terminology resource."""
    if HAS_C_FOUNDATION:
        try:
            return fhir_foundation_c.is_terminology_resource(resource_type)
        except:
            pass
    
    # Python fallback
    terminology_types = {"CodeSystem", "ValueSet", "ConceptMap", "NamingSystem"}
    return resource_type in terminology_types


# Export all Terminology resources and utilities
__all__ = [
    'FHIRCodeSystem', 'FHIRValueSet', 'FHIRConceptMap', 'FHIRBinary', 'FHIRBundle',
    'is_terminology_resource'
]