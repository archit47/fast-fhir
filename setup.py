"""Setup script for Fast-FHIR with high-performance C extensions."""

from setuptools import setup, Extension, find_packages
import pkgconfig

# Get cJSON library flags
import platform

try:
    cjson_flags = pkgconfig.parse('libcjson')
    include_dirs = cjson_flags['include_dirs']
    library_dirs = cjson_flags['library_dirs']
    libraries = cjson_flags['libraries']
except:
    # Fallback if pkg-config not available
    if platform.system() == 'Darwin':  # macOS
        # Try both Intel and Apple Silicon paths
        include_dirs = ['/usr/local/include', '/opt/homebrew/include']
        library_dirs = ['/usr/local/lib', '/opt/homebrew/lib']
    else:
        include_dirs = ['/usr/local/include']
        library_dirs = ['/usr/local/lib']
    libraries = ['cjson']

# Additional compile args for better compatibility
extra_compile_args = ['-O3', '-std=c99']
if platform.system() == 'Darwin':
    # Fix macOS universal build issues
    extra_compile_args.extend(['-Wno-error=unused-command-line-argument-hard-error-in-future'])
    # Don't force architecture - let Python decide
    import sysconfig
    if 'arm64' in sysconfig.get_platform():
        extra_compile_args.extend(['-arch', 'arm64'])
    elif 'x86_64' in sysconfig.get_platform():
        extra_compile_args.extend(['-arch', 'x86_64'])

# Define the C extensions
fhir_parser_c = Extension(
    'fast_fhir.fhir_parser_c',
    sources=['src/fast_fhir/ext/fhir_parser.c'],
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    libraries=libraries,
    extra_compile_args=extra_compile_args
)

fhir_datatypes_c = Extension(
    'fast_fhir.fhir_datatypes_c',
    sources=[
        'src/fast_fhir/ext/fhir_datatypes.c',
        'src/fast_fhir/ext/fhir_datatypes_python.c'
    ],
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    libraries=libraries,
    extra_compile_args=extra_compile_args
)

fhir_foundation_c = Extension(
    'fast_fhir.fhir_foundation_c',
    sources=[
        'src/fast_fhir/ext/fhir_foundation.c',
        'src/fast_fhir/ext/fhir_foundation_python.c',
        'src/fast_fhir/ext/fhir_datatypes.c'  # Foundation depends on datatypes
    ],
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    libraries=libraries,
    extra_compile_args=extra_compile_args
)

fhir_clinical_c = Extension(
    'fast_fhir.fhir_clinical_c',
    sources=[
        'src/fast_fhir/ext/fhir_clinical.c',
        'src/fast_fhir/ext/fhir_clinical_python.c',
        'src/fast_fhir/ext/fhir_datatypes.c',
        'src/fast_fhir/ext/fhir_foundation.c'
    ],
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    libraries=libraries,
    extra_compile_args=extra_compile_args
)

fhir_medication_c = Extension(
    'fast_fhir.fhir_medication_c',
    sources=[
        'src/fast_fhir/ext/fhir_medication.c',
        'src/fast_fhir/ext/fhir_medication_python.c',
        'src/fast_fhir/ext/fhir_datatypes.c',
        'src/fast_fhir/ext/fhir_foundation.c'
    ],
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    libraries=libraries,
    extra_compile_args=extra_compile_args
)

fhir_workflow_c = Extension(
    'fast_fhir.fhir_workflow_c',
    sources=[
        'src/fast_fhir/ext/fhir_workflow.c',
        'src/fast_fhir/ext/fhir_workflow_python.c',
        'src/fast_fhir/ext/fhir_datatypes.c',
        'src/fast_fhir/ext/fhir_foundation.c'
    ],
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    libraries=libraries,
    extra_compile_args=extra_compile_args
)

fhir_specialized_c = Extension(
    'fast_fhir.fhir_specialized_c',
    sources=[
        'src/fast_fhir/ext/fhir_specialized.c',
        'src/fast_fhir/ext/fhir_specialized_python.c',
        'src/fast_fhir/ext/fhir_datatypes.c',
        'src/fast_fhir/ext/fhir_foundation.c'
    ],
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    libraries=libraries,
    extra_compile_args=extra_compile_args
)

fhir_new_resources_c = Extension(
    'fast_fhir.fhir_new_resources_c',
    sources=[
        'src/fast_fhir/ext/fhir_new_resources.c',
        'src/fast_fhir/ext/fhir_new_resources_python.c',
        'src/fast_fhir/ext/fhir_datatypes.c',
        'src/fast_fhir/ext/fhir_foundation.c'
    ],
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    libraries=libraries,
    extra_compile_args=extra_compile_args
)

setup(
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    ext_modules=[
        fhir_parser_c, 
        fhir_datatypes_c, 
        fhir_foundation_c,
        fhir_clinical_c,
        fhir_medication_c,
        fhir_workflow_c,
        fhir_specialized_c,
        fhir_new_resources_c
    ],
    package_data={
        "fast_fhir": ["ext/*.c", "ext/*.h"],
    },
    include_package_data=True,
)