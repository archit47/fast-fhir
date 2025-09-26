/**
 * @file fhir_device_metric.c
 * @brief FHIR R5 DeviceMetric resource C implementation
 * @version 1.0.0
 * @date 2024-01-01
 * 
 * Implementation of FHIR R5 DeviceMetric resource following
 * C99 standards and best practices for memory management and error handling.
 */

#include "fhir_device_metric.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <errno.h>

/* ========================================================================== */
/* String Conversion Tables                                                   */
/* ========================================================================== */

static const char* operational_status_strings[] = {
    [FHIR_DEVICE_METRIC_STATUS_ON] = "on",
    [FHIR_DEVICE_METRIC_STATUS_OFF] = "off",
    [FHIR_DEVICE_METRIC_STATUS_STANDBY] = "standby",
    [FHIR_DEVICE_METRIC_STATUS_ENTERED_IN_ERROR] = "entered-in-error"
};

static const char* color_strings[] = {
    [FHIR_DEVICE_METRIC_COLOR_BLACK] = "black",
    [FHIR_DEVICE_METRIC_COLOR_RED] = "red",
    [FHIR_DEVICE_METRIC_COLOR_GREEN] = "green",
    [FHIR_DEVICE_METRIC_COLOR_YELLOW] = "yellow",
    [FHIR_DEVICE_METRIC_COLOR_BLUE] = "blue",
    [FHIR_DEVICE_METRIC_COLOR_MAGENTA] = "magenta",
    [FHIR_DEVICE_METRIC_COLOR_CYAN] = "cyan",
    [FHIR_DEVICE_METRIC_COLOR_WHITE] = "white"
};

static const char* category_strings[] = {
    [FHIR_DEVICE_METRIC_CATEGORY_MEASUREMENT] = "measurement",
    [FHIR_DEVICE_METRIC_CATEGORY_SETTING] = "setting",
    [FHIR_DEVICE_METRIC_CATEGORY_CALCULATION] = "calculation",
    [FHIR_DEVICE_METRIC_CATEGORY_UNSPECIFIED] = "unspecified"
};

static const char* calibration_type_strings[] = {
    [FHIR_DEVICE_METRIC_CALIBRATION_UNSPECIFIED] = "unspecified",
    [FHIR_DEVICE_METRIC_CALIBRATION_OFFSET] = "offset",
    [FHIR_DEVICE_METRIC_CALIBRATION_GAIN] = "gain",
    [FHIR_DEVICE_METRIC_CALIBRATION_TWO_POINT] = "two-point"
};

static const char* calibration_state_strings[] = {
    [FHIR_DEVICE_METRIC_CALIBRATION_STATE_NOT_CALIBRATED] = "not-calibrated",
    [FHIR_DEVICE_METRIC_CALIBRATION_STATE_CALIBRATION_REQUIRED] = "calibration-required",
    [FHIR_DEVICE_METRIC_CALIBRATION_STATE_CALIBRATED] = "calibrated",
    [FHIR_DEVICE_METRIC_CALIBRATION_STATE_UNSPECIFIED] = "unspecified"
};

/* ========================================================================== */
/* Private Helper Functions                                                   */
/* ========================================================================== */

/**
 * @brief Initialize base domain resource fields
 * @param metric Target DeviceMetric
 * @param id Resource identifier
 * @return true on success, false on failure
 */
static bool init_base_resource(FHIRDeviceMetric* metric, const char* id) {
    if (!metric || !id) {
        return false;
    }
    
    metric->domain_resource.resource.resource_type = strdup("DeviceMetric");
    if (!metric->domain_resource.resource.resource_type) {
        return false;
    }
    
    metric->domain_resource.resource.id = strdup(id);
    if (!metric->domain_resource.resource.id) {
        free(metric->domain_resource.resource.resource_type);
        return false;
    }
    
    return true;
}

/**
 * @brief Free calibration array
 * @param calibrations Array of calibrations to free
 * @param count Number of calibrations
 */
static void free_calibration_array(FHIRDeviceMetricCalibration** calibrations, size_t count) {
    if (!calibrations) return;
    
    for (size_t i = 0; i < count; i++) {
        if (calibrations[i]) {
            free(calibrations[i]->time);
            free(calibrations[i]);
        }
    }
    free(calibrations);
}

