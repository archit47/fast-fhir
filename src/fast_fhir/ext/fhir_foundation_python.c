#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "fhir_foundation.h"

// Python wrapper functions for FHIR Foundation resources

// Patient resource functions
static PyObject* py_fhir_patient_create(PyObject* self, PyObject* args) {
    const char* id = NULL;
    if (!PyArg_ParseTuple(args, "|z", &id)) {
        return NULL;
    }
    
    FHIRPatient* patient = fhir_patient_create(id);
    if (!patient) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create FHIR Patient");
        return NULL;
    }
    
    // Convert to Python dictionary
    cJSON* json = fhir_patient_to_json(patient);
    fhir_patient_free(patient);
    
    if (!json) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to serialize Patient to JSON");
        return NULL;
    }
    
    char* json_string = cJSON_Print(json);
    cJSON_Delete(json);
    
    if (!json_string) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to convert JSON to string");
        return NULL;
    }
    
    PyObject* json_module = PyImport_ImportModule("json");
    if (!json_module) {
        free(json_string);
        return NULL;
    }
    
    PyObject* loads_func = PyObject_GetAttrString(json_module, "loads");
    Py_DECREF(json_module);
    
    if (!loads_func) {
        free(json_string);
        return NULL;
    }
    
    PyObject* json_str_obj = PyUnicode_FromString(json_string);
    free(json_string);
    
    if (!json_str_obj) {
        Py_DECREF(loads_func);
        return NULL;
    }
    
    PyObject* result = PyObject_CallFunctionObjArgs(loads_func, json_str_obj, NULL);
    Py_DECREF(loads_func);
    Py_DECREF(json_str_obj);
    
    return result;
}

static PyObject* py_fhir_parse_patient(PyObject* self, PyObject* args) {
    const char* json_string;
    if (!PyArg_ParseTuple(args, "s", &json_string)) {
        return NULL;
    }
    
    cJSON* json = cJSON_Parse(json_string);
    if (!json) {
        PyErr_SetString(PyExc_ValueError, "Invalid JSON");
        return NULL;
    }
    
    FHIRPatient* patient = fhir_parse_patient(json);
    cJSON_Delete(json);
    
    if (!patient) {
        PyErr_SetString(PyExc_ValueError, "Failed to parse FHIR Patient");
        return NULL;
    }
    
    // Convert back to JSON for Python
    cJSON* result_json = fhir_patient_to_json(patient);
    fhir_patient_free(patient);
    
    if (!result_json) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to serialize Patient");
        return NULL;
    }
    
    char* result_string = cJSON_Print(result_json);
    cJSON_Delete(result_json);
    
    if (!result_string) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to convert JSON to string");
        return NULL;
    }
    
    PyObject* json_module = PyImport_ImportModule("json");
    if (!json_module) {
        free(result_string);
        return NULL;
    }
    
    PyObject* loads_func = PyObject_GetAttrString(json_module, "loads");
    Py_DECREF(json_module);
    
    if (!loads_func) {
        free(result_string);
        return NULL;
    }
    
    PyObject* json_str_obj = PyUnicode_FromString(result_string);
    free(result_string);
    
    if (!json_str_obj) {
        Py_DECREF(loads_func);
        return NULL;
    }
    
    PyObject* result = PyObject_CallFunctionObjArgs(loads_func, json_str_obj, NULL);
    Py_DECREF(loads_func);
    Py_DECREF(json_str_obj);
    
    return result;
}

static PyObject* py_fhir_patient_get_full_name(PyObject* self, PyObject* args) {
    const char* json_string;
    if (!PyArg_ParseTuple(args, "s", &json_string)) {
        return NULL;
    }
    
    cJSON* json = cJSON_Parse(json_string);
    if (!json) {
        PyErr_SetString(PyExc_ValueError, "Invalid JSON");
        return NULL;
    }
    
    FHIRPatient* patient = fhir_parse_patient(json);
    cJSON_Delete(json);
    
    if (!patient) {
        PyErr_SetString(PyExc_ValueError, "Failed to parse FHIR Patient");
        return NULL;
    }
    
    char* full_name = fhir_patient_get_full_name(patient);
    fhir_patient_free(patient);
    
    if (!full_name) {
        Py_RETURN_NONE;
    }
    
    PyObject* result = PyUnicode_FromString(full_name);
    fhir_string_free(full_name);
    
    return result;
}

