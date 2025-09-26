# Fast-FHIR

A high-performance Python library for parsing and processing FHIR R5 (Fast Healthcare Interoperability Resources) data with C extensions for maximum speed.

## ⚡ Key Features

- **High Performance**: C extensions for 10-100x faster JSON parsing
- **Complete FHIR R5 Support**: 24+ implemented resource types with 128 total planned
- **Advanced Deserializers**: JSON to Python objects with Pydantic validation
- **Memory Efficient**: Optimized for large healthcare datasets
- **Developer Friendly**: Intuitive API with comprehensive error handling

## 🚀 Performance

- **Fast JSON Parsing**: C-optimized parsers for healthcare data
- **Efficient Memory Usage**: Minimal overhead for large FHIR bundles  
- **Scalable Processing**: Built for high-throughput healthcare systems
- **Optional Validation**: Pydantic integration for data quality assurance

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Build C extensions (for maximum performance):
   ```bash
   python setup.py build_ext --inplace
   ```

## 📦 Installation

### From Source (Recommended for Development)
```bash
git clone https://github.com/your-username/fast-fhir.git
cd fast-fhir
pip install -r requirements.txt
python setup.py build_ext --inplace
```

### PyPI Installation
```bash
pip install fast-fhir
```

## 🚀 Quick Start

```python
import fast_fhir
from fast_fhir import FHIRParser
from fast_fhir.deserializers import deserialize_care_plan

# Initialize high-performance parser
parser = FHIRParser()

# Parse FHIR resources
patient_data = parser.parse_patient(json_data)

# Use deserializers for specific resource types
care_plan = deserialize_care_plan(care_plan_json)
print(f"Care Plan: {care_plan.title}")
```

## Usage

### Basic Usage

Show FHIR implementation status:
```bash
python main.py --status
```

Parse a FHIR resource from JSON file:
```bash
python main.py --parse patient.json
```

Show all available options:
```bash
python main.py --help
```

### Examples and Demonstrations

The `examples/` directory contains comprehensive demonstration scripts:

- **Complete System Demo**: `examples/demo_comprehensive.py`
- **Care Provision Resources Demo**: `examples/demo_care_provision.py`
- **JSON Deserializers Demo**: `examples/demo_deserializers.py`
- **Implementation Testing**: `examples/test_implementation.py`

Run examples with:
```bash
PYTHONPATH=. python3 examples/demo_comprehensive.py
PYTHONPATH=. python3 examples/demo_care_provision.py
PYTHONPATH=. python3 examples/demo_deserializers.py
```

### FHIR Deserializers Package

The `fast_fhir.deserializers` package provides comprehensive JSON deserialization functionality:

```python
from fast_fhir.deserializers import (
    FHIRCareProvisionDeserializer,
    deserialize_care_plan,
    deserialize_care_team,
    deserialize_goal
)

# Quick deserialization
care_plan = deserialize_care_plan(json_data)

# Advanced deserialization with validation
deserializer = FHIRCareProvisionDeserializer(use_pydantic_validation=True)
care_team = deserializer.deserialize_care_team(json_data)
```

**Supported Resources:**
- CarePlan, CareTeam, Goal
- ServiceRequest, RiskAssessment
- VisionPrescription, NutritionOrder

See the deserializers documentation for detailed information.

## Development

Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

Run tests:
```bash
pytest
```