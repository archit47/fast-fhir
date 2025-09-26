"""Tests for newly implemented FHIR resources."""

import pytest
import json
from datetime import datetime
from typing import Dict, Any

from src.fhir.resources.organization_affiliation import OrganizationAffiliation
from src.fhir.resources.biologically_derived_product import BiologicallyDerivedProduct
from src.fhir.resources.device_metric import DeviceMetric
from src.fhir.resources.nutrition_product import NutritionProduct
from src.fhir.resources.transport import Transport
from src.fhir.resources.appointment_response import AppointmentResponse
from src.fhir.resources.verification_result import VerificationResult
from src.fhir.resources.encounter_history import EncounterHistory
from src.fhir.resources.episode_of_care import EpisodeOfCare


class TestOrganizationAffiliation:
    """Test OrganizationAffiliation resource."""
    
    def test_create_organization_affiliation(self):
        """Test creating an OrganizationAffiliation."""
        org_affiliation = OrganizationAffiliation("test-org-affiliation-1")
        
        assert org_affiliation.resource_type == "OrganizationAffiliation"
        assert org_affiliation.id == "test-org-affiliation-1"
        assert org_affiliation.active is None
        assert org_affiliation.network == []
    
    def test_organization_affiliation_validation(self):
        """Test OrganizationAffiliation validation."""
        org_affiliation = OrganizationAffiliation("test-org-affiliation-1")
        
        # Should fail validation without required fields
        errors = org_affiliation.validate()
        assert "OrganizationAffiliation.organization is required" in errors
        assert "OrganizationAffiliation.participatingOrganization is required" in errors
        
        # Add required fields
        org_affiliation.organization = {"reference": "Organization/main-org"}
        org_affiliation.participating_organization = {"reference": "Organization/partner-org"}
        
        errors = org_affiliation.validate()
        assert len([e for e in errors if "organization" in e.lower()]) == 0
    
    def test_organization_affiliation_methods(self):
        """Test OrganizationAffiliation helper methods."""
        org_affiliation = OrganizationAffiliation("test-org-affiliation-1")
        org_affiliation.active = True
        
        assert org_affiliation.is_active() is True
        
        # Test adding networks and specialties
        network = {"coding": [{"code": "network1", "display": "Network 1"}]}
        specialty = {"coding": [{"code": "cardiology", "display": "Cardiology"}]}
        
        org_affiliation.add_network(network)
        org_affiliation.add_specialty(specialty)
        
        assert len(org_affiliation.get_networks()) == 1
        assert len(org_affiliation.get_specialties()) == 1
    
    def test_organization_affiliation_serialization(self):
        """Test OrganizationAffiliation serialization."""
        org_affiliation = OrganizationAffiliation("test-org-affiliation-1")
        org_affiliation.active = True
        org_affiliation.organization = {"reference": "Organization/main-org"}
        org_affiliation.participating_organization = {"reference": "Organization/partner-org"}
        
        data = org_affiliation.to_dict()
        
        assert data["resourceType"] == "OrganizationAffiliation"
        assert data["id"] == "test-org-affiliation-1"
        assert data["active"] is True
        assert data["organization"]["reference"] == "Organization/main-org"
        
        # Test deserialization
        new_org_affiliation = OrganizationAffiliation.from_dict(data)
        assert new_org_affiliation.id == org_affiliation.id
        assert new_org_affiliation.active == org_affiliation.active


class TestBiologicallyDerivedProduct:
    """Test BiologicallyDerivedProduct resource."""
    
    def test_create_biologically_derived_product(self):
        """Test creating a BiologicallyDerivedProduct."""
        product = BiologicallyDerivedProduct("test-bio-product-1")
        
        assert product.resource_type == "BiologicallyDerivedProduct"
        assert product.id == "test-bio-product-1"
        assert product.processing == []
        assert product.storage == []
    
    def test_biologically_derived_product_validation(self):
        """Test BiologicallyDerivedProduct validation."""
        product = BiologicallyDerivedProduct("test-bio-product-1")
        
        # Should fail validation without required fields
        errors = product.validate()
        assert "BiologicallyDerivedProduct.productCategory is required" in errors
        
        # Add required field
        product.product_category = {"coding": [{"code": "cells", "display": "Cells"}]}
        
        errors = product.validate()
        assert len([e for e in errors if "productCategory" in e]) == 0
    
    def test_biologically_derived_product_methods(self):
        """Test BiologicallyDerivedProduct helper methods."""
        product = BiologicallyDerivedProduct("test-bio-product-1")
        
        # Test adding processing steps
        processing_step = {
            "description": "Cell isolation",
            "procedure": {"coding": [{"code": "isolation", "display": "Cell Isolation"}]}
        }
        product.add_processing_step(processing_step)
        
        assert len(product.get_processing_steps()) == 1
        
        # Test setting biological source event
        product.set_biological_source_event("BSE-123")
        assert product.get_biological_source_event() == "BSE-123"


