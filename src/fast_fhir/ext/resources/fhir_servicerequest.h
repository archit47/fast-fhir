/**
 * @file fhir_servicerequest.h
 * @brief FHIR R5 ServiceRequest resource C interface with OOP principles
 * @version 1.0.0
 * @date 2024-01-01
 * 
 * A record of a request for service such as diagnostic investigations, treatments, or operations to be performed
 */

#ifndef FHIR_SERVICEREQUEST_H
#define FHIR_SERVICEREQUEST_H

#include "../common/fhir_resource_base.h"
#include "../fhir_datatypes.h"
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================== */
/* ServiceRequest-Specific Enumerations                                      */
/* ========================================================================== */

/**
 * @brief ServiceRequest status enumeration
 */
typedef enum {
    FHIR_SERVICEREQUEST_STATUS_DRAFT = 0,
    FHIR_SERVICEREQUEST_STATUS_ACTIVE,
    FHIR_SERVICEREQUEST_STATUS_ON_HOLD,
    FHIR_SERVICEREQUEST_STATUS_REVOKED,
    FHIR_SERVICEREQUEST_STATUS_COMPLETED,
    FHIR_SERVICEREQUEST_STATUS_ENTERED_IN_ERROR,
    FHIR_SERVICEREQUEST_STATUS_UNKNOWN
} FHIRServiceRequestStatus;

/**
 * @brief ServiceRequest intent enumeration
 */
typedef enum {
    FHIR_SERVICEREQUEST_INTENT_PROPOSAL = 0,
    FHIR_SERVICEREQUEST_INTENT_PLAN,
    FHIR_SERVICEREQUEST_INTENT_DIRECTIVE,
    FHIR_SERVICEREQUEST_INTENT_ORDER,
    FHIR_SERVICEREQUEST_INTENT_ORIGINAL_ORDER,
    FHIR_SERVICEREQUEST_INTENT_REFLEX_ORDER,
    FHIR_SERVICEREQUEST_INTENT_FILLER_ORDER,
    FHIR_SERVICEREQUEST_INTENT_INSTANCE_ORDER,
    FHIR_SERVICEREQUEST_INTENT_OPTION
} FHIRServiceRequestIntent;

/**
 * @brief ServiceRequest priority enumeration
 */
typedef enum {
    FHIR_SERVICEREQUEST_PRIORITY_ROUTINE = 0,
    FHIR_SERVICEREQUEST_PRIORITY_URGENT,
    FHIR_SERVICEREQUEST_PRIORITY_ASAP,
    FHIR_SERVICEREQUEST_PRIORITY_STAT
} FHIRServiceRequestPriority;

/* ========================================================================== */
/* ServiceRequest Sub-structures                                             */
/* ========================================================================== */

/**
 * @brief ServiceRequest order detail information
 */
typedef struct FHIRServiceRequestOrderDetail {
    FHIRElement base;
    FHIRCodeableConcept* parameter_code;
    
    // Value (choice type)
    FHIRQuantity* value_quantity;
    FHIRRatio* value_ratio;
    FHIRRange* value_range;
    FHIRBoolean* value_boolean;
    FHIRCodeableConcept* value_codeable_concept;
    FHIRString* value_string;
    FHIRPeriod* value_period;
} FHIRServiceRequestOrderDetail;

/* ========================================================================== */
/* ServiceRequest Resource Structure                                         */
/* ========================================================================== */

/**
 * @brief FHIR R5 ServiceRequest resource structure
 * 
 * A record of a request for service such as diagnostic investigations, treatments, or operations
 */
FHIR_RESOURCE_DEFINE(ServiceRequest)
    // ServiceRequest-specific fields
    FHIRIdentifier** identifier;
    size_t identifier_count;
    
    FHIRReference** instantiates_canonical;
    size_t instantiates_canonical_count;
    
    FHIRReference** instantiates_uri;
    size_t instantiates_uri_count;
    
    FHIRReference** based_on;
    size_t based_on_count;
    
    FHIRReference** replaces;
    size_t replaces_count;
    
    FHIRIdentifier* requisition;
    
    FHIRServiceRequestStatus status;
    
    FHIRServiceRequestIntent intent;
    
    FHIRCodeableConcept** category;
    size_t category_count;
    
    FHIRServiceRequestPriority priority;
    
    FHIRBoolean* do_not_perform;
    
    FHIRCodeableConcept* code;
    
    FHIRServiceRequestOrderDetail** order_detail;
    size_t order_detail_count;
    
    // Quantity (choice type)
    FHIRQuantity* quantity_quantity;
    FHIRRatio* quantity_ratio;
    FHIRRange* quantity_range;
    
    FHIRReference* subject;
    
    FHIRCodeableConcept* focus;
    
    FHIRReference* for_reference;
    
    FHIRReference* encounter;
    
    // Occurrence (choice type)
    FHIRDateTime* occurrence_date_time;
    FHIRPeriod* occurrence_period;
    FHIRTiming* occurrence_timing;
    
    // As needed (choice type)
    FHIRBoolean* as_needed_boolean;
    FHIRCodeableConcept* as_needed_codeable_concept;
    
    FHIRDateTime* authored_on;
    
    FHIRReference* requester;
    
    FHIRCodeableConcept* performer_type;
    
    FHIRReference** performer;
    size_t performer_count;
    
    FHIRReference** location_code;
    size_t location_code_count;
    
    FHIRReference** location_reference;
    size_t location_reference_count;
    
    FHIRCodeableConcept** reason_code;
    size_t reason_code_count;
    
    FHIRReference** reason_reference;
    size_t reason_reference_count;
    
    FHIRReference** insurance;
    size_t insurance_count;
    
    FHIRReference** supporting_info;
    size_t supporting_info_count;
    
    FHIRReference** specimen;
    size_t specimen_count;
    
    FHIRCodeableConcept** body_site;
    size_t body_site_count;
    
    FHIRCodeableConcept* body_structure;
    
    FHIRAnnotation** note;
    size_t note_count;
    
    FHIRString* patient_instruction;
    
    FHIRReference** relevant_history;
    size_t relevant_history_count;
};

