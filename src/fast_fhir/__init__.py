"""Fast-FHIR: High-performance FHIR R5 parser and processor with C extensions."""

__version__ = "0.1.0"
__fhir_version__ = "5.0.0"

# Import main functionality for easy access
try:
    from .parser import FHIRParser
    from .fast_parser import FastFHIRParser
except ImportError:
    # Fallback if C extensions aren't built yet
    FHIRParser = None
    FastFHIRParser = None

# Import deserializers
try:
    from .deserializers import *
except ImportError:
    pass

__all__ = [
    "__version__",
    "__fhir_version__", 
    "FHIRParser",
    "FastFHIRParser",
]