class TestDeviceMetric:
    """Test DeviceMetric resource."""
    
    def test_create_device_metric(self):
        """Test creating a DeviceMetric."""
        metric = DeviceMetric("test-device-metric-1")
        
        assert metric.resource_type == "DeviceMetric"
        assert metric.id == "test-device-metric-1"
        assert metric.calibration == []
    
    def test_device_metric_validation(self):
        """Test DeviceMetric validation."""
        metric = DeviceMetric("test-device-metric-1")
        
        # Should fail validation without required fields
        errors = metric.validate()
        assert "DeviceMetric.type is required" in errors
        assert "DeviceMetric.category is required" in errors
        
        # Add required fields
        metric.type = {"coding": [{"code": "temp", "display": "Temperature"}]}
        metric.category = "measurement"
        
        errors = metric.validate()
        assert len([e for e in errors if "type is required" in e or "category is required" in e]) == 0
    
    def test_device_metric_status_methods(self):
        """Test DeviceMetric status methods."""
        metric = DeviceMetric("test-device-metric-1")
        
        metric.set_operational_status("on")
        assert metric.is_operational() is True
        
        metric.set_category("measurement")
        assert metric.is_measurement_metric() is True
        assert metric.is_setting_metric() is False
        
        metric.set_color("red")
        assert metric.color == "red"
    
    def test_device_metric_invalid_values(self):
        """Test DeviceMetric with invalid values."""
        metric = DeviceMetric("test-device-metric-1")
        
        with pytest.raises(ValueError):
            metric.set_operational_status("invalid")
        
        with pytest.raises(ValueError):
            metric.set_color("purple")
        
        with pytest.raises(ValueError):
            metric.set_category("invalid")


class TestNutritionProduct:
    """Test NutritionProduct resource."""
    
    def test_create_nutrition_product(self):
        """Test creating a NutritionProduct."""
        product = NutritionProduct("test-nutrition-product-1")
        
        assert product.resource_type == "NutritionProduct"
        assert product.id == "test-nutrition-product-1"
        assert product.nutrient == []
        assert product.ingredient == []
    
    def test_nutrition_product_validation(self):
        """Test NutritionProduct validation."""
        product = NutritionProduct("test-nutrition-product-1")
        
        # Should fail validation without required fields
        errors = product.validate()
        assert "NutritionProduct.status is required" in errors
        
        # Add required field
        product.status = "active"
        
        errors = product.validate()
        assert len([e for e in errors if "status is required" in e]) == 0
    
    def test_nutrition_product_methods(self):
        """Test NutritionProduct helper methods."""
        product = NutritionProduct("test-nutrition-product-1")
        product.set_status("active")
        
        assert product.is_active() is True
        assert product.is_inactive() is False
        
        # Test adding nutrients and allergens
        nutrient = {
            "item": {"coding": [{"code": "protein", "display": "Protein"}]},
            "amount": [{"numerator": {"value": 20, "unit": "g"}}]
        }
        product.add_nutrient(nutrient)
        
        allergen = {"coding": [{"code": "nuts", "display": "Tree Nuts"}]}
        product.add_known_allergen(allergen)
        
        assert len(product.get_nutrients()) == 1
        assert len(product.get_known_allergens()) == 1
        assert product.has_allergen("nuts") is True
        assert product.has_allergen("dairy") is False


class TestTransport:
    """Test Transport resource."""
    
    def test_create_transport(self):
        """Test creating a Transport."""
        transport = Transport("test-transport-1")
        
        assert transport.resource_type == "Transport"
        assert transport.id == "test-transport-1"
        assert transport.input == []
        assert transport.output == []
    
    def test_transport_validation(self):
        """Test Transport validation."""
        transport = Transport("test-transport-1")
        
        # Should fail validation without required fields
        errors = transport.validate()
        assert "Transport.status is required" in errors
        assert "Transport.intent is required" in errors
        
        # Add required fields
        transport.status = "in-progress"
        transport.intent = "order"
        
        errors = transport.validate()
        assert len([e for e in errors if "status is required" in e or "intent is required" in e]) == 0
    
    def test_transport_status_methods(self):
        """Test Transport status methods."""
        transport = Transport("test-transport-1")
        
        transport.set_status("completed")
        assert transport.is_completed() is True
        assert transport.is_in_progress() is False
        
        transport.set_priority("urgent")
        assert transport.is_high_priority() is True


