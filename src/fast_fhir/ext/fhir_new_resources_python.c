/**
 * Python bindings for new FHIR resources C implementation
 * 
 * This file provides Python bindings for the newly implemented FHIR resources
 * using the Python C API.
 */

#include <Python.h>
#include "fhir_foundation.h"
#include "fhir_specialized.h"
#include "fhir_workflow.h"

// ============================================================================
// OrganizationAffiliation Python Bindings
// ============================================================================

static PyObject* py_organization_affiliation_create(PyObject* self, PyObject* args) {
    const char* id;
    if (!PyArg_ParseTuple(args, "s", &id)) {
        return NULL;
    }
    
    FHIROrganizationAffiliation* org_affiliation = fhir_organization_affiliation_create(id);
    if (!org_affiliation) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create OrganizationAffiliation");
        return NULL;
    }
    
    return PyCapsule_New(org_affiliation, "FHIROrganizationAffiliation", NULL);
}

static PyObject* py_organization_affiliation_validate(PyObject* self, PyObject* args) {
    PyObject* capsule;
    if (!PyArg_ParseTuple(args, "O", &capsule)) {
        return NULL;
    }
    
    FHIROrganizationAffiliation* org_affiliation = (FHIROrganizationAffiliation*)PyCapsule_GetPointer(capsule, "FHIROrganizationAffiliation");
    if (!org_affiliation) {
        PyErr_SetString(PyExc_ValueError, "Invalid OrganizationAffiliation object");
        return NULL;
    }
    
    bool is_valid = fhir_validate_organization_affiliation(org_affiliation);
    return PyBool_FromLong(is_valid);
}

// ============================================================================
// BiologicallyDerivedProduct Python Bindings
// ============================================================================

static PyObject* py_biologically_derived_product_create(PyObject* self, PyObject* args) {
    const char* id;
    if (!PyArg_ParseTuple(args, "s", &id)) {
        return NULL;
    }
    
    FHIRBiologicallyDerivedProduct* product = fhir_biologically_derived_product_create(id);
    if (!product) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create BiologicallyDerivedProduct");
        return NULL;
    }
    
    return PyCapsule_New(product, "FHIRBiologicallyDerivedProduct", NULL);
}

static PyObject* py_biologically_derived_product_validate(PyObject* self, PyObject* args) {
    PyObject* capsule;
    if (!PyArg_ParseTuple(args, "O", &capsule)) {
        return NULL;
    }
    
    FHIRBiologicallyDerivedProduct* product = (FHIRBiologicallyDerivedProduct*)PyCapsule_GetPointer(capsule, "FHIRBiologicallyDerivedProduct");
    if (!product) {
        PyErr_SetString(PyExc_ValueError, "Invalid BiologicallyDerivedProduct object");
        return NULL;
    }
    
    bool is_valid = fhir_validate_biologically_derived_product(product);
    return PyBool_FromLong(is_valid);
}

// ============================================================================
// DeviceMetric Python Bindings
// ============================================================================

static PyObject* py_device_metric_create(PyObject* self, PyObject* args) {
    const char* id;
    if (!PyArg_ParseTuple(args, "s", &id)) {
        return NULL;
    }
    
    FHIRDeviceMetric* metric = fhir_device_metric_create(id);
    if (!metric) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create DeviceMetric");
        return NULL;
    }
    
    return PyCapsule_New(metric, "FHIRDeviceMetric", NULL);
}

static PyObject* py_device_metric_validate(PyObject* self, PyObject* args) {
    PyObject* capsule;
    if (!PyArg_ParseTuple(args, "O", &capsule)) {
        return NULL;
    }
    
    FHIRDeviceMetric* metric = (FHIRDeviceMetric*)PyCapsule_GetPointer(capsule, "FHIRDeviceMetric");
    if (!metric) {
        PyErr_SetString(PyExc_ValueError, "Invalid DeviceMetric object");
        return NULL;
    }
    
    bool is_valid = fhir_validate_device_metric(metric);
    return PyBool_FromLong(is_valid);
}

// ============================================================================
// NutritionProduct Python Bindings
// ============================================================================

static PyObject* py_nutrition_product_create(PyObject* self, PyObject* args) {
    const char* id;
    if (!PyArg_ParseTuple(args, "s", &id)) {
        return NULL;
    }
    
    FHIRNutritionProduct* product = fhir_nutrition_product_create(id);
    if (!product) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create NutritionProduct");
        return NULL;
    }
    
    return PyCapsule_New(product, "FHIRNutritionProduct", NULL);
}

