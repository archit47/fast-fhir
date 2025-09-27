"""
Pydantic models for FHIR R5 Foundation resources
Provides validation and serialization for core FHIR resources like Patient, Practitioner, etc.
"""

from typing import List, Optional, Union, Any, Literal
from datetime import datetime, date
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

# Base FHIR types
class FHIRElement(BaseModel):
    """Base FHIR Element"""
    id: Optional[str] = None
    extension: Optional[List[dict]] = None

class FHIRResource(BaseModel):
    """Base FHIR Resource"""
    resourceType: str
    id: Optional[str] = None
    meta: Optional[dict] = None
    implicitRules: Optional[str] = None
    language: Optional[str] = None

class FHIRDomainResource(FHIRResource):
    """Base FHIR Domain Resource"""
    text: Optional[dict] = None
    contained: Optional[List[dict]] = None
    extension: Optional[List[dict]] = None
    modifierExtension: Optional[List[dict]] = None

# Enums for FHIR value sets
class AdministrativeGender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"

class NameUse(str, Enum):
    USUAL = "usual"
    OFFICIAL = "official"
    TEMP = "temp"
    NICKNAME = "nickname"
    ANONYMOUS = "anonymous"
    OLD = "old"
    MAIDEN = "maiden"

class ContactPointSystem(str, Enum):
    PHONE = "phone"
    FAX = "fax"
    EMAIL = "email"
    PAGER = "pager"
    URL = "url"
    SMS = "sms"
    OTHER = "other"

class ContactPointUse(str, Enum):
    HOME = "home"
    WORK = "work"
    TEMP = "temp"
    OLD = "old"
    MOBILE = "mobile"

class AddressUse(str, Enum):
    HOME = "home"
    WORK = "work"
    TEMP = "temp"
    OLD = "old"
    BILLING = "billing"

class AddressType(str, Enum):
    POSTAL = "postal"
    PHYSICAL = "physical"
    BOTH = "both"

class EncounterStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in-progress"
    ON_HOLD = "on-hold"
    DISCHARGED = "discharged"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DISCONTINUED = "discontinued"
    ENTERED_IN_ERROR = "entered-in-error"
    UNKNOWN = "unknown"

# Complex FHIR datatypes
class HumanName(BaseModel):
    """FHIR HumanName datatype"""
    use: Optional[NameUse] = None
    text: Optional[str] = None
    family: Optional[str] = None
    given: Optional[List[str]] = None
    prefix: Optional[List[str]] = None
    suffix: Optional[List[str]] = None
    period: Optional[dict] = None

class ContactPoint(BaseModel):
    """FHIR ContactPoint datatype"""
    system: Optional[ContactPointSystem] = None
    value: Optional[str] = None
    use: Optional[ContactPointUse] = None
    rank: Optional[int] = None
    period: Optional[dict] = None

class Address(BaseModel):
    """FHIR Address datatype"""
    use: Optional[AddressUse] = None
    type: Optional[AddressType] = None
    text: Optional[str] = None
    line: Optional[List[str]] = None
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None
    period: Optional[dict] = None

class Identifier(BaseModel):
    """FHIR Identifier datatype"""
    use: Optional[str] = None
    type: Optional[dict] = None
    system: Optional[str] = None
    value: Optional[str] = None
    period: Optional[dict] = None
    assigner: Optional[dict] = None

class Reference(BaseModel):
    """FHIR Reference datatype"""
    reference: Optional[str] = None
    type: Optional[str] = None
    identifier: Optional[Identifier] = None
    display: Optional[str] = None

class CodeableConcept(BaseModel):
    """FHIR CodeableConcept datatype"""
    coding: Optional[List[dict]] = None
    text: Optional[str] = None

class Period(BaseModel):
    """FHIR Period datatype"""
    start: Optional[datetime] = None
    end: Optional[datetime] = None

# Foundation Resource Models
class PatientContact(BaseModel):
    """Patient contact information"""
    relationship: Optional[List[CodeableConcept]] = None
    name: Optional[HumanName] = None
    telecom: Optional[List[ContactPoint]] = None
    address: Optional[Address] = None
    gender: Optional[AdministrativeGender] = None
    organization: Optional[Reference] = None
    period: Optional[Period] = None

class PatientCommunication(BaseModel):
    """Patient communication preferences"""
    language: CodeableConcept
    preferred: Optional[bool] = None

class PatientLink(BaseModel):
    """Patient link to another patient resource"""
    other: Reference
    type: str  # replaced-by | replaces | refer | seealso

