"""Fast-FHIR - High-Performance FHIR R5 Parser - Main Entry Point"""

import sys
import argparse
from src.fhir.parser import FHIRParser
from src.fhir.all_resources import FHIRResourceFactory, get_fhir_implementation_status


def show_status():
    """Show FHIR implementation status"""
    status = get_fhir_implementation_status()
    factory = FHIRResourceFactory()
    factory_info = factory.get_performance_info()
    
    print("Fast-FHIR R5 Implementation Status")
    print("=" * 30)
    print(f"Total FHIR R5 resource types: {factory_info['total_resource_types']}")
    print(f"Implemented resource types: {factory_info['implemented_resource_types']}")
    print(f"Implementation coverage: {factory_info['implementation_coverage']}")
    print(f"C extensions available: {factory_info['c_extensions_available']}")
    
    print("\nResource categories:")
    for category, count in factory_info['categories'].items():
        print(f"  {category.title()}: {count} resources")
    
    print(f"\nImplemented resources: {', '.join(status['implemented_list'][:10])}...")
    if len(status['implemented_list']) > 10:
        print(f"... and {len(status['implemented_list']) - 10} more")


def parse_resource(json_file):
    """Parse a FHIR resource from JSON file"""
    try:
        parser = FHIRParser()
        factory = FHIRResourceFactory()
        
        with open(json_file, 'r') as f:
            data = f.read()
        
        # Try parsing with factory first
        resource = factory.parse_resource(data)
        
        if hasattr(resource, 'to_dict'):
            print(f"Successfully parsed {resource.__class__.__name__}")
            print(f"Resource ID: {getattr(resource, 'id', 'N/A')}")
            if hasattr(resource, 'validate'):
                print(f"Valid: {resource.validate()}")
        else:
            print(f"Parsed as generic resource: {type(resource)}")
            
    except Exception as e:
        print(f"Error parsing resource: {e}")


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
    elif args.parse:
        parse_resource(args.parse)
    elif args.demo:
        print("Running comprehensive demo...")
        print("For the full demo experience, run:")
        print("  python examples/demo_comprehensive.py")
        print()
        show_status()
    else:
        # Default behavior - show status and help
        show_status()
        print("\nFor more options, run: python main.py --help")
        print("For demonstrations, see the examples/ directory")


if __name__ == "__main__":
    main()