static PyObject* py_fhir_patient_is_active(PyObject* self, PyObject* args) {
    const char* json_string;
    if (!PyArg_ParseTuple(args, "s", &json_string)) {
        return NULL;
    }
    
    cJSON* json = cJSON_Parse(json_string);
    if (!json) {
        PyErr_SetString(PyExc_ValueError, "Invalid JSON");
        return NULL;
    }
    
    FHIRPatient* patient = fhir_parse_patient(json);
    cJSON_Delete(json);
    
    if (!patient) {
        PyErr_SetString(PyExc_ValueError, "Failed to parse FHIR Patient");
        return NULL;
    }
    
    bool is_active = fhir_patient_is_active(patient);
    fhir_patient_free(patient);
    
    return PyBool_FromLong(is_active);
}

static PyObject* py_fhir_validate_patient(PyObject* self, PyObject* args) {
    const char* json_string;
    if (!PyArg_ParseTuple(args, "s", &json_string)) {
        return NULL;
    }
    
    cJSON* json = cJSON_Parse(json_string);
    if (!json) {
        PyErr_SetString(PyExc_ValueError, "Invalid JSON");
        return NULL;
    }
    
    FHIRPatient* patient = fhir_parse_patient(json);
    cJSON_Delete(json);
    
    if (!patient) {
        return PyBool_FromLong(false);
    }
    
    bool is_valid = fhir_validate_patient(patient);
    fhir_patient_free(patient);
    
    return PyBool_FromLong(is_valid);
}

// Practitioner resource functions
static PyObject* py_fhir_practitioner_create(PyObject* self, PyObject* args) {
    const char* id = NULL;
    if (!PyArg_ParseTuple(args, "|z", &id)) {
        return NULL;
    }
    
    FHIRPractitioner* practitioner = fhir_practitioner_create(id);
    if (!practitioner) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create FHIR Practitioner");
        return NULL;
    }
    
    // Convert to Python dictionary
    cJSON* json = fhir_practitioner_to_json(practitioner);
    fhir_practitioner_free(practitioner);
    
    if (!json) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to serialize Practitioner to JSON");
        return NULL;
    }
    
    char* json_string = cJSON_Print(json);
    cJSON_Delete(json);
    
    if (!json_string) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to convert JSON to string");
        return NULL;
    }
    
    PyObject* json_module = PyImport_ImportModule("json");
    if (!json_module) {
        free(json_string);
        return NULL;
    }
    
    PyObject* loads_func = PyObject_GetAttrString(json_module, "loads");
    Py_DECREF(json_module);
    
    if (!loads_func) {
        free(json_string);
        return NULL;
    }
    
    PyObject* json_str_obj = PyUnicode_FromString(json_string);
    free(json_string);
    
    if (!json_str_obj) {
        Py_DECREF(loads_func);
        return NULL;
    }
    
    PyObject* result = PyObject_CallFunctionObjArgs(loads_func, json_str_obj, NULL);
    Py_DECREF(loads_func);
    Py_DECREF(json_str_obj);
    
    return result;
}

// Organization resource functions
static PyObject* py_fhir_organization_create(PyObject* self, PyObject* args) {
    const char* id = NULL;
    if (!PyArg_ParseTuple(args, "|z", &id)) {
        return NULL;
    }
    
    FHIROrganization* organization = fhir_organization_create(id);
    if (!organization) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create FHIR Organization");
        return NULL;
    }
    
    // Convert to Python dictionary
    cJSON* json = fhir_organization_to_json(organization);
    fhir_organization_free(organization);
    
    if (!json) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to serialize Organization to JSON");
        return NULL;
    }
    
    char* json_string = cJSON_Print(json);
    cJSON_Delete(json);
    
    if (!json_string) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to convert JSON to string");
        return NULL;
    }
    
    PyObject* json_module = PyImport_ImportModule("json");
    if (!json_module) {
        free(json_string);
        return NULL;
    }
    
    PyObject* loads_func = PyObject_GetAttrString(json_module, "loads");
    Py_DECREF(json_module);
    
    if (!loads_func) {
        free(json_string);
        return NULL;
    }
    
    PyObject* json_str_obj = PyUnicode_FromString(json_string);
    free(json_string);
    
    if (!json_str_obj) {
        Py_DECREF(loads_func);
        return NULL;
    }
    
    PyObject* result = PyObject_CallFunctionObjArgs(loads_func, json_str_obj, NULL);
    Py_DECREF(loads_func);
    Py_DECREF(json_str_obj);
    
    return result;
}

