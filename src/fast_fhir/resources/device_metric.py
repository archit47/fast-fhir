"""FHIR R5 DeviceMetric resource implementation following DRY principles."""

from typing import Optional, List, Dict, Any
from .base import FHIRResourceBase


class DeviceMetric(FHIRResourceBase):
    """FHIR R5 DeviceMetric resource following DRY principles."""
    
    def __init__(self, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize DeviceMetric resource."""
        super().__init__("DeviceMetric", id, use_c_extensions)
    
    def _init_resource_fields(self) -> None:
        """Initialize DeviceMetric-specific fields."""
        self.type: Optional[Dict[str, Any]] = None
        self.unit: Optional[Dict[str, Any]] = None
        self.source: Optional[Dict[str, Any]] = None
        self.parent: Optional[Dict[str, Any]] = None
        self.operational_status: Optional[str] = None  # on | off | standby | entered-in-error
        self.color: Optional[str] = None  # black | red | green | yellow | blue | magenta | cyan | white
        self.category: Optional[str] = None  # measurement | setting | calculation | unspecified
        self.measurement_period: Optional[Dict[str, Any]] = None
        self.calibration: List[Dict[str, Any]] = []
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get the C extension create function name."""
        return "create_device_metric"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get the C extension parse function name."""
        return "parse_device_metric"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of _get_c_extension_parse_function."""
        return "parse_device_metric"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add DeviceMetric-specific fields to the result dictionary."""
        if self.type:
            result["type"] = self.type
        if self.unit:
            result["unit"] = self.unit
        if self.source:
            result["source"] = self.source
        if self.parent:
            result["parent"] = self.parent
        if self.operational_status:
            result["operationalStatus"] = self.operational_status
        if self.color:
            result["color"] = self.color
        if self.category:
            result["category"] = self.category
        if self.measurement_period:
            result["measurementPeriod"] = self.measurement_period
        if self.calibration:
            result["calibration"] = self.calibration
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse DeviceMetric-specific fields from data dictionary."""
        self.type = data.get("type")
        self.unit = data.get("unit")
        self.source = data.get("source")
        self.parent = data.get("parent")
        self.operational_status = data.get("operationalStatus")
        self.color = data.get("color")
        self.category = data.get("category")
        self.measurement_period = data.get("measurementPeriod")
        self.calibration = data.get("calibration", [])
    
    def _validate_resource_specific(self) -> bool:
        """Perform DeviceMetric-specific validation."""
        # DeviceMetric requires type and category
        if not self.type or not self.category:
            return False
        
        # Validate operational status values
        valid_operational_statuses = ["on", "off", "standby", "entered-in-error"]
        if self.operational_status and self.operational_status not in valid_operational_statuses:
            return False
        
        # Validate color values
        valid_colors = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
        if self.color and self.color not in valid_colors:
            return False
        
        # Validate category values
        valid_categories = ["measurement", "setting", "calculation", "unspecified"]
        if self.category and self.category not in valid_categories:
            return False
        
        return True
    

    

    
    def is_operational(self) -> bool:
        """Check if the device metric is operational (on)."""
        return self.operational_status == "on"
    
    def is_measurement_metric(self) -> bool:
        """Check if this is a measurement metric."""
        return self.category == "measurement"
    
    def is_setting_metric(self) -> bool:
        """Check if this is a setting metric."""
        return self.category == "setting"
    
    def is_calculation_metric(self) -> bool:
        """Check if this is a calculation metric."""
        return self.category == "calculation"
    
    def get_metric_type(self) -> Optional[Dict[str, Any]]:
        """Get the metric type."""
        return self.type
    
    def get_unit(self) -> Optional[Dict[str, Any]]:
        """Get the unit of measurement."""
        return self.unit
    
    def get_source_device(self) -> Optional[Dict[str, Any]]:
        """Get the source device reference."""
        return self.source
    
    def get_parent_device(self) -> Optional[Dict[str, Any]]:
        """Get the parent device reference."""
        return self.parent
    
    def get_calibration_info(self) -> List[Dict[str, Any]]:
        """Get all calibration information."""
        return self.calibration.copy()
    
    def add_calibration(self, calibration: Dict[str, Any]) -> None:
        """Add calibration information."""
        self.calibration.append(calibration)
    
    def set_operational_status(self, status: str) -> None:
        """Set the operational status."""
        valid_statuses = ["on", "off", "standby", "entered-in-error"]
        if status in valid_statuses:
            self.operational_status = status
        else:
            raise ValueError(f"Invalid operational status: {status}")
    
    def set_color(self, color: str) -> None:
        """Set the color indicator."""
        valid_colors = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
        if color in valid_colors:
            self.color = color
        else:
            raise ValueError(f"Invalid color: {color}")
    
    def set_category(self, category: str) -> None:
        """Set the metric category."""
        valid_categories = ["measurement", "setting", "calculation", "unspecified"]
        if category in valid_categories:
            self.category = category
        else:
            raise ValueError(f"Invalid category: {category}")