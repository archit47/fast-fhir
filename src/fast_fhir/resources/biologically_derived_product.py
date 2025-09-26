"""FHIR R5 BiologicallyDerivedProduct resource implementation following DRY principles."""

from typing import Optional, List, Dict, Any
from .base import FHIRResourceBase


class BiologicallyDerivedProduct(FHIRResourceBase):
    """FHIR R5 BiologicallyDerivedProduct resource following DRY principles."""
    
    def __init__(self, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize BiologicallyDerivedProduct resource."""
        super().__init__("BiologicallyDerivedProduct", id, use_c_extensions)
    
    def _init_resource_fields(self) -> None:
        """Initialize BiologicallyDerivedProduct-specific fields."""
        self.product_category: Optional[Dict[str, Any]] = None
        self.product_code: Optional[Dict[str, Any]] = None
        self.parent: List[Dict[str, Any]] = []
        self.request: List[Dict[str, Any]] = []
        self.biological_source_event: Optional[str] = None
        self.processing: List[Dict[str, Any]] = []
        self.manipulation: Optional[str] = None
        self.storage: List[Dict[str, Any]] = []
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get the C extension create function name."""
        return "biologically_derived_product_create"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get the C extension parse function name."""
        return "biologically_derived_product_parse"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of _get_c_extension_parse_function."""
        return "biologically_derived_product_parse"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add BiologicallyDerivedProduct-specific fields to the result dictionary."""
        if self.product_category:
            result["productCategory"] = self.product_category
        if self.product_code:
            result["productCode"] = self.product_code
        if self.parent:
            result["parent"] = self.parent
        if self.request:
            result["request"] = self.request
        if self.biological_source_event:
            result["biologicalSourceEvent"] = self.biological_source_event
        if self.processing:
            result["processing"] = self.processing
        if self.manipulation:
            result["manipulation"] = self.manipulation
        if self.storage:
            result["storage"] = self.storage
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse BiologicallyDerivedProduct-specific fields from data dictionary."""
        self.product_category = data.get("productCategory")
        self.product_code = data.get("productCode")
        self.parent = data.get("parent", [])
        self.request = data.get("request", [])
        self.biological_source_event = data.get("biologicalSourceEvent")
        self.processing = data.get("processing", [])
        self.manipulation = data.get("manipulation")
        self.storage = data.get("storage", [])
    
    def _validate_resource_specific(self) -> bool:
        """Perform BiologicallyDerivedProduct-specific validation."""
        if not self.product_category:
            return False
        return True
    
    def validate(self) -> List[str]:
        """Validate BiologicallyDerivedProduct resource and return list of errors."""
        errors = []
        
        # Basic validation
        if not self.resource_type:
            errors.append("Resource type is required")
        
        # BiologicallyDerivedProduct-specific validation
        if not self.product_category:
            errors.append("BiologicallyDerivedProduct.productCategory is required")
        
        return errors
    
    def get_product_category(self) -> Optional[Dict[str, Any]]:
        """Get the product category."""
        return self.product_category
    
    def get_product_code(self) -> Optional[Dict[str, Any]]:
        """Get the product code."""
        return self.product_code
    
    def get_parent_products(self) -> List[Dict[str, Any]]:
        """Get all parent product references."""
        return self.parent.copy()
    
    def get_processing_steps(self) -> List[Dict[str, Any]]:
        """Get all processing steps."""
        return self.processing.copy()
    
    def get_storage_requirements(self) -> List[Dict[str, Any]]:
        """Get all storage requirements."""
        return self.storage.copy()
    
    def add_parent_product(self, parent: Dict[str, Any]) -> None:
        """Add a parent product reference."""
        if parent not in self.parent:
            self.parent.append(parent)
    
    def add_processing_step(self, processing_step: Dict[str, Any]) -> None:
        """Add a processing step."""
        self.processing.append(processing_step)
    
    def add_storage_requirement(self, storage_req: Dict[str, Any]) -> None:
        """Add a storage requirement."""
        self.storage.append(storage_req)
    
    def set_manipulation(self, manipulation: str) -> None:
        """Set the manipulation description."""
        self.manipulation = manipulation
    
    def get_biological_source_event(self) -> Optional[str]:
        """Get the biological source event identifier."""
        return self.biological_source_event
    
    def set_biological_source_event(self, event: str) -> None:
        """Set the biological source event identifier."""
        self.biological_source_event = event