// Utility functions
static PyObject* py_fhir_is_foundation_resource(PyObject* self, PyObject* args) {
    const char* resource_type;
    if (!PyArg_ParseTuple(args, "s", &resource_type)) {
        return NULL;
    }
    
    bool is_foundation = fhir_is_foundation_resource(resource_type);
    return PyBool_FromLong(is_foundation);
}

static PyObject* py_fhir_get_resource_type(PyObject* self, PyObject* args) {
    const char* json_string;
    if (!PyArg_ParseTuple(args, "s", &json_string)) {
        return NULL;
    }
    
    cJSON* json = cJSON_Parse(json_string);
    if (!json) {
        PyErr_SetString(PyExc_ValueError, "Invalid JSON");
        return NULL;
    }
    
    cJSON* resource_type = cJSON_GetObjectItemCaseSensitive(json, "resourceType");
    if (!cJSON_IsString(resource_type)) {
        cJSON_Delete(json);
        Py_RETURN_NONE;
    }
    
    PyObject* result = PyUnicode_FromString(resource_type->valuestring);
    cJSON_Delete(json);
    
    return result;
}

// Method definitions
static PyMethodDef FHIRFoundationMethods[] = {
    // Patient functions
    {"create_patient", py_fhir_patient_create, METH_VARARGS, "Create FHIR Patient resource"},
    {"parse_patient", py_fhir_parse_patient, METH_VARARGS, "Parse FHIR Patient from JSON"},
    {"patient_get_full_name", py_fhir_patient_get_full_name, METH_VARARGS, "Get patient full name"},
    {"patient_is_active", py_fhir_patient_is_active, METH_VARARGS, "Check if patient is active"},
    {"validate_patient", py_fhir_validate_patient, METH_VARARGS, "Validate FHIR Patient"},
    
    // Practitioner functions
    {"create_practitioner", py_fhir_practitioner_create, METH_VARARGS, "Create FHIR Practitioner resource"},
    
    // Organization functions
    {"create_organization", py_fhir_organization_create, METH_VARARGS, "Create FHIR Organization resource"},
    
    // CodeSystem functions
    {"create_code_system", py_fhir_code_system_create, METH_VARARGS, "Create FHIR CodeSystem resource"},
    {"parse_code_system", py_fhir_parse_code_system, METH_VARARGS, "Parse FHIR CodeSystem from JSON"},
    
    // ValueSet functions
    {"create_value_set", py_fhir_value_set_create, METH_VARARGS, "Create FHIR ValueSet resource"},
    
    // Binary functions
    {"create_binary", py_fhir_binary_create, METH_VARARGS, "Create FHIR Binary resource"},
    
    // Bundle functions
    {"create_bundle", py_fhir_bundle_create, METH_VARARGS, "Create FHIR Bundle resource"},
    {"parse_bundle", py_fhir_parse_bundle, METH_VARARGS, "Parse FHIR Bundle from JSON"},
    {"bundle_get_entry_count", py_fhir_bundle_get_entry_count, METH_VARARGS, "Get Bundle entry count"},
    
    // Utility functions
    {"is_foundation_resource", py_fhir_is_foundation_resource, METH_VARARGS, "Check if resource type is Foundation"},
    {"is_terminology_resource", py_fhir_is_terminology_resource, METH_VARARGS, "Check if resource type is Terminology"},
    {"get_resource_type", py_fhir_get_resource_type, METH_VARARGS, "Get resource type from JSON"},
    
    {NULL, NULL, 0, NULL}
};

// Module definition
static struct PyModuleDef fhir_foundation_module = {
    PyModuleDef_HEAD_INIT,
    "fhir_foundation_c",
    "FHIR R5 Foundation resources implemented in C",
    -1,
    FHIRFoundationMethods
};

// Module initialization
PyMODINIT_FUNC PyInit_fhir_foundation_c(void) {
    return PyModule_Create(&fhir_foundation_module);
}
//
 Additional Python wrapper functions for new Foundation resources