class PatientModel(FHIRDomainResource):
    """FHIR Patient resource model"""
    resourceType: Literal["Patient"] = Field(default="Patient")
    
    # Patient-specific fields
    identifier: Optional[List[Identifier]] = None
    active: Optional[bool] = None
    name: Optional[List[HumanName]] = None
    telecom: Optional[List[ContactPoint]] = None
    gender: Optional[AdministrativeGender] = None
    birthDate: Optional[date] = None
    deceasedBoolean: Optional[bool] = None
    deceasedDateTime: Optional[datetime] = None
    address: Optional[List[Address]] = None
    maritalStatus: Optional[CodeableConcept] = None
    multipleBirthBoolean: Optional[bool] = None
    multipleBirthInteger: Optional[int] = None
    photo: Optional[List[dict]] = None  # Attachment
    contact: Optional[List[PatientContact]] = None
    communication: Optional[List[PatientCommunication]] = None
    generalPractitioner: Optional[List[Reference]] = None
    managingOrganization: Optional[Reference] = None
    link: Optional[List[PatientLink]] = None

    @validator('deceasedBoolean', 'deceasedDateTime')
    def validate_deceased(cls, v, values):
        """Ensure only one deceased field is set"""
        if 'deceasedBoolean' in values and 'deceasedDateTime' in values:
            if values.get('deceasedBoolean') is not None and v is not None:
                raise ValueError("Cannot have both deceasedBoolean and deceasedDateTime")
        return v

class PractitionerQualification(BaseModel):
    """Practitioner qualification"""
    identifier: Optional[List[Identifier]] = None
    code: CodeableConcept
    period: Optional[Period] = None
    issuer: Optional[Reference] = None

class PractitionerModel(FHIRDomainResource):
    """FHIR Practitioner resource model"""
    resourceType: Literal["Practitioner"] = Field(default="Practitioner")
    
    identifier: Optional[List[Identifier]] = None
    active: Optional[bool] = None
    name: Optional[List[HumanName]] = None
    telecom: Optional[List[ContactPoint]] = None
    address: Optional[List[Address]] = None
    gender: Optional[AdministrativeGender] = None
    birthDate: Optional[date] = None
    photo: Optional[List[dict]] = None  # Attachment
    qualification: Optional[List[PractitionerQualification]] = None
    communication: Optional[List[CodeableConcept]] = None

class PractitionerRoleAvailableTime(BaseModel):
    """Available time for practitioner role"""
    daysOfWeek: Optional[List[str]] = None  # mon | tue | wed | thu | fri | sat | sun
    allDay: Optional[bool] = None
    availableStartTime: Optional[str] = None  # time format
    availableEndTime: Optional[str] = None    # time format

class PractitionerRoleNotAvailable(BaseModel):
    """Not available time for practitioner role"""
    description: str
    during: Optional[Period] = None

class PractitionerRoleModel(FHIRDomainResource):
    """FHIR PractitionerRole resource model"""
    resourceType: Literal["PractitionerRole"] = Field(default="PractitionerRole")
    
    identifier: Optional[List[Identifier]] = None
    active: Optional[bool] = None
    period: Optional[Period] = None
    practitioner: Optional[Reference] = None
    organization: Optional[Reference] = None
    code: Optional[List[CodeableConcept]] = None
    specialty: Optional[List[CodeableConcept]] = None
    location: Optional[List[Reference]] = None
    healthcareService: Optional[List[Reference]] = None
    telecom: Optional[List[ContactPoint]] = None
    availableTime: Optional[List[PractitionerRoleAvailableTime]] = None
    notAvailable: Optional[List[PractitionerRoleNotAvailable]] = None
    availabilityExceptions: Optional[str] = None
    endpoint: Optional[List[Reference]] = None

class EncounterStatusHistory(BaseModel):
    """Encounter status history"""
    status: EncounterStatus
    period: Period

class EncounterParticipant(BaseModel):
    """Encounter participant"""
    type: Optional[List[CodeableConcept]] = None
    period: Optional[Period] = None
    individual: Optional[Reference] = None

class EncounterDiagnosis(BaseModel):
    """Encounter diagnosis"""
    condition: Reference
    use: Optional[CodeableConcept] = None
    rank: Optional[int] = None

class EncounterHospitalization(BaseModel):
    """Encounter hospitalization details"""
    preAdmissionIdentifier: Optional[Identifier] = None
    origin: Optional[Reference] = None
    admitSource: Optional[CodeableConcept] = None
    reAdmission: Optional[CodeableConcept] = None
    dietPreference: Optional[List[CodeableConcept]] = None
    specialCourtesy: Optional[List[CodeableConcept]] = None
    specialArrangement: Optional[List[CodeableConcept]] = None
    destination: Optional[Reference] = None
    dischargeDisposition: Optional[CodeableConcept] = None

class EncounterLocation(BaseModel):
    """Encounter location"""
    location: Reference
    status: Optional[str] = None  # planned | active | reserved | completed
    physicalType: Optional[CodeableConcept] = None
    period: Optional[Period] = None