/**
 * @brief Resize array with proper error handling
 * @param array Pointer to array pointer
 * @param old_size Current size
 * @param new_size New size
 * @param element_size Size of each element
 * @return true on success, false on failure
 */
static bool resize_array(void** array, size_t old_size, size_t new_size, size_t element_size) {
    if (new_size == 0) {
        free(*array);
        *array = NULL;
        return true;
    }
    
    void* new_array = realloc(*array, new_size * element_size);
    if (!new_array) {
        return false;
    }
    
    *array = new_array;
    
    // Initialize new elements to NULL
    if (new_size > old_size) {
        memset((char*)*array + (old_size * element_size), 0, 
               (new_size - old_size) * element_size);
    }
    
    return true;
}

/* ========================================================================== */
/* Public API Implementation                                                  */
/* ========================================================================== */

FHIRDeviceMetric* fhir_device_metric_create(const char* id) {
    if (!id || strlen(id) == 0) {
        errno = EINVAL;
        return NULL;
    }
    
    FHIRDeviceMetric* metric = calloc(1, sizeof(FHIRDeviceMetric));
    if (!metric) {
        errno = ENOMEM;
        return NULL;
    }
    
    if (!init_base_resource(metric, id)) {
        free(metric);
        errno = ENOMEM;
        return NULL;
    }
    
    // Initialize with default values
    metric->operational_status = FHIR_DEVICE_METRIC_STATUS_OFF;
    metric->color = FHIR_DEVICE_METRIC_COLOR_BLACK;
    metric->category = FHIR_DEVICE_METRIC_CATEGORY_UNSPECIFIED;
    
    return metric;
}

void fhir_device_metric_free(FHIRDeviceMetric* metric) {
    if (!metric) {
        return;
    }
    
    // Free base resource fields
    free(metric->domain_resource.resource.resource_type);
    free(metric->domain_resource.resource.id);
    
    // Free DeviceMetric-specific fields
    if (metric->identifier) {
        for (size_t i = 0; i < metric->identifier_count; i++) {
            free(metric->identifier[i]);
        }
        free(metric->identifier);
    }
    
    free(metric->type);
    free(metric->unit);
    free(metric->source);
    free(metric->parent);
    free(metric->measurement_period);
    
    // Free calibration array
    free_calibration_array(metric->calibration, metric->calibration_count);
    
    free(metric);
}