// CodeSystem resource functions
static PyObject* py_fhir_code_system_create(PyObject* self, PyObject* args) {
    const char* id = NULL;
    if (!PyArg_ParseTuple(args, "|z", &id)) {
        return NULL;
    }
    
    FHIRCodeSystem* code_system = fhir_code_system_create(id);
    if (!code_system) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create FHIR CodeSystem");
        return NULL;
    }
    
    // Convert to Python dictionary
    cJSON* json = fhir_code_system_to_json(code_system);
    fhir_code_system_free(code_system);
    
    if (!json) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to serialize CodeSystem to JSON");
        return NULL;
    }
    
    char* json_string = cJSON_Print(json);
    cJSON_Delete(json);
    
    if (!json_string) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to convert JSON to string");
        return NULL;
    }
    
    PyObject* json_module = PyImport_ImportModule("json");
    if (!json_module) {
        free(json_string);
        return NULL;
    }
    
    PyObject* loads_func = PyObject_GetAttrString(json_module, "loads");
    Py_DECREF(json_module);
    
    if (!loads_func) {
        free(json_string);
        return NULL;
    }
    
    PyObject* json_str_obj = PyUnicode_FromString(json_string);
    free(json_string);
    
    if (!json_str_obj) {
        Py_DECREF(loads_func);
        return NULL;
    }
    
    PyObject* result = PyObject_CallFunctionObjArgs(loads_func, json_str_obj, NULL);
    Py_DECREF(loads_func);
    Py_DECREF(json_str_obj);
    
    return result;
}

static PyObject* py_fhir_parse_code_system(PyObject* self, PyObject* args) {
    const char* json_string;
    if (!PyArg_ParseTuple(args, "s", &json_string)) {
        return NULL;
    }
    
    cJSON* json = cJSON_Parse(json_string);
    if (!json) {
        PyErr_SetString(PyExc_ValueError, "Invalid JSON");
        return NULL;
    }
    
    FHIRCodeSystem* code_system = fhir_parse_code_system(json);
    cJSON_Delete(json);
    
    if (!code_system) {
        PyErr_SetString(PyExc_ValueError, "Failed to parse FHIR CodeSystem");
        return NULL;
    }
    
    // Convert back to JSON for Python
    cJSON* result_json = fhir_code_system_to_json(code_system);
    fhir_code_system_free(code_system);
    
    if (!result_json) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to serialize CodeSystem");
        return NULL;
    }
    
    char* result_string = cJSON_Print(result_json);
    cJSON_Delete(result_json);
    
    if (!result_string) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to convert JSON to string");
        return NULL;
    }
    
    PyObject* json_module = PyImport_ImportModule("json");
    if (!json_module) {
        free(result_string);
        return NULL;
    }
    
    PyObject* loads_func = PyObject_GetAttrString(json_module, "loads");
    Py_DECREF(json_module);
    
    if (!loads_func) {
        free(result_string);
        return NULL;
    }
    
    PyObject* json_str_obj = PyUnicode_FromString(result_string);
    free(result_string);
    
    if (!json_str_obj) {
        Py_DECREF(loads_func);
        return NULL;
    }
    
    PyObject* result = PyObject_CallFunctionObjArgs(loads_func, json_str_obj, NULL);
    Py_DECREF(loads_func);
    Py_DECREF(json_str_obj);
    
    return result;
}

// ValueSet resource functions
static PyObject* py_fhir_value_set_create(PyObject* self, PyObject* args) {
    const char* id = NULL;
    if (!PyArg_ParseTuple(args, "|z", &id)) {
        return NULL;
    }
    
    FHIRValueSet* value_set = fhir_value_set_create(id);
    if (!value_set) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create FHIR ValueSet");
        return NULL;
    }
    
    // Convert to Python dictionary
    cJSON* json = fhir_value_set_to_json(value_set);
    fhir_value_set_free(value_set);
    
    if (!json) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to serialize ValueSet to JSON");
        return NULL;
    }
    
    char* json_string = cJSON_Print(json);
    cJSON_Delete(json);
    
    if (!json_string) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to convert JSON to string");
        return NULL;
    }
    
    PyObject* json_module = PyImport_ImportModule("json");
    if (!json_module) {
        free(json_string);
        return NULL;
    }
    
    PyObject* loads_func = PyObject_GetAttrString(json_module, "loads");
    Py_DECREF(json_module);
    
    if (!loads_func) {
        free(json_string);
        return NULL;
    }
    
    PyObject* json_str_obj = PyUnicode_FromString(json_string);
    free(json_string);
    
    if (!json_str_obj) {
        Py_DECREF(loads_func);
        return NULL;
    }
    
    PyObject* result = PyObject_CallFunctionObjArgs(loads_func, json_str_obj, NULL);
    Py_DECREF(loads_func);
    Py_DECREF(json_str_obj);
    
    return result;
}