class EncounterModel(FHIRDomainResource):
    """FHIR Encounter resource model"""
    resourceType: Literal["Encounter"] = Field(default="Encounter")
    
    identifier: Optional[List[Identifier]] = None
    status: EncounterStatus
    statusHistory: Optional[List[EncounterStatusHistory]] = None
    class_: Optional[dict] = Field(None, alias="class")  # Coding
    classHistory: Optional[List[dict]] = None
    type: Optional[List[CodeableConcept]] = None
    serviceType: Optional[CodeableConcept] = None
    priority: Optional[CodeableConcept] = None
    subject: Optional[Reference] = None
    episodeOfCare: Optional[List[Reference]] = None
    basedOn: Optional[List[Reference]] = None
    participant: Optional[List[EncounterParticipant]] = None
    appointment: Optional[List[Reference]] = None
    period: Optional[Period] = None
    length: Optional[dict] = None  # Duration
    reasonCode: Optional[List[CodeableConcept]] = None
    reasonReference: Optional[List[Reference]] = None
    diagnosis: Optional[List[EncounterDiagnosis]] = None
    account: Optional[List[Reference]] = None
    hospitalization: Optional[EncounterHospitalization] = None
    location: Optional[List[EncounterLocation]] = None
    serviceProvider: Optional[Reference] = None
    partOf: Optional[Reference] = None

class PersonLink(BaseModel):
    """Person link to another person or patient"""
    target: Reference
    assurance: Optional[str] = None  # level1 | level2 | level3 | level4

class PersonModel(FHIRDomainResource):
    """FHIR Person resource model"""
    resourceType: Literal["Person"] = Field(default="Person")
    
    identifier: Optional[List[Identifier]] = None
    name: Optional[List[HumanName]] = None
    telecom: Optional[List[ContactPoint]] = None
    gender: Optional[AdministrativeGender] = None
    birthDate: Optional[date] = None
    address: Optional[List[Address]] = None
    photo: Optional[dict] = None  # Attachment
    managingOrganization: Optional[Reference] = None
    active: Optional[bool] = None
    link: Optional[List[PersonLink]] = None

class RelatedPersonCommunication(BaseModel):
    """Related person communication preferences"""
    language: CodeableConcept
    preferred: Optional[bool] = None

class RelatedPersonModel(FHIRDomainResource):
    """FHIR RelatedPerson resource model"""
    resourceType: Literal["RelatedPerson"] = Field(default="RelatedPerson")
    
    identifier: Optional[List[Identifier]] = None
    active: Optional[bool] = None
    patient: Reference
    relationship: Optional[List[CodeableConcept]] = None
    name: Optional[List[HumanName]] = None
    telecom: Optional[List[ContactPoint]] = None
    gender: Optional[AdministrativeGender] = None
    birthDate: Optional[date] = None
    address: Optional[List[Address]] = None
    photo: Optional[List[dict]] = None  # Attachment
    period: Optional[Period] = None
    communication: Optional[List[RelatedPersonCommunication]] = None

# Group-related enums and classes
class GroupType(str, Enum):
    PERSON = "person"
    ANIMAL = "animal"
    PRACTITIONER = "practitioner"
    DEVICE = "device"
    MEDICATION = "medication"
    SUBSTANCE = "substance"

class GroupMembershipBasis(str, Enum):
    DEFINITIONAL = "definitional"
    ENUMERATED = "enumerated"

class GroupCharacteristic(BaseModel):
    """Group characteristic"""
    code: CodeableConcept
    valueCodeableConcept: Optional[CodeableConcept] = None
    valueBoolean: Optional[bool] = None
    valueQuantity: Optional[dict] = None  # Quantity
    valueRange: Optional[dict] = None     # Range
    valueReference: Optional[Reference] = None
    exclude: bool
    period: Optional[Period] = None

class GroupMember(BaseModel):
    """Group member"""
    entity: Reference
    period: Optional[Period] = None
    inactive: Optional[bool] = None

class GroupModel(FHIRDomainResource):
    """FHIR Group resource model"""
    resourceType: Literal["Group"] = Field(default="Group")
    
    identifier: Optional[List[Identifier]] = None
    active: Optional[bool] = None
    type: GroupType
    membership: GroupMembershipBasis
    code: Optional[CodeableConcept] = None
    name: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    managingEntity: Optional[Reference] = None
    characteristic: Optional[List[GroupCharacteristic]] = None
    member: Optional[List[GroupMember]] = None

# Export all models
__all__ = [
    'HAS_PYDANTIC',
    'PatientModel',
    'PractitionerModel', 
    'PractitionerRoleModel',
    'EncounterModel',
    'PersonModel',
    'RelatedPersonModel',
    'GroupModel',
    # Supporting classes
    'HumanName',
    'ContactPoint',
    'Address',
    'Identifier',
    'Reference',
    'CodeableConcept',
    'Period',
    'GroupCharacteristic',
    'GroupMember',
    # Enums
    'AdministrativeGender',
    'NameUse',
    'ContactPointSystem',
    'ContactPointUse',
    'AddressUse',
    'AddressType',
    'EncounterStatus',
    'GroupType',
    'GroupMembershipBasis'
]