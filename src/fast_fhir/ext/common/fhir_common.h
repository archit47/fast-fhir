/**
 * @file fhir_common.h
 * @brief Common utilities and helper functions for FHIR C implementation
 * @version 0.1.0
 * @date 2024-01-01
 * 
 * This header provides common utilities, error handling, and helper functions
 * used across all FHIR resource implementations.
 */

#ifndef FHIR_COMMON_H
#define FHIR_COMMON_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <cjson/cJSON.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================== */
/* Error Handling                                                             */
/* ========================================================================== */

/**
 * @brief FHIR error codes
 */
typedef enum {
    FHIR_ERROR_NONE = 0,
    FHIR_ERROR_INVALID_ARGUMENT,
    FHIR_ERROR_OUT_OF_MEMORY,
    FHIR_ERROR_INVALID_JSON,
    FHIR_ERROR_INVALID_RESOURCE_TYPE,
    FHIR_ERROR_MISSING_REQUIRED_FIELD,
    FHIR_ERROR_VALIDATION_FAILED,
    FHIR_ERROR_PARSE_FAILED,
    FHIR_ERROR_SERIALIZE_FAILED,
    FHIR_ERROR_UNKNOWN
} FHIRErrorCode;

/**
 * @brief Error information structure
 */
typedef struct {
    FHIRErrorCode code;
    char* message;
    char* field;
    int line;
    const char* file;
} FHIRError;

/**
 * @brief Get the last error that occurred
 * @return Pointer to error information or NULL if no error
 */
const FHIRError* fhir_get_last_error(void);

/**
 * @brief Set error information
 * @param code Error code
 * @param message Error message
 * @param field Field name (optional)
 * @param file Source file name
 * @param line Source line number
 */
void fhir_set_error(FHIRErrorCode code, const char* message, const char* field, 
                   const char* file, int line);

/**
 * @brief Clear the last error
 */
void fhir_clear_error(void);

/**
 * @brief Convert error code to string
 * @param code Error code
 * @return String representation of error code
 */
const char* fhir_error_code_to_string(FHIRErrorCode code);

/* Convenience macros for error handling */
#define FHIR_SET_ERROR(code, msg) fhir_set_error(code, msg, NULL, __FILE__, __LINE__)
#define FHIR_SET_FIELD_ERROR(code, msg, field) fhir_set_error(code, msg, field, __FILE__, __LINE__)

/* ========================================================================== */
/* Memory Management                                                          */
/* ========================================================================== */

/**
 * @brief Safe string duplication with error handling
 * @param str String to duplicate
 * @return Duplicated string or NULL on failure
 */
char* fhir_strdup(const char* str);

/**
 * @brief Safe memory allocation with error handling
 * @param size Number of bytes to allocate
 * @return Allocated memory or NULL on failure
 */
void* fhir_malloc(size_t size);

/**
 * @brief Safe memory reallocation with error handling
 * @param ptr Pointer to existing memory
 * @param size New size in bytes
 * @return Reallocated memory or NULL on failure
 */
void* fhir_realloc(void* ptr, size_t size);

/**
 * @brief Safe memory allocation and initialization to zero
 * @param count Number of elements
 * @param size Size of each element
 * @return Allocated and zeroed memory or NULL on failure
 */
void* fhir_calloc(size_t count, size_t size);

/**
 * @brief Safe memory deallocation
 * @param ptr Pointer to memory to free (can be NULL)
 */
void fhir_free(void* ptr);

/* ========================================================================== */
/* Array Management                                                           */
/* ========================================================================== */

/**
 * @brief Resize array with proper error handling and initialization
 * @param array Pointer to array pointer
 * @param old_size Current size
 * @param new_size New size
 * @param element_size Size of each element
 * @return true on success, false on failure
 */
bool fhir_resize_array(void** array, size_t old_size, size_t new_size, size_t element_size);

/**
 * @brief Add element to array, resizing if necessary
 * @param array Pointer to array pointer
 * @param count Pointer to current count
 * @param element Element to add
 * @param element_size Size of each element
 * @return true on success, false on failure
 */
bool fhir_array_add(void** array, size_t* count, const void* element, size_t element_size);

/**
 * @brief Remove element from array at specified index
 * @param array Pointer to array
 * @param count Pointer to current count
 * @param index Index to remove
 * @param element_size Size of each element
 * @return true on success, false on failure
 */
bool fhir_array_remove(void* array, size_t* count, size_t index, size_t element_size);

/**
 * @brief Free array of pointers, calling free function for each element
 * @param array Array to free
 * @param count Number of elements
 * @param free_func Function to free each element (can be NULL for simple free)
 */
void fhir_free_pointer_array(void** array, size_t count, void (*free_func)(void*));

/* ========================================================================== */
/* String Utilities                                                           */
/* ========================================================================== */

/**
 * @brief Safe string comparison (handles NULL pointers)
 * @param str1 First string
 * @param str2 Second string
 * @return 0 if equal, non-zero otherwise
 */
int fhir_strcmp(const char* str1, const char* str2);

/**
 * @brief Check if string is empty or NULL
 * @param str String to check
 * @return true if empty or NULL, false otherwise
 */
bool fhir_string_is_empty(const char* str);

/**
 * @brief Trim whitespace from string
 * @param str String to trim (modified in place)
 * @return Pointer to trimmed string
 */
char* fhir_string_trim(char* str);

/**
 * @brief Convert string to lowercase
 * @param str String to convert (modified in place)
 * @return Pointer to converted string
 */
char* fhir_string_to_lower(char* str);

/* ========================================================================== */
/* JSON Utilities                                                             */
/* ========================================================================== */