// Binary resource functions
static PyObject* py_fhir_binary_create(PyObject* self, PyObject* args) {
    const char* id = NULL;
    if (!PyArg_ParseTuple(args, "|z", &id)) {
        return NULL;
    }
    
    FHIRBinary* binary = fhir_binary_create(id);
    if (!binary) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create FHIR Binary");
        return NULL;
    }
    
    // Convert to Python dictionary
    cJSON* json = fhir_binary_to_json(binary);
    fhir_binary_free(binary);
    
    if (!json) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to serialize Binary to JSON");
        return NULL;
    }
    
    char* json_string = cJSON_Print(json);
    cJSON_Delete(json);
    
    if (!json_string) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to convert JSON to string");
        return NULL;
    }
    
    PyObject* json_module = PyImport_ImportModule("json");
    if (!json_module) {
        free(json_string);
        return NULL;
    }
    
    PyObject* loads_func = PyObject_GetAttrString(json_module, "loads");
    Py_DECREF(json_module);
    
    if (!loads_func) {
        free(json_string);
        return NULL;
    }
    
    PyObject* json_str_obj = PyUnicode_FromString(json_string);
    free(json_string);
    
    if (!json_str_obj) {
        Py_DECREF(loads_func);
        return NULL;
    }
    
    PyObject* result = PyObject_CallFunctionObjArgs(loads_func, json_str_obj, NULL);
    Py_DECREF(loads_func);
    Py_DECREF(json_str_obj);
    
    return result;
}

// Bundle resource functions
static PyObject* py_fhir_bundle_create(PyObject* self, PyObject* args) {
    const char* id = NULL;
    if (!PyArg_ParseTuple(args, "|z", &id)) {
        return NULL;
    }
    
    FHIRBundle* bundle = fhir_bundle_create(id);
    if (!bundle) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create FHIR Bundle");
        return NULL;
    }
    
    // Convert to Python dictionary
    cJSON* json = fhir_bundle_to_json(bundle);
    fhir_bundle_free(bundle);
    
    if (!json) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to serialize Bundle to JSON");
        return NULL;
    }
    
    char* json_string = cJSON_Print(json);
    cJSON_Delete(json);
    
    if (!json_string) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to convert JSON to string");
        return NULL;
    }
    
    PyObject* json_module = PyImport_ImportModule("json");
    if (!json_module) {
        free(json_string);
        return NULL;
    }
    
    PyObject* loads_func = PyObject_GetAttrString(json_module, "loads");
    Py_DECREF(json_module);
    
    if (!loads_func) {
        free(json_string);
        return NULL;
    }
    
    PyObject* json_str_obj = PyUnicode_FromString(json_string);
    free(json_string);
    
    if (!json_str_obj) {
        Py_DECREF(loads_func);
        return NULL;
    }
    
    PyObject* result = PyObject_CallFunctionObjArgs(loads_func, json_str_obj, NULL);
    Py_DECREF(loads_func);
    Py_DECREF(json_str_obj);
    
    return result;
}

static PyObject* py_fhir_parse_bundle(PyObject* self, PyObject* args) {
    const char* json_string;
    if (!PyArg_ParseTuple(args, "s", &json_string)) {
        return NULL;
    }
    
    cJSON* json = cJSON_Parse(json_string);
    if (!json) {
        PyErr_SetString(PyExc_ValueError, "Invalid JSON");
        return NULL;
    }
    
    FHIRBundle* bundle = fhir_parse_bundle(json);
    cJSON_Delete(json);
    
    if (!bundle) {
        PyErr_SetString(PyExc_ValueError, "Failed to parse FHIR Bundle");
        return NULL;
    }
    
    // Convert back to JSON for Python
    cJSON* result_json = fhir_bundle_to_json(bundle);
    fhir_bundle_free(bundle);
    
    if (!result_json) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to serialize Bundle");
        return NULL;
    }
    
    char* result_string = cJSON_Print(result_json);
    cJSON_Delete(result_json);
    
    if (!result_string) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to convert JSON to string");
        return NULL;
    }
    
    PyObject* json_module = PyImport_ImportModule("json");
    if (!json_module) {
        free(result_string);
        return NULL;
    }
    
    PyObject* loads_func = PyObject_GetAttrString(json_module, "loads");
    Py_DECREF(json_module);
    
    if (!loads_func) {
        free(result_string);
        return NULL;
    }
    
    PyObject* json_str_obj = PyUnicode_FromString(result_string);
    free(result_string);
    
    if (!json_str_obj) {
        Py_DECREF(loads_func);
        return NULL;
    }
    
    PyObject* result = PyObject_CallFunctionObjArgs(loads_func, json_str_obj, NULL);
    Py_DECREF(loads_func);
    Py_DECREF(json_str_obj);
    
    return result;
}

