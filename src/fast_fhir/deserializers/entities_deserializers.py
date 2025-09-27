"""
FHIR R5 Entities Resource Deserializers
Converts JSON strings to FHIR entities resource objects (Organization, Location, etc.)
"""

import json
from typing import Union, Dict, Any, Optional, Type, TypeVar
from datetime import datetime, date

from .pydantic_entities import (
    HAS_PYDANTIC,
    OrganizationModel, LocationModel, HealthcareServiceModel, EndpointModel,
    DeviceModel, SubstanceModel, OrganizationAffiliationModel
)

# Import the actual FHIR resource classes
try:
    from ..resources.organization import Organization
    from ..resources.location import Location
    from ..resources.healthcare_service import HealthcareService
    from ..resources.endpoint import Endpoint
    from ..resources.device import Device

    from ..resources.substance import Substance
    from ..resources.organization_affiliation import OrganizationAffiliation
    from ..resources.biologically_derived_product import BiologicallyDerivedProduct
    from ..resources.nutrition_product import NutritionProduct
    from ..resources.device_metric import DeviceMetric
except ImportError:
    # Fallback classes if resource classes aren't implemented yet
    class Organization:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class Location:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class HealthcareService:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class Endpoint:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class Device:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    

    
    class Substance:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class OrganizationAffiliation:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class BiologicallyDerivedProduct:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class NutritionProduct:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class DeviceMetric:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

T = TypeVar('T')


class FHIREntitiesDeserializationError(Exception):
    """Exception raised when FHIR entities resource deserialization fails"""
    pass


class FHIREntitiesDeserializer:
    """
    Deserializer for FHIR R5 Entities resources
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
            'Organization': (OrganizationModel, Organization),
            'Location': (LocationModel, Location),
            'HealthcareService': (HealthcareServiceModel, HealthcareService),
            'Endpoint': (EndpointModel, Endpoint),
            'Device': (DeviceModel, Device),
            'Substance': (SubstanceModel, Substance),
            'OrganizationAffiliation': (OrganizationAffiliationModel, OrganizationAffiliation),
            'BiologicallyDerivedProduct': (None, BiologicallyDerivedProduct),  # No Pydantic model yet
            'NutritionProduct': (None, NutritionProduct),  # No Pydantic model yet
            'DeviceMetric': (None, DeviceMetric)  # No Pydantic model yet
        }
    
    def deserialize_entities_resource(self, json_data: Union[str, Dict[str, Any]], 
                                    resource_type: Optional[str] = None) -> Any:
        """
        Deserialize a FHIR entities resource from JSON
        
        Args:
            json_data: JSON string or dictionary containing FHIR resource
            resource_type: Optional resource type hint
            
        Returns:
            Deserialized FHIR resource object
            
        Raises:
            FHIREntitiesDeserializationError: If deserialization fails
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
                    raise FHIREntitiesDeserializationError("No resourceType found in JSON data")
            
            # If resource_type hint is provided, validate it matches
            if resource_type and detected_type != resource_type:
                raise FHIREntitiesDeserializationError(
                    f"Resource type mismatch: expected {resource_type}, got {detected_type}"
                )
            
            # Check if we support this resource type
            if detected_type not in self.resource_map:
                raise FHIREntitiesDeserializationError(f"Unsupported resource type: {detected_type}")
            
            pydantic_model, resource_class = self.resource_map[detected_type]
            
            # Validate with Pydantic if enabled and model exists
            if self.use_pydantic_validation and pydantic_model:
                validated_data = pydantic_model(**data)
                return self._convert_to_resource(validated_data.dict(), resource_class)
            else:
                return self._convert_to_resource(data, resource_class)
                
        except json.JSONDecodeError as e:
            raise FHIREntitiesDeserializationError(f"Invalid JSON: {e}")
        except Exception as e:
            raise FHIREntitiesDeserializationError(f"Deserialization failed: {e}")
    
    def _convert_to_resource(self, data: Dict[str, Any], resource_class: Type[T]) -> T:
        """Convert validated data to FHIR resource object"""
        # Convert datetime strings to datetime objects
        data = self._convert_datetime_fields(data)
        
        # Convert date strings to date objects
        data = self._convert_date_fields(data)
        
        # Create resource instance with minimal constructor args
        resource_id = data.get('id')
        
        # Try to create the resource instance - some classes may not accept resource_type
        try:
            resource_type = data.get('resourceType', data.get('resource_type'))
            resource = resource_class(resource_type=resource_type, id=resource_id)
        except TypeError:
            # Fallback for classes that don't accept resource_type parameter
            try:
                resource = resource_class(id=resource_id)
            except TypeError:
                # Final fallback for classes with different constructor signatures
                resource = resource_class()
                if resource_id:
                    resource.id = resource_id
        
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
            'manufactureDate', 'expirationDate', 'expiry', 'lastUpdated'
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
        date_fields = []  # Entities resources typically use datetime, not date
        
        for field in date_fields:
            if field in data and isinstance(data[field], str):
                try:
                    data[field] = datetime.fromisoformat(data[field]).date()
                except ValueError:
                    pass  # Keep as string if parsing fails
        
        return data
    
    # Convenience methods for specific resources
    def deserialize_organization(self, json_data: Union[str, Dict[str, Any]]) -> Organization:
        """Deserialize an Organization resource"""
        return self.deserialize_entities_resource(json_data, 'Organization')
    
    def deserialize_location(self, json_data: Union[str, Dict[str, Any]]) -> Location:
        """Deserialize a Location resource"""
        return self.deserialize_entities_resource(json_data, 'Location')
    
    def deserialize_healthcare_service(self, json_data: Union[str, Dict[str, Any]]) -> HealthcareService:
        """Deserialize a HealthcareService resource"""
        return self.deserialize_entities_resource(json_data, 'HealthcareService')
    
    def deserialize_endpoint(self, json_data: Union[str, Dict[str, Any]]) -> Endpoint:
        """Deserialize an Endpoint resource"""
        return self.deserialize_entities_resource(json_data, 'Endpoint')
    
    def deserialize_device(self, json_data: Union[str, Dict[str, Any]]) -> Device:
        """Deserialize a Device resource"""
        return self.deserialize_entities_resource(json_data, 'Device')
    

    
    def deserialize_substance(self, json_data: Union[str, Dict[str, Any]]) -> Substance:
        """Deserialize a Substance resource"""
        return self.deserialize_entities_resource(json_data, 'Substance')
    
    def deserialize_organization_affiliation(self, json_data: Union[str, Dict[str, Any]]) -> OrganizationAffiliation:
        """Deserialize an OrganizationAffiliation resource"""
        return self.deserialize_entities_resource(json_data, 'OrganizationAffiliation')
    
    def deserialize_biologically_derived_product(self, json_data: Union[str, Dict[str, Any]]) -> BiologicallyDerivedProduct:
        """Deserialize a BiologicallyDerivedProduct resource"""
        return self.deserialize_entities_resource(json_data, 'BiologicallyDerivedProduct')
    
    def deserialize_nutrition_product(self, json_data: Union[str, Dict[str, Any]]) -> NutritionProduct:
        """Deserialize a NutritionProduct resource"""
        return self.deserialize_entities_resource(json_data, 'NutritionProduct')
    
    def deserialize_device_metric(self, json_data: Union[str, Dict[str, Any]]) -> DeviceMetric:
        """Deserialize a DeviceMetric resource"""
        return self.deserialize_entities_resource(json_data, 'DeviceMetric')