FHIRDeviceMetric* fhir_device_metric_parse(cJSON* json) {
    if (!json || !cJSON_IsObject(json)) {
        errno = EINVAL;
        return NULL;
    }
    
    // Validate resource type
    cJSON* resource_type_json = cJSON_GetObjectItem(json, "resourceType");
    if (!resource_type_json || !cJSON_IsString(resource_type_json) ||
        strcmp(resource_type_json->valuestring, "DeviceMetric") != 0) {
        errno = EINVAL;
        return NULL;
    }
    
    // Get ID
    cJSON* id_json = cJSON_GetObjectItem(json, "id");
    if (!id_json || !cJSON_IsString(id_json)) {
        errno = EINVAL;
        return NULL;
    }
    
    FHIRDeviceMetric* metric = fhir_device_metric_create(id_json->valuestring);
    if (!metric) {
        return NULL;
    }
    
    // Parse operational status
    cJSON* status_json = cJSON_GetObjectItem(json, "operationalStatus");
    if (status_json && cJSON_IsString(status_json)) {
        int status = fhir_device_metric_operational_status_from_string(status_json->valuestring);
        if (status >= 0) {
            metric->operational_status = (FHIRDeviceMetricOperationalStatus)status;
        }
    }
    
    // Parse color
    cJSON* color_json = cJSON_GetObjectItem(json, "color");
    if (color_json && cJSON_IsString(color_json)) {
        int color = fhir_device_metric_color_from_string(color_json->valuestring);
        if (color >= 0) {
            metric->color = (FHIRDeviceMetricColor)color;
        }
    }
    
    // Parse category
    cJSON* category_json = cJSON_GetObjectItem(json, "category");
    if (category_json && cJSON_IsString(category_json)) {
        for (int i = 0; i < 4; i++) {
            if (strcmp(category_json->valuestring, category_strings[i]) == 0) {
                metric->category = (FHIRDeviceMetricCategory)i;
                break;
            }
        }
    }
    
    // Parse type (CodeableConcept)
    cJSON* type_json = cJSON_GetObjectItem(json, "type");
    if (type_json && cJSON_IsObject(type_json)) {
        metric->type = malloc(sizeof(FHIRCodeableConcept));
        if (metric->type) {
            // Parse CodeableConcept fields (implementation depends on structure)
        }
    }
    
    // Parse unit (CodeableConcept)
    cJSON* unit_json = cJSON_GetObjectItem(json, "unit");
    if (unit_json && cJSON_IsObject(unit_json)) {
        metric->unit = malloc(sizeof(FHIRCodeableConcept));
        if (metric->unit) {
            // Parse CodeableConcept fields
        }
    }
    
    // Parse source reference
    cJSON* source_json = cJSON_GetObjectItem(json, "source");
    if (source_json && cJSON_IsObject(source_json)) {
        metric->source = malloc(sizeof(FHIRReference));
        if (metric->source) {
            // Parse Reference fields
        }
    }
    
    // Parse calibration array
    cJSON* calibration_json = cJSON_GetObjectItem(json, "calibration");
    if (calibration_json && cJSON_IsArray(calibration_json)) {
        int array_size = cJSON_GetArraySize(calibration_json);
        if (array_size > 0) {
            metric->calibration = calloc(array_size, sizeof(FHIRDeviceMetricCalibration*));
            if (metric->calibration) {
                metric->calibration_count = array_size;
                
                for (int i = 0; i < array_size; i++) {
                    cJSON* cal_item = cJSON_GetArrayItem(calibration_json, i);
                    if (cal_item && cJSON_IsObject(cal_item)) {
                        metric->calibration[i] = malloc(sizeof(FHIRDeviceMetricCalibration));
                        if (metric->calibration[i]) {
                            // Parse calibration fields
                            cJSON* type_json = cJSON_GetObjectItem(cal_item, "type");
                            if (type_json && cJSON_IsString(type_json)) {
                                // Parse calibration type
                            }
                            
                            cJSON* state_json = cJSON_GetObjectItem(cal_item, "state");
                            if (state_json && cJSON_IsString(state_json)) {
                                // Parse calibration state
                            }
                        }
                    }
                }
            }
        }
    }
    
    return metric;
}

cJSON* fhir_device_metric_to_json(const FHIRDeviceMetric* metric) {
    if (!metric) {
        errno = EINVAL;
        return NULL;
    }
    
    cJSON* json = cJSON_CreateObject();
    if (!json) {
        errno = ENOMEM;
        return NULL;
    }
    
    // Add resource type and id
    if (!cJSON_AddStringToObject(json, "resourceType", "DeviceMetric") ||
        !cJSON_AddStringToObject(json, "id", metric->domain_resource.resource.id)) {
        cJSON_Delete(json);
        errno = ENOMEM;
        return NULL;
    }
    
    // Add operational status
    const char* status_str = fhir_device_metric_operational_status_to_string(metric->operational_status);
    if (status_str) {
        cJSON_AddStringToObject(json, "operationalStatus", status_str);
    }
    
    // Add color
    const char* color_str = fhir_device_metric_color_to_string(metric->color);
    if (color_str) {
        cJSON_AddStringToObject(json, "color", color_str);
    }
    
    // Add category
    if (metric->category < 4) {
        cJSON_AddStringToObject(json, "category", category_strings[metric->category]);
    }
    
    // Add type
    if (metric->type) {
        cJSON* type_json = cJSON_CreateObject();
        if (type_json) {
            // Serialize CodeableConcept
            cJSON_AddItemToObject(json, "type", type_json);
        }
    }
    
    // Add unit
    if (metric->unit) {
        cJSON* unit_json = cJSON_CreateObject();
        if (unit_json) {
            // Serialize CodeableConcept
            cJSON_AddItemToObject(json, "unit", unit_json);
        }
    }
    
    // Add calibration array
    if (metric->calibration && metric->calibration_count > 0) {
        cJSON* calibration_array = cJSON_CreateArray();
        if (calibration_array) {
            for (size_t i = 0; i < metric->calibration_count; i++) {
                if (metric->calibration[i]) {
                    cJSON* cal_json = cJSON_CreateObject();
                    if (cal_json) {
                        // Add calibration fields
                        cJSON_AddItemToArray(calibration_array, cal_json);
                    }
                }
            }
            cJSON_AddItemToObject(json, "calibration", calibration_array);
        }
    }
    
    return json;
}

