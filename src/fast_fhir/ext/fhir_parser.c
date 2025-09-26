#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <string.h>
#include <cjson/cJSON.h>

// Fast JSON validation for FHIR resources
static PyObject* validate_fhir_json(PyObject* self, PyObject* args) {
    const char* json_string;
    if (!PyArg_ParseTuple(args, "s", &json_string)) {
        return NULL;
    }
    
    cJSON* json = cJSON_Parse(json_string);
    if (json == NULL) {
        PyErr_SetString(PyExc_ValueError, "Invalid JSON");
        return NULL;
    }
    
    // Check for required FHIR fields
    cJSON* resource_type = cJSON_GetObjectItemCaseSensitive(json, "resourceType");
    if (!cJSON_IsString(resource_type) || (resource_type->valuestring == NULL)) {
        cJSON_Delete(json);
        PyErr_SetString(PyExc_ValueError, "Missing or invalid resourceType");
        return NULL;
    }
    
    cJSON_Delete(json);
    Py_RETURN_TRUE;
}

// Fast resource type extraction
static PyObject* extract_resource_type(PyObject* self, PyObject* args) {
    const char* json_string;
    if (!PyArg_ParseTuple(args, "s", &json_string)) {
        return NULL;
    }
    
    cJSON* json = cJSON_Parse(json_string);
    if (json == NULL) {
        PyErr_SetString(PyExc_ValueError, "Invalid JSON");
        return NULL;
    }
    
    cJSON* resource_type = cJSON_GetObjectItemCaseSensitive(json, "resourceType");
    if (!cJSON_IsString(resource_type) || (resource_type->valuestring == NULL)) {
        cJSON_Delete(json);
        Py_RETURN_NONE;
    }
    
    PyObject* result = PyUnicode_FromString(resource_type->valuestring);
    cJSON_Delete(json);
    return result;
}

// Fast bundle entry count
static PyObject* count_bundle_entries(PyObject* self, PyObject* args) {
    const char* json_string;
    if (!PyArg_ParseTuple(args, "s", &json_string)) {
        return NULL;
    }
    
    cJSON* json = cJSON_Parse(json_string);
    if (json == NULL) {
        PyErr_SetString(PyExc_ValueError, "Invalid JSON");
        return NULL;
    }
    
    cJSON* entry = cJSON_GetObjectItemCaseSensitive(json, "entry");
    int count = 0;
    
    if (cJSON_IsArray(entry)) {
        count = cJSON_GetArraySize(entry);
    }
    
    cJSON_Delete(json);
    return PyLong_FromLong(count);
}

// Fast field extraction for common FHIR fields
static PyObject* extract_field(PyObject* self, PyObject* args) {
    const char* json_string;
    const char* field_name;
    
    if (!PyArg_ParseTuple(args, "ss", &json_string, &field_name)) {
        return NULL;
    }
    
    cJSON* json = cJSON_Parse(json_string);
    if (json == NULL) {
        PyErr_SetString(PyExc_ValueError, "Invalid JSON");
        return NULL;
    }
    
    cJSON* field = cJSON_GetObjectItemCaseSensitive(json, field_name);
    PyObject* result = Py_None;
    Py_INCREF(result);
    
    if (field != NULL) {
        if (cJSON_IsString(field) && (field->valuestring != NULL)) {
            result = PyUnicode_FromString(field->valuestring);
            Py_DECREF(Py_None);
        } else if (cJSON_IsBool(field)) {
            result = cJSON_IsTrue(field) ? Py_True : Py_False;
            Py_INCREF(result);
            Py_DECREF(Py_None);
        } else if (cJSON_IsNumber(field)) {
            if (field->valuedouble == (int)field->valuedouble) {
                result = PyLong_FromLong((long)field->valuedouble);
            } else {
                result = PyFloat_FromDouble(field->valuedouble);
            }
            Py_DECREF(Py_None);
        }
    }
    
    cJSON_Delete(json);
    return result;
}

// Method definitions
static PyMethodDef FHIRParserMethods[] = {
    {"validate_fhir_json", validate_fhir_json, METH_VARARGS, "Validate FHIR JSON structure"},
    {"extract_resource_type", extract_resource_type, METH_VARARGS, "Extract resourceType from JSON"},
    {"count_bundle_entries", count_bundle_entries, METH_VARARGS, "Count entries in FHIR Bundle"},
    {"extract_field", extract_field, METH_VARARGS, "Extract field value from JSON"},
    {NULL, NULL, 0, NULL}
};

// Module definition
static struct PyModuleDef fhir_parser_module = {
    PyModuleDef_HEAD_INIT,
    "fhir_parser_c",
    "Fast FHIR parsing utilities in C",
    -1,
    FHIRParserMethods
};

// Module initialization
PyMODINIT_FUNC PyInit_fhir_parser_c(void) {
    return PyModule_Create(&fhir_parser_module);
}