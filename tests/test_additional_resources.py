"""Tests for additional FHIR R5 resources following DRY principles."""

import json
import pytest
from src.fhir.resources import (
    Location, Task, HealthcareService, Endpoint, Appointment, 
    Slot, Schedule, Flag, Device, Substance, ListResource, Library
)


class TestLocation:
    """Test Location resource."""
    
    def test_location_creation(self):
        """Test Location creation."""
        location = Location("test-location-1")
        assert location.resource_type == "Location"
        assert location.id == "test-location-1"
    
    def test_location_coordinates(self):
        """Test Location coordinates."""
        location = Location("test-location")
        location.set_coordinates(-122.4194, 37.7749, 10.0)
        
        coords = location.get_coordinates()
        assert coords["longitude"] == -122.4194
        assert coords["latitude"] == 37.7749
        assert coords["altitude"] == 10.0
    
    def test_location_validation(self):
        """Test Location validation."""
        location = Location("test-location")
        location.status = "active"
        location.mode = "instance"
        assert location.validate() is True
        
        location.status = "invalid-status"
        assert location.validate() is False


class TestTask:
    """Test Task resource."""
    
    def test_task_creation(self):
        """Test Task creation."""
        task = Task("test-task-1")
        assert task.resource_type == "Task"
        assert task.id == "test-task-1"
    
    def test_task_validation(self):
        """Test Task validation."""
        task = Task("test-task")
        
        # Should fail without required fields
        assert task.validate() is False
        
        # Should pass with required fields
        task.status = "completed"
        task.intent = "order"
        assert task.validate() is True
    
    def test_task_status_methods(self):
        """Test Task status methods."""
        task = Task("test-task")
        task.status = "completed"
        
        assert task.is_completed() is True
        assert task.is_in_progress() is False
        assert task.is_ready() is False
    
    def test_task_input_output(self):
        """Test Task input/output."""
        task = Task("test-task")
        task.add_input("patient", {"reference": "Patient/123"})
        task.add_output("result", {"valueString": "Success"})
        
        assert len(task.input) == 1
        assert len(task.output) == 1
        assert task.input[0]["type"]["coding"][0]["code"] == "patient"


class TestHealthcareService:
    """Test HealthcareService resource."""
    
    def test_healthcare_service_creation(self):
        """Test HealthcareService creation."""
        service = HealthcareService("test-service-1")
        assert service.resource_type == "HealthcareService"
        assert service.id == "test-service-1"
    
    def test_healthcare_service_methods(self):
        """Test HealthcareService methods."""
        service = HealthcareService("test-service")
        service.active = True
        service.appointment_required = True
        
        assert service.is_active() is True
        assert service.requires_appointment() is True


class TestEndpoint:
    """Test Endpoint resource."""
    
    def test_endpoint_creation(self):
        """Test Endpoint creation."""
        endpoint = Endpoint("test-endpoint-1")
        assert endpoint.resource_type == "Endpoint"
        assert endpoint.id == "test-endpoint-1"
    
    def test_endpoint_validation(self):
        """Test Endpoint validation."""
        endpoint = Endpoint("test-endpoint")
        
        # Should fail without required fields
        assert endpoint.validate() is False
        
        # Should pass with required fields
        endpoint.status = "active"
        endpoint.connection_type = [{"coding": [{"code": "hl7-fhir-rest"}]}]
        endpoint.address = "https://example.com/fhir"
        assert endpoint.validate() is True


class TestAppointment:
    """Test Appointment resource."""
    
    def test_appointment_creation(self):
        """Test Appointment creation."""
        appointment = Appointment("test-appointment-1")
        assert appointment.resource_type == "Appointment"
        assert appointment.id == "test-appointment-1"
    
    def test_appointment_validation(self):
        """Test Appointment validation."""
        appointment = Appointment("test-appointment")
        
        # Should fail without required fields
        assert appointment.validate() is False
        
        # Should pass with required fields
        appointment.status = "booked"
        appointment.participant = [{"actor": {"reference": "Patient/123"}, "status": "accepted"}]
        assert appointment.validate() is True
    
    def test_appointment_participants(self):
        """Test Appointment participants."""
        appointment = Appointment("test-appointment")
        appointment.add_participant("Patient/123", [{"coding": [{"code": "PART"}]}])
        
        assert len(appointment.participant) == 1
        assert appointment.participant[0]["actor"]["reference"] == "Patient/123"