/**
 * @brief Safely get string value from JSON object
 * @param json JSON object
 * @param key Key to look for
 * @return String value or NULL if not found or not a string
 */
const char* fhir_json_get_string(const cJSON* json, const char* key);

/**
 * @brief Safely get boolean value from JSON object
 * @param json JSON object
 * @param key Key to look for
 * @param default_value Default value if not found
 * @return Boolean value
 */
bool fhir_json_get_bool(const cJSON* json, const char* key, bool default_value);

/**
 * @brief Safely get integer value from JSON object
 * @param json JSON object
 * @param key Key to look for
 * @param default_value Default value if not found
 * @return Integer value
 */
int fhir_json_get_int(const cJSON* json, const char* key, int default_value);

/**
 * @brief Safely get double value from JSON object
 * @param json JSON object
 * @param key Key to look for
 * @param default_value Default value if not found
 * @return Double value
 */
double fhir_json_get_double(const cJSON* json, const char* key, double default_value);

/**
 * @brief Safely add string to JSON object
 * @param json JSON object
 * @param key Key to add
 * @param value String value
 * @return true on success, false on failure
 */
bool fhir_json_add_string(cJSON* json, const char* key, const char* value);

/**
 * @brief Safely add boolean to JSON object
 * @param json JSON object
 * @param key Key to add
 * @param value Boolean value
 * @return true on success, false on failure
 */
bool fhir_json_add_bool(cJSON* json, const char* key, bool value);

/**
 * @brief Safely add integer to JSON object
 * @param json JSON object
 * @param key Key to add
 * @param value Integer value
 * @return true on success, false on failure
 */
bool fhir_json_add_int(cJSON* json, const char* key, int value);

/* ========================================================================== */
/* Validation Utilities                                                       */
/* ========================================================================== */

/**
 * @brief Validate FHIR ID format
 * @param id ID string to validate
 * @return true if valid, false otherwise
 */
bool fhir_validate_id(const char* id);

/**
 * @brief Validate FHIR URI format
 * @param uri URI string to validate
 * @return true if valid, false otherwise
 */
bool fhir_validate_uri(const char* uri);

/**
 * @brief Validate FHIR date format (YYYY-MM-DD)
 * @param date Date string to validate
 * @return true if valid, false otherwise
 */
bool fhir_validate_date(const char* date);

/**
 * @brief Validate FHIR datetime format (YYYY-MM-DDTHH:MM:SS[.sss][Z|(+|-)HH:MM])
 * @param datetime Datetime string to validate
 * @return true if valid, false otherwise
 */
bool fhir_validate_datetime(const char* datetime);

/**
 * @brief Validate FHIR code format
 * @param code Code string to validate
 * @return true if valid, false otherwise
 */
bool fhir_validate_code(const char* code);

/* ========================================================================== */
/* Resource Utilities                                                         */
/* ========================================================================== */

/**
 * @brief Initialize base resource fields
 * @param resource_type Resource type string
 * @param id Resource ID
 * @param resource_type_field Pointer to resource type field
 * @param id_field Pointer to ID field
 * @return true on success, false on failure
 */
bool fhir_init_base_resource(const char* resource_type, const char* id,
                            char** resource_type_field, char** id_field);

/**
 * @brief Free base resource fields
 * @param resource_type_field Pointer to resource type field
 * @param id_field Pointer to ID field
 */
void fhir_free_base_resource(char** resource_type_field, char** id_field);

/**
 * @brief Validate base resource fields
 * @param resource_type Resource type string
 * @param id Resource ID
 * @return true if valid, false otherwise
 */
bool fhir_validate_base_resource(const char* resource_type, const char* id);

/* ========================================================================== */
/* Debugging and Logging                                                      */
/* ========================================================================== */

/**
 * @brief Log levels
 */
typedef enum {
    FHIR_LOG_LEVEL_DEBUG = 0,
    FHIR_LOG_LEVEL_INFO,
    FHIR_LOG_LEVEL_WARN,
    FHIR_LOG_LEVEL_ERROR,
    FHIR_LOG_LEVEL_FATAL
} FHIRLogLevel;

/**
 * @brief Set logging level
 * @param level Log level
 */
void fhir_set_log_level(FHIRLogLevel level);

/**
 * @brief Log message
 * @param level Log level
 * @param file Source file
 * @param line Source line
 * @param format Format string
 * @param ... Format arguments
 */
void fhir_log(FHIRLogLevel level, const char* file, int line, const char* format, ...);

/* Convenience macros for logging */
#define FHIR_LOG_DEBUG(fmt, ...) fhir_log(FHIR_LOG_LEVEL_DEBUG, __FILE__, __LINE__, fmt, ##__VA_ARGS__)
#define FHIR_LOG_INFO(fmt, ...) fhir_log(FHIR_LOG_LEVEL_INFO, __FILE__, __LINE__, fmt, ##__VA_ARGS__)
#define FHIR_LOG_WARN(fmt, ...) fhir_log(FHIR_LOG_LEVEL_WARN, __FILE__, __LINE__, fmt, ##__VA_ARGS__)
#define FHIR_LOG_ERROR(fmt, ...) fhir_log(FHIR_LOG_LEVEL_ERROR, __FILE__, __LINE__, fmt, ##__VA_ARGS__)
#define FHIR_LOG_FATAL(fmt, ...) fhir_log(FHIR_LOG_LEVEL_FATAL, __FILE__, __LINE__, fmt, ##__VA_ARGS__)

#ifdef __cplusplus
}
#endif

#endif /* FHIR_COMMON_H */