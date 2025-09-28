/**
 * @file fhir_nutritionorder.h
 * @brief FHIR R5 NutritionOrder resource C interface with OOP principles
 * @version 0.1.0
 * @date 2024-01-01
 * 
 * A request to supply a diet, formula feeding (enteral) or oral nutritional supplement to a patient/resident
 */

#ifndef FHIR_NUTRITIONORDER_H
#define FHIR_NUTRITIONORDER_H

#include "../common/fhir_resource_base.h"
#include "../fhir_datatypes.h"
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================== */
/* NutritionOrder-Specific Enumerations                                      */
/* ========================================================================== */

/**
 * @brief NutritionOrder status enumeration
 */
typedef enum {
    FHIR_NUTRITIONORDER_STATUS_DRAFT = 0,
    FHIR_NUTRITIONORDER_STATUS_ACTIVE,
    FHIR_NUTRITIONORDER_STATUS_ON_HOLD,
    FHIR_NUTRITIONORDER_STATUS_REVOKED,
    FHIR_NUTRITIONORDER_STATUS_COMPLETED,
    FHIR_NUTRITIONORDER_STATUS_ENTERED_IN_ERROR,
    FHIR_NUTRITIONORDER_STATUS_UNKNOWN
} FHIRNutritionOrderStatus;

/**
 * @brief NutritionOrder intent enumeration
 */
typedef enum {
    FHIR_NUTRITIONORDER_INTENT_PROPOSAL = 0,
    FHIR_NUTRITIONORDER_INTENT_PLAN,
    FHIR_NUTRITIONORDER_INTENT_DIRECTIVE,
    FHIR_NUTRITIONORDER_INTENT_ORDER,
    FHIR_NUTRITIONORDER_INTENT_ORIGINAL_ORDER,
    FHIR_NUTRITIONORDER_INTENT_REFLEX_ORDER,
    FHIR_NUTRITIONORDER_INTENT_FILLER_ORDER,
    FHIR_NUTRITIONORDER_INTENT_INSTANCE_ORDER,
    FHIR_NUTRITIONORDER_INTENT_OPTION
} FHIRNutritionOrderIntent;

/* ========================================================================== */
/* NutritionOrder Sub-structures                                             */
/* ========================================================================== */

/**
 * @brief NutritionOrder oral diet nutrient information
 */
typedef struct FHIRNutritionOrderOralDietNutrient {
    FHIRElement base;
    FHIRCodeableConcept* modifier;
    FHIRQuantity* amount;
} FHIRNutritionOrderOralDietNutrient;

/**
 * @brief NutritionOrder oral diet texture information
 */
typedef struct FHIRNutritionOrderOralDietTexture {
    FHIRElement base;
    FHIRCodeableConcept* modifier;
    FHIRCodeableConcept* food_type;
} FHIRNutritionOrderOralDietTexture;

/**
 * @brief NutritionOrder oral diet information
 */
typedef struct FHIRNutritionOrderOralDiet {
    FHIRElement base;
    FHIRCodeableConcept** type;
    size_t type_count;
    FHIRTiming** schedule;
    size_t schedule_count;
    FHIRNutritionOrderOralDietNutrient** nutrient;
    size_t nutrient_count;
    FHIRNutritionOrderOralDietTexture** texture;
    size_t texture_count;
    FHIRCodeableConcept** fluid_consistency_type;
    size_t fluid_consistency_type_count;
    FHIRString* instruction;
} FHIRNutritionOrderOralDiet;

/**
 * @brief NutritionOrder supplement information
 */
typedef struct FHIRNutritionOrderSupplement {
    FHIRElement base;
    FHIRCodeableConcept* type;
    FHIRString* product_name;
    FHIRTiming** schedule;
    size_t schedule_count;
    FHIRQuantity* quantity;
    FHIRString* instruction;
} FHIRNutritionOrderSupplement;

/**
 * @brief NutritionOrder enteral formula additive information
 */
