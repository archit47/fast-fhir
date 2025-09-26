/**
 * @file fhir_biologically_derived_product.h
 * @brief FHIR R5 BiologicallyDerivedProduct resource C interface
 * @version 1.0.0
 * @date 2024-01-01
 * 
 * This header defines the C interface for the FHIR R5 BiologicallyDerivedProduct resource.
 * Follows FHIR R5 specification and C99 standards.
 */

#ifndef FHIR_BIOLOGICALLY_DERIVED_PRODUCT_H
#define FHIR_BIOLOGICALLY_DERIVED_PRODUCT_H

#include "../fhir_datatypes.h"
#include "../fhir_foundation.h"
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Processing step for BiologicallyDerivedProduct
 */
typedef struct FHIRBiologicallyDerivedProductProcessing {
    FHIRElement base;
    FHIRString* description;
    FHIRCodeableConcept* procedure;
    FHIRReference* additive;
    FHIRDateTime* time_date_time;
    FHIRPeriod* time_period;
} FHIRBiologicallyDerivedProductProcessing;

/**
 * @brief Storage requirements for BiologicallyDerivedProduct
 */
typedef struct FHIRBiologicallyDerivedProductStorage {
    FHIRElement base;
    FHIRString* description;
    FHIRDecimal* temperature;
    FHIRCode* scale;  /**< farenheit | celsius | kelvin */
    FHIRPeriod* duration;
} FHIRBiologicallyDerivedProductStorage;

/**
 * @brief FHIR R5 BiologicallyDerivedProduct resource structure
 * 
 * A material substance originating from a biological entity intended to be
 * transplanted or infused into another (possibly the same) biological entity.
 */
typedef struct FHIRBiologicallyDerivedProduct {
    /** Base domain resource */
    FHIRDomainResource domain_resource;
    
    /** Broad category of this product */
    FHIRCodeableConcept* product_category;
    
    /** A code that identifies the kind of this biologically derived product */
    FHIRCodeableConcept* product_code;
    
    /** Parent product (if any) */
    FHIRReference** parent;
    size_t parent_count;
    
    /** Procedure request */
    FHIRReference** request;
    size_t request_count;
    
    /** Business identifier */
    FHIRIdentifier** identifier;
    size_t identifier_count;
    
    /** An identifier that supports traceability to the event during which material was collected */
    FHIRString* biological_source_event;
    
    /** Any processing of the product during collection */
    FHIRBiologicallyDerivedProductProcessing** processing;
    size_t processing_count;
    
    /** Any manipulation of product post-collection */
    FHIRString* manipulation;
    
    /** Product storage */
    FHIRBiologicallyDerivedProductStorage** storage;
    size_t storage_count;
} FHIRBiologicallyDerivedProduct;

/**
 * @brief Create a new BiologicallyDerivedProduct resource
 * @param id Resource identifier (required)
 * @return Pointer to new BiologicallyDerivedProduct or NULL on failure
 */
FHIRBiologicallyDerivedProduct* fhir_biologically_derived_product_create(const char* id);

/**
 * @brief Free a BiologicallyDerivedProduct resource
 * @param product Pointer to BiologicallyDerivedProduct to free (can be NULL)
 */
void fhir_biologically_derived_product_free(FHIRBiologicallyDerivedProduct* product);

/**
 * @brief Parse BiologicallyDerivedProduct from JSON
 * @param json JSON object containing BiologicallyDerivedProduct data
 * @return Pointer to parsed BiologicallyDerivedProduct or NULL on failure
 */
FHIRBiologicallyDerivedProduct* fhir_biologically_derived_product_parse(cJSON* json);

/**
 * @brief Convert BiologicallyDerivedProduct to JSON
 * @param product BiologicallyDerivedProduct to convert
 * @return JSON object or NULL on failure
 */
cJSON* fhir_biologically_derived_product_to_json(const FHIRBiologicallyDerivedProduct* product);

/**
 * @brief Validate BiologicallyDerivedProduct resource
 * @param product BiologicallyDerivedProduct to validate
 * @return true if valid, false otherwise
 */
bool fhir_biologically_derived_product_validate(const FHIRBiologicallyDerivedProduct* product);

/**
 * @brief Add a processing step to BiologicallyDerivedProduct
 * @param product Target BiologicallyDerivedProduct
 * @param processing Processing step to add
 * @return true on success, false on failure
 */
bool fhir_biologically_derived_product_add_processing(FHIRBiologicallyDerivedProduct* product,
                                                     const FHIRBiologicallyDerivedProductProcessing* processing);

/**
 * @brief Add storage requirements to BiologicallyDerivedProduct
 * @param product Target BiologicallyDerivedProduct
 * @param storage Storage requirements to add
 * @return true on success, false on failure
 */
bool fhir_biologically_derived_product_add_storage(FHIRBiologicallyDerivedProduct* product,
                                                  const FHIRBiologicallyDerivedProductStorage* storage);

/**
 * @brief Set biological source event
 * @param product Target BiologicallyDerivedProduct
 * @param event Biological source event identifier
 * @return true on success, false on failure
 */
bool fhir_biologically_derived_product_set_biological_source_event(FHIRBiologicallyDerivedProduct* product,
                                                                  const char* event);

/**
 * @brief Get biological source event
 * @param product BiologicallyDerivedProduct to query
 * @return Biological source event identifier or NULL
 */
const char* fhir_biologically_derived_product_get_biological_source_event(const FHIRBiologicallyDerivedProduct* product);

#ifdef __cplusplus
}
#endif

#endif /* FHIR_BIOLOGICALLY_DERIVED_PRODUCT_H */