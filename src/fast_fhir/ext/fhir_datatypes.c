#include "fhir_datatypes.h"
#include <stdlib.h>
#include <string.h>
#include <regex.h>
#include <ctype.h>

// Utility functions
char* fhir_string_duplicate(const char* str) {
    if (!str) return NULL;
    size_t len = strlen(str);
    char* copy = malloc(len + 1);
    if (copy) {
        strcpy(copy, str);
    }
    return copy;
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

// Base Element functions
FHIRElement* fhir_element_create(const char* id) {
    FHIRElement* element = calloc(1, sizeof(FHIRElement));
    if (element && id) {
        element->id = fhir_string_duplicate(id);
    }
    return element;
}

void fhir_element_free(FHIRElement* element) {
    if (element) {
        fhir_string_free(element->id);
        if (element->extensions) {
            for (size_t i = 0; i < element->extension_count; i++) {
                // Free extensions (implementation depends on extension structure)
                free(element->extensions[i]);
            }
            free(element->extensions);
        }
        free(element);
    }
}

// Primitive type constructors
FHIRString* fhir_string_create(const char* value) {
    FHIRString* str = calloc(1, sizeof(FHIRString));
    if (str) {
        str->base.id = NULL;
        str->value = fhir_string_duplicate(value);
    }
    return str;
}

FHIRBoolean* fhir_boolean_create(bool value) {
    FHIRBoolean* boolean = calloc(1, sizeof(FHIRBoolean));
    if (boolean) {
        boolean->value = value;
    }
    return boolean;
}

FHIRInteger* fhir_integer_create(int value) {
    FHIRInteger* integer = calloc(1, sizeof(FHIRInteger));
    if (integer) {
        integer->value = value;
    }
    return integer;
}

FHIRDecimal* fhir_decimal_create(double value) {
    FHIRDecimal* decimal = calloc(1, sizeof(FHIRDecimal));
    if (decimal) {
        decimal->value = value;
    }
    return decimal;
}

// Complex type constructors
FHIRCoding* fhir_coding_create(const char* system, const char* code, const char* display) {
    FHIRCoding* coding = calloc(1, sizeof(FHIRCoding));
    if (coding) {
        coding->system = fhir_string_duplicate(system);
        coding->code = fhir_string_duplicate(code);
        coding->display = fhir_string_duplicate(display);
        coding->user_selected = false;
    }
    return coding;
}

FHIRCodeableConcept* fhir_codeable_concept_create(const char* text) {
    FHIRCodeableConcept* concept = calloc(1, sizeof(FHIRCodeableConcept));
    if (concept) {
        concept->text = fhir_string_duplicate(text);
        concept->coding = NULL;
        concept->coding_count = 0;
    }
    return concept;
}

FHIRQuantity* fhir_quantity_create(double value, const char* unit, const char* system, const char* code) {
    FHIRQuantity* quantity = calloc(1, sizeof(FHIRQuantity));
    if (quantity) {
        quantity->value = value;
        quantity->unit = fhir_string_duplicate(unit);
        quantity->system = fhir_string_duplicate(system);
        quantity->code = fhir_string_duplicate(code);
    }
    return quantity;
}

FHIRIdentifier* fhir_identifier_create(const char* system, const char* value) {
    FHIRIdentifier* identifier = calloc(1, sizeof(FHIRIdentifier));
    if (identifier) {
        identifier->system = fhir_string_duplicate(system);
        identifier->value = fhir_string_duplicate(value);
    }
    return identifier;
}

FHIRReference* fhir_reference_create(const char* reference, const char* display) {
    FHIRReference* ref = calloc(1, sizeof(FHIRReference));
    if (ref) {
        ref->reference = fhir_string_duplicate(reference);
        ref->display = fhir_string_duplicate(display);
    }
    return ref;
}

// JSON parsing functions
FHIRElement* fhir_parse_element(cJSON* json) {
    if (!json) return NULL;
    
    cJSON* id_item = cJSON_GetObjectItemCaseSensitive(json, "id");
    const char* id = cJSON_IsString(id_item) ? id_item->valuestring : NULL;
    
    return fhir_element_create(id);
}

FHIRString* fhir_parse_string(cJSON* json) {
    if (!cJSON_IsString(json)) return NULL;
    return fhir_string_create(json->valuestring);
}

FHIRBoolean* fhir_parse_boolean(cJSON* json) {
    if (!cJSON_IsBool(json)) return NULL;
    return fhir_boolean_create(cJSON_IsTrue(json));
}

FHIRInteger* fhir_parse_integer(cJSON* json) {
    if (!cJSON_IsNumber(json)) return NULL;
    return fhir_integer_create((int)json->valuedouble);
}

FHIRDecimal* fhir_parse_decimal(cJSON* json) {
    if (!cJSON_IsNumber(json)) return NULL;
    return fhir_decimal_create(json->valuedouble);
}

FHIRCoding* fhir_parse_coding(cJSON* json) {
    if (!cJSON_IsObject(json)) return NULL;
    
    cJSON* system = cJSON_GetObjectItemCaseSensitive(json, "system");
    cJSON* code = cJSON_GetObjectItemCaseSensitive(json, "code");
    cJSON* display = cJSON_GetObjectItemCaseSensitive(json, "display");
    cJSON* user_selected = cJSON_GetObjectItemCaseSensitive(json, "userSelected");
    
    FHIRCoding* coding = fhir_coding_create(
        cJSON_IsString(system) ? system->valuestring : NULL,
        cJSON_IsString(code) ? code->valuestring : NULL,
        cJSON_IsString(display) ? display->valuestring : NULL
    );
    
    if (coding && cJSON_IsBool(user_selected)) {
        coding->user_selected = cJSON_IsTrue(user_selected);
    }
    
    return coding;
}

FHIRCodeableConcept* fhir_parse_codeable_concept(cJSON* json) {
    if (!cJSON_IsObject(json)) return NULL;
    
    cJSON* text = cJSON_GetObjectItemCaseSensitive(json, "text");
    cJSON* coding_array = cJSON_GetObjectItemCaseSensitive(json, "coding");
    
    FHIRCodeableConcept* concept = fhir_codeable_concept_create(
        cJSON_IsString(text) ? text->valuestring : NULL
    );
    
    if (concept && cJSON_IsArray(coding_array)) {
        int array_size = cJSON_GetArraySize(coding_array);
        if (array_size > 0) {
            concept->coding = calloc(array_size, sizeof(FHIRCoding*));
            concept->coding_count = 0;
            
            cJSON* coding_item = NULL;
            cJSON_ArrayForEach(coding_item, coding_array) {
                FHIRCoding* coding = fhir_parse_coding(coding_item);
                if (coding) {
                    concept->coding[concept->coding_count++] = coding;
                }
            }
        }
    }
    
    return concept;
}

FHIRQuantity* fhir_parse_quantity(cJSON* json) {
    if (!cJSON_IsObject(json)) return NULL;
    
    cJSON* value = cJSON_GetObjectItemCaseSensitive(json, "value");
    cJSON* unit = cJSON_GetObjectItemCaseSensitive(json, "unit");
    cJSON* system = cJSON_GetObjectItemCaseSensitive(json, "system");
    cJSON* code = cJSON_GetObjectItemCaseSensitive(json, "code");
    cJSON* comparator = cJSON_GetObjectItemCaseSensitive(json, "comparator");
    
    if (!cJSON_IsNumber(value)) return NULL;
    
    FHIRQuantity* quantity = fhir_quantity_create(
        value->valuedouble,
        cJSON_IsString(unit) ? unit->valuestring : NULL,
        cJSON_IsString(system) ? system->valuestring : NULL,
        cJSON_IsString(code) ? code->valuestring : NULL
    );
    
    if (quantity && cJSON_IsString(comparator)) {
        quantity->comparator = fhir_string_duplicate(comparator->valuestring);
    }
    
    return quantity;
}

FHIRHumanName* fhir_parse_human_name(cJSON* json) {
    if (!cJSON_IsObject(json)) return NULL;
    
    FHIRHumanName* name = calloc(1, sizeof(FHIRHumanName));
    if (!name) return NULL;
    
    cJSON* use = cJSON_GetObjectItemCaseSensitive(json, "use");
    cJSON* text = cJSON_GetObjectItemCaseSensitive(json, "text");
    cJSON* family = cJSON_GetObjectItemCaseSensitive(json, "family");
    cJSON* given = cJSON_GetObjectItemCaseSensitive(json, "given");
    cJSON* prefix = cJSON_GetObjectItemCaseSensitive(json, "prefix");
    cJSON* suffix = cJSON_GetObjectItemCaseSensitive(json, "suffix");
    
    if (cJSON_IsString(use)) {
        name->use = fhir_string_duplicate(use->valuestring);
    }
    if (cJSON_IsString(text)) {
        name->text = fhir_string_duplicate(text->valuestring);
    }
    if (cJSON_IsString(family)) {
        name->family = fhir_string_array_create(1);
        name->family[0] = fhir_string_duplicate(family->valuestring);
        name->family_count = 1;
    }
    
    // Parse given names array
    if (cJSON_IsArray(given)) {
        int array_size = cJSON_GetArraySize(given);
        if (array_size > 0) {
            name->given = fhir_string_array_create(array_size);
            name->given_count = 0;
            
            cJSON* given_item = NULL;
            cJSON_ArrayForEach(given_item, given) {
                if (cJSON_IsString(given_item)) {
                    name->given[name->given_count++] = fhir_string_duplicate(given_item->valuestring);
                }
            }
        }
    }
    
    return name;
}

// JSON serialization functions
cJSON* fhir_string_to_json(const FHIRString* str) {
    if (!str || !str->value) return NULL;
    return cJSON_CreateString(str->value);
}

cJSON* fhir_boolean_to_json(const FHIRBoolean* boolean) {
    if (!boolean) return NULL;
    return cJSON_CreateBool(boolean->value);
}

cJSON* fhir_integer_to_json(const FHIRInteger* integer) {
    if (!integer) return NULL;
    return cJSON_CreateNumber(integer->value);
}

cJSON* fhir_decimal_to_json(const FHIRDecimal* decimal) {
    if (!decimal) return NULL;
    return cJSON_CreateNumber(decimal->value);
}

cJSON* fhir_coding_to_json(const FHIRCoding* coding) {
    if (!coding) return NULL;
    
    cJSON* json = cJSON_CreateObject();
    if (!json) return NULL;
    
    if (coding->system) {
        cJSON_AddStringToObject(json, "system", coding->system);
    }
    if (coding->version) {
        cJSON_AddStringToObject(json, "version", coding->version);
    }
    if (coding->code) {
        cJSON_AddStringToObject(json, "code", coding->code);
    }
    if (coding->display) {
        cJSON_AddStringToObject(json, "display", coding->display);
    }
    if (coding->user_selected) {
        cJSON_AddBoolToObject(json, "userSelected", coding->user_selected);
    }
    
    return json;
}

cJSON* fhir_codeable_concept_to_json(const FHIRCodeableConcept* concept) {
    if (!concept) return NULL;
    
    cJSON* json = cJSON_CreateObject();
    if (!json) return NULL;
    
    if (concept->coding && concept->coding_count > 0) {
        cJSON* coding_array = cJSON_CreateArray();
        for (size_t i = 0; i < concept->coding_count; i++) {
            cJSON* coding_json = fhir_coding_to_json(concept->coding[i]);
            if (coding_json) {
                cJSON_AddItemToArray(coding_array, coding_json);
            }
        }
        cJSON_AddItemToObject(json, "coding", coding_array);
    }
    
    if (concept->text) {
        cJSON_AddStringToObject(json, "text", concept->text);
    }
    
    return json;
}

cJSON* fhir_quantity_to_json(const FHIRQuantity* quantity) {
    if (!quantity) return NULL;
    
    cJSON* json = cJSON_CreateObject();
    if (!json) return NULL;
    
    cJSON_AddNumberToObject(json, "value", quantity->value);
    
    if (quantity->comparator) {
        cJSON_AddStringToObject(json, "comparator", quantity->comparator);
    }
    if (quantity->unit) {
        cJSON_AddStringToObject(json, "unit", quantity->unit);
    }
    if (quantity->system) {
        cJSON_AddStringToObject(json, "system", quantity->system);
    }
    if (quantity->code) {
        cJSON_AddStringToObject(json, "code", quantity->code);
    }
    
    return json;
}

// Validation functions
bool fhir_validate_uri(const char* uri) {
    if (!uri) return false;
    // Basic URI validation - should contain scheme
    return strchr(uri, ':') != NULL;
}

bool fhir_validate_url(const char* url) {
    if (!url) return false;
    // Basic URL validation
    return strncmp(url, "http://", 7) == 0 || strncmp(url, "https://", 8) == 0;
}

bool fhir_validate_date(const char* date) {
    if (!date) return false;
    
    // FHIR date format: YYYY, YYYY-MM, or YYYY-MM-DD
    size_t len = strlen(date);
    if (len != 4 && len != 7 && len != 10) return false;
    
    // Check year (YYYY)
    for (int i = 0; i < 4; i++) {
        if (!isdigit(date[i])) return false;
    }
    
    if (len >= 7) {
        // Check month format (-MM)
        if (date[4] != '-') return false;
        if (!isdigit(date[5]) || !isdigit(date[6])) return false;
        int month = (date[5] - '0') * 10 + (date[6] - '0');
        if (month < 1 || month > 12) return false;
    }
    
    if (len == 10) {
        // Check day format (-DD)
        if (date[7] != '-') return false;
        if (!isdigit(date[8]) || !isdigit(date[9])) return false;
        int day = (date[8] - '0') * 10 + (date[9] - '0');
        if (day < 1 || day > 31) return false;
    }
    
    return true;
}

bool fhir_validate_time(const char* time) {
    if (!time) return false;
    
    // FHIR time format: HH:mm:ss or HH:mm:ss.fff
    size_t len = strlen(time);
    if (len < 8) return false;
    
    // Check HH:mm:ss
    if (!isdigit(time[0]) || !isdigit(time[1])) return false;
    if (time[2] != ':') return false;
    if (!isdigit(time[3]) || !isdigit(time[4])) return false;
    if (time[5] != ':') return false;
    if (!isdigit(time[6]) || !isdigit(time[7])) return false;
    
    int hour = (time[0] - '0') * 10 + (time[1] - '0');
    int minute = (time[3] - '0') * 10 + (time[4] - '0');
    int second = (time[6] - '0') * 10 + (time[7] - '0');
    
    if (hour > 23 || minute > 59 || second > 59) return false;
    
    return true;
}

bool fhir_validate_code(const char* code) {
    if (!code) return false;
    
    // FHIR code: no whitespace, at least one character
    size_t len = strlen(code);
    if (len == 0) return false;
    
    for (size_t i = 0; i < len; i++) {
        if (isspace(code[i])) return false;
    }
    
    return true;
}