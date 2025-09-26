"""FHIR R5 Resources Package following DRY principles."""

from .base import FHIRResourceBase, FHIRPersonResourceMixin, FHIROrganizationResourceMixin
from .patient import Patient
from .practitioner import Practitioner
from .practitioner_role import PractitionerRole
from .related_person import RelatedPerson
from .organization import Organization
from .encounter import Encounter
from .group import Group
from .person import Person
from .location import Location
from .task import Task
from .healthcare_service import HealthcareService
from .endpoint import Endpoint
from .appointment import Appointment
from .slot import Slot
from .schedule import Schedule
from .flag import Flag
from .device import Device
from .substance import Substance
from .list_resource import ListResource
from .library import Library

__all__ = [
    'FHIRResourceBase', 'FHIRPersonResourceMixin', 'FHIROrganizationResourceMixin',
    'Patient', 'Practitioner', 'PractitionerRole', 'RelatedPerson', 
    'Organization', 'Encounter', 'Group', 'Person', 'Location', 'Task',
    'HealthcareService', 'Endpoint', 'Appointment', 'Slot', 'Schedule',
    'Flag', 'Device', 'Substance', 'ListResource', 'Library'
]