static PyObject* py_nutrition_product_validate(PyObject* self, PyObject* args) {
    PyObject* capsule;
    if (!PyArg_ParseTuple(args, "O", &capsule)) {
        return NULL;
    }
    
    FHIRNutritionProduct* product = (FHIRNutritionProduct*)PyCapsule_GetPointer(capsule, "FHIRNutritionProduct");
    if (!product) {
        PyErr_SetString(PyExc_ValueError, "Invalid NutritionProduct object");
        return NULL;
    }
    
    bool is_valid = fhir_validate_nutrition_product(product);
    return PyBool_FromLong(is_valid);
}

static PyObject* py_nutrition_product_is_active(PyObject* self, PyObject* args) {
    PyObject* capsule;
    if (!PyArg_ParseTuple(args, "O", &capsule)) {
        return NULL;
    }
    
    FHIRNutritionProduct* product = (FHIRNutritionProduct*)PyCapsule_GetPointer(capsule, "FHIRNutritionProduct");
    if (!product) {
        PyErr_SetString(PyExc_ValueError, "Invalid NutritionProduct object");
        return NULL;
    }
    
    bool is_active = fhir_is_active_nutrition_product(product);
    return PyBool_FromLong(is_active);
}

// ============================================================================
// Transport Python Bindings
// ============================================================================

static PyObject* py_transport_create(PyObject* self, PyObject* args) {
    const char* id;
    if (!PyArg_ParseTuple(args, "s", &id)) {
        return NULL;
    }
    
    FHIRTransport* transport = fhir_transport_create(id);
    if (!transport) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create Transport");
        return NULL;
    }
    
    return PyCapsule_New(transport, "FHIRTransport", NULL);
}

static PyObject* py_transport_validate(PyObject* self, PyObject* args) {
    PyObject* capsule;
    if (!PyArg_ParseTuple(args, "O", &capsule)) {
        return NULL;
    }
    
    FHIRTransport* transport = (FHIRTransport*)PyCapsule_GetPointer(capsule, "FHIRTransport");
    if (!transport) {
        PyErr_SetString(PyExc_ValueError, "Invalid Transport object");
        return NULL;
    }
    
    bool is_valid = fhir_validate_transport(transport);
    return PyBool_FromLong(is_valid);
}

// ============================================================================
// VerificationResult Python Bindings
// ============================================================================

static PyObject* py_verification_result_create(PyObject* self, PyObject* args) {
    const char* id;
    if (!PyArg_ParseTuple(args, "s", &id)) {
        return NULL;
    }
    
    FHIRVerificationResult* result = fhir_verification_result_create(id);
    if (!result) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create VerificationResult");
        return NULL;
    }
    
    return PyCapsule_New(result, "FHIRVerificationResult", NULL);
}

static PyObject* py_verification_result_validate(PyObject* self, PyObject* args) {
    PyObject* capsule;
    if (!PyArg_ParseTuple(args, "O", &capsule)) {
        return NULL;
    }
    
    FHIRVerificationResult* result = (FHIRVerificationResult*)PyCapsule_GetPointer(capsule, "FHIRVerificationResult");
    if (!result) {
        PyErr_SetString(PyExc_ValueError, "Invalid VerificationResult object");
        return NULL;
    }
    
    bool is_valid = fhir_validate_verification_result(result);
    return PyBool_FromLong(is_valid);
}

static PyObject* py_verification_result_is_validated(PyObject* self, PyObject* args) {
    PyObject* capsule;
    if (!PyArg_ParseTuple(args, "O", &capsule)) {
        return NULL;
    }
    
    FHIRVerificationResult* result = (FHIRVerificationResult*)PyCapsule_GetPointer(capsule, "FHIRVerificationResult");
    if (!result) {
        PyErr_SetString(PyExc_ValueError, "Invalid VerificationResult object");
        return NULL;
    }
    
    bool is_validated = fhir_is_validated_verification_result(result);
    return PyBool_FromLong(is_validated);
}

// ============================================================================
// EncounterHistory Python Bindings
// ============================================================================

static PyObject* py_encounter_history_create(PyObject* self, PyObject* args) {
    const char* id;
    if (!PyArg_ParseTuple(args, "s", &id)) {
        return NULL;
    }
    
    FHIREncounterHistory* history = fhir_encounter_history_create(id);
    if (!history) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create EncounterHistory");
        return NULL;
    }
    
    return PyCapsule_New(history, "FHIREncounterHistory", NULL);
}

static PyObject* py_encounter_history_validate(PyObject* self, PyObject* args) {
    PyObject* capsule;
    if (!PyArg_ParseTuple(args, "O", &capsule)) {
        return NULL;
    }
    
    FHIREncounterHistory* history = (FHIREncounterHistory*)PyCapsule_GetPointer(capsule, "FHIREncounterHistory");
    if (!history) {
        PyErr_SetString(PyExc_ValueError, "Invalid EncounterHistory object");
        return NULL;
    }
    
    bool is_valid = fhir_validate_encounter_history(history);
    return PyBool_FromLong(is_valid);
}

