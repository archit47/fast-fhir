/**
 * @file test_common.c
 * @brief Unit tests for common FHIR utilities
 * @version 0.1.0
 * @date 2024-01-01
 */

#include "test_framework.h"
#include "../common/fhir_common.h"
#include <string.h>

/* ========================================================================== */
/* Error Handling Tests                                                       */
/* ========================================================================== */

bool test_error_handling_basic(void) {
    // Clear any existing error
    fhir_clear_error();
    
    // Initially no error
    ASSERT_NULL(fhir_get_last_error());
    
    // Set an error
    fhir_set_error(FHIR_ERROR_INVALID_ARGUMENT, "Test error", "test_field", __FILE__, __LINE__);
    
    // Check error was set
    const FHIRError* error = fhir_get_last_error();
    ASSERT_NOT_NULL(error);
    ASSERT_EQ(FHIR_ERROR_INVALID_ARGUMENT, error->code);
    ASSERT_STR_EQ("Test error", error->message);
    ASSERT_STR_EQ("test_field", error->field);
    
    // Clear error
    fhir_clear_error();
    ASSERT_NULL(fhir_get_last_error());
    
    return true;
}

bool test_error_code_to_string(void) {
    ASSERT_STR_EQ("No error", fhir_error_code_to_string(FHIR_ERROR_NONE));
    ASSERT_STR_EQ("Invalid argument", fhir_error_code_to_string(FHIR_ERROR_INVALID_ARGUMENT));
    ASSERT_STR_EQ("Out of memory", fhir_error_code_to_string(FHIR_ERROR_OUT_OF_MEMORY));
    ASSERT_STR_EQ("Invalid JSON", fhir_error_code_to_string(FHIR_ERROR_INVALID_JSON));
    
    return true;
}

/* ========================================================================== */
/* Memory Management Tests                                                    */
/* ========================================================================== */

bool test_fhir_strdup(void) {
    // Test normal string duplication
    char* dup = fhir_strdup("test string");
    ASSERT_NOT_NULL(dup);
    ASSERT_STR_EQ("test string", dup);
    free(dup);
    
    // Test empty string
    dup = fhir_strdup("");
    ASSERT_NOT_NULL(dup);
    ASSERT_STR_EQ("", dup);
    free(dup);
    
    // Test NULL input
    dup = fhir_strdup(NULL);
    ASSERT_NULL(dup);
    
    return true;
}

bool test_fhir_malloc(void) {
    // Test normal allocation
    void* ptr = fhir_malloc(100);
    ASSERT_NOT_NULL(ptr);
    free(ptr);
    
    // Test zero allocation
    ptr = fhir_malloc(0);
    ASSERT_NULL(ptr);
    
    return true;
}

bool test_fhir_calloc(void) {
    // Test normal allocation
    int* ptr = (int*)fhir_calloc(10, sizeof(int));
    ASSERT_NOT_NULL(ptr);
    
    // Check that memory is zeroed
    for (int i = 0; i < 10; i++) {
        ASSERT_EQ(0, ptr[i]);
    }
    
    free(ptr);
    
    // Test zero count
    ptr = (int*)fhir_calloc(0, sizeof(int));
    ASSERT_NULL(ptr);
    
    // Test zero size
    ptr = (int*)fhir_calloc(10, 0);
    ASSERT_NULL(ptr);
    
    return true;
}

/* ========================================================================== */
/* Array Management Tests                                                     */
/* ========================================================================== */

bool test_fhir_resize_array(void) {
    int* array = NULL;
    
    // Resize from NULL to 5 elements
    ASSERT_TRUE(fhir_resize_array((void**)&array, 0, 5, sizeof(int)));
    ASSERT_NOT_NULL(array);
    
    // Initialize array
    for (int i = 0; i < 5; i++) {
        array[i] = i;
    }
    
    // Resize to 10 elements
    ASSERT_TRUE(fhir_resize_array((void**)&array, 5, 10, sizeof(int)));
    ASSERT_NOT_NULL(array);
    
    // Check original values are preserved
    for (int i = 0; i < 5; i++) {
        ASSERT_EQ(i, array[i]);
    }
    
    // Check new elements are zeroed
    for (int i = 5; i < 10; i++) {
        ASSERT_EQ(0, array[i]);
    }
    
    // Resize to 0 (should free array)
    ASSERT_TRUE(fhir_resize_array((void**)&array, 10, 0, sizeof(int)));
    ASSERT_NULL(array);
    
    return true;
}

