/**
 * @file test_framework.c
 * @brief Simple test framework implementation for FHIR C extensions
 * @version 1.0.0
 * @date 2024-01-01
 */

#include "test_framework.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>
#include <unistd.h>

/* ========================================================================== */
/* Global Variables                                                           */
/* ========================================================================== */

TestStats g_test_stats = {0};

/* ========================================================================== */
/* Test Utilities Implementation                                              */
/* ========================================================================== */

char* create_temp_file(const char* content) {
    if (!content) return NULL;
    
    // Create temporary filename
    char* template = strdup("/tmp/fhir_test_XXXXXX");
    if (!template) return NULL;
    
    int fd = mkstemp(template);
    if (fd == -1) {
        free(template);
        return NULL;
    }
    
    // Write content to file
    size_t content_len = strlen(content);
    ssize_t written = write(fd, content, content_len);
    close(fd);
    
    if (written != (ssize_t)content_len) {
        remove(template);
        free(template);
        return NULL;
    }
    
    return template;
}

bool remove_file(const char* filepath) {
    if (!filepath) return false;
    return remove(filepath) == 0;
}

char* read_file_content(const char* filepath) {
    if (!filepath) return NULL;
    
    FILE* file = fopen(filepath, "r");
    if (!file) return NULL;
    
    // Get file size
    fseek(file, 0, SEEK_END);
    long size = ftell(file);
    fseek(file, 0, SEEK_SET);
    
    if (size < 0) {
        fclose(file);
        return NULL;
    }
    
    // Allocate buffer
    char* content = malloc(size + 1);
    if (!content) {
        fclose(file);
        return NULL;
    }
    
    // Read content
    size_t read_size = fread(content, 1, size, file);
    fclose(file);
    
    if (read_size != (size_t)size) {
        free(content);
        return NULL;
    }
    
    content[size] = '\0';
    return content;
}

bool file_exists(const char* filepath) {
    if (!filepath) return false;
    return access(filepath, F_OK) == 0;
}

long long get_timestamp_ms(void) {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (long long)tv.tv_sec * 1000 + tv.tv_usec / 1000;
}

void sleep_ms(int ms) {
    if (ms <= 0) return;
    usleep(ms * 1000);
}