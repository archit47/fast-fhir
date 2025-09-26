/**
 * @file fhir_common.c
 * @brief Common utilities and helper functions for FHIR C implementation
 * @version 1.0.0
 * @date 2024-01-01
 * 
 * Implementation of common utilities, error handling, and helper functions
 * used across all FHIR resource implementations.
 */

#include "fhir_common.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdarg.h>
#include <ctype.h>
#include <errno.h>
#include <regex.h>

/* ========================================================================== */
/* Global Variables                                                           */
/* ========================================================================== */

static FHIRError g_last_error = {0};
static FHIRLogLevel g_log_level = FHIR_LOG_LEVEL_INFO;

/* ========================================================================== */
/* Error Handling Implementation                                              */
/* ========================================================================== */

const FHIRError* fhir_get_last_error(void) {
    return g_last_error.code != FHIR_ERROR_NONE ? &g_last_error : NULL;
}

void fhir_set_error(FHIRErrorCode code, const char* message, const char* field, 
                   const char* file, int line) {
    // Clear previous error
    fhir_clear_error();
    
    g_last_error.code = code;
    
    if (message) {
        g_last_error.message = fhir_strdup(message);
    }
    
    if (field) {
        g_last_error.field = fhir_strdup(field);
    }
    
    g_last_error.file = file;
    g_last_error.line = line;
}

void fhir_clear_error(void) {
    free(g_last_error.message);
    free(g_last_error.field);
    memset(&g_last_error, 0, sizeof(FHIRError));
}

const char* fhir_error_code_to_string(FHIRErrorCode code) {
    switch (code) {
        case FHIR_ERROR_NONE: return "No error";
        case FHIR_ERROR_INVALID_ARGUMENT: return "Invalid argument";
        case FHIR_ERROR_OUT_OF_MEMORY: return "Out of memory";
        case FHIR_ERROR_INVALID_JSON: return "Invalid JSON";
        case FHIR_ERROR_INVALID_RESOURCE_TYPE: return "Invalid resource type";
        case FHIR_ERROR_MISSING_REQUIRED_FIELD: return "Missing required field";
        case FHIR_ERROR_VALIDATION_FAILED: return "Validation failed";
        case FHIR_ERROR_PARSE_FAILED: return "Parse failed";
        case FHIR_ERROR_SERIALIZE_FAILED: return "Serialize failed";
        case FHIR_ERROR_UNKNOWN: return "Unknown error";
        default: return "Invalid error code";
    }
}

/* ========================================================================== */
/* Memory Management Implementation                                           */
/* ========================================================================== */

char* fhir_strdup(const char* str) {
    if (!str) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "String is NULL");
        return NULL;
    }
    
    size_t len = strlen(str) + 1;
    char* dup = malloc(len);
    if (!dup) {
        FHIR_SET_ERROR(FHIR_ERROR_OUT_OF_MEMORY, "Failed to allocate memory for string");
        return NULL;
    }
    
    memcpy(dup, str, len);
    return dup;
}

void* fhir_malloc(size_t size) {
    if (size == 0) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Size is zero");
        return NULL;
    }
    
    void* ptr = malloc(size);
    if (!ptr) {
        FHIR_SET_ERROR(FHIR_ERROR_OUT_OF_MEMORY, "Failed to allocate memory");
    }
    
    return ptr;
}

void* fhir_realloc(void* ptr, size_t size) {
    if (size == 0) {
        free(ptr);
        return NULL;
    }
    
    void* new_ptr = realloc(ptr, size);
    if (!new_ptr) {
        FHIR_SET_ERROR(FHIR_ERROR_OUT_OF_MEMORY, "Failed to reallocate memory");
    }
    
    return new_ptr;
}

void* fhir_calloc(size_t count, size_t size) {
    if (count == 0 || size == 0) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Count or size is zero");
        return NULL;
    }
    
    void* ptr = calloc(count, size);
    if (!ptr) {
        FHIR_SET_ERROR(FHIR_ERROR_OUT_OF_MEMORY, "Failed to allocate memory");
    }
    
    return ptr;
}

void fhir_free(void* ptr) {
    free(ptr);
}

/* ========================================================================== */
/* Array Management Implementation                                            */
/* ========================================================================== */

