"""
FHIR R5 Foundation Resource Deserializers
Converts JSON strings to FHIR foundation resource objects (Patient, Practitioner, etc.)
"""

import json
from typing import Union, Dict, Any, Optional, Type, TypeVar
from datetime import datetime, date

from .pydantic_foundation import (
    HAS_PYDANTIC,
    PatientModel, PractitionerModel, PractitionerRoleModel,
    EncounterModel, PersonModel, RelatedPersonModel
)

# Import the actual FHIR resource classes (these would need to be implemented)
try:
    from ..resources.patient import Patient
    from ..resources.practitioner import Practitioner
    from ..resources.practitioner_role import PractitionerRole
    from ..resources.encounter import Encounter
    from ..resources.person import Person
    from ..resources.related_person import RelatedPerson
except ImportError:
    # Fallback classes if resource classes aren't implemented yet
    class Patient:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class Practitioner:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class PractitionerRole:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class Encounter:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class Person:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class RelatedPerson:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

# Import FHIR datatypes
try:
    from ..datatypes import (
        FHIRString, FHIRReference, FHIRCodeableConcept, FHIRDateTime, 
        FHIRPeriod, FHIRDecimal, FHIRBoolean, FHIRInteger, FHIRIdentifier,
        FHIRQuantity, FHIRAnnotation, FHIRTiming, FHIRContactPoint, FHIRRange
    )
except ImportError:
    # Fallback classes - use composition instead of inheritance for built-in types
    class FHIRString:
        def __init__(self, value):
            self.value = str(value) if value is not None else None
    
    class FHIRReference:
        def __init__(self, value):
            self.value = dict(value) if value is not None else {}
    
    class FHIRCodeableConcept:
        def __init__(self, value):
            self.value = dict(value) if value is not None else {}
    
    class FHIRDateTime:
        def __init__(self, value):
            self.value = value
    
    class FHIRPeriod:
        def __init__(self, value):
            self.value = dict(value) if value is not None else {}
    
    class FHIRDecimal:
        def __init__(self, value):
            self.value = float(value) if value is not None else None
    
    class FHIRBoolean:
        def __init__(self, value):
            self.value = bool(value) if value is not None else None
    
    class FHIRInteger:
        def __init__(self, value):
            self.value = int(value) if value is not None else None
    
    class FHIRIdentifier:
        def __init__(self, value):
            self.value = dict(value) if value is not None else {}
    
    class FHIRQuantity:
        def __init__(self, value):
            self.value = dict(value) if value is not None else {}
    
    class FHIRAnnotation:
        def __init__(self, value):
            self.value = dict(value) if value is not None else {}
    
    class FHIRTiming:
        def __init__(self, value):
            self.value = dict(value) if value is not None else {}
    
    class FHIRContactPoint:
        def __init__(self, value):
            self.value = dict(value) if value is not None else {}
    
    class FHIRRange:
        def __init__(self, value):
            self.value = dict(value) if value is not None else {}

T = TypeVar('T')


class FHIRFoundationDeserializationError(Exception):
    """Exception raised when FHIR foundation resource deserialization fails"""
    pass