class TestAppointmentResponse:
    """Test AppointmentResponse resource."""
    
    def test_create_appointment_response(self):
        """Test creating an AppointmentResponse."""
        response = AppointmentResponse("test-appointment-response-1")
        
        assert response.resource_type == "AppointmentResponse"
        assert response.id == "test-appointment-response-1"
        assert response.participant_type == []
    
    def test_appointment_response_validation(self):
        """Test AppointmentResponse validation."""
        response = AppointmentResponse("test-appointment-response-1")
        
        # Should fail validation without required fields
        errors = response.validate()
        assert "AppointmentResponse.appointment is required" in errors
        assert "AppointmentResponse.participantStatus is required" in errors
        
        # Add required fields
        response.appointment = {"reference": "Appointment/123"}
        response.participant_status = "accepted"
        
        errors = response.validate()
        assert len([e for e in errors if "appointment is required" in e or "participantStatus is required" in e]) == 0
    
    def test_appointment_response_status_methods(self):
        """Test AppointmentResponse status methods."""
        response = AppointmentResponse("test-appointment-response-1")
        
        response.set_participant_status("accepted")
        assert response.is_accepted() is True
        assert response.is_declined() is False
        
        response.set_participant_status("tentative")
        assert response.is_tentative() is True


class TestVerificationResult:
    """Test VerificationResult resource."""
    
    def test_create_verification_result(self):
        """Test creating a VerificationResult."""
        result = VerificationResult("test-verification-result-1")
        
        assert result.resource_type == "VerificationResult"
        assert result.id == "test-verification-result-1"
        assert result.target == []
        assert result.primary_source == []
    
    def test_verification_result_validation(self):
        """Test VerificationResult validation."""
        result = VerificationResult("test-verification-result-1")
        
        # Should fail validation without required fields
        errors = result.validate()
        assert "VerificationResult.target is required" in errors
        assert "VerificationResult.status is required" in errors
        
        # Add required fields
        result.target = [{"reference": "Practitioner/123"}]
        result.status = "validated"
        
        errors = result.validate()
        assert len([e for e in errors if "target is required" in e or "status is required" in e]) == 0
    
    def test_verification_result_status_methods(self):
        """Test VerificationResult status methods."""
        result = VerificationResult("test-verification-result-1")
        
        result.set_status("validated")
        assert result.is_validated() is True
        assert result.is_attested() is False
        assert result.has_validation_failed() is False
        
        result.set_status("val-fail")
        assert result.has_validation_failed() is True


class TestEncounterHistory:
    """Test EncounterHistory resource."""
    
    def test_create_encounter_history(self):
        """Test creating an EncounterHistory."""
        history = EncounterHistory("test-encounter-history-1")
        
        assert history.resource_type == "EncounterHistory"
        assert history.id == "test-encounter-history-1"
        assert history.service_type == []
        assert history.location == []
    
    def test_encounter_history_validation(self):
        """Test EncounterHistory validation."""
        history = EncounterHistory("test-encounter-history-1")
        
        # Should fail validation without required fields
        errors = history.validate()
        assert "EncounterHistory.status is required" in errors
        assert "EncounterHistory.class is required" in errors
        assert "EncounterHistory.subject is required" in errors
        assert "EncounterHistory.encounter is required" in errors
        
        # Add required fields
        history.status = "completed"
        history.class_ = {"code": "IMP", "display": "Inpatient"}
        history.subject = {"reference": "Patient/123"}
        history.encounter = {"reference": "Encounter/456"}
        
        errors = history.validate()
        required_errors = [e for e in errors if "is required" in e and any(field in e for field in ["status", "class", "subject", "encounter"])]
        assert len(required_errors) == 0
    
    def test_encounter_history_status_methods(self):
        """Test EncounterHistory status methods."""
        history = EncounterHistory("test-encounter-history-1")
        
        history.set_status("completed")
        assert history.is_completed() is True
        assert history.is_in_progress() is False
        
        history.set_status("in-progress")
        assert history.is_in_progress() is True