typedef struct FHIRNutritionOrderEnteralFormulaAdditive {
    FHIRElement base;
    FHIRCodeableConcept* type;
    FHIRString* product_name;
    FHIRQuantity* quantity;
} FHIRNutritionOrderEnteralFormulaAdditive;

/**
 * @brief NutritionOrder enteral formula administration information
 */
typedef struct FHIRNutritionOrderEnteralFormulaAdministration {
    FHIRElement base;
    FHIRTiming* schedule;
    FHIRQuantity* quantity;
    FHIRQuantity* rate_quantity;
    FHIRRatio* rate_ratio;
} FHIRNutritionOrderEnteralFormulaAdministration;

/**
 * @brief NutritionOrder enteral formula information
 */
typedef struct FHIRNutritionOrderEnteralFormula {
    FHIRElement base;
    FHIRCodeableConcept* base_formula_type;
    FHIRString* base_formula_product_name;
    FHIRNutritionOrderEnteralFormulaAdditive** additive;
    size_t additive_count;
    FHIRQuantity* caloric_density;
    FHIRCodeableConcept* routeof_administration;
    FHIRNutritionOrderEnteralFormulaAdministration** administration;
    size_t administration_count;
    FHIRQuantity* max_volume_to_deliver;
    FHIRString* administration_instruction;
} FHIRNutritionOrderEnteralFormula;

/* ========================================================================== */
/* NutritionOrder Resource Structure                                         */
/* ========================================================================== */

/**
 * @brief FHIR R5 NutritionOrder resource structure
 * 
 * A request to supply a diet, formula feeding or oral nutritional supplement
 */
FHIR_RESOURCE_DEFINE(NutritionOrder)
    // NutritionOrder-specific fields
    FHIRIdentifier** identifier;
    size_t identifier_count;
    
    FHIRReference** instantiates_canonical;
    size_t instantiates_canonical_count;
    
    FHIRReference** instantiates_uri;
    size_t instantiates_uri_count;
    
    FHIRReference** based_on;
    size_t based_on_count;
    
    FHIRIdentifier* group_identifier;
    
    FHIRNutritionOrderStatus status;
    
    FHIRNutritionOrderIntent intent;
    
    FHIRCodeableConcept* priority;
    
    FHIRReference* subject;
    
    FHIRReference* encounter;
    
    FHIRReference** supporting_information;
    size_t supporting_information_count;
    
    FHIRDateTime* date_time;
    
    FHIRReference* orderer;
    
    FHIRReference** performer;
    size_t performer_count;
    
    FHIRReference** allergy_intolerance;
    size_t allergy_intolerance_count;
    
    FHIRCodeableConcept** food_preference_modifier;
    size_t food_preference_modifier_count;
    
    FHIRCodeableConcept** exclude_food_modifier;
    size_t exclude_food_modifier_count;
    
    FHIRBoolean* outside_food_allowed;
    
    FHIRNutritionOrderOralDiet* oral_diet;
    
    FHIRNutritionOrderSupplement** supplement;
    size_t supplement_count;
    
    FHIRNutritionOrderEnteralFormula* enteral_formula;
    
    FHIRAnnotation** note;
    size_t note_count;
};

/* ========================================================================== */
/* NutritionOrder Factory and Lifecycle Methods                             */
/* ========================================================================== */

/**
 * @brief Create a new NutritionOrder resource
 * @param id Resource identifier (required)
 * @return Pointer to new NutritionOrder or NULL on failure
 */
FHIRNutritionOrder* fhir_nutritionorder_create(const char* id);

/**
 * @brief Destroy NutritionOrder resource (virtual destructor)
 * @param self NutritionOrder to destroy
 */
void fhir_nutritionorder_destroy(FHIRNutritionOrder* self);

/**
 * @brief Clone NutritionOrder resource (virtual clone)
 * @param self NutritionOrder to clone
 * @return Cloned NutritionOrder or NULL on failure
 */
FHIRNutritionOrder* fhir_nutritionorder_clone(const FHIRNutritionOrder* self);