# Convenience functions for direct use
def deserialize_organization(json_data: Union[str, Dict[str, Any]], 
                           use_pydantic_validation: bool = True) -> Organization:
    """Convenience function to deserialize an Organization resource"""
    deserializer = FHIREntitiesDeserializer(use_pydantic_validation)
    return deserializer.deserialize_organization(json_data)


def deserialize_location(json_data: Union[str, Dict[str, Any]], 
                        use_pydantic_validation: bool = True) -> Location:
    """Convenience function to deserialize a Location resource"""
    deserializer = FHIREntitiesDeserializer(use_pydantic_validation)
    return deserializer.deserialize_location(json_data)


def deserialize_healthcare_service(json_data: Union[str, Dict[str, Any]], 
                                  use_pydantic_validation: bool = True) -> HealthcareService:
    """Convenience function to deserialize a HealthcareService resource"""
    deserializer = FHIREntitiesDeserializer(use_pydantic_validation)
    return deserializer.deserialize_healthcare_service(json_data)


def deserialize_endpoint(json_data: Union[str, Dict[str, Any]], 
                        use_pydantic_validation: bool = True) -> Endpoint:
    """Convenience function to deserialize an Endpoint resource"""
    deserializer = FHIREntitiesDeserializer(use_pydantic_validation)
    return deserializer.deserialize_endpoint(json_data)


def deserialize_device(json_data: Union[str, Dict[str, Any]], 
                      use_pydantic_validation: bool = True) -> Device:
    """Convenience function to deserialize a Device resource"""
    deserializer = FHIREntitiesDeserializer(use_pydantic_validation)
    return deserializer.deserialize_device(json_data)





def deserialize_substance(json_data: Union[str, Dict[str, Any]], 
                         use_pydantic_validation: bool = True) -> Substance:
    """Convenience function to deserialize a Substance resource"""
    deserializer = FHIREntitiesDeserializer(use_pydantic_validation)
    return deserializer.deserialize_substance(json_data)


def deserialize_organization_affiliation(json_data: Union[str, Dict[str, Any]], 
                                       use_pydantic_validation: bool = True) -> OrganizationAffiliation:
    """Convenience function to deserialize an OrganizationAffiliation resource"""
    deserializer = FHIREntitiesDeserializer(use_pydantic_validation)
    return deserializer.deserialize_organization_affiliation(json_data)


def deserialize_biologically_derived_product(json_data: Union[str, Dict[str, Any]], 
                                           use_pydantic_validation: bool = True) -> BiologicallyDerivedProduct:
    """Convenience function to deserialize a BiologicallyDerivedProduct resource"""
    deserializer = FHIREntitiesDeserializer(use_pydantic_validation)
    return deserializer.deserialize_biologically_derived_product(json_data)


def deserialize_nutrition_product(json_data: Union[str, Dict[str, Any]], 
                                 use_pydantic_validation: bool = True) -> NutritionProduct:
    """Convenience function to deserialize a NutritionProduct resource"""
    deserializer = FHIREntitiesDeserializer(use_pydantic_validation)
    return deserializer.deserialize_nutrition_product(json_data)


def deserialize_device_metric(json_data: Union[str, Dict[str, Any]], 
                             use_pydantic_validation: bool = True) -> DeviceMetric:
    """Convenience function to deserialize a DeviceMetric resource"""
    deserializer = FHIREntitiesDeserializer(use_pydantic_validation)
    return deserializer.deserialize_device_metric(json_data)


# Export all functions and classes
__all__ = [
    'FHIREntitiesDeserializer',
    'FHIREntitiesDeserializationError',
    'deserialize_organization',
    'deserialize_location',
    'deserialize_healthcare_service',
    'deserialize_endpoint',
    'deserialize_device',

    'deserialize_substance',
    'deserialize_organization_affiliation',
    'deserialize_biologically_derived_product',
    'deserialize_nutrition_product',
    'deserialize_device_metric'
]