static PyObject* py_fhir_bundle_get_entry_count(PyObject* self, PyObject* args) {
    const char* json_string;
    if (!PyArg_ParseTuple(args, "s", &json_string)) {
        return NULL;
    }
    
    cJSON* json = cJSON_Parse(json_string);
    if (!json) {
        PyErr_SetString(PyExc_ValueError, "Invalid JSON");
        return NULL;
    }
    
    FHIRBundle* bundle = fhir_parse_bundle(json);
    cJSON_Delete(json);
    
    if (!bundle) {
        PyErr_SetString(PyExc_ValueError, "Failed to parse FHIR Bundle");
        return NULL;
    }
    
    size_t count = fhir_bundle_get_entry_count(bundle);
    fhir_bundle_free(bundle);
    
    return PyLong_FromSize_t(count);
}

// Utility functions
static PyObject* py_fhir_is_terminology_resource(PyObject* self, PyObject* args) {
    const char* resource_type;
    if (!PyArg_ParseTuple(args, "s", &resource_type)) {
        return NULL;
    }
    
    bool is_terminology = fhir_is_terminology_resource(resource_type);
    return PyBool_FromLong(is_terminology);
}// Ad
ditional Python wrapper functions for new Foundation resources

// Location resource functions
static PyObject* py_fhir_location_create(PyObject* self, PyObject* args) {
    const char* id = NULL;
    if (!PyArg_ParseTuple(args, "|z", &id)) {
        return NULL;
    }
    
    FHIRLocation* location = fhir_location_create(id);
    if (!location) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create FHIR Location");
        return NULL;
    }
    
    // Convert to Python dictionary
    cJSON* json = fhir_location_to_json(location);
    fhir_location_free(location);
    
    if (!json) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to serialize Location to JSON");
        return NULL;
    }
    
    char* json_string = cJSON_Print(json);
    cJSON_Delete(json);
    
    if (!json_string) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to convert JSON to string");
        return NULL;
    }
    
    PyObject* json_module = PyImport_ImportModule("json");
    if (!json_module) {
        free(json_string);
        return NULL;
    }
    
    PyObject* loads_func = PyObject_GetAttrString(json_module, "loads");
    Py_DECREF(json_module);
    
    if (!loads_func) {
        free(json_string);
        return NULL;
    }
    
    PyObject* json_str_obj = PyUnicode_FromString(json_string);
    free(json_string);
    
    if (!json_str_obj) {
        Py_DECREF(loads_func);
        return NULL;
    }
    
    PyObject* result = PyObject_CallFunctionObjArgs(loads_func, json_str_obj, NULL);
    Py_DECREF(loads_func);
    Py_DECREF(json_str_obj);
    
    return result;
}

// Task resource functions
static PyObject* py_fhir_task_create(PyObject* self, PyObject* args) {
    const char* id = NULL;
    if (!PyArg_ParseTuple(args, "|z", &id)) {
        return NULL;
    }
    
    FHIRTask* task = fhir_task_create(id);
    if (!task) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create FHIR Task");
        return NULL;
    }
    
    // Convert to Python dictionary
    cJSON* json = fhir_task_to_json(task);
    fhir_task_free(task);
    
    if (!json) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to serialize Task to JSON");
        return NULL;
    }
    
    char* json_string = cJSON_Print(json);
    cJSON_Delete(json);
    
    if (!json_string) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to convert JSON to string");
        return NULL;
    }
    
    PyObject* json_module = PyImport_ImportModule("json");
    if (!json_module) {
        free(json_string);
        return NULL;
    }
    
    PyObject* loads_func = PyObject_GetAttrString(json_module, "loads");
    Py_DECREF(json_module);
    
    if (!loads_func) {
        free(json_string);
        return NULL;
    }
    
    PyObject* json_str_obj = PyUnicode_FromString(json_string);
    free(json_string);
    
    if (!json_str_obj) {
        Py_DECREF(loads_func);
        return NULL;
    }
    
    PyObject* result = PyObject_CallFunctionObjArgs(loads_func, json_str_obj, NULL);
    Py_DECREF(loads_func);
    Py_DECREF(json_str_obj);
    
    return result;
}