class FHIRFoundationDeserializer:
    """
    Deserializer for FHIR R5 Foundation resources
    Uses Pydantic for validation and converts to native FHIR resource objects
    """
    
    def __init__(self, use_pydantic_validation: bool = True):
        """
        Initialize the deserializer
        
        Args:
            use_pydantic_validation: Whether to use Pydantic for validation
        """
        self.use_pydantic_validation = use_pydantic_validation and HAS_PYDANTIC
        
        # Resource type mapping
        self.resource_map = {
            'Patient': (PatientModel, Patient),
            'Practitioner': (PractitionerModel, Practitioner),
            'PractitionerRole': (PractitionerRoleModel, PractitionerRole),
            'Encounter': (EncounterModel, Encounter),
            'Person': (PersonModel, Person),
            'RelatedPerson': (RelatedPersonModel, RelatedPerson)
        }
    
    def deserialize_foundation_resource(self, json_data: Union[str, Dict[str, Any]], 
                                      resource_type: Optional[str] = None) -> Any:
        """
        Deserialize a FHIR foundation resource from JSON
        
        Args:
            json_data: JSON string or dictionary containing FHIR resource
            resource_type: Optional resource type hint
            
        Returns:
            Deserialized FHIR resource object
            
        Raises:
            FHIRFoundationDeserializationError: If deserialization fails
        """
        try:
            # Parse JSON if string
            if isinstance(json_data, str):
                data = json.loads(json_data)
            else:
                data = json_data.copy()
            
            # Determine resource type
            detected_type = data.get('resourceType')
            if not detected_type:
                if resource_type:
                    detected_type = resource_type
                    data['resourceType'] = resource_type
                else:
                    raise FHIRFoundationDeserializationError("No resourceType found in JSON data")
            
            # If resource_type hint is provided, validate it matches
            if resource_type and detected_type != resource_type:
                raise FHIRFoundationDeserializationError(
                    f"Resource type mismatch: expected {resource_type}, got {detected_type}"
                )
            
            # Check if we support this resource type
            if detected_type not in self.resource_map:
                raise FHIRFoundationDeserializationError(f"Unsupported resource type: {detected_type}")
            
            pydantic_model, resource_class = self.resource_map[detected_type]
            
            # Validate with Pydantic if enabled
            if self.use_pydantic_validation:
                validated_data = pydantic_model(**data)
                return self._convert_to_resource(validated_data.dict(), resource_class)
            else:
                return self._convert_to_resource(data, resource_class)
                
        except json.JSONDecodeError as e:
            raise FHIRFoundationDeserializationError(f"Invalid JSON: {e}")
        except Exception as e:
            raise FHIRFoundationDeserializationError(f"Deserialization failed: {e}")
    
    def _convert_to_resource(self, data: Dict[str, Any], resource_class: Type[T]) -> T:
        """Convert validated data to FHIR resource object"""
        # Convert datetime strings to datetime objects
        data = self._convert_datetime_fields(data)
        
        # Convert date strings to date objects
        data = self._convert_date_fields(data)
        
        # Create resource instance with minimal constructor args
        resource_type = data.get('resourceType', data.get('resource_type'))
        resource_id = data.get('id')
        
        # Create the resource instance
        resource = resource_class(resource_type=resource_type, id=resource_id)
        
        # Set all other fields as attributes
        self._set_resource_attributes(resource, data)
        
        return resource
    
    def _set_resource_attributes(self, resource: Any, data: Dict[str, Any]) -> None:
        """Set resource attributes from data"""
        # Skip constructor fields
        skip_fields = {'resourceType', 'resource_type', 'id'}
        
        for key, value in data.items():
            if key not in skip_fields:
                # Convert camelCase to snake_case for Python attributes
                attr_name = self._camel_to_snake(key)
                setattr(resource, attr_name, value)
    
    def _camel_to_snake(self, name: str) -> str:
        """Convert camelCase to snake_case"""
        import re
        # Insert underscore before uppercase letters that follow lowercase letters
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        # Insert underscore before uppercase letters that follow lowercase letters or digits
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    def _convert_datetime_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert datetime string fields to datetime objects"""
        datetime_fields = [
            'deceasedDateTime', 'lastUpdated', 'versionId'
        ]
        
        for field in datetime_fields:
            if field in data and isinstance(data[field], str):
                try:
                    data[field] = datetime.fromisoformat(data[field].replace('Z', '+00:00'))
                except ValueError:
                    pass  # Keep as string if parsing fails
        
        return data
    
    def _convert_date_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert date string fields to date objects"""
        date_fields = ['birthDate']
        
        for field in date_fields:
            if field in data and isinstance(data[field], str):
                try:
                    data[field] = datetime.fromisoformat(data[field]).date()
                except ValueError:
                    pass  # Keep as string if parsing fails
        
        return data
    
    # Convenience methods for specific resources
    def deserialize_patient(self, json_data: Union[str, Dict[str, Any]]) -> Patient:
        """Deserialize a Patient resource"""
        return self.deserialize_foundation_resource(json_data, 'Patient')
    
    def deserialize_practitioner(self, json_data: Union[str, Dict[str, Any]]) -> Practitioner:
        """Deserialize a Practitioner resource"""
        return self.deserialize_foundation_resource(json_data, 'Practitioner')
    
    def deserialize_practitioner_role(self, json_data: Union[str, Dict[str, Any]]) -> PractitionerRole:
        """Deserialize a PractitionerRole resource"""
        return self.deserialize_foundation_resource(json_data, 'PractitionerRole')
    
    def deserialize_encounter(self, json_data: Union[str, Dict[str, Any]]) -> Encounter:
        """Deserialize an Encounter resource"""
        return self.deserialize_foundation_resource(json_data, 'Encounter')
    
    def deserialize_person(self, json_data: Union[str, Dict[str, Any]]) -> Person:
        """Deserialize a Person resource"""
        return self.deserialize_foundation_resource(json_data, 'Person')
    
    def deserialize_related_person(self, json_data: Union[str, Dict[str, Any]]) -> RelatedPerson:
        """Deserialize a RelatedPerson resource"""
        return self.deserialize_foundation_resource(json_data, 'RelatedPerson')