bool test_fhir_array_add(void) {
    int* array = NULL;
    size_t count = 0;
    
    // Add elements
    for (int i = 0; i < 5; i++) {
        ASSERT_TRUE(fhir_array_add((void**)&array, &count, &i, sizeof(int)));
        ASSERT_EQ(i + 1, count);
    }
    
    // Check values
    for (int i = 0; i < 5; i++) {
        ASSERT_EQ(i, array[i]);
    }
    
    free(array);
    
    return true;
}

bool test_fhir_array_remove(void) {
    int array[] = {0, 1, 2, 3, 4};
    size_t count = 5;
    
    // Remove middle element
    ASSERT_TRUE(fhir_array_remove(array, &count, 2, sizeof(int)));
    ASSERT_EQ(4, count);
    
    // Check remaining values
    ASSERT_EQ(0, array[0]);
    ASSERT_EQ(1, array[1]);
    ASSERT_EQ(3, array[2]);  // 3 moved to position 2
    ASSERT_EQ(4, array[3]);  // 4 moved to position 3
    
    // Remove first element
    ASSERT_TRUE(fhir_array_remove(array, &count, 0, sizeof(int)));
    ASSERT_EQ(3, count);
    ASSERT_EQ(1, array[0]);  // 1 moved to position 0
    
    // Remove last element
    ASSERT_TRUE(fhir_array_remove(array, &count, 2, sizeof(int)));
    ASSERT_EQ(2, count);
    
    return true;
}

/* ========================================================================== */
/* String Utilities Tests                                                     */
/* ========================================================================== */

bool test_fhir_strcmp(void) {
    // Normal comparison
    ASSERT_EQ(0, fhir_strcmp("test", "test"));
    ASSERT_NE(0, fhir_strcmp("test", "other"));
    
    // NULL handling
    ASSERT_EQ(0, fhir_strcmp(NULL, NULL));
    ASSERT_NE(0, fhir_strcmp("test", NULL));
    ASSERT_NE(0, fhir_strcmp(NULL, "test"));
    
    return true;
}

bool test_fhir_string_is_empty(void) {
    ASSERT_TRUE(fhir_string_is_empty(NULL));
    ASSERT_TRUE(fhir_string_is_empty(""));
    ASSERT_FALSE(fhir_string_is_empty("test"));
    ASSERT_FALSE(fhir_string_is_empty(" "));  // Space is not empty
    
    return true;
}

bool test_fhir_string_trim(void) {
    char str1[] = "  test  ";
    char* result = fhir_string_trim(str1);
    ASSERT_STR_EQ("test", result);
    
    char str2[] = "test";
    result = fhir_string_trim(str2);
    ASSERT_STR_EQ("test", result);
    
    char str3[] = "   ";
    result = fhir_string_trim(str3);
    ASSERT_STR_EQ("", result);
    
    // Test NULL
    result = fhir_string_trim(NULL);
    ASSERT_NULL(result);
    
    return true;
}

bool test_fhir_string_to_lower(void) {
    char str1[] = "TEST";
    char* result = fhir_string_to_lower(str1);
    ASSERT_STR_EQ("test", result);
    
    char str2[] = "Test123";
    result = fhir_string_to_lower(str2);
    ASSERT_STR_EQ("test123", result);
    
    char str3[] = "already_lower";
    result = fhir_string_to_lower(str3);
    ASSERT_STR_EQ("already_lower", result);
    
    // Test NULL
    result = fhir_string_to_lower(NULL);
    ASSERT_NULL(result);
    
    return true;
}

/* ========================================================================== */
/* Validation Tests                                                           */
/* ========================================================================== */

bool test_fhir_validate_id(void) {
    // Valid IDs
    ASSERT_TRUE(fhir_validate_id("test"));
    ASSERT_TRUE(fhir_validate_id("test-123"));
    ASSERT_TRUE(fhir_validate_id("test.123"));
    ASSERT_TRUE(fhir_validate_id("123"));
    
    // Invalid IDs
    ASSERT_FALSE(fhir_validate_id(""));
    ASSERT_FALSE(fhir_validate_id(NULL));
    ASSERT_FALSE(fhir_validate_id("test space"));  // Space not allowed
    ASSERT_FALSE(fhir_validate_id("test@123"));    // @ not allowed
    
    // Test length limit (64 characters)
    char long_id[70];
    memset(long_id, 'a', 65);
    long_id[65] = '\0';
    ASSERT_FALSE(fhir_validate_id(long_id));  // Too long
    
    memset(long_id, 'a', 64);
    long_id[64] = '\0';
    ASSERT_TRUE(fhir_validate_id(long_id));   // Exactly 64 chars
    
    return true;
}