/* ========================================================================== */
/* ServiceRequest Factory and Lifecycle Methods                             */
/* ========================================================================== */

/**
 * @brief Create a new ServiceRequest resource
 * @param id Resource identifier (required)
 * @return Pointer to new ServiceRequest or NULL on failure
 */
FHIRServiceRequest* fhir_servicerequest_create(const char* id);

/**
 * @brief Destroy ServiceRequest resource (virtual destructor)
 * @param self ServiceRequest to destroy
 */
void fhir_servicerequest_destroy(FHIRServiceRequest* self);

/**
 * @brief Clone ServiceRequest resource (virtual clone)
 * @param self ServiceRequest to clone
 * @return Cloned ServiceRequest or NULL on failure
 */
FHIRServiceRequest* fhir_servicerequest_clone(const FHIRServiceRequest* self);

/* ========================================================================== */
/* ServiceRequest Serialization Methods                                      */
/* ========================================================================== */

/**
 * @brief Convert ServiceRequest to JSON (virtual method)
 * @param self ServiceRequest to convert
 * @return JSON object or NULL on failure
 */
cJSON* fhir_servicerequest_to_json(const FHIRServiceRequest* self);

/**
 * @brief Load ServiceRequest from JSON (virtual method)
 * @param self ServiceRequest to populate
 * @param json JSON object
 * @return true on success, false on failure
 */
bool fhir_servicerequest_from_json(FHIRServiceRequest* self, const cJSON* json);

/**
 * @brief Parse ServiceRequest from JSON string
 * @param json_string JSON string
 * @return New ServiceRequest or NULL on failure
 */
FHIRServiceRequest* fhir_servicerequest_parse(const char* json_string);

/* ========================================================================== */
/* ServiceRequest Validation Methods                                         */
/* ========================================================================== */

/**
 * @brief Validate ServiceRequest resource (virtual method)
 * @param self ServiceRequest to validate
 * @return true if valid, false otherwise
 */
bool fhir_servicerequest_validate(const FHIRServiceRequest* self);

/* ========================================================================== */
/* ServiceRequest-Specific Methods                                           */
/* ========================================================================== */

/**
 * @brief Check if ServiceRequest is active (virtual method)
 * @param self ServiceRequest to check
 * @return true if status is active, false otherwise
 */
bool fhir_servicerequest_is_active(const FHIRServiceRequest* self);

/**
 * @brief Get ServiceRequest display name (virtual method)
 * @param self ServiceRequest to get name from
 * @return Display name or NULL
 */
const char* fhir_servicerequest_get_display_name(const FHIRServiceRequest* self);

/**
 * @brief Set ServiceRequest status
 * @param self ServiceRequest to modify
 * @param status New status
 * @return true on success, false on failure
 */
bool fhir_servicerequest_set_status(FHIRServiceRequest* self, FHIRServiceRequestStatus status);

/**
 * @brief Set ServiceRequest intent
 * @param self ServiceRequest to modify
 * @param intent New intent
 * @return true on success, false on failure
 */
bool fhir_servicerequest_set_intent(FHIRServiceRequest* self, FHIRServiceRequestIntent intent);

/**
 * @brief Set ServiceRequest priority
 * @param self ServiceRequest to modify
 * @param priority New priority
 * @return true on success, false on failure
 */
bool fhir_servicerequest_set_priority(FHIRServiceRequest* self, FHIRServiceRequestPriority priority);

/**
 * @brief Convert status enum to string
 * @param status Status enum
 * @return String representation or NULL for unknown status
 */
const char* fhir_servicerequest_status_to_string(FHIRServiceRequestStatus status);

/**
 * @brief Convert string to status enum
 * @param status_str String representation
 * @return Status enum or FHIR_SERVICEREQUEST_STATUS_UNKNOWN for invalid string
 */
FHIRServiceRequestStatus fhir_servicerequest_status_from_string(const char* status_str);

/**
 * @brief Convert intent enum to string
 * @param intent Intent enum
 * @return String representation or NULL for unknown intent
 */
const char* fhir_servicerequest_intent_to_string(FHIRServiceRequestIntent intent);

/**
 * @brief Convert string to intent enum
 * @param intent_str String representation
 * @return Intent enum or FHIR_SERVICEREQUEST_INTENT_PROPOSAL for invalid string
 */
FHIRServiceRequestIntent fhir_servicerequest_intent_from_string(const char* intent_str);

/**
 * @brief Convert priority enum to string
 * @param priority Priority enum
 * @return String representation or NULL for unknown priority
 */
const char* fhir_servicerequest_priority_to_string(FHIRServiceRequestPriority priority);

/**
 * @brief Convert string to priority enum
 * @param priority_str String representation
 * @return Priority enum or FHIR_SERVICEREQUEST_PRIORITY_ROUTINE for invalid string
 */
FHIRServiceRequestPriority fhir_servicerequest_priority_from_string(const char* priority_str);

/**
 * @brief Register ServiceRequest resource type
 * @return true on success, false on failure
 */
bool fhir_servicerequest_register(void);

#ifdef __cplusplus
}
#endif

#endif /* FHIR_SERVICEREQUEST_H */