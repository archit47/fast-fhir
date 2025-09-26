#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "fhir_datatypes.h"

// Python wrapper functions for FHIR data types

// Create Python objects from C structures
static PyObject* py_fhir_string_create(PyObject* self, PyObject* args) {
    const char* value;
    if (!PyArg_ParseTuple(args, "s", &value)) {
        return NULL;
    }
    
    FHIRString* fhir_str = fhir_string_create(value);
    if (!fhir_str) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create FHIR string");
        return NULL;
    }
    
    // Create Python dictionary representation
    PyObject* dict = PyDict_New();
    if (fhir_str->value) {
        PyDict_SetItemString(dict, "value", PyUnicode_FromString(fhir_str->value));
    }
    
    // Clean up C structure
    fhir_string_free(fhir_str->value);
    free(fhir_str);
    
    return dict;
}

static PyObject* py_fhir_boolean_create(PyObject* self, PyObject* args) {
    int value;
    if (!PyArg_ParseTuple(args, "p", &value)) {
        return NULL;
    }
    
    FHIRBoolean* fhir_bool = fhir_boolean_create(value);
    if (!fhir_bool) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create FHIR boolean");
        return NULL;
    }
    
    PyObject* dict = PyDict_New();
    PyDict_SetItemString(dict, "value", PyBool_FromLong(fhir_bool->value));
    
    free(fhir_bool);
    return dict;
}

static PyObject* py_fhir_integer_create(PyObject* self, PyObject* args) {
    int value;
    if (!PyArg_ParseTuple(args, "i", &value)) {
        return NULL;
    }
    
    FHIRInteger* fhir_int = fhir_integer_create(value);
    if (!fhir_int) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create FHIR integer");
        return NULL;
    }
    
    PyObject* dict = PyDict_New();
    PyDict_SetItemString(dict, "value", PyLong_FromLong(fhir_int->value));
    
    free(fhir_int);
    return dict;
}

static PyObject* py_fhir_decimal_create(PyObject* self, PyObject* args) {
    double value;
    if (!PyArg_ParseTuple(args, "d", &value)) {
        return NULL;
    }
    
    FHIRDecimal* fhir_decimal = fhir_decimal_create(value);
    if (!fhir_decimal) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create FHIR decimal");
        return NULL;
    }
    
    PyObject* dict = PyDict_New();
    PyDict_SetItemString(dict, "value", PyFloat_FromDouble(fhir_decimal->value));
    
    free(fhir_decimal);
    return dict;
}

static PyObject* py_fhir_coding_create(PyObject* self, PyObject* args) {
    const char* system = NULL;
    const char* code = NULL;
    const char* display = NULL;
    
    if (!PyArg_ParseTuple(args, "|zzz", &system, &code, &display)) {
        return NULL;
    }
    
    FHIRCoding* coding = fhir_coding_create(system, code, display);
    if (!coding) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create FHIR coding");
        return NULL;
    }
    
    PyObject* dict = PyDict_New();
    if (coding->system) {
        PyDict_SetItemString(dict, "system", PyUnicode_FromString(coding->system));
    }
    if (coding->code) {
        PyDict_SetItemString(dict, "code", PyUnicode_FromString(coding->code));
    }
    if (coding->display) {
        PyDict_SetItemString(dict, "display", PyUnicode_FromString(coding->display));
    }
    PyDict_SetItemString(dict, "userSelected", PyBool_FromLong(coding->user_selected));
    
    // Clean up
    fhir_string_free(coding->system);
    fhir_string_free(coding->code);
    fhir_string_free(coding->display);
    free(coding);
    
    return dict;
}

static PyObject* py_fhir_quantity_create(PyObject* self, PyObject* args) {
    double value;
    const char* unit = NULL;
    const char* system = NULL;
    const char* code = NULL;
    
    if (!PyArg_ParseTuple(args, "d|zzz", &value, &unit, &system, &code)) {
        return NULL;
    }
    
    FHIRQuantity* quantity = fhir_quantity_create(value, unit, system, code);
    if (!quantity) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create FHIR quantity");
        return NULL;
    }
    
    PyObject* dict = PyDict_New();
    PyDict_SetItemString(dict, "value", PyFloat_FromDouble(quantity->value));
    if (quantity->unit) {
        PyDict_SetItemString(dict, "unit", PyUnicode_FromString(quantity->unit));
    }
    if (quantity->system) {
        PyDict_SetItemString(dict, "system", PyUnicode_FromString(quantity->system));
    }
    if (quantity->code) {
        PyDict_SetItemString(dict, "code", PyUnicode_FromString(quantity->code));
    }
    
    // Clean up
    fhir_string_free(quantity->unit);
    fhir_string_free(quantity->system);
    fhir_string_free(quantity->code);
    free(quantity);
    
    return dict;
}