bool test_fhir_validate_date(void) {
    // Valid dates
    ASSERT_TRUE(fhir_validate_date("2023-01-01"));
    ASSERT_TRUE(fhir_validate_date("2023-12-31"));
    ASSERT_TRUE(fhir_validate_date("1900-01-01"));
    
    // Invalid dates
    ASSERT_FALSE(fhir_validate_date(""));
    ASSERT_FALSE(fhir_validate_date(NULL));
    ASSERT_FALSE(fhir_validate_date("2023-1-1"));     // Missing leading zeros
    ASSERT_FALSE(fhir_validate_date("23-01-01"));     // Wrong year format
    ASSERT_FALSE(fhir_validate_date("2023/01/01"));   // Wrong separator
    ASSERT_FALSE(fhir_validate_date("2023-01-01T"));  // Extra characters
    
    return true;
}

bool test_fhir_validate_datetime(void) {
    // Valid datetimes
    ASSERT_TRUE(fhir_validate_datetime("2023-01-01T10:30:45"));
    ASSERT_TRUE(fhir_validate_datetime("2023-12-31T23:59:59"));
    
    // Invalid datetimes
    ASSERT_FALSE(fhir_validate_datetime(""));
    ASSERT_FALSE(fhir_validate_datetime(NULL));
    ASSERT_FALSE(fhir_validate_datetime("2023-01-01"));        // Missing time
    ASSERT_FALSE(fhir_validate_datetime("2023-01-01 10:30:45")); // Wrong separator
    
    return true;
}

/* ========================================================================== */
/* Resource Utilities Tests                                                   */
/* ========================================================================== */

bool test_fhir_init_base_resource(void) {
    char* resource_type = NULL;
    char* id = NULL;
    
    // Test successful initialization
    ASSERT_TRUE(fhir_init_base_resource("Patient", "test-123", &resource_type, &id));
    ASSERT_NOT_NULL(resource_type);
    ASSERT_NOT_NULL(id);
    ASSERT_STR_EQ("Patient", resource_type);
    ASSERT_STR_EQ("test-123", id);
    
    // Clean up
    fhir_free_base_resource(&resource_type, &id);
    ASSERT_NULL(resource_type);
    ASSERT_NULL(id);
    
    // Test invalid ID
    ASSERT_FALSE(fhir_init_base_resource("Patient", "invalid id", &resource_type, &id));
    ASSERT_NULL(resource_type);
    ASSERT_NULL(id);
    
    return true;
}

bool test_fhir_validate_base_resource(void) {
    // Valid resource
    ASSERT_TRUE(fhir_validate_base_resource("Patient", "test-123"));
    
    // Invalid resource type
    ASSERT_FALSE(fhir_validate_base_resource("", "test-123"));
    ASSERT_FALSE(fhir_validate_base_resource(NULL, "test-123"));
    
    // Invalid ID
    ASSERT_FALSE(fhir_validate_base_resource("Patient", ""));
    ASSERT_FALSE(fhir_validate_base_resource("Patient", NULL));
    ASSERT_FALSE(fhir_validate_base_resource("Patient", "invalid id"));
    
    return true;
}

/* ========================================================================== */
/* Main Test Runner                                                           */
/* ========================================================================== */

int main(void) {
    TEST_INIT();
    
    // Error handling tests
    RUN_TEST(test_error_handling_basic);
    RUN_TEST(test_error_code_to_string);
    
    // Memory management tests
    RUN_TEST(test_fhir_strdup);
    RUN_TEST(test_fhir_malloc);
    RUN_TEST(test_fhir_calloc);
    
    // Array management tests
    RUN_TEST(test_fhir_resize_array);
    RUN_TEST(test_fhir_array_add);
    RUN_TEST(test_fhir_array_remove);
    
    // String utilities tests
    RUN_TEST(test_fhir_strcmp);
    RUN_TEST(test_fhir_string_is_empty);
    RUN_TEST(test_fhir_string_trim);
    RUN_TEST(test_fhir_string_to_lower);
    
    // Validation tests
    RUN_TEST(test_fhir_validate_id);
    RUN_TEST(test_fhir_validate_date);
    RUN_TEST(test_fhir_validate_datetime);
    
    // Resource utilities tests
    RUN_TEST(test_fhir_init_base_resource);
    RUN_TEST(test_fhir_validate_base_resource);
    
    TEST_FINALIZE();
    return 0;
}