bool fhir_resize_array(void** array, size_t old_size, size_t new_size, size_t element_size) {
    if (!array) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Array pointer is NULL");
        return false;
    }
    
    if (element_size == 0) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Element size is zero");
        return false;
    }
    
    if (new_size == 0) {
        free(*array);
        *array = NULL;
        return true;
    }
    
    void* new_array = fhir_realloc(*array, new_size * element_size);
    if (!new_array) {
        return false;
    }
    
    *array = new_array;
    
    // Initialize new elements to zero
    if (new_size > old_size) {
        memset((char*)*array + (old_size * element_size), 0, 
               (new_size - old_size) * element_size);
    }
    
    return true;
}

bool fhir_array_add(void** array, size_t* count, const void* element, size_t element_size) {
    if (!array || !count || !element) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return false;
    }
    
    if (!fhir_resize_array(array, *count, *count + 1, element_size)) {
        return false;
    }
    
    memcpy((char*)*array + (*count * element_size), element, element_size);
    (*count)++;
    
    return true;
}

bool fhir_array_remove(void* array, size_t* count, size_t index, size_t element_size) {
    if (!array || !count || index >= *count) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return false;
    }
    
    // Move elements after the removed index
    if (index < *count - 1) {
        memmove((char*)array + (index * element_size),
                (char*)array + ((index + 1) * element_size),
                (*count - index - 1) * element_size);
    }
    
    (*count)--;
    return true;
}

void fhir_free_pointer_array(void** array, size_t count, void (*free_func)(void*)) {
    if (!array) return;
    
    for (size_t i = 0; i < count; i++) {
        if (array[i]) {
            if (free_func) {
                free_func(array[i]);
            } else {
                free(array[i]);
            }
        }
    }
    
    free(array);
}

/* ========================================================================== */
/* String Utilities Implementation                                            */
/* ========================================================================== */

int fhir_strcmp(const char* str1, const char* str2) {
    if (str1 == str2) return 0;
    if (!str1) return -1;
    if (!str2) return 1;
    return strcmp(str1, str2);
}

bool fhir_string_is_empty(const char* str) {
    return !str || strlen(str) == 0;
}

char* fhir_string_trim(char* str) {
    if (!str) return NULL;
    
    // Trim leading whitespace
    while (isspace((unsigned char)*str)) str++;
    
    if (*str == 0) return str;
    
    // Trim trailing whitespace
    char* end = str + strlen(str) - 1;
    while (end > str && isspace((unsigned char)*end)) end--;
    
    end[1] = '\0';
    return str;
}

char* fhir_string_to_lower(char* str) {
    if (!str) return NULL;
    
    for (char* p = str; *p; p++) {
        *p = tolower((unsigned char)*p);
    }
    
    return str;
}

/* ========================================================================== */
/* JSON Utilities Implementation                                              */
/* ========================================================================== */

const char* fhir_json_get_string(const cJSON* json, const char* key) {
    if (!json || !key) return NULL;
    
    cJSON* item = cJSON_GetObjectItem(json, key);
    if (!item || !cJSON_IsString(item)) return NULL;
    
    return item->valuestring;
}

bool fhir_json_get_bool(const cJSON* json, const char* key, bool default_value) {
    if (!json || !key) return default_value;
    
    cJSON* item = cJSON_GetObjectItem(json, key);
    if (!item || !cJSON_IsBool(item)) return default_value;
    
    return cJSON_IsTrue(item);
}

int fhir_json_get_int(const cJSON* json, const char* key, int default_value) {
    if (!json || !key) return default_value;
    
    cJSON* item = cJSON_GetObjectItem(json, key);
    if (!item || !cJSON_IsNumber(item)) return default_value;
    
    return item->valueint;
}

double fhir_json_get_double(const cJSON* json, const char* key, double default_value) {
    if (!json || !key) return default_value;
    
    cJSON* item = cJSON_GetObjectItem(json, key);
    if (!item || !cJSON_IsNumber(item)) return default_value;
    
    return item->valuedouble;
}

bool fhir_json_add_string(cJSON* json, const char* key, const char* value) {
    if (!json || !key || !value) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return false;
    }
    
    return cJSON_AddStringToObject(json, key, value) != NULL;
}

bool fhir_json_add_bool(cJSON* json, const char* key, bool value) {
    if (!json || !key) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return false;
    }
    
    return cJSON_AddBoolToObject(json, key, value) != NULL;
}

bool fhir_json_add_int(cJSON* json, const char* key, int value) {
    if (!json || !key) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return false;
    }
    
    return cJSON_AddNumberToObject(json, key, value) != NULL;
}

/* ========================================================================== */
/* Validation Utilities Implementation                                        */
/* ========================================================================== */

