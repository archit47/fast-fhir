"""Python wrapper for FHIR R5 data types implemented in C."""

from typing import Any, Dict, List, Optional, Union
import json

try:
    import fhir_datatypes_c
    HAS_C_DATATYPES = True
except ImportError:
    HAS_C_DATATYPES = False


class FHIRDataType:
    """Base class for all FHIR data types."""
    
    def __init__(self, use_c_extensions: bool = True):
        """Initialize FHIR data type."""
        self.use_c_extensions = use_c_extensions and HAS_C_DATATYPES
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        raise NotImplementedError
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRDataType':
        """Create from dictionary representation."""
        raise NotImplementedError


class FHIRString(FHIRDataType):
    """FHIR string data type."""
    
    def __init__(self, value: str, use_c_extensions: bool = True):
        """Initialize FHIR string."""
        super().__init__(use_c_extensions)
        self.value = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        if self.use_c_extensions:
            try:
                return fhir_datatypes_c.create_string(self.value)
            except:
                pass
        return {"value": self.value}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRString':
        """Create from dictionary."""
        return cls(data.get("value", ""))


class FHIRBoolean(FHIRDataType):
    """FHIR boolean data type."""
    
    def __init__(self, value: bool, use_c_extensions: bool = True):
        """Initialize FHIR boolean."""
        super().__init__(use_c_extensions)
        self.value = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        if self.use_c_extensions:
            try:
                return fhir_datatypes_c.create_boolean(self.value)
            except:
                pass
        return {"value": self.value}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRBoolean':
        """Create from dictionary."""
        return cls(data.get("value", False))


class FHIRInteger(FHIRDataType):
    """FHIR integer data type."""
    
    def __init__(self, value: int, use_c_extensions: bool = True):
        """Initialize FHIR integer."""
        super().__init__(use_c_extensions)
        self.value = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        if self.use_c_extensions:
            try:
                return fhir_datatypes_c.create_integer(self.value)
            except:
                pass
        return {"value": self.value}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRInteger':
        """Create from dictionary."""
        return cls(data.get("value", 0))


class FHIRDecimal(FHIRDataType):
    """FHIR decimal data type."""
    
    def __init__(self, value: float, use_c_extensions: bool = True):
        """Initialize FHIR decimal."""
        super().__init__(use_c_extensions)
        self.value = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        if self.use_c_extensions:
            try:
                return fhir_datatypes_c.create_decimal(self.value)
            except:
                pass
        return {"value": self.value}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRDecimal':
        """Create from dictionary."""
        return cls(data.get("value", 0.0))

class FHIRCoding(FHIRDataType):
    """FHIR Coding data type."""
    
    def __init__(self, system: Optional[str] = None, code: Optional[str] = None, 
                 display: Optional[str] = None, user_selected: bool = False,
                 use_c_extensions: bool = True):
        """Initialize FHIR Coding."""
        super().__init__(use_c_extensions)
        self.system = system
        self.code = code
        self.display = display
        self.user_selected = user_selected
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        if self.use_c_extensions:
            try:
                return fhir_datatypes_c.create_coding(self.system, self.code, self.display)
            except:
                pass
        
        result = {}
        if self.system:
            result["system"] = self.system
        if self.code:
            result["code"] = self.code
        if self.display:
            result["display"] = self.display
        if self.user_selected:
            result["userSelected"] = self.user_selected
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRCoding':
        """Create from dictionary."""
        return cls(
            system=data.get("system"),
            code=data.get("code"),
            display=data.get("display"),
            user_selected=data.get("userSelected", False)
        )
    
    @classmethod
    def from_json(cls, json_string: str) -> 'FHIRCoding':
        """Create from JSON string using C extension if available."""
        if HAS_C_DATATYPES:
            try:
                data = fhir_datatypes_c.parse_coding(json_string)
                return cls.from_dict(data)
            except:
                pass
        
        # Fallback to Python JSON parsing
        data = json.loads(json_string)
        return cls.from_dict(data)


class FHIRCodeableConcept(FHIRDataType):
    """FHIR CodeableConcept data type."""
    
    def __init__(self, text: Optional[str] = None, coding: Optional[List[FHIRCoding]] = None,
                 use_c_extensions: bool = True):
        """Initialize FHIR CodeableConcept."""
        super().__init__(use_c_extensions)
        self.text = text
        self.coding = coding or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {}
        if self.coding:
            result["coding"] = [c.to_dict() for c in self.coding]
        if self.text:
            result["text"] = self.text
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRCodeableConcept':
        """Create from dictionary."""
        coding_data = data.get("coding", [])
        coding = [FHIRCoding.from_dict(c) for c in coding_data]
        return cls(text=data.get("text"), coding=coding)