# Convenience functions for direct use
def deserialize_patient(json_data: Union[str, Dict[str, Any]], 
                       use_pydantic_validation: bool = True) -> Patient:
    """
    Convenience function to deserialize a Patient resource
    
    Args:
        json_data: JSON string or dictionary containing Patient resource
        use_pydantic_validation: Whether to use Pydantic validation
        
    Returns:
        Patient resource object
    """
    deserializer = FHIRFoundationDeserializer(use_pydantic_validation)
    return deserializer.deserialize_patient(json_data)


def deserialize_practitioner(json_data: Union[str, Dict[str, Any]], 
                           use_pydantic_validation: bool = True) -> Practitioner:
    """
    Convenience function to deserialize a Practitioner resource
    
    Args:
        json_data: JSON string or dictionary containing Practitioner resource
        use_pydantic_validation: Whether to use Pydantic validation
        
    Returns:
        Practitioner resource object
    """
    deserializer = FHIRFoundationDeserializer(use_pydantic_validation)
    return deserializer.deserialize_practitioner(json_data)


def deserialize_practitioner_role(json_data: Union[str, Dict[str, Any]], 
                                 use_pydantic_validation: bool = True) -> PractitionerRole:
    """
    Convenience function to deserialize a PractitionerRole resource
    
    Args:
        json_data: JSON string or dictionary containing PractitionerRole resource
        use_pydantic_validation: Whether to use Pydantic validation
        
    Returns:
        PractitionerRole resource object
    """
    deserializer = FHIRFoundationDeserializer(use_pydantic_validation)
    return deserializer.deserialize_practitioner_role(json_data)


def deserialize_encounter(json_data: Union[str, Dict[str, Any]], 
                         use_pydantic_validation: bool = True) -> Encounter:
    """
    Convenience function to deserialize an Encounter resource
    
    Args:
        json_data: JSON string or dictionary containing Encounter resource
        use_pydantic_validation: Whether to use Pydantic validation
        
    Returns:
        Encounter resource object
    """
    deserializer = FHIRFoundationDeserializer(use_pydantic_validation)
    return deserializer.deserialize_encounter(json_data)


def deserialize_person(json_data: Union[str, Dict[str, Any]], 
                      use_pydantic_validation: bool = True) -> Person:
    """
    Convenience function to deserialize a Person resource
    
    Args:
        json_data: JSON string or dictionary containing Person resource
        use_pydantic_validation: Whether to use Pydantic validation
        
    Returns:
        Person resource object
    """
    deserializer = FHIRFoundationDeserializer(use_pydantic_validation)
    return deserializer.deserialize_person(json_data)


def deserialize_related_person(json_data: Union[str, Dict[str, Any]], 
                              use_pydantic_validation: bool = True) -> RelatedPerson:
    """
    Convenience function to deserialize a RelatedPerson resource
    
    Args:
        json_data: JSON string or dictionary containing RelatedPerson resource
        use_pydantic_validation: Whether to use Pydantic validation
        
    Returns:
        RelatedPerson resource object
    """
    deserializer = FHIRFoundationDeserializer(use_pydantic_validation)
    return deserializer.deserialize_related_person(json_data)


# Export all functions and classes
__all__ = [
    'FHIRFoundationDeserializer',
    'FHIRFoundationDeserializationError',
    'deserialize_patient',
    'deserialize_practitioner',
    'deserialize_practitioner_role',
    'deserialize_encounter',
    'deserialize_person',
    'deserialize_related_person'
]