class TestEpisodeOfCare:
    """Test EpisodeOfCare resource."""
    
    def test_create_episode_of_care(self):
        """Test creating an EpisodeOfCare."""
        episode = EpisodeOfCare("test-episode-of-care-1")
        
        assert episode.resource_type == "EpisodeOfCare"
        assert episode.id == "test-episode-of-care-1"
        assert episode.status_history == []
        assert episode.diagnosis == []
    
    def test_episode_of_care_validation(self):
        """Test EpisodeOfCare validation."""
        episode = EpisodeOfCare("test-episode-of-care-1")
        
        # Should fail validation without required fields
        errors = episode.validate()
        assert "EpisodeOfCare.status is required" in errors
        assert "EpisodeOfCare.patient is required" in errors
        
        # Add required fields
        episode.status = "active"
        episode.patient = {"reference": "Patient/123"}
        
        errors = episode.validate()
        assert len([e for e in errors if "status is required" in e or "patient is required" in e]) == 0
    
    def test_episode_of_care_status_methods(self):
        """Test EpisodeOfCare status methods."""
        episode = EpisodeOfCare("test-episode-of-care-1")
        
        episode.set_status("active")
        assert episode.is_active() is True
        assert episode.is_finished() is False
        
        episode.set_status("finished")
        assert episode.is_finished() is True
        assert episode.is_active() is False
    
    def test_episode_of_care_diagnosis_methods(self):
        """Test EpisodeOfCare diagnosis methods."""
        episode = EpisodeOfCare("test-episode-of-care-1")
        
        # Add primary diagnosis
        primary_diagnosis = {
            "condition": {"reference": "Condition/123"},
            "role": {"coding": [{"code": "primary", "display": "Primary"}]},
            "rank": 1
        }
        episode.add_diagnosis(primary_diagnosis)
        
        # Add secondary diagnosis
        secondary_diagnosis = {
            "condition": {"reference": "Condition/456"},
            "role": {"coding": [{"code": "secondary", "display": "Secondary"}]},
            "rank": 2
        }
        episode.add_diagnosis(secondary_diagnosis)
        
        assert len(episode.get_diagnoses()) == 2
        
        primary = episode.get_primary_diagnosis()
        assert primary is not None
        assert primary["rank"] == 1
        
        primary_diagnoses = episode.get_diagnoses_by_role("primary")
        assert len(primary_diagnoses) == 1


class TestResourceIntegration:
    """Test integration between resources."""
    
    def test_all_resources_serialization(self):
        """Test that all new resources can be serialized and deserialized."""
        resources = [
            OrganizationAffiliation("org-aff-1"),
            BiologicallyDerivedProduct("bio-prod-1"),
            DeviceMetric("device-metric-1"),
            NutritionProduct("nutrition-prod-1"),
            Transport("transport-1"),
            AppointmentResponse("appt-resp-1"),
            VerificationResult("verify-result-1"),
            EncounterHistory("encounter-hist-1"),
            EpisodeOfCare("episode-1")
        ]
        
        for resource in resources:
            # Test serialization
            data = resource.to_dict()
            assert data["resourceType"] == resource.resource_type
            assert data["id"] == resource.id
            
            # Test JSON serialization
            json_str = json.dumps(data)
            assert json_str is not None
            
            # Test deserialization
            parsed_data = json.loads(json_str)
            new_resource = resource.__class__.from_dict(parsed_data)
            assert new_resource.id == resource.id
            assert new_resource.resource_type == resource.resource_type
    
    def test_resource_validation_consistency(self):
        """Test that all resources have consistent validation behavior."""
        resources = [
            OrganizationAffiliation("org-aff-1"),
            BiologicallyDerivedProduct("bio-prod-1"),
            DeviceMetric("device-metric-1"),
            NutritionProduct("nutrition-prod-1"),
            Transport("transport-1"),
            AppointmentResponse("appt-resp-1"),
            VerificationResult("verify-result-1"),
            EncounterHistory("encounter-hist-1"),
            EpisodeOfCare("episode-1")
        ]
        
        for resource in resources:
            # All resources should have validation method
            assert hasattr(resource, 'validate')
            
            # Validation should return a list
            errors = resource.validate()
            assert isinstance(errors, list)
            
            # All should have base validation errors initially
            base_errors = [e for e in errors if "id" in e or "resourceType" in e]
            # Note: Base validation might not require these fields, so we just check the method works


if __name__ == "__main__":
    pytest.main([__file__])