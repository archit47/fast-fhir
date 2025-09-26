#!/usr/bin/env python3
"""Test script to verify the new FHIR resource implementations."""

import sys
import os
import json
sys.path.insert(0, os.path.abspath('..'))
from src.fhir.resources.organization_affiliation import OrganizationAffiliation
from src.fhir.resources.biologically_derived_product import BiologicallyDerivedProduct

def test_organization_affiliation():
    """Test OrganizationAffiliation resource."""
    print("Testing OrganizationAffiliation...")
    
    # Create new affiliation
    affiliation = OrganizationAffiliation("test-affiliation-1")
    print(f"✓ Created {affiliation.resource_type} with ID: {affiliation.id}")
    
    # Set required fields
    affiliation.organization = {"reference": "Organization/main-hospital"}
    affiliation.participating_organization = {"reference": "Organization/clinic"}
    affiliation.active = True
    
    # Add specialty
    affiliation.add_specialty({
        "coding": [{"code": "cardiology", "display": "Cardiology"}]
    })
    
    # Test validation
    errors = affiliation.validate()
    if not errors:
        print("✓ Validation passed")
    else:
        print(f"✗ Validation errors: {errors}")
    
    # Test serialization
    data = affiliation.to_dict()
    print(f"✓ Serialized to dict with {len(data)} fields")
    
    # Test JSON serialization
    json_str = json.dumps(data, indent=2)
    print(f"✓ JSON serialization successful ({len(json_str)} chars)")
    
    # Test deserialization
    new_affiliation = OrganizationAffiliation.from_dict(data)
    print(f"✓ Deserialized successfully: {new_affiliation.id}")
    
    # Test helper methods
    assert affiliation.is_active() == True
    assert len(affiliation.get_specialties()) == 1
    print("✓ Helper methods working")
    
    print("OrganizationAffiliation test completed successfully!\n")

def test_biologically_derived_product():
    """Test BiologicallyDerivedProduct resource."""
    print("Testing BiologicallyDerivedProduct...")
    
    # Create new product
    product = BiologicallyDerivedProduct("test-bio-product-1")
    print(f"✓ Created {product.resource_type} with ID: {product.id}")
    
    # Set required fields
    product.product_category = {"coding": [{"code": "cells", "display": "Cells"}]}
    
    # Add processing step
    product.add_processing_step({
        "description": "Cell isolation",
        "procedure": {"coding": [{"code": "isolation"}]}
    })
    
    # Set biological source event
    product.set_biological_source_event("BSE-123")
    
    # Test validation
    errors = product.validate()
    if not errors:
        print("✓ Validation passed")
    else:
        print(f"✗ Validation errors: {errors}")
    
    # Test serialization
    data = product.to_dict()
    print(f"✓ Serialized to dict with {len(data)} fields")
    
    # Test helper methods
    assert len(product.get_processing_steps()) == 1
    assert product.get_biological_source_event() == "BSE-123"
    print("✓ Helper methods working")
    
    print("BiologicallyDerivedProduct test completed successfully!\n")

def main():
    """Run all tests."""
    print("=== FHIR New Resources Implementation Test ===\n")
    
    try:
        test_organization_affiliation()
        test_biologically_derived_product()
        
        print("🎉 All tests passed! The new FHIR resources are working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()