/* ========================================================================== */
/* NutritionOrder Serialization Methods                                      */
/* ========================================================================== */

/**
 * @brief Convert NutritionOrder to JSON (virtual method)
 * @param self NutritionOrder to convert
 * @return JSON object or NULL on failure
 */
cJSON* fhir_nutritionorder_to_json(const FHIRNutritionOrder* self);

/**
 * @brief Load NutritionOrder from JSON (virtual method)
 * @param self NutritionOrder to populate
 * @param json JSON object
 * @return true on success, false on failure
 */
bool fhir_nutritionorder_from_json(FHIRNutritionOrder* self, const cJSON* json);

/**
 * @brief Parse NutritionOrder from JSON string
 * @param json_string JSON string
 * @return New NutritionOrder or NULL on failure
 */
FHIRNutritionOrder* fhir_nutritionorder_parse(const char* json_string);

/* ========================================================================== */
/* NutritionOrder Validation Methods                                         */
/* ========================================================================== */

/**
 * @brief Validate NutritionOrder resource (virtual method)
 * @param self NutritionOrder to validate
 * @return true if valid, false otherwise
 */
bool fhir_nutritionorder_validate(const FHIRNutritionOrder* self);

/* ========================================================================== */
/* NutritionOrder-Specific Methods                                           */
/* ========================================================================== */

/**
 * @brief Check if NutritionOrder is active (virtual method)
 * @param self NutritionOrder to check
 * @return true if status is active, false otherwise
 */
bool fhir_nutritionorder_is_active(const FHIRNutritionOrder* self);

/**
 * @brief Get NutritionOrder display name (virtual method)
 * @param self NutritionOrder to get name from
 * @return Display name or NULL
 */
const char* fhir_nutritionorder_get_display_name(const FHIRNutritionOrder* self);

/**
 * @brief Set NutritionOrder status
 * @param self NutritionOrder to modify
 * @param status New status
 * @return true on success, false on failure
 */
bool fhir_nutritionorder_set_status(FHIRNutritionOrder* self, FHIRNutritionOrderStatus status);

/**
 * @brief Set NutritionOrder intent
 * @param self NutritionOrder to modify
 * @param intent New intent
 * @return true on success, false on failure
 */
bool fhir_nutritionorder_set_intent(FHIRNutritionOrder* self, FHIRNutritionOrderIntent intent);

/**
 * @brief Add supplement to NutritionOrder
 * @param self NutritionOrder to modify
 * @param supplement Supplement to add
 * @return true on success, false on failure
 */
bool fhir_nutritionorder_add_supplement(FHIRNutritionOrder* self, const FHIRNutritionOrderSupplement* supplement);

/**
 * @brief Convert status enum to string
 * @param status Status enum
 * @return String representation or NULL for unknown status
 */
const char* fhir_nutritionorder_status_to_string(FHIRNutritionOrderStatus status);

/**
 * @brief Convert string to status enum
 * @param status_str String representation
 * @return Status enum or FHIR_NUTRITIONORDER_STATUS_UNKNOWN for invalid string
 */
FHIRNutritionOrderStatus fhir_nutritionorder_status_from_string(const char* status_str);

/**
 * @brief Convert intent enum to string
 * @param intent Intent enum
 * @return String representation or NULL for unknown intent
 */
const char* fhir_nutritionorder_intent_to_string(FHIRNutritionOrderIntent intent);

/**
 * @brief Convert string to intent enum
 * @param intent_str String representation
 * @return Intent enum or FHIR_NUTRITIONORDER_INTENT_PROPOSAL for invalid string
 */
FHIRNutritionOrderIntent fhir_nutritionorder_intent_from_string(const char* intent_str);

/**
 * @brief Register NutritionOrder resource type
 * @return true on success, false on failure
 */
bool fhir_nutritionorder_register(void);

#ifdef __cplusplus
}
#endif

#endif /* FHIR_NUTRITIONORDER_H */