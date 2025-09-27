"""
Pydantic models for FHIR R5 Entities resources
Provides validation and serialization for Organization, Location, HealthcareService, etc.
"""

from typing import List, Optional, Union, Any
from datetime import datetime, date, time
from enum import Enum

try:
    from pydantic import BaseModel, Field, validator, root_validator
    HAS_PYDANTIC = True
except ImportError:
    # Fallback base class if Pydantic is not available
    class BaseModel:
        pass
    def Field(*args, **kwargs):
        return None
    def validator(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    def root_validator(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    HAS_PYDANTIC = False

# Import base types from foundation models
from .pydantic_foundation import (
    FHIRResource, FHIRDomainResource, FHIRElement,
    HumanName, ContactPoint, Address, Identifier, Reference, CodeableConcept, Period,
    AdministrativeGender, ContactPointSystem, ContactPointUse, AddressUse, AddressType
)

# Entities-specific enums
class OrganizationType(str, Enum):
    PROV = "prov"  # Healthcare Provider
    DEPT = "dept"  # Hospital Department
    TEAM = "team"  # Organizational team
    GOVT = "govt"  # Government
    INS = "ins"    # Insurance Company
    PAY = "pay"    # Payer
    EDU = "edu"    # Educational Institute
    RELI = "reli"  # Religious Institution
    CRS = "crs"    # Clinical Research Sponsor
    CG = "cg"      # Community Group
    BUS = "bus"    # Non-Healthcare Business
    OTHER = "other" # Other

class LocationStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"

class LocationMode(str, Enum):
    INSTANCE = "instance"
    KIND = "kind"

class DaysOfWeek(str, Enum):
    MON = "mon"
    TUE = "tue"
    WED = "wed"
    THU = "thu"
    FRI = "fri"
    SAT = "sat"
    SUN = "sun"

class DeviceStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ENTERED_IN_ERROR = "entered-in-error"
    UNKNOWN = "unknown"



# Complex datatypes for entities resources
class OrganizationContact(BaseModel):
    """Organization contact information"""
    purpose: Optional[CodeableConcept] = None
    name: Optional[HumanName] = None
    telecom: Optional[List[ContactPoint]] = None
    address: Optional[Address] = None

class LocationPosition(BaseModel):
    """Location position (coordinates)"""
    longitude: float
    latitude: float
    altitude: Optional[float] = None

class LocationHoursOfOperation(BaseModel):
    """Location hours of operation"""
    daysOfWeek: Optional[List[DaysOfWeek]] = None
    allDay: Optional[bool] = None
    openingTime: Optional[time] = None
    closingTime: Optional[time] = None

class HealthcareServiceAvailableTime(BaseModel):
    """Healthcare service available time"""
    daysOfWeek: Optional[List[DaysOfWeek]] = None
    allDay: Optional[bool] = None
    availableStartTime: Optional[time] = None
    availableEndTime: Optional[time] = None

class HealthcareServiceNotAvailable(BaseModel):
    """Healthcare service not available time"""
    description: str
    during: Optional[Period] = None

class HealthcareServiceEligibility(BaseModel):
    """Healthcare service eligibility"""
    code: Optional[CodeableConcept] = None
    comment: Optional[str] = None

class DeviceUdiCarrier(BaseModel):
    """Device UDI carrier information"""
    deviceIdentifier: Optional[str] = None
    issuer: Optional[str] = None
    jurisdiction: Optional[str] = None
    carrierAIDC: Optional[str] = None  # Base64 encoded
    carrierHRF: Optional[str] = None   # Human readable form
    entryType: Optional[str] = None    # barcode | rfid | manual | card | self-reported | unknown

class DeviceVersion(BaseModel):
    """Device version information"""
    type: Optional[CodeableConcept] = None
    component: Optional[Identifier] = None
    value: str

class DeviceProperty(BaseModel):
    """Device property"""
    type: CodeableConcept
    valueQuantity: Optional[List[dict]] = None  # Quantity
    valueCode: Optional[List[CodeableConcept]] = None



# Entities Resource Models
class OrganizationModel(FHIRDomainResource):
    """FHIR Organization resource model"""
    resourceType: str = Field(default="Organization", const=True)
    
    identifier: Optional[List[Identifier]] = None
    active: Optional[bool] = None
    type: Optional[List[CodeableConcept]] = None
    name: Optional[str] = None
    alias: Optional[List[str]] = None
    description: Optional[str] = None
    contact: Optional[List[OrganizationContact]] = None
    partOf: Optional[Reference] = None
    endpoint: Optional[List[Reference]] = None

class LocationModel(FHIRDomainResource):
    """FHIR Location resource model"""
    resourceType: str = Field(default="Location", const=True)
    
    identifier: Optional[List[Identifier]] = None
    status: Optional[LocationStatus] = None
    operationalStatus: Optional[dict] = None  # Coding
    name: Optional[str] = None
    alias: Optional[List[str]] = None
    description: Optional[str] = None
    mode: Optional[LocationMode] = None
    type: Optional[List[CodeableConcept]] = None
    telecom: Optional[List[ContactPoint]] = None
    address: Optional[Address] = None
    physicalType: Optional[CodeableConcept] = None
    position: Optional[LocationPosition] = None
    managingOrganization: Optional[Reference] = None
    partOf: Optional[Reference] = None
    hoursOfOperation: Optional[List[LocationHoursOfOperation]] = None
    availabilityExceptions: Optional[str] = None
    endpoint: Optional[List[Reference]] = None

class HealthcareServiceModel(FHIRDomainResource):
    """FHIR HealthcareService resource model"""
    resourceType: str = Field(default="HealthcareService", const=True)
    
    identifier: Optional[List[Identifier]] = None
    active: Optional[bool] = None
    providedBy: Optional[Reference] = None
    category: Optional[List[CodeableConcept]] = None
    type: Optional[List[CodeableConcept]] = None
    specialty: Optional[List[CodeableConcept]] = None
    location: Optional[List[Reference]] = None
    name: Optional[str] = None
    comment: Optional[str] = None
    extraDetails: Optional[str] = None  # markdown
    photo: Optional[dict] = None        # Attachment
    telecom: Optional[List[ContactPoint]] = None
    coverageArea: Optional[List[Reference]] = None
    serviceProvisionCode: Optional[List[CodeableConcept]] = None
    eligibility: Optional[List[HealthcareServiceEligibility]] = None
    program: Optional[List[CodeableConcept]] = None
    characteristic: Optional[List[CodeableConcept]] = None
    communication: Optional[List[CodeableConcept]] = None
    referralMethod: Optional[List[CodeableConcept]] = None
    appointmentRequired: Optional[bool] = None
    availableTime: Optional[List[HealthcareServiceAvailableTime]] = None
    notAvailable: Optional[List[HealthcareServiceNotAvailable]] = None
    availabilityExceptions: Optional[str] = None
    endpoint: Optional[List[Reference]] = None

class EndpointModel(FHIRDomainResource):
    """FHIR Endpoint resource model"""
    resourceType: str = Field(default="Endpoint", const=True)
    
    identifier: Optional[List[Identifier]] = None
    status: str  # active | suspended | error | off | entered-in-error | test
    connectionType: dict  # Coding - required
    name: Optional[str] = None
    managingOrganization: Optional[Reference] = None
    contact: Optional[List[ContactPoint]] = None
    period: Optional[Period] = None
    payloadType: List[CodeableConcept]  # Required
    payloadMimeType: Optional[List[str]] = None
    address: str  # Required - URL
    header: Optional[List[str]] = None

class DeviceModel(FHIRDomainResource):
    """FHIR Device resource model"""
    resourceType: str = Field(default="Device", const=True)
    
    identifier: Optional[List[Identifier]] = None
    definition: Optional[Reference] = None
    udiCarrier: Optional[List[DeviceUdiCarrier]] = None
    status: Optional[DeviceStatus] = None
    statusReason: Optional[List[CodeableConcept]] = None
    distinctIdentifier: Optional[str] = None
    manufacturer: Optional[str] = None
    manufactureDate: Optional[datetime] = None
    expirationDate: Optional[datetime] = None
    lotNumber: Optional[str] = None
    serialNumber: Optional[str] = None
    deviceName: Optional[List[dict]] = None  # DeviceName
    modelNumber: Optional[str] = None
    partNumber: Optional[str] = None
    type: Optional[CodeableConcept] = None
    version: Optional[List[DeviceVersion]] = None
    property: Optional[List[DeviceProperty]] = None
    patient: Optional[Reference] = None
    owner: Optional[Reference] = None
    contact: Optional[List[ContactPoint]] = None
    location: Optional[Reference] = None
    url: Optional[str] = None
    note: Optional[List[dict]] = None  # Annotation
    safety: Optional[List[CodeableConcept]] = None
    parent: Optional[Reference] = None



class SubstanceModel(FHIRDomainResource):
    """FHIR Substance resource model"""
    resourceType: str = Field(default="Substance", const=True)
    
    identifier: Optional[List[Identifier]] = None
    instance: bool
    status: Optional[str] = None  # active | inactive | entered-in-error
    category: Optional[List[CodeableConcept]] = None
    code: CodeableConcept
    description: Optional[str] = None
    expiry: Optional[datetime] = None
    quantity: Optional[dict] = None  # Quantity
    ingredient: Optional[List[dict]] = None  # SubstanceIngredient

class OrganizationAffiliationModel(FHIRDomainResource):
    """FHIR OrganizationAffiliation resource model"""
    resourceType: str = Field(default="OrganizationAffiliation", const=True)
    
    identifier: Optional[List[Identifier]] = None
    active: Optional[bool] = None
    period: Optional[Period] = None
    organization: Optional[Reference] = None
    participatingOrganization: Optional[Reference] = None
    network: Optional[List[Reference]] = None
    code: Optional[List[CodeableConcept]] = None
    specialty: Optional[List[CodeableConcept]] = None
    location: Optional[List[Reference]] = None
    healthcareService: Optional[List[Reference]] = None
    telecom: Optional[List[ContactPoint]] = None
    endpoint: Optional[List[Reference]] = None

# Export all models
__all__ = [
    'HAS_PYDANTIC',
    'OrganizationModel',
    'LocationModel',
    'HealthcareServiceModel',
    'EndpointModel',
    'DeviceModel',

    'SubstanceModel',
    'OrganizationAffiliationModel',
    # Supporting classes
    'OrganizationContact',
    'LocationPosition',
    'LocationHoursOfOperation',
    'HealthcareServiceAvailableTime',
    'HealthcareServiceNotAvailable',
    'HealthcareServiceEligibility',
    'DeviceUdiCarrier',
    'DeviceVersion',
    'DeviceProperty',

    # Enums
    'OrganizationType',
    'LocationStatus',
    'LocationMode',
    'DaysOfWeek',
    'DeviceStatus',

]