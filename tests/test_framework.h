/**
 * @file test_framework.h
 * @brief Simple test framework for FHIR C extensions
 * @version 0.1.0
 * @date 2024-01-01
 * 
 * A lightweight test framework for C code following best practices.
 */

#ifndef TEST_FRAMEWORK_H
#define TEST_FRAMEWORK_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================== */
/* Test Framework Macros                                                     */
/* ========================================================================== */

/**
 * @brief Test statistics
 */
typedef struct {
    int total_tests;
    int passed_tests;
    int failed_tests;
    int skipped_tests;
} TestStats;

extern TestStats g_test_stats;

/**
 * @brief Initialize test framework
 */
#define TEST_INIT() \
    do { \
        memset(&g_test_stats, 0, sizeof(TestStats)); \
        printf("Starting test suite...\n"); \
    } while(0)

/**
 * @brief Finalize test framework and print results
 */
#define TEST_FINALIZE() \
    do { \
        printf("\n=== Test Results ===\n"); \
        printf("Total:   %d\n", g_test_stats.total_tests); \
        printf("Passed:  %d\n", g_test_stats.passed_tests); \
        printf("Failed:  %d\n", g_test_stats.failed_tests); \
        printf("Skipped: %d\n", g_test_stats.skipped_tests); \
        printf("Success Rate: %.1f%%\n", \
               g_test_stats.total_tests > 0 ? \
               (100.0 * g_test_stats.passed_tests / g_test_stats.total_tests) : 0.0); \
        exit(g_test_stats.failed_tests > 0 ? 1 : 0); \
    } while(0)

/**
 * @brief Run a test function
 */
#define RUN_TEST(test_func) \
    do { \
        printf("Running %s... ", #test_func); \
        fflush(stdout); \
        g_test_stats.total_tests++; \
        if (test_func()) { \
            printf("PASSED\n"); \
            g_test_stats.passed_tests++; \
        } else { \
            printf("FAILED\n"); \
            g_test_stats.failed_tests++; \
        } \
    } while(0)

/**
 * @brief Skip a test
 */
#define SKIP_TEST(test_func, reason) \
    do { \
        printf("Skipping %s... SKIPPED (%s)\n", #test_func, reason); \
        g_test_stats.total_tests++; \
        g_test_stats.skipped_tests++; \
    } while(0)

/* ========================================================================== */
/* Assertion Macros                                                          */
/* ========================================================================== */

/**
 * @brief Assert that condition is true
 */
#define ASSERT_TRUE(condition) \
    do { \
        if (!(condition)) { \
            printf("\n  ASSERTION FAILED: %s (line %d)\n", #condition, __LINE__); \
            return false; \
        } \
    } while(0)

/**
 * @brief Assert that condition is false
 */
#define ASSERT_FALSE(condition) \
    do { \
        if (condition) { \
            printf("\n  ASSERTION FAILED: !(%s) (line %d)\n", #condition, __LINE__); \
            return false; \
        } \
    } while(0)

/**
 * @brief Assert that two values are equal
 */
#define ASSERT_EQ(expected, actual) \
    do { \
        if ((expected) != (actual)) { \
            printf("\n  ASSERTION FAILED: Expected %ld, got %ld (line %d)\n", \
                   (long)(expected), (long)(actual), __LINE__); \
            return false; \
        } \
    } while(0)

/**
 * @brief Assert that two values are not equal
 */
#define ASSERT_NE(expected, actual) \
    do { \
        if ((expected) == (actual)) { \
            printf("\n  ASSERTION FAILED: Expected not %ld, got %ld (line %d)\n", \
                   (long)(expected), (long)(actual), __LINE__); \
            return false; \
        } \
    } while(0)

/**
 * @brief Assert that pointer is not NULL
 */
#define ASSERT_NOT_NULL(ptr) \
    do { \
        if ((ptr) == NULL) { \
            printf("\n  ASSERTION FAILED: %s is NULL (line %d)\n", #ptr, __LINE__); \
            return false; \
        } \
    } while(0)

/**
 * @brief Assert that pointer is NULL
 */
#define ASSERT_NULL(ptr) \
    do { \
        if ((ptr) != NULL) { \
            printf("\n  ASSERTION FAILED: %s is not NULL (line %d)\n", #ptr, __LINE__); \
            return false; \
        } \
    } while(0)

/**
 * @brief Assert that two strings are equal
 */
#define ASSERT_STR_EQ(expected, actual) \
    do { \
        if (strcmp((expected), (actual)) != 0) { \
            printf("\n  ASSERTION FAILED: Expected \"%s\", got \"%s\" (line %d)\n", \
                   (expected), (actual), __LINE__); \
            return false; \
        } \
    } while(0)

/**
 * @brief Assert that two strings are not equal
 */
#define ASSERT_STR_NE(expected, actual) \
    do { \
        if (strcmp((expected), (actual)) == 0) { \
            printf("\n  ASSERTION FAILED: Expected not \"%s\", got \"%s\" (line %d)\n", \
                   (expected), (actual), __LINE__); \
            return false; \
        } \
    } while(0)

/**
 * @brief Assert that two memory blocks are equal
 */
#define ASSERT_MEM_EQ(expected, actual, size) \
    do { \
        if (memcmp((expected), (actual), (size)) != 0) { \
            printf("\n  ASSERTION FAILED: Memory blocks differ (line %d)\n", __LINE__); \
            return false; \
        } \
    } while(0)

/**
 * @brief Assert that two floating point values are approximately equal
 */
#define ASSERT_FLOAT_EQ(expected, actual, epsilon) \
    do { \
        double diff = (expected) - (actual); \
        if (diff < 0) diff = -diff; \
        if (diff > (epsilon)) { \
            printf("\n  ASSERTION FAILED: Expected %f, got %f (diff %f > %f) (line %d)\n", \
                   (double)(expected), (double)(actual), diff, (double)(epsilon), __LINE__); \
            return false; \
        } \
    } while(0)

/* ========================================================================== */
/* Test Utilities                                                            */
/* ========================================================================== */

/**
 * @brief Create a temporary file for testing
 * @param content Content to write to file
 * @return File path (must be freed by caller) or NULL on failure
 */
char* create_temp_file(const char* content);

/**
 * @brief Remove a file
 * @param filepath Path to file to remove
 * @return true on success, false on failure
 */
bool remove_file(const char* filepath);

/**
 * @brief Read entire file content
 * @param filepath Path to file
 * @return File content (must be freed by caller) or NULL on failure
 */
char* read_file_content(const char* filepath);

/**
 * @brief Check if file exists
 * @param filepath Path to file
 * @return true if file exists, false otherwise
 */
bool file_exists(const char* filepath);

/**
 * @brief Get current timestamp in milliseconds
 * @return Timestamp in milliseconds
 */
long long get_timestamp_ms(void);

/**
 * @brief Sleep for specified milliseconds
 * @param ms Milliseconds to sleep
 */
void sleep_ms(int ms);

#ifdef __cplusplus
}
#endif

#endif /* TEST_FRAMEWORK_H */