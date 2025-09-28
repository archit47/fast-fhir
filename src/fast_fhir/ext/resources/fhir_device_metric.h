/**
 * @file fhir_device_metric.h
 * @brief FHIR R5 DeviceMetric resource C interface
 * @version 0.1.0
 * @date 2024-01-01
 * 
 * This header defines the C interface for the FHIR R5 DeviceMetric resource.
 * Follows FHIR R5 specification and C99 standards.
 */

#ifndef FHIR_DEVICE_METRIC_H
#define FHIR_DEVICE_METRIC_H

#include "../fhir_datatypes.h"
#include "../fhir_foundation.h"
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief DeviceMetric operational status enumeration
 */
typedef enum {
    FHIR_DEVICE_METRIC_STATUS_ON,
    FHIR_DEVICE_METRIC_STATUS_OFF,
    FHIR_DEVICE_METRIC_STATUS_STANDBY,
    FHIR_DEVICE_METRIC_STATUS_ENTERED_IN_ERROR
} FHIRDeviceMetricOperationalStatus;

/**
 * @brief DeviceMetric color enumeration
 */
typedef enum {
    FHIR_DEVICE_METRIC_COLOR_BLACK,
    FHIR_DEVICE_METRIC_COLOR_RED,
    FHIR_DEVICE_METRIC_COLOR_GREEN,
    FHIR_DEVICE_METRIC_COLOR_YELLOW,
    FHIR_DEVICE_METRIC_COLOR_BLUE,
    FHIR_DEVICE_METRIC_COLOR_MAGENTA,
    FHIR_DEVICE_METRIC_COLOR_CYAN,
    FHIR_DEVICE_METRIC_COLOR_WHITE
} FHIRDeviceMetricColor;

/**
 * @brief DeviceMetric category enumeration
 */
typedef enum {
    FHIR_DEVICE_METRIC_CATEGORY_MEASUREMENT,
    FHIR_DEVICE_METRIC_CATEGORY_SETTING,
    FHIR_DEVICE_METRIC_CATEGORY_CALCULATION,
    FHIR_DEVICE_METRIC_CATEGORY_UNSPECIFIED
} FHIRDeviceMetricCategory;

/**
 * @brief DeviceMetric calibration type enumeration
 */
typedef enum {
    FHIR_DEVICE_METRIC_CALIBRATION_UNSPECIFIED,
    FHIR_DEVICE_METRIC_CALIBRATION_OFFSET,
    FHIR_DEVICE_METRIC_CALIBRATION_GAIN,
    FHIR_DEVICE_METRIC_CALIBRATION_TWO_POINT
} FHIRDeviceMetricCalibrationType;

/**
 * @brief DeviceMetric calibration state enumeration
 */
typedef enum {
    FHIR_DEVICE_METRIC_CALIBRATION_STATE_NOT_CALIBRATED,
    FHIR_DEVICE_METRIC_CALIBRATION_STATE_CALIBRATION_REQUIRED,
    FHIR_DEVICE_METRIC_CALIBRATION_STATE_CALIBRATED,
    FHIR_DEVICE_METRIC_CALIBRATION_STATE_UNSPECIFIED
} FHIRDeviceMetricCalibrationState;

/**
 * @brief DeviceMetric calibration information
 */
typedef struct FHIRDeviceMetricCalibration {
    FHIRElement base;
    FHIRDeviceMetricCalibrationType type;
    FHIRDeviceMetricCalibrationState state;
    FHIRInstant* time;
} FHIRDeviceMetricCalibration;

/**
 * @brief FHIR R5 DeviceMetric resource structure
 * 
 * Describes a measurement, calculation or setting capability of a medical device.
 */
typedef struct FHIRDeviceMetric {
    /** Base domain resource */
    FHIRDomainResource domain_resource;
    
    /** Instance identifiers assigned to a device */
    FHIRIdentifier** identifier;
    size_t identifier_count;
    
    /** Identity of metric, for example Heart Rate or PEEP Setting */
    FHIRCodeableConcept* type;
    
    /** Unit of Measure for the Metric */
    FHIRCodeableConcept* unit;
    
    /** Describes the link to the Device that this DeviceMetric belongs to */
    FHIRReference* source;
    
    /** Describes the link to the Device that this DeviceMetric belongs to */
    FHIRReference* parent;
    
    /** Indicates current operational state of the device */
    FHIRDeviceMetricOperationalStatus operational_status;
    
    /** Describes the color representation for the metric */
    FHIRDeviceMetricColor color;
    
    /** Indicates the category of the observation generation process */
    FHIRDeviceMetricCategory category;
    
    /** Describes the measurement repetition time */
    FHIRTiming* measurement_period;
    
    /** Describes the calibrations that have been performed or that are required to be performed */
    FHIRDeviceMetricCalibration** calibration;
    size_t calibration_count;
} FHIRDeviceMetric;

