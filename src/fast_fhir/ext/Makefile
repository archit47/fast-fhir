# Makefile for FHIR C Extensions
# Following best practices for C project organization

# Compiler and flags
CC = gcc
CFLAGS = -std=c99 -Wall -Wextra -Wpedantic -O2 -fPIC
DEBUG_CFLAGS = -std=c99 -Wall -Wextra -Wpedantic -g -O0 -fPIC -DDEBUG
INCLUDES = -I. -I./common -I./resources
LIBS = -lcjson

# Python configuration
PYTHON_CONFIG = python3-config
PYTHON_INCLUDES = $(shell $(PYTHON_CONFIG) --includes)
PYTHON_LIBS = $(shell $(PYTHON_CONFIG) --ldflags)

# Directories
SRCDIR = .
COMMONDIR = common
RESOURCESDIR = resources
BUILDDIR = build
OBJDIR = $(BUILDDIR)/obj
LIBDIR = $(BUILDDIR)/lib

# Source files
COMMON_SOURCES = $(wildcard $(COMMONDIR)/*.c)
RESOURCE_SOURCES = $(wildcard $(RESOURCESDIR)/*.c)
PYTHON_SOURCES = $(wildcard *_python.c)

# Object files
COMMON_OBJECTS = $(COMMON_SOURCES:$(COMMONDIR)/%.c=$(OBJDIR)/common/%.o)
RESOURCE_OBJECTS = $(RESOURCE_SOURCES:$(RESOURCESDIR)/%.c=$(OBJDIR)/resources/%.o)
PYTHON_OBJECTS = $(PYTHON_SOURCES:%.c=$(OBJDIR)/%.o)

# Library targets
COMMON_LIB = $(LIBDIR)/libfhir_common.a
RESOURCE_LIBS = $(LIBDIR)/libfhir_organization_affiliation.so \
                $(LIBDIR)/libfhir_biologically_derived_product.so \
                $(LIBDIR)/libfhir_device_metric.so \
                $(LIBDIR)/libfhir_nutrition_product.so \
                $(LIBDIR)/libfhir_transport.so \
                $(LIBDIR)/libfhir_verification_result.so \
                $(LIBDIR)/libfhir_encounter_history.so \
                $(LIBDIR)/libfhir_episode_of_care.so

PYTHON_EXTENSIONS = $(LIBDIR)/fhir_new_resources_c.so

# Default target
all: directories $(COMMON_LIB) $(RESOURCE_LIBS) $(PYTHON_EXTENSIONS)

# Debug target
debug: CFLAGS = $(DEBUG_CFLAGS)
debug: all

# Create directories
directories:
	@mkdir -p $(OBJDIR)/common
	@mkdir -p $(OBJDIR)/resources
	@mkdir -p $(LIBDIR)

# Common library (static)
$(COMMON_LIB): $(COMMON_OBJECTS)
	@echo "Creating common library: $@"
	ar rcs $@ $^

# Resource libraries (shared)
$(LIBDIR)/libfhir_organization_affiliation.so: $(OBJDIR)/resources/fhir_organization_affiliation.o $(COMMON_LIB)
	@echo "Creating shared library: $@"
	$(CC) -shared -o $@ $< -L$(LIBDIR) -lfhir_common $(LIBS)

$(LIBDIR)/libfhir_biologically_derived_product.so: $(OBJDIR)/resources/fhir_biologically_derived_product.o $(COMMON_LIB)
	@echo "Creating shared library: $@"
	$(CC) -shared -o $@ $< -L$(LIBDIR) -lfhir_common $(LIBS)

$(LIBDIR)/libfhir_device_metric.so: $(OBJDIR)/resources/fhir_device_metric.o $(COMMON_LIB)
	@echo "Creating shared library: $@"
	$(CC) -shared -o $@ $< -L$(LIBDIR) -lfhir_common $(LIBS)

# Add more resource libraries as needed...

# Python extension
$(LIBDIR)/fhir_new_resources_c.so: $(OBJDIR)/fhir_new_resources_python.o $(OBJDIR)/fhir_new_resources.o $(COMMON_LIB)
	@echo "Creating Python extension: $@"
	$(CC) -shared -o $@ $^ -L$(LIBDIR) -lfhir_common $(LIBS) $(PYTHON_LIBS)

# Object file rules
$(OBJDIR)/common/%.o: $(COMMONDIR)/%.c
	@echo "Compiling: $<"
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

$(OBJDIR)/resources/%.o: $(RESOURCESDIR)/%.c
	@echo "Compiling: $<"
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

$(OBJDIR)/%.o: %.c
	@echo "Compiling: $<"
	$(CC) $(CFLAGS) $(INCLUDES) $(PYTHON_INCLUDES) -c $< -o $@

# Clean
clean:
	@echo "Cleaning build files..."
	rm -rf $(BUILDDIR)

# Install (copy to Python site-packages or appropriate location)
install: all
	@echo "Installing libraries..."
	# Add installation commands here

# Test
test: all
	@echo "Running tests..."
	# Add test commands here

# Format code
format:
	@echo "Formatting code..."
	find . -name "*.c" -o -name "*.h" | xargs clang-format -i

# Static analysis
analyze:
	@echo "Running static analysis..."
	cppcheck --enable=all --std=c99 $(COMMONDIR) $(RESOURCESDIR)

# Documentation
docs:
	@echo "Generating documentation..."
	doxygen Doxyfile

# Help
help:
	@echo "Available targets:"
	@echo "  all      - Build all libraries and extensions"
	@echo "  debug    - Build with debug flags"
	@echo "  clean    - Remove build files"
	@echo "  install  - Install libraries"
	@echo "  test     - Run tests"
	@echo "  format   - Format source code"
	@echo "  analyze  - Run static analysis"
	@echo "  docs     - Generate documentation"
	@echo "  help     - Show this help"

.PHONY: all debug directories clean install test format analyze docs help

# Dependencies (auto-generated)
-include $(OBJDIR)/*.d
-include $(OBJDIR)/common/*.d
-include $(OBJDIR)/resources/*.d