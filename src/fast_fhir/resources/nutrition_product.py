"""FHIR R5 NutritionProduct resource implementation following DRY principles."""

from typing import Optional, List, Dict, Any
from .base import FHIRResourceBase


class NutritionProduct(FHIRResourceBase):
    """FHIR R5 NutritionProduct resource following DRY principles."""
    
    def __init__(self, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize NutritionProduct resource."""
        super().__init__("NutritionProduct", id, use_c_extensions)
    
    def _init_resource_fields(self) -> None:
        """Initialize NutritionProduct-specific fields."""
        # NutritionProduct-specific attributes
        self.status: Optional[str] = None  # active | inactive | entered-in-error
        self.category: List[Dict[str, Any]] = []
        self.code: Optional[Dict[str, Any]] = None
        self.manufacturer: Optional[str] = None
        self.nutrient: List[Dict[str, Any]] = []
        self.ingredient: List[Dict[str, Any]] = []
        self.known_allergen: List[Dict[str, Any]] = []
        self.characteristic: List[Dict[str, Any]] = []
        self.instance: List[Dict[str, Any]] = []
        self.note: List[Dict[str, Any]] = []
    def to_dict(self) -> Dict[str, Any]:
        """Convert NutritionProduct to dictionary representation."""
        result = super().to_dict()
        
        # Add NutritionProduct-specific fields
        if self.status:
            result["status"] = self.status
        if self.category:
            result["category"] = self.category
        if self.code:
            result["code"] = self.code
        if self.manufacturer:
            result["manufacturer"] = self.manufacturer
        if self.nutrient:
            result["nutrient"] = self.nutrient
        if self.ingredient:
            result["ingredient"] = self.ingredient
        if self.known_allergen:
            result["knownAllergen"] = self.known_allergen
        if self.characteristic:
            result["characteristic"] = self.characteristic
        if self.instance:
            result["instance"] = self.instance
        if self.note:
            result["note"] = self.note
        
        return result
    
    
    
    def is_active(self) -> bool:
        """Check if the nutrition product is active."""
        return self.status == "active"
    
    def is_inactive(self) -> bool:
        """Check if the nutrition product is inactive."""
        return self.status == "inactive"
    
    def get_product_code(self) -> Optional[Dict[str, Any]]:
        """Get the product code."""
        return self.code
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """Get all product categories."""
        return self.category.copy()
    
    def get_manufacturer(self) -> Optional[str]:
        """Get the manufacturer name."""
        return self.manufacturer
    
    def get_nutrients(self) -> List[Dict[str, Any]]:
        """Get all nutrient information."""
        return self.nutrient.copy()
    
    def get_ingredients(self) -> List[Dict[str, Any]]:
        """Get all ingredient information."""
        return self.ingredient.copy()
    
    def get_known_allergens(self) -> List[Dict[str, Any]]:
        """Get all known allergens."""
        return self.known_allergen.copy()
    
    def get_characteristics(self) -> List[Dict[str, Any]]:
        """Get all product characteristics."""
        return self.characteristic.copy()
    
    def get_instances(self) -> List[Dict[str, Any]]:
        """Get all product instances."""
        return self.instance.copy()
    
    def add_category(self, category: Dict[str, Any]) -> None:
        """Add a product category."""
        if category not in self.category:
            self.category.append(category)
    
    def add_nutrient(self, nutrient: Dict[str, Any]) -> None:
        """Add nutrient information."""
        self.nutrient.append(nutrient)
    
    def add_ingredient(self, ingredient: Dict[str, Any]) -> None:
        """Add ingredient information."""
        self.ingredient.append(ingredient)
    
    def add_known_allergen(self, allergen: Dict[str, Any]) -> None:
        """Add a known allergen."""
        if allergen not in self.known_allergen:
            self.known_allergen.append(allergen)
    
    def add_characteristic(self, characteristic: Dict[str, Any]) -> None:
        """Add a product characteristic."""
        self.characteristic.append(characteristic)
    
    def add_instance(self, instance: Dict[str, Any]) -> None:
        """Add a product instance."""
        self.instance.append(instance)
    
    def add_note(self, note: Dict[str, Any]) -> None:
        """Add a note."""
        self.note.append(note)
    
    def set_status(self, status: str) -> None:
        """Set the product status."""
        valid_statuses = ["active", "inactive", "entered-in-error"]
        if status in valid_statuses:
            self.status = status
        else:
            raise ValueError(f"Invalid status: {status}")
    
    def set_manufacturer(self, manufacturer: str) -> None:
        """Set the manufacturer name."""
        self.manufacturer = manufacturer
    
    def has_allergen(self, allergen_code: str) -> bool:
        """Check if the product contains a specific allergen."""
        for allergen in self.known_allergen:
            if isinstance(allergen, dict) and allergen.get("coding"):
                for coding in allergen["coding"]:
                    if coding.get("code") == allergen_code:
                        return True
        return False
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get the C extension create function name."""
        return "create_nutrition_product"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get the C extension parse function name."""
        return "parse_nutrition_product"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of _get_c_extension_parse_function."""
        return "parse_nutrition_product"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add NutritionProduct-specific fields to the result dictionary."""
        # TODO: Implement resource-specific field serialization
        pass
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse NutritionProduct-specific fields from data dictionary."""
        # TODO: Implement resource-specific field parsing
        pass
    
    def _validate_resource_specific(self) -> bool:
        """Perform NutritionProduct-specific validation."""
        # NutritionProduct requires status
        return self.status is not None