/**
 * @brief Create a new DeviceMetric resource
 * @param id Resource identifier (required)
 * @return Pointer to new DeviceMetric or NULL on failure
 */
FHIRDeviceMetric* fhir_device_metric_create(const char* id);

/**
 * @brief Free a DeviceMetric resource
 * @param metric Pointer to DeviceMetric to free (can be NULL)
 */
void fhir_device_metric_free(FHIRDeviceMetric* metric);

/**
 * @brief Parse DeviceMetric from JSON
 * @param json JSON object containing DeviceMetric data
 * @return Pointer to parsed DeviceMetric or NULL on failure
 */
FHIRDeviceMetric* fhir_device_metric_parse(cJSON* json);

/**
 * @brief Convert DeviceMetric to JSON
 * @param metric DeviceMetric to convert
 * @return JSON object or NULL on failure
 */
cJSON* fhir_device_metric_to_json(const FHIRDeviceMetric* metric);

/**
 * @brief Validate DeviceMetric resource
 * @param metric DeviceMetric to validate
 * @return true if valid, false otherwise
 */
bool fhir_device_metric_validate(const FHIRDeviceMetric* metric);

/**
 * @brief Check if DeviceMetric is operational (on)
 * @param metric DeviceMetric to check
 * @return true if operational, false otherwise
 */
bool fhir_device_metric_is_operational(const FHIRDeviceMetric* metric);

/**
 * @brief Check if DeviceMetric is a measurement metric
 * @param metric DeviceMetric to check
 * @return true if measurement metric, false otherwise
 */
bool fhir_device_metric_is_measurement(const FHIRDeviceMetric* metric);

/**
 * @brief Set operational status
 * @param metric Target DeviceMetric
 * @param status Operational status to set
 * @return true on success, false on failure
 */
bool fhir_device_metric_set_operational_status(FHIRDeviceMetric* metric, 
                                              FHIRDeviceMetricOperationalStatus status);

/**
 * @brief Set color indicator
 * @param metric Target DeviceMetric
 * @param color Color to set
 * @return true on success, false on failure
 */
bool fhir_device_metric_set_color(FHIRDeviceMetric* metric, FHIRDeviceMetricColor color);

/**
 * @brief Set category
 * @param metric Target DeviceMetric
 * @param category Category to set
 * @return true on success, false on failure
 */
bool fhir_device_metric_set_category(FHIRDeviceMetric* metric, FHIRDeviceMetricCategory category);

/**
 * @brief Add calibration information
 * @param metric Target DeviceMetric
 * @param calibration Calibration to add
 * @return true on success, false on failure
 */
bool fhir_device_metric_add_calibration(FHIRDeviceMetric* metric, 
                                       const FHIRDeviceMetricCalibration* calibration);

/**
 * @brief Convert operational status enum to string
 * @param status Operational status enum
 * @return String representation or NULL for invalid status
 */
const char* fhir_device_metric_operational_status_to_string(FHIRDeviceMetricOperationalStatus status);

/**
 * @brief Convert string to operational status enum
 * @param status_str String representation
 * @return Operational status enum or -1 for invalid string
 */
int fhir_device_metric_operational_status_from_string(const char* status_str);

/**
 * @brief Convert color enum to string
 * @param color Color enum
 * @return String representation or NULL for invalid color
 */
const char* fhir_device_metric_color_to_string(FHIRDeviceMetricColor color);

/**
 * @brief Convert string to color enum
 * @param color_str String representation
 * @return Color enum or -1 for invalid string
 */
int fhir_device_metric_color_from_string(const char* color_str);

#ifdef __cplusplus
}
#endif

#endif /* FHIR_DEVICE_METRIC_H */