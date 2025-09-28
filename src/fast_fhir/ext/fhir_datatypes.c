#include "fhir_datatypes.h"
#include <stdlib.h>
#include <string.h>

// Utility functions
char* fhir_string_duplicate(const char* str) {
    if (!str) return NULL;
    size_t len = strlen(str);
    char* dup = malloc(len + 1);
    if (dup) {
        strcpy(dup, str);
    }
    return dup;
}

void fhir_string_free(char* str) {
    if (str) {
        free(str);
    }
}

char** fhir_string_array_create(size_t size) {
    return calloc(size, sizeof(char*));
}

void fhir_string_array_free(char** array, size_t size) {
    if (array) {
        for (size_t i = 0; i < size; i++) {
            fhir_string_free(array[i]);
        }
        free(array);
    }
}

// FHIR typed string utility functions
void fhir_uri_free(FHIRUri* uri) {
    if (uri) {
        free(uri);
    }
}

void fhir_code_free(FHIRCode* code) {
    if (code) {
        free(code);
    }
}

void fhir_markdown_free(FHIRMarkdown* markdown) {
    if (markdown) {
        free(markdown);
    }
}

void fhir_datetime_free(FHIRDateTime* datetime) {
    if (datetime) {
        free(datetime);
    }
}

void fhir_instant_free(FHIRInstant* instant) {
    if (instant) {
        free(instant);
    }
}

void fhir_canonical_free(FHIRCanonical* canonical) {
    if (canonical) {
        free(canonical);
    }
}

void fhir_base64binary_free(FHIRBase64Binary* binary) {
    if (binary) {
        free(binary);
    }
}