bool fhir_device_metric_validate(const FHIRDeviceMetric* metric) {
    if (!metric) {
        return false;
    }
    
    // Validate required fields according to FHIR R5 specification
    if (!metric->type) {
        return false;
    }
    
    if (metric->category == FHIR_DEVICE_METRIC_CATEGORY_UNSPECIFIED) {
        return false;
    }
    
    return true;
}

bool fhir_device_metric_is_operational(const FHIRDeviceMetric* metric) {
    if (!metric) {
        return false;
    }
    
    return metric->operational_status == FHIR_DEVICE_METRIC_STATUS_ON;
}

bool fhir_device_metric_is_measurement(const FHIRDeviceMetric* metric) {
    if (!metric) {
        return false;
    }
    
    return metric->category == FHIR_DEVICE_METRIC_CATEGORY_MEASUREMENT;
}

bool fhir_device_metric_set_operational_status(FHIRDeviceMetric* metric, 
                                              FHIRDeviceMetricOperationalStatus status) {
    if (!metric || status < 0 || status > FHIR_DEVICE_METRIC_STATUS_ENTERED_IN_ERROR) {
        errno = EINVAL;
        return false;
    }
    
    metric->operational_status = status;
    return true;
}

bool fhir_device_metric_set_color(FHIRDeviceMetric* metric, FHIRDeviceMetricColor color) {
    if (!metric || color < 0 || color > FHIR_DEVICE_METRIC_COLOR_WHITE) {
        errno = EINVAL;
        return false;
    }
    
    metric->color = color;
    return true;
}

bool fhir_device_metric_set_category(FHIRDeviceMetric* metric, FHIRDeviceMetricCategory category) {
    if (!metric || category < 0 || category > FHIR_DEVICE_METRIC_CATEGORY_UNSPECIFIED) {
        errno = EINVAL;
        return false;
    }
    
    metric->category = category;
    return true;
}

bool fhir_device_metric_add_calibration(FHIRDeviceMetric* metric, 
                                       const FHIRDeviceMetricCalibration* calibration) {
    if (!metric || !calibration) {
        errno = EINVAL;
        return false;
    }
    
    // Resize calibration array
    if (!resize_array((void**)&metric->calibration, 
                     metric->calibration_count,
                     metric->calibration_count + 1,
                     sizeof(FHIRDeviceMetricCalibration*))) {
        errno = ENOMEM;
        return false;
    }
    
    // Allocate and copy calibration
    metric->calibration[metric->calibration_count] = malloc(sizeof(FHIRDeviceMetricCalibration));
    if (!metric->calibration[metric->calibration_count]) {
        errno = ENOMEM;
        return false;
    }
    
    memcpy(metric->calibration[metric->calibration_count], calibration, sizeof(FHIRDeviceMetricCalibration));
    metric->calibration_count++;
    
    return true;
}

const char* fhir_device_metric_operational_status_to_string(FHIRDeviceMetricOperationalStatus status) {
    if (status < 0 || status > FHIR_DEVICE_METRIC_STATUS_ENTERED_IN_ERROR) {
        return NULL;
    }
    
    return operational_status_strings[status];
}

int fhir_device_metric_operational_status_from_string(const char* status_str) {
    if (!status_str) {
        return -1;
    }
    
    for (int i = 0; i <= FHIR_DEVICE_METRIC_STATUS_ENTERED_IN_ERROR; i++) {
        if (strcmp(status_str, operational_status_strings[i]) == 0) {
            return i;
        }
    }
    
    return -1;
}

const char* fhir_device_metric_color_to_string(FHIRDeviceMetricColor color) {
    if (color < 0 || color > FHIR_DEVICE_METRIC_COLOR_WHITE) {
        return NULL;
    }
    
    return color_strings[color];
}

int fhir_device_metric_color_from_string(const char* color_str) {
    if (!color_str) {
        return -1;
    }
    
    for (int i = 0; i <= FHIR_DEVICE_METRIC_COLOR_WHITE; i++) {
        if (strcmp(color_str, color_strings[i]) == 0) {
            return i;
        }
    }
    
    return -1;
}