class FHIRQuantity(FHIRDataType):
    """FHIR Quantity data type."""
    
    def __init__(self, value: float, unit: Optional[str] = None, 
                 system: Optional[str] = None, code: Optional[str] = None,
                 comparator: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize FHIR Quantity."""
        super().__init__(use_c_extensions)
        self.value = value
        self.unit = unit
        self.system = system
        self.code = code
        self.comparator = comparator
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        if self.use_c_extensions:
            try:
                return fhir_datatypes_c.create_quantity(self.value, self.unit, self.system, self.code)
            except:
                pass
        
        result = {"value": self.value}
        if self.comparator:
            result["comparator"] = self.comparator
        if self.unit:
            result["unit"] = self.unit
        if self.system:
            result["system"] = self.system
        if self.code:
            result["code"] = self.code
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRQuantity':
        """Create from dictionary."""
        return cls(
            value=data.get("value", 0.0),
            unit=data.get("unit"),
            system=data.get("system"),
            code=data.get("code"),
            comparator=data.get("comparator")
        )
    
    @classmethod
    def from_json(cls, json_string: str) -> 'FHIRQuantity':
        """Create from JSON string using C extension if available."""
        if HAS_C_DATATYPES:
            try:
                data = fhir_datatypes_c.parse_quantity(json_string)
                return cls.from_dict(data)
            except:
                pass
        
        # Fallback to Python JSON parsing
        data = json.loads(json_string)
        return cls.from_dict(data)


class FHIRIdentifier(FHIRDataType):
    """FHIR Identifier data type."""
    
    def __init__(self, system: Optional[str] = None, value: Optional[str] = None,
                 use: Optional[str] = None, type_concept: Optional[FHIRCodeableConcept] = None,
                 use_c_extensions: bool = True):
        """Initialize FHIR Identifier."""
        super().__init__(use_c_extensions)
        self.system = system
        self.value = value
        self.use = use
        self.type = type_concept
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {}
        if self.use:
            result["use"] = self.use
        if self.type:
            result["type"] = self.type.to_dict()
        if self.system:
            result["system"] = self.system
        if self.value:
            result["value"] = self.value
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRIdentifier':
        """Create from dictionary."""
        type_data = data.get("type")
        type_concept = FHIRCodeableConcept.from_dict(type_data) if type_data else None
        
        return cls(
            system=data.get("system"),
            value=data.get("value"),
            use=data.get("use"),
            type_concept=type_concept
        )


class FHIRReference(FHIRDataType):
    """FHIR Reference data type."""
    
    def __init__(self, reference: Optional[str] = None, display: Optional[str] = None,
                 identifier: Optional[FHIRIdentifier] = None, use_c_extensions: bool = True):
        """Initialize FHIR Reference."""
        super().__init__(use_c_extensions)
        self.reference = reference
        self.display = display
        self.identifier = identifier
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {}
        if self.reference:
            result["reference"] = self.reference
        if self.display:
            result["display"] = self.display
        if self.identifier:
            result["identifier"] = self.identifier.to_dict()
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRReference':
        """Create from dictionary."""
        identifier_data = data.get("identifier")
        identifier = FHIRIdentifier.from_dict(identifier_data) if identifier_data else None
        
        return cls(
            reference=data.get("reference"),
            display=data.get("display"),
            identifier=identifier
        )


# Validation functions using C extensions when available
def validate_date(date_string: str) -> bool:
    """Validate FHIR date format."""
    if HAS_C_DATATYPES:
        try:
            return fhir_datatypes_c.validate_date(date_string)
        except:
            pass
    
    # Python fallback validation
    import re
    from datetime import datetime
    
    # Basic format check
    pattern = r'^\d{4}(-\d{2}(-\d{2})?)?$'
    if not re.match(pattern, date_string):
        return False
    
    # Validate actual date values
    try:
        parts = date_string.split('-')
        year = int(parts[0])
        
        if len(parts) >= 2:
            month = int(parts[1])
            if month < 1 or month > 12:
                return False
        
        if len(parts) == 3:
            day = int(parts[2])
            # Use datetime to validate the full date
            datetime(year, month, day)
        
        return True
    except (ValueError, IndexError):
        return False


def validate_time(time_string: str) -> bool:
    """Validate FHIR time format."""
    if HAS_C_DATATYPES:
        try:
            return fhir_datatypes_c.validate_time(time_string)
        except:
            pass
    
    # Python fallback validation
    import re
    from datetime import time
    
    # Basic format check
    pattern = r'^\d{2}:\d{2}:\d{2}(\.\d{3})?$'
    if not re.match(pattern, time_string):
        return False
    
    # Validate actual time values
    try:
        parts = time_string.split(':')
        hour = int(parts[0])
        minute = int(parts[1])
        
        # Handle seconds with optional milliseconds
        second_part = parts[2]
        if '.' in second_part:
            second = int(second_part.split('.')[0])
            millisecond = int(second_part.split('.')[1])
            if millisecond >= 1000:
                return False
        else:
            second = int(second_part)
        
        # Validate ranges
        if hour > 23 or minute > 59 or second > 59:
            return False
        
        # Use datetime.time to validate
        time(hour, minute, second)
        return True
    except (ValueError, IndexError):
        return False


def validate_uri(uri_string: str) -> bool:
    """Validate FHIR URI format."""
    if HAS_C_DATATYPES:
        try:
            return fhir_datatypes_c.validate_uri(uri_string)
        except:
            pass
    
    # Python fallback validation
    return ':' in uri_string


def validate_code(code_string: str) -> bool:
    """Validate FHIR code format."""
    if HAS_C_DATATYPES:
        try:
            return fhir_datatypes_c.validate_code(code_string)
        except:
            pass
    
    # Python fallback validation
    return len(code_string) > 0 and not any(c.isspace() for c in code_string)


# Export all data types and validation functions
__all__ = [
    'FHIRDataType', 'FHIRString', 'FHIRBoolean', 'FHIRInteger', 'FHIRDecimal',
    'FHIRCoding', 'FHIRCodeableConcept', 'FHIRQuantity', 'FHIRIdentifier', 'FHIRReference',
    'validate_date', 'validate_time', 'validate_uri', 'validate_code',
    'HAS_C_DATATYPES'
]


class FHIRDateTime(FHIRDataType):
    """FHIR dateTime data type."""
    
    def __init__(self, value: str, use_c_extensions: bool = True):
        """Initialize FHIR dateTime."""
        super().__init__(use_c_extensions)
        self.value = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        if self.use_c_extensions:
            try:
                return fhir_datatypes_c.create_datetime(self.value)
            except:
                pass
        return {"value": self.value}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRDateTime':
        """Create from dictionary."""
        return cls(data.get("value", ""))


class FHIRPeriod(FHIRDataType):
    """FHIR Period data type."""
    
    def __init__(self, start: Optional[str] = None, end: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize FHIR Period."""
        super().__init__(use_c_extensions)
        self.start = start
        self.end = end
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {}
        if self.start:
            result["start"] = self.start
        if self.end:
            result["end"] = self.end
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRPeriod':
        """Create from dictionary."""
        return cls(
            start=data.get("start"),
            end=data.get("end")
        )


class FHIRAnnotation(FHIRDataType):
    """FHIR Annotation data type."""
    
    def __init__(self, text: str, author_reference: Optional['FHIRReference'] = None, 
                 author_string: Optional[str] = None, time: Optional[str] = None, 
                 use_c_extensions: bool = True):
        """Initialize FHIR Annotation."""
        super().__init__(use_c_extensions)
        self.text = text
        self.author_reference = author_reference
        self.author_string = author_string
        self.time = time
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {"text": self.text}
        if self.author_reference:
            result["authorReference"] = self.author_reference.to_dict()
        if self.author_string:
            result["authorString"] = self.author_string
        if self.time:
            result["time"] = self.time
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRAnnotation':
        """Create from dictionary."""
        author_ref = None
        if "authorReference" in data:
            author_ref = FHIRReference.from_dict(data["authorReference"])
        
        return cls(
            text=data.get("text", ""),
            author_reference=author_ref,
            author_string=data.get("authorString"),
            time=data.get("time")
        )


class FHIRTiming(FHIRDataType):
    """FHIR Timing data type."""
    
    def __init__(self, event: Optional[List[str]] = None, repeat: Optional[Dict[str, Any]] = None,
                 code: Optional['FHIRCodeableConcept'] = None, use_c_extensions: bool = True):
        """Initialize FHIR Timing."""
        super().__init__(use_c_extensions)
        self.event = event or []
        self.repeat = repeat
        self.code = code
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {}
        if self.event:
            result["event"] = self.event
        if self.repeat:
            result["repeat"] = self.repeat
        if self.code:
            result["code"] = self.code.to_dict()
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRTiming':
        """Create from dictionary."""
        code = None
        if "code" in data:
            code = FHIRCodeableConcept.from_dict(data["code"])
        
        return cls(
            event=data.get("event", []),
            repeat=data.get("repeat"),
            code=code
        )


class FHIRContactPoint(FHIRDataType):
    """FHIR ContactPoint data type."""
    
    def __init__(self, system: Optional[str] = None, value: Optional[str] = None,
                 use: Optional[str] = None, rank: Optional[int] = None,
                 period: Optional['FHIRPeriod'] = None, use_c_extensions: bool = True):
        """Initialize FHIR ContactPoint."""
        super().__init__(use_c_extensions)
        self.system = system
        self.value = value
        self.use = use
        self.rank = rank
        self.period = period
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {}
        if self.system:
            result["system"] = self.system
        if self.value:
            result["value"] = self.value
        if self.use:
            result["use"] = self.use
        if self.rank:
            result["rank"] = self.rank
        if self.period:
            result["period"] = self.period.to_dict()
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRContactPoint':
        """Create from dictionary."""
        period = None
        if "period" in data:
            period = FHIRPeriod.from_dict(data["period"])
        
        return cls(
            system=data.get("system"),
            value=data.get("value"),
            use=data.get("use"),
            rank=data.get("rank"),
            period=period
        )


class FHIRRange(FHIRDataType):
    """FHIR Range data type."""
    
    def __init__(self, low: Optional['FHIRQuantity'] = None, high: Optional['FHIRQuantity'] = None,
                 use_c_extensions: bool = True):
        """Initialize FHIR Range."""
        super().__init__(use_c_extensions)
        self.low = low
        self.high = high
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {}
        if self.low:
            result["low"] = self.low.to_dict()
        if self.high:
            result["high"] = self.high.to_dict()
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRRange':
        """Create from dictionary."""
        low = None
        if "low" in data:
            low = FHIRQuantity.from_dict(data["low"])
        
        high = None
        if "high" in data:
            high = FHIRQuantity.from_dict(data["high"])
        
        return cls(low=low, high=high)


# Update the __all__ export list
__all__ = [
    'FHIRDataType', 'FHIRString', 'FHIRBoolean', 'FHIRInteger', 'FHIRDecimal',
    'FHIRCoding', 'FHIRCodeableConcept', 'FHIRQuantity', 'FHIRIdentifier', 'FHIRReference',
    'FHIRDateTime', 'FHIRPeriod', 'FHIRAnnotation', 'FHIRTiming', 'FHIRContactPoint', 'FHIRRange',
    'validate_date', 'validate_time', 'validate_uri', 'validate_code',
    'HAS_C_DATATYPES'
]
class FHIRDuration(FHIRQuantity):
    """FHIR Duration data type (extends Quantity)."""
    
    def __init__(self, value: Optional[float] = None, unit: Optional[str] = None,
                 system: Optional[str] = None, code: Optional[str] = None,
                 use_c_extensions: bool = True):
        """Initialize FHIR Duration."""
        super().__init__(value, unit, system, code, use_c_extensions)


class FHIRDate(FHIRDataType):
    """FHIR date data type."""
    
    def __init__(self, value: str, use_c_extensions: bool = True):
        """Initialize FHIR date."""
        super().__init__(use_c_extensions)
        self.value = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        if self.use_c_extensions:
            try:
                return fhir_datatypes_c.create_date(self.value)
            except:
                pass
        return {"value": self.value}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRDate':
        """Create from dictionary."""
        return cls(data.get("value", ""))


class FHIRRatio(FHIRDataType):
    """FHIR Ratio data type."""
    
    def __init__(self, numerator: Optional['FHIRQuantity'] = None, 
                 denominator: Optional['FHIRQuantity'] = None,
                 use_c_extensions: bool = True):
        """Initialize FHIR Ratio."""
        super().__init__(use_c_extensions)
        self.numerator = numerator
        self.denominator = denominator
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {}
        if self.numerator:
            result["numerator"] = self.numerator.to_dict()
        if self.denominator:
            result["denominator"] = self.denominator.to_dict()
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRRatio':
        """Create from dictionary."""
        numerator = None
        if "numerator" in data:
            numerator = FHIRQuantity.from_dict(data["numerator"])
        
        denominator = None
        if "denominator" in data:
            denominator = FHIRQuantity.from_dict(data["denominator"])
        
        return cls(numerator=numerator, denominator=denominator)


# Update the __all__ export list again
__all__ = [
    'FHIRDataType', 'FHIRString', 'FHIRBoolean', 'FHIRInteger', 'FHIRDecimal',
    'FHIRCoding', 'FHIRCodeableConcept', 'FHIRQuantity', 'FHIRIdentifier', 'FHIRReference',
    'FHIRDateTime', 'FHIRPeriod', 'FHIRAnnotation', 'FHIRTiming', 'FHIRContactPoint', 'FHIRRange',
    'FHIRDuration', 'FHIRDate', 'FHIRRatio',
    'validate_date', 'validate_time', 'validate_uri', 'validate_code',
    'HAS_C_DATATYPES'
]