class TestSlot:
    """Test Slot resource."""
    
    def test_slot_creation(self):
        """Test Slot creation."""
        slot = Slot("test-slot-1")
        assert slot.resource_type == "Slot"
        assert slot.id == "test-slot-1"
    
    def test_slot_validation(self):
        """Test Slot validation."""
        slot = Slot("test-slot")
        
        # Should fail without required fields
        assert slot.validate() is False
        
        # Should pass with required fields
        slot.schedule = {"reference": "Schedule/123"}
        slot.status = "free"
        slot.start = "2023-12-25T10:00:00Z"
        slot.end = "2023-12-25T11:00:00Z"
        assert slot.validate() is True
    
    def test_slot_status_methods(self):
        """Test Slot status methods."""
        slot = Slot("test-slot")
        slot.status = "free"
        slot.overbooked = True
        
        assert slot.is_free() is True
        assert slot.is_busy() is False
        assert slot.is_overbooked() is True


class TestSchedule:
    """Test Schedule resource."""
    
    def test_schedule_creation(self):
        """Test Schedule creation."""
        schedule = Schedule("test-schedule-1")
        assert schedule.resource_type == "Schedule"
        assert schedule.id == "test-schedule-1"
    
    def test_schedule_validation(self):
        """Test Schedule validation."""
        schedule = Schedule("test-schedule")
        
        # Should fail without required fields
        assert schedule.validate() is False
        
        # Should pass with required fields
        schedule.actor = [{"reference": "Practitioner/123"}]
        assert schedule.validate() is True
    
    def test_schedule_actors(self):
        """Test Schedule actors."""
        schedule = Schedule("test-schedule")
        schedule.add_actor("Practitioner/123")
        schedule.add_actor("Location/456")
        
        assert len(schedule.get_actors()) == 2


class TestFlag:
    """Test Flag resource."""
    
    def test_flag_creation(self):
        """Test Flag creation."""
        flag = Flag("test-flag-1")
        assert flag.resource_type == "Flag"
        assert flag.id == "test-flag-1"
    
    def test_flag_validation(self):
        """Test Flag validation."""
        flag = Flag("test-flag")
        
        # Should fail without required fields
        assert flag.validate() is False
        
        # Should pass with required fields
        flag.status = "active"
        flag.code = {"coding": [{"code": "alert"}]}
        flag.subject = {"reference": "Patient/123"}
        assert flag.validate() is True


class TestDevice:
    """Test Device resource."""
    
    def test_device_creation(self):
        """Test Device creation."""
        device = Device("test-device-1")
        assert device.resource_type == "Device"
        assert device.id == "test-device-1"
    
    def test_device_methods(self):
        """Test Device methods."""
        device = Device("test-device")
        device.display_name = "Test Device"
        device.status = "active"
        device.udi_carrier = [{"deviceIdentifier": "12345"}]
        
        assert device.get_device_name() == "Test Device"
        assert device.is_active() is True
        assert device.get_udi_device_identifier() == "12345"


class TestSubstance:
    """Test Substance resource."""
    
    def test_substance_creation(self):
        """Test Substance creation."""
        substance = Substance("test-substance-1")
        assert substance.resource_type == "Substance"
        assert substance.id == "test-substance-1"
    
    def test_substance_validation(self):
        """Test Substance validation."""
        substance = Substance("test-substance")
        
        # Should fail without required fields
        assert substance.validate() is False
        
        # Should pass with required fields
        substance.instance = True
        substance.code = {"coding": [{"code": "substance-code"}]}
        assert substance.validate() is True
    
    def test_substance_methods(self):
        """Test Substance methods."""
        substance = Substance("test-substance")
        substance.instance = True
        substance.status = "active"
        substance.code = {"coding": [{"code": "H2O"}]}
        
        assert substance.is_instance() is True
        assert substance.is_active() is True
        assert substance.get_substance_code() == "H2O"