bool fhir_validate_id(const char* id) {
    if (fhir_string_is_empty(id)) return false;
    
    // FHIR ID regex: [A-Za-z0-9\-\.]{1,64}
    regex_t regex;
    int result = regcomp(&regex, "^[A-Za-z0-9\\-\\.]{1,64}$", REG_EXTENDED);
    if (result != 0) return false;
    
    result = regexec(&regex, id, 0, NULL, 0);
    regfree(&regex);
    
    return result == 0;
}

bool fhir_validate_uri(const char* uri) {
    if (fhir_string_is_empty(uri)) return false;
    
    // Basic URI validation - can be enhanced
    return strlen(uri) > 0 && strlen(uri) <= 4096;
}

bool fhir_validate_date(const char* date) {
    if (fhir_string_is_empty(date)) return false;
    
    // FHIR date regex: YYYY-MM-DD
    regex_t regex;
    int result = regcomp(&regex, "^[0-9]{4}-[0-9]{2}-[0-9]{2}$", REG_EXTENDED);
    if (result != 0) return false;
    
    result = regexec(&regex, date, 0, NULL, 0);
    regfree(&regex);
    
    return result == 0;
}

bool fhir_validate_datetime(const char* datetime) {
    if (fhir_string_is_empty(datetime)) return false;
    
    // FHIR datetime regex (simplified)
    regex_t regex;
    int result = regcomp(&regex, "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}", REG_EXTENDED);
    if (result != 0) return false;
    
    result = regexec(&regex, datetime, 0, NULL, 0);
    regfree(&regex);
    
    return result == 0;
}

bool fhir_validate_code(const char* code) {
    if (fhir_string_is_empty(code)) return false;
    
    // FHIR code regex: [^\s]+(\s[^\s]+)*
    regex_t regex;
    int result = regcomp(&regex, "^[^\\s]+(\\s[^\\s]+)*$", REG_EXTENDED);
    if (result != 0) return false;
    
    result = regexec(&regex, code, 0, NULL, 0);
    regfree(&regex);
    
    return result == 0;
}

/* ========================================================================== */
/* Resource Utilities Implementation                                          */
/* ========================================================================== */

bool fhir_init_base_resource(const char* resource_type, const char* id,
                            char** resource_type_field, char** id_field) {
    if (!resource_type || !id || !resource_type_field || !id_field) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return false;
    }
    
    if (!fhir_validate_id(id)) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_VALIDATION_FAILED, "Invalid ID format", "id");
        return false;
    }
    
    *resource_type_field = fhir_strdup(resource_type);
    if (!*resource_type_field) {
        return false;
    }
    
    *id_field = fhir_strdup(id);
    if (!*id_field) {
        free(*resource_type_field);
        *resource_type_field = NULL;
        return false;
    }
    
    return true;
}

void fhir_free_base_resource(char** resource_type_field, char** id_field) {
    if (resource_type_field) {
        free(*resource_type_field);
        *resource_type_field = NULL;
    }
    
    if (id_field) {
        free(*id_field);
        *id_field = NULL;
    }
}

bool fhir_validate_base_resource(const char* resource_type, const char* id) {
    if (fhir_string_is_empty(resource_type)) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_MISSING_REQUIRED_FIELD, "Resource type is required", "resourceType");
        return false;
    }
    
    if (fhir_string_is_empty(id)) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_MISSING_REQUIRED_FIELD, "ID is required", "id");
        return false;
    }
    
    if (!fhir_validate_id(id)) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_VALIDATION_FAILED, "Invalid ID format", "id");
        return false;
    }
    
    return true;
}

/* ========================================================================== */
/* Debugging and Logging Implementation                                       */
/* ========================================================================== */

void fhir_set_log_level(FHIRLogLevel level) {
    g_log_level = level;
}

void fhir_log(FHIRLogLevel level, const char* file, int line, const char* format, ...) {
    if (level < g_log_level) return;
    
    const char* level_strings[] = {"DEBUG", "INFO", "WARN", "ERROR", "FATAL"};
    const char* level_str = (level >= 0 && level <= FHIR_LOG_LEVEL_FATAL) ? 
                           level_strings[level] : "UNKNOWN";
    
    fprintf(stderr, "[%s] %s:%d - ", level_str, file ? file : "unknown", line);
    
    va_list args;
    va_start(args, format);
    vfprintf(stderr, format, args);
    va_end(args);
    
    fprintf(stderr, "\n");
    fflush(stderr);
}