// Parse JSON to FHIR data types
static PyObject* py_fhir_parse_coding(PyObject* self, PyObject* args) {
    const char* json_string;
    if (!PyArg_ParseTuple(args, "s", &json_string)) {
        return NULL;
    }
    
    cJSON* json = cJSON_Parse(json_string);
    if (!json) {
        PyErr_SetString(PyExc_ValueError, "Invalid JSON");
        return NULL;
    }
    
    FHIRCoding* coding = fhir_parse_coding(json);
    cJSON_Delete(json);
    
    if (!coding) {
        PyErr_SetString(PyExc_ValueError, "Failed to parse FHIR Coding");
        return NULL;
    }
    
    // Convert to Python dict
    PyObject* dict = PyDict_New();
    if (coding->system) {
        PyDict_SetItemString(dict, "system", PyUnicode_FromString(coding->system));
    }
    if (coding->code) {
        PyDict_SetItemString(dict, "code", PyUnicode_FromString(coding->code));
    }
    if (coding->display) {
        PyDict_SetItemString(dict, "display", PyUnicode_FromString(coding->display));
    }
    PyDict_SetItemString(dict, "userSelected", PyBool_FromLong(coding->user_selected));
    
    // Clean up
    fhir_string_free(coding->system);
    fhir_string_free(coding->code);
    fhir_string_free(coding->display);
    free(coding);
    
    return dict;
}

static PyObject* py_fhir_parse_quantity(PyObject* self, PyObject* args) {
    const char* json_string;
    if (!PyArg_ParseTuple(args, "s", &json_string)) {
        return NULL;
    }
    
    cJSON* json = cJSON_Parse(json_string);
    if (!json) {
        PyErr_SetString(PyExc_ValueError, "Invalid JSON");
        return NULL;
    }
    
    FHIRQuantity* quantity = fhir_parse_quantity(json);
    cJSON_Delete(json);
    
    if (!quantity) {
        PyErr_SetString(PyExc_ValueError, "Failed to parse FHIR Quantity");
        return NULL;
    }
    
    // Convert to Python dict
    PyObject* dict = PyDict_New();
    PyDict_SetItemString(dict, "value", PyFloat_FromDouble(quantity->value));
    if (quantity->unit) {
        PyDict_SetItemString(dict, "unit", PyUnicode_FromString(quantity->unit));
    }
    if (quantity->system) {
        PyDict_SetItemString(dict, "system", PyUnicode_FromString(quantity->system));
    }
    if (quantity->code) {
        PyDict_SetItemString(dict, "code", PyUnicode_FromString(quantity->code));
    }
    if (quantity->comparator) {
        PyDict_SetItemString(dict, "comparator", PyUnicode_FromString(quantity->comparator));
    }
    
    // Clean up
    fhir_string_free(quantity->unit);
    fhir_string_free(quantity->system);
    fhir_string_free(quantity->code);
    fhir_string_free(quantity->comparator);
    free(quantity);
    
    return dict;
}

// Validation functions
static PyObject* py_fhir_validate_date(PyObject* self, PyObject* args) {
    const char* date;
    if (!PyArg_ParseTuple(args, "s", &date)) {
        return NULL;
    }
    
    bool is_valid = fhir_validate_date(date);
    return PyBool_FromLong(is_valid);
}

static PyObject* py_fhir_validate_time(PyObject* self, PyObject* args) {
    const char* time;
    if (!PyArg_ParseTuple(args, "s", &time)) {
        return NULL;
    }
    
    bool is_valid = fhir_validate_time(time);
    return PyBool_FromLong(is_valid);
}

static PyObject* py_fhir_validate_uri(PyObject* self, PyObject* args) {
    const char* uri;
    if (!PyArg_ParseTuple(args, "s", &uri)) {
        return NULL;
    }
    
    bool is_valid = fhir_validate_uri(uri);
    return PyBool_FromLong(is_valid);
}

static PyObject* py_fhir_validate_code(PyObject* self, PyObject* args) {
    const char* code;
    if (!PyArg_ParseTuple(args, "s", &code)) {
        return NULL;
    }
    
    bool is_valid = fhir_validate_code(code);
    return PyBool_FromLong(is_valid);
}

// Method definitions
static PyMethodDef FHIRDatatypesMethods[] = {
    // Creation functions
    {"create_string", py_fhir_string_create, METH_VARARGS, "Create FHIR string"},
    {"create_boolean", py_fhir_boolean_create, METH_VARARGS, "Create FHIR boolean"},
    {"create_integer", py_fhir_integer_create, METH_VARARGS, "Create FHIR integer"},
    {"create_decimal", py_fhir_decimal_create, METH_VARARGS, "Create FHIR decimal"},
    {"create_coding", py_fhir_coding_create, METH_VARARGS, "Create FHIR coding"},
    {"create_quantity", py_fhir_quantity_create, METH_VARARGS, "Create FHIR quantity"},
    
    // Parsing functions
    {"parse_coding", py_fhir_parse_coding, METH_VARARGS, "Parse FHIR Coding from JSON"},
    {"parse_quantity", py_fhir_parse_quantity, METH_VARARGS, "Parse FHIR Quantity from JSON"},
    
    // Validation functions
    {"validate_date", py_fhir_validate_date, METH_VARARGS, "Validate FHIR date format"},
    {"validate_time", py_fhir_validate_time, METH_VARARGS, "Validate FHIR time format"},
    {"validate_uri", py_fhir_validate_uri, METH_VARARGS, "Validate FHIR URI format"},
    {"validate_code", py_fhir_validate_code, METH_VARARGS, "Validate FHIR code format"},
    
    {NULL, NULL, 0, NULL}
};

// Module definition
static struct PyModuleDef fhir_datatypes_module = {
    PyModuleDef_HEAD_INIT,
    "fhir_datatypes_c",
    "FHIR R5 data types implemented in C",
    -1,
    FHIRDatatypesMethods
};

// Module initialization
PyMODINIT_FUNC PyInit_fhir_datatypes_c(void) {
    return PyModule_Create(&fhir_datatypes_module);
}