class TestListResource:
    """Test List resource."""
    
    def test_list_creation(self):
        """Test List creation."""
        list_resource = ListResource("test-list-1")
        assert list_resource.resource_type == "List"
        assert list_resource.id == "test-list-1"
    
    def test_list_validation(self):
        """Test List validation."""
        list_resource = ListResource("test-list")
        
        # Should fail without required fields
        assert list_resource.validate() is False
        
        # Should pass with required fields
        list_resource.status = "current"
        list_resource.mode = "working"
        assert list_resource.validate() is True
    
    def test_list_entries(self):
        """Test List entries."""
        list_resource = ListResource("test-list")
        list_resource.add_entry("Patient/123")
        list_resource.add_entry("Patient/456", deleted=True)
        
        assert list_resource.get_entry_count() == 2
        entries = list_resource.get_entries()
        assert entries[0]["item"]["reference"] == "Patient/123"
        assert entries[1]["deleted"] is True


class TestLibrary:
    """Test Library resource."""
    
    def test_library_creation(self):
        """Test Library creation."""
        library = Library("test-library-1")
        assert library.resource_type == "Library"
        assert library.id == "test-library-1"
    
    def test_library_validation(self):
        """Test Library validation."""
        library = Library("test-library")
        
        # Should fail without required fields
        assert library.validate() is False
        
        # Should pass with required fields
        library.status = "active"
        library.type = {"coding": [{"code": "logic-library"}]}
        assert library.validate() is True
    
    def test_library_methods(self):
        """Test Library methods."""
        library = Library("test-library")
        library.status = "active"
        library.type = {"coding": [{"code": "model-definition"}]}
        
        assert library.is_active() is True
        assert library.get_library_type() == "model-definition"


class TestDRYPrinciplesAdditional:
    """Test DRY principles for additional resources."""
    
    def test_base_class_consistency(self):
        """Test all resources follow base class patterns."""
        resources = [
            Location("l1"), Task("t1"), HealthcareService("hs1"),
            Endpoint("e1"), Appointment("a1"), Slot("s1"),
            Schedule("sc1"), Flag("f1"), Device("d1"),
            Substance("sub1"), ListResource("list1"), Library("lib1")
        ]
        
        for resource in resources:
            # All should have common base functionality
            assert hasattr(resource, 'to_dict')
            assert hasattr(resource, 'validate')
            assert hasattr(resource, 'resource_type')
            assert hasattr(resource, 'id')
            
            # All should produce valid dictionaries
            result = resource.to_dict()
            assert isinstance(result, dict)
            assert result.get("resourceType") == resource.resource_type
            assert result.get("id") == resource.id
    
    def test_validation_patterns(self):
        """Test validation follows consistent patterns."""
        # Resources with required status field
        status_resources = [
            (Task("t1"), "completed"),
            (Endpoint("e1"), "active"),
            (Appointment("a1"), "booked"),
            (Slot("s1"), "free"),
            (Flag("f1"), "active"),
            (ListResource("l1"), "current"),
            (Library("lib1"), "active")
        ]
        
        for resource, valid_status in status_resources:
            # Should fail without status
            assert resource.validate() is False
            
            # Should pass with valid status (and other required fields)
            resource.status = valid_status
            
            # Add other required fields based on resource type
            if isinstance(resource, Task):
                resource.intent = "order"
            elif isinstance(resource, Endpoint):
                resource.connection_type = [{"coding": [{"code": "hl7-fhir-rest"}]}]
                resource.address = "https://example.com"
            elif isinstance(resource, Appointment):
                resource.participant = [{"actor": {"reference": "Patient/123"}}]
            elif isinstance(resource, Slot):
                resource.schedule = {"reference": "Schedule/123"}
                resource.start = "2023-12-25T10:00:00Z"
                resource.end = "2023-12-25T11:00:00Z"
            elif isinstance(resource, Flag):
                resource.code = {"coding": [{"code": "alert"}]}
                resource.subject = {"reference": "Patient/123"}
            elif isinstance(resource, ListResource):
                resource.mode = "working"
            elif isinstance(resource, Library):
                resource.type = {"coding": [{"code": "logic-library"}]}
            
            # Now should pass validation
            assert resource.validate() is True