// ============================================================================
// EpisodeOfCare Python Bindings
// ============================================================================

static PyObject* py_episode_of_care_create(PyObject* self, PyObject* args) {
    const char* id;
    if (!PyArg_ParseTuple(args, "s", &id)) {
        return NULL;
    }
    
    FHIREpisodeOfCare* episode = fhir_episode_of_care_create(id);
    if (!episode) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create EpisodeOfCare");
        return NULL;
    }
    
    return PyCapsule_New(episode, "FHIREpisodeOfCare", NULL);
}

static PyObject* py_episode_of_care_validate(PyObject* self, PyObject* args) {
    PyObject* capsule;
    if (!PyArg_ParseTuple(args, "O", &capsule)) {
        return NULL;
    }
    
    FHIREpisodeOfCare* episode = (FHIREpisodeOfCare*)PyCapsule_GetPointer(capsule, "FHIREpisodeOfCare");
    if (!episode) {
        PyErr_SetString(PyExc_ValueError, "Invalid EpisodeOfCare object");
        return NULL;
    }
    
    bool is_valid = fhir_validate_episode_of_care(episode);
    return PyBool_FromLong(is_valid);
}

// ============================================================================
// Method Definitions
// ============================================================================

static PyMethodDef FHIRNewResourcesMethods[] = {
    // OrganizationAffiliation methods
    {"organization_affiliation_create", py_organization_affiliation_create, METH_VARARGS, "Create OrganizationAffiliation"},
    {"organization_affiliation_validate", py_organization_affiliation_validate, METH_VARARGS, "Validate OrganizationAffiliation"},
    
    // BiologicallyDerivedProduct methods
    {"biologically_derived_product_create", py_biologically_derived_product_create, METH_VARARGS, "Create BiologicallyDerivedProduct"},
    {"biologically_derived_product_validate", py_biologically_derived_product_validate, METH_VARARGS, "Validate BiologicallyDerivedProduct"},
    
    // DeviceMetric methods
    {"device_metric_create", py_device_metric_create, METH_VARARGS, "Create DeviceMetric"},
    {"device_metric_validate", py_device_metric_validate, METH_VARARGS, "Validate DeviceMetric"},
    
    // NutritionProduct methods
    {"nutrition_product_create", py_nutrition_product_create, METH_VARARGS, "Create NutritionProduct"},
    {"nutrition_product_validate", py_nutrition_product_validate, METH_VARARGS, "Validate NutritionProduct"},
    {"nutrition_product_is_active", py_nutrition_product_is_active, METH_VARARGS, "Check if NutritionProduct is active"},
    
    // Transport methods
    {"transport_create", py_transport_create, METH_VARARGS, "Create Transport"},
    {"transport_validate", py_transport_validate, METH_VARARGS, "Validate Transport"},
    
    // VerificationResult methods
    {"verification_result_create", py_verification_result_create, METH_VARARGS, "Create VerificationResult"},
    {"verification_result_validate", py_verification_result_validate, METH_VARARGS, "Validate VerificationResult"},
    {"verification_result_is_validated", py_verification_result_is_validated, METH_VARARGS, "Check if VerificationResult is validated"},
    
    // EncounterHistory methods
    {"encounter_history_create", py_encounter_history_create, METH_VARARGS, "Create EncounterHistory"},
    {"encounter_history_validate", py_encounter_history_validate, METH_VARARGS, "Validate EncounterHistory"},
    
    // EpisodeOfCare methods
    {"episode_of_care_create", py_episode_of_care_create, METH_VARARGS, "Create EpisodeOfCare"},
    {"episode_of_care_validate", py_episode_of_care_validate, METH_VARARGS, "Validate EpisodeOfCare"},
    
    {NULL, NULL, 0, NULL}  // Sentinel
};

// ============================================================================
// Module Definition
// ============================================================================

static struct PyModuleDef fhir_new_resources_module = {
    PyModuleDef_HEAD_INIT,
    "fhir_new_resources_c",
    "FHIR New Resources C Extension Module",
    -1,
    FHIRNewResourcesMethods
};

PyMODINIT_FUNC PyInit_fhir_new_resources_c(void) {
    PyObject* module = PyModule_Create(&fhir_new_resources_module);
    if (module == NULL) {
        return NULL;
    }
    
    // Add module constants
    PyModule_AddStringConstant(module, "__version__", "0.1.0");
    PyModule_AddStringConstant(module, "__author__", "FHIR Implementation Team");
    
    return module;
}