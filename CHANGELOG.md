# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.1.0] - 2024-09-27

### Added
- 🚀 **Initial stable release of Fast-FHIR**
- High-performance FHIR R5 parser and validator for SMART on FHIR applications
- Fast JSON deserialization with Pydantic validation for healthcare interoperability
- Support for all major FHIR R5 resource types:
  - Foundation resources (Patient, Practitioner, Organization, etc.)
  - Clinical resources (Observation, Condition, Procedure, etc.)
  - Care Provision resources (CarePlan, CareTeam, Goal, etc.)
  - Entities resources (Location, Device, Substance, etc.)
- Comprehensive deserializer system with optional Pydantic validation
- **C extensions**: 3 compiled extensions (fhir_parser_c, fhir_datatypes_c, fhir_foundation_c) for enhanced performance
- Python 3.8+ compatibility
- Pydantic v1.8+ and v2.x compatibility
- Extensive test coverage (60+ tests)

### Features
- **Fast JSON Parsing**: Optimized deserialization for FHIR resources
- **Pydantic Integration**: Optional validation with Pydantic models
- **Type Safety**: Full type hints and validation support
- **Extensible Architecture**: Easy to extend for custom FHIR profiles
- **Error Handling**: Comprehensive error handling and validation
- **Performance Optimized**: C extensions for critical parsing paths
- **Healthcare Standards**: Full FHIR R5 specification compliance

### Technical Details
- Supports FHIR R5 (5.0.0) specification
- Compatible with Python 3.8, 3.9, 3.10, 3.11, 3.12
- Works with Pydantic 1.8+ and 2.x
- Optional C extensions for performance
- Comprehensive test suite with 100% core functionality coverage
- MIT License for commercial and open-source use

### Documentation
- Complete README with installation and usage examples
- API documentation for all deserializers
- Performance benchmarks and comparisons
- SMART on FHIR integration examples

[0.1.0]: https://github.com/archit47/fast-fhir/releases/tag/v0.1.0