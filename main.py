"""Fast-FHIR - High-Performance FHIR R5 Parser - Main Entry Point"""

import sys
import argparse

def show_status():
    """Show FHIR implementation status"""
    try:
        from src.fast_fhir.deserializers import (
            PYDANTIC_FOUNDATION_AVAILABLE,
            PYDANTIC_ENTITIES_AVAILABLE,
            PYDANTIC_CARE_PROVISION_AVAILABLE
        )
        
        print("Fast-FHIR R5 Implementation Status")
        print("=" * 40)
        print(f"Foundation Deserializers: ✅ Available")
        print(f"Entities Deserializers: ✅ Available") 
        print(f"Care Provision Deserializers: ✅ Available")
        print(f"Pydantic Foundation: {'✅' if PYDANTIC_FOUNDATION_AVAILABLE else '❌'}")
        print(f"Pydantic Entities: {'✅' if PYDANTIC_ENTITIES_AVAILABLE else '❌'}")
        print(f"Pydantic Care Provision: {'✅' if PYDANTIC_CARE_PROVISION_AVAILABLE else '❌'}")
        
    except ImportError as e:
        print(f"Fast-FHIR not available: {e}")
        print("Please install Fast-FHIR or check your PYTHONPATH")

def parse_resource(json_file):
    """Parse a FHIR resource from JSON file"""
    try:
        from src.fast_fhir.deserializers import (
            deserialize_patient,
            deserialize_organization,
            deserialize_care_plan
        )
        import json
        
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        resource_type = data.get('resourceType')
        
        if resource_type == 'Patient':
            result = deserialize_patient(data)
        elif resource_type == 'Organization':
            result = deserialize_organization(data)
        elif resource_type == 'CarePlan':
            result = deserialize_care_plan(data)
        else:
            print(f"Resource type {resource_type} not supported in this demo")
            return None
            
        print(f"Successfully parsed {resource_type} resource: {result.id}")
        return result
        
    except Exception as e:
        print(f"Error parsing resource: {e}")
        return None


def main():
    """Main entry point for FHIR R5 Parser"""
    parser = argparse.ArgumentParser(
        description="FHIR R5 Parser - Fast Healthcare Interoperability Resources",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --status                    Show implementation status
  python main.py --parse patient.json       Parse a FHIR resource file
  python main.py --demo                      Run comprehensive demo
  
For more examples and demonstrations, see the examples/ directory:
  python examples/demo_comprehensive.py     Complete system demonstration
  python examples/demo_care_provision.py   Care Provision resources demo
  python examples/demo_deserializers.py    JSON deserializers demo
        """
    )
    
    parser.add_argument(
        '--status', 
        action='store_true',
        help='Show FHIR implementation status and coverage'
    )
    
    parser.add_argument(
        '--parse',
        metavar='FILE',
        help='Parse a FHIR resource from JSON file'
    )
    
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run comprehensive system demonstration'
    )
    
    args = parser.parse_args()
    
    if args.status:
        show_status()
        return None
    elif args.parse:
        parse_resource(args.parse)
        return None
    elif args.demo:
        print("Running comprehensive demo...")
        print("For the full demo experience, run:")
        print("  python examples/demo_comprehensive.py")
        print()
        show_status()
        return None
    else:
        # Default behavior - show status and help
        show_status()
        print("\nFor more options, run: python main.py --help")
        print("For demonstrations, see the examples/ directory")
        return None


if __name__ == "__main__":
    main()