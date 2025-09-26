#ifndef FHIR_SPECIALIZED_H
#define FHIR_SPECIALIZED_H

#include "fhir_datatypes.h"
#include "fhir_foundation.h"
#include <Python.h>
#include <stdbool.h>
#include <cjson/cJSON.h>

// Specialized Resource Types - Public Health, Research, Quality Reporting, etc.

// Device Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRString* display_name;
    struct DeviceDefinition* definition;
    struct DeviceUdiCarrier** udi_carrier;
    size_t udi_carrier_count;
    FHIRCode* status;  // active | inactive | entered-in-error
    FHIRCodeableConcept** availability_status;
    size_t availability_status_count;
    FHIRString* biological_source_event;
    FHIRString* manufacturer;
    FHIRDateTime* manufacture_date;
    FHIRDateTime* expiration_date;
    FHIRString* lot_number;
    FHIRString* serial_number;
    struct DeviceName** name;
    size_t name_count;
    FHIRString* model_number;
    FHIRString* part_number;
    FHIRCodeableConcept** category;
    size_t category_count;
    FHIRCodeableConcept** type;
    size_t type_count;
    struct DeviceVersion** version;
    size_t version_count;
    struct DeviceConformsTo** conforms_to;
    size_t conforms_to_count;
    struct DeviceProperty** property;
    size_t property_count;
    FHIRCodeableConcept* mode;
    FHIRCount* cycle;
    FHIRDuration* duration;
    FHIRReference* owner;
    FHIRContactPoint** contact;
    size_t contact_count;
    FHIRReference* location;
    FHIRUri* url;
    FHIRReference* endpoint;
    FHIRCodeableConcept** gateway;
    size_t gateway_count;
    FHIRAnnotation** note;
    size_t note_count;
    FHIRCodeableConcept** safety;
    size_t safety_count;
    FHIRReference* parent;
} FHIRDevice;

// Device UDI Carrier structure
typedef struct DeviceUdiCarrier {
    FHIRElement base;
    FHIRString* device_identifier;
    FHIRUri* issuer;
    FHIRUri* jurisdiction;
    FHIRBase64Binary* carrier_aidc;
    FHIRString* carrier_hrf;
    FHIRCode* entry_type;  // barcode | rfid | manual | card | self-reported | electronic-transmission | unknown
} DeviceUdiCarrier;

// Device Name structure
typedef struct DeviceName {
    FHIRElement base;
    FHIRString* value;
    FHIRCode* type;  // registered-name | user-friendly-name | patient-reported-name
} DeviceName;

// Device Version structure
typedef struct DeviceVersion {
    FHIRElement base;
    FHIRCodeableConcept* type;
    FHIRIdentifier* component;
    FHIRString* install_date;
    FHIRString* value;
} DeviceVersion;

// Device Conforms To structure
typedef struct DeviceConformsTo {
    FHIRElement base;
    FHIRCodeableConcept* category;
    FHIRCodeableConcept* specification;
    FHIRString* version;
} DeviceConformsTo;

// Device Property structure
typedef struct DeviceProperty {
    FHIRElement base;
    FHIRCodeableConcept* type;
    FHIRQuantity** value_quantity;
    size_t value_quantity_count;
    FHIRCodeableConcept** value_codeable_concept;
    size_t value_codeable_concept_count;
    FHIRString** value_string;
    size_t value_string_count;
    FHIRBoolean** value_boolean;
    size_t value_boolean_count;
    FHIRInteger** value_integer;
    size_t value_integer_count;
    FHIRRange** value_range;
    size_t value_range_count;
    FHIRAttachment** value_attachment;
    size_t value_attachment_count;
} DeviceProperty;

// DeviceDefinition Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRString* description;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    struct DeviceDefinitionUdiDeviceIdentifier** udi_device_identifier;
    size_t udi_device_identifier_count;
    struct DeviceDefinitionRegulatoryIdentifier** regulatory_identifier;
    size_t regulatory_identifier_count;
    FHIRString* part_number;
    FHIRReference* manufacturer;
    struct DeviceDefinitionDeviceName** device_name;
    size_t device_name_count;
    FHIRString* model_number;
    struct DeviceDefinitionClassification** classification;
    size_t classification_count;
    struct DeviceDefinitionConformsTo** conforms_to;
    size_t conforms_to_count;
    struct DeviceDefinitionHasPart** has_part;
    size_t has_part_count;
    struct DeviceDefinitionPackaging** packaging;
    size_t packaging_count;
    struct DeviceDefinitionVersion** version;
    size_t version_count;
    struct DeviceDefinitionSafety** safety;
    size_t safety_count;
    struct DeviceDefinitionShelfLifeStorage** shelf_life_storage;
    size_t shelf_life_storage_count;
    FHIRString* language_code;
    struct DeviceDefinitionProperty** property;
    size_t property_count;
    FHIRReference* owner;
    FHIRContactPoint** contact;
    size_t contact_count;
    FHIRUri* online_information;
    FHIRAnnotation** note;
    size_t note_count;
    FHIRQuantity* quantity;
    FHIRReference* parent_device;
    struct DeviceDefinitionMaterial** material;
    size_t material_count;
    struct DeviceDefinitionProductionIdentifierInUDI** production_identifier_in_udi;
    size_t production_identifier_in_udi_count;
    FHIRCode* guideline;
    struct DeviceDefinitionCorrectiveAction* corrective_action;
    struct DeviceDefinitionChargeItem** charge_item;
    size_t charge_item_count;
} FHIRDeviceDefinition;

// DeviceDefinition UDI Device Identifier structure
typedef struct DeviceDefinitionUdiDeviceIdentifier {
    FHIRElement base;
    FHIRString* device_identifier;
    FHIRUri* issuer;
    FHIRUri* jurisdiction;
    struct DeviceDefinitionUdiDeviceIdentifierMarketDistribution** market_distribution;
    size_t market_distribution_count;
} DeviceDefinitionUdiDeviceIdentifier;

// DeviceDefinition UDI Device Identifier Market Distribution structure
typedef struct DeviceDefinitionUdiDeviceIdentifierMarketDistribution {
    FHIRElement base;
    FHIRPeriod* market_period;
    FHIRString* sub_jurisdiction;
} DeviceDefinitionUdiDeviceIdentifierMarketDistribution;

// DeviceDefinition Regulatory Identifier structure
typedef struct DeviceDefinitionRegulatoryIdentifier {
    FHIRElement base;
    FHIRCode* type;  // basic | master | license
    FHIRString* device_identifier;
    FHIRUri* issuer;
    FHIRUri* jurisdiction;
} DeviceDefinitionRegulatoryIdentifier;

// DeviceDefinition Device Name structure
typedef struct DeviceDefinitionDeviceName {
    FHIRElement base;
    FHIRString* name;
    FHIRCode* type;  // registered-name | user-friendly-name | patient-reported-name
} DeviceDefinitionDeviceName;

// DeviceDefinition Classification structure
typedef struct DeviceDefinitionClassification {
    FHIRElement base;
    FHIRCodeableConcept* type;
    FHIRString* justification;
} DeviceDefinitionClassification;

// DeviceDefinition Conforms To structure
typedef struct DeviceDefinitionConformsTo {
    FHIRElement base;
    FHIRCodeableConcept* category;
    FHIRCodeableConcept* specification;
    FHIRString* version;
    FHIRReference** source;
    size_t source_count;
} DeviceDefinitionConformsTo;

// DeviceDefinition Has Part structure
typedef struct DeviceDefinitionHasPart {
    FHIRElement base;
    FHIRReference* reference;
    FHIRInteger* count;
} DeviceDefinitionHasPart;

// DeviceDefinition Packaging structure
typedef struct DeviceDefinitionPackaging {
    FHIRElement base;
    FHIRIdentifier* identifier;
    FHIRCodeableConcept* type;
    FHIRInteger* count;
    struct DeviceDefinitionPackagingDistributor** distributor;
    size_t distributor_count;
    struct DeviceDefinitionPackaging** packaging;
    size_t packaging_count;
} DeviceDefinitionPackaging;

// DeviceDefinition Packaging Distributor structure
typedef struct DeviceDefinitionPackagingDistributor {
    FHIRElement base;
    FHIRString* name;
    FHIRString** organization_reference;
    size_t organization_reference_count;
} DeviceDefinitionPackagingDistributor;

// DeviceDefinition Version structure
typedef struct DeviceDefinitionVersion {
    FHIRElement base;
    FHIRCodeableConcept* type;
    FHIRIdentifier* component;
    FHIRString* install_date;
    FHIRString* value;
} DeviceDefinitionVersion;

// DeviceDefinition Safety structure
typedef struct DeviceDefinitionSafety {
    FHIRElement base;
    FHIRCodeableConcept* category;
} DeviceDefinitionSafety;

// DeviceDefinition Shelf Life Storage structure
typedef struct DeviceDefinitionShelfLifeStorage {
    FHIRElement base;
    FHIRCodeableConcept* type;
    FHIRPeriod* period;
    FHIRCodeableConcept** special_precautions_for_storage;
    size_t special_precautions_for_storage_count;
} DeviceDefinitionShelfLifeStorage;

// DeviceDefinition Property structure
typedef struct DeviceDefinitionProperty {
    FHIRElement base;
    FHIRCodeableConcept* type;
    FHIRQuantity** value_quantity;
    size_t value_quantity_count;
    FHIRCodeableConcept** value_codeable_concept;
    size_t value_codeable_concept_count;
    FHIRString** value_string;
    size_t value_string_count;
    FHIRBoolean** value_boolean;
    size_t value_boolean_count;
    FHIRInteger** value_integer;
    size_t value_integer_count;
    FHIRRange** value_range;
    size_t value_range_count;
    FHIRAttachment** value_attachment;
    size_t value_attachment_count;
} DeviceDefinitionProperty;

// DeviceDefinition Material structure
typedef struct DeviceDefinitionMaterial {
    FHIRElement base;
    FHIRCodeableConcept* substance;
    FHIRBoolean* alternate;
    FHIRBoolean* allergenic_indicator;
} DeviceDefinitionMaterial;

// DeviceDefinition Production Identifier In UDI structure
typedef struct DeviceDefinitionProductionIdentifierInUDI {
    FHIRElement base;
    FHIRCode* type;  // lot-number | manufactured-date | serial-number | expiration-date | biological-source | software-version
    FHIRBoolean* assigned;
} DeviceDefinitionProductionIdentifierInUDI;

// DeviceDefinition Corrective Action structure
typedef struct DeviceDefinitionCorrectiveAction {
    FHIRElement base;
    FHIRBoolean* recall;
    FHIRCodeableConcept* scope;
    FHIRPeriod* period;
} DeviceDefinitionCorrectiveAction;

// DeviceDefinition Charge Item structure
typedef struct DeviceDefinitionChargeItem {
    FHIRElement base;
    FHIRCodeableConcept* charge_item_code;
    FHIRQuantity* count;
    FHIRPeriod* effective_period;
    FHIRReference** use_context;
    size_t use_context_count;
} DeviceDefinitionChargeItem;

// Specimen Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRIdentifier* accession_identifier;
    FHIRCode* status;  // available | unavailable | unsatisfactory | entered-in-error
    FHIRCodeableConcept* type;
    FHIRReference* subject;
    FHIRDateTime* received_time;
    FHIRReference** parent;
    size_t parent_count;
    FHIRReference** request;
    size_t request_count;
    FHIRCode* combined;  // grouped | pooled
    FHIRCodeableConcept** role;
    size_t role_count;
    struct SpecimenFeature** feature;
    size_t feature_count;
    struct SpecimenCollection* collection;
    struct SpecimenProcessing** processing;
    size_t processing_count;
    struct SpecimenContainer** container;
    size_t container_count;
    FHIRCodeableConcept** condition;
    size_t condition_count;
    FHIRAnnotation** note;
    size_t note_count;
} FHIRSpecimen;

// Specimen Feature structure
typedef struct SpecimenFeature {
    FHIRElement base;
    FHIRCodeableConcept* type;
    FHIRString* description;
} SpecimenFeature;

// Specimen Collection structure
typedef struct SpecimenCollection {
    FHIRElement base;
    FHIRReference* collector;
    FHIRDateTime* collected_date_time;
    FHIRPeriod* collected_period;
    FHIRDuration* duration;
    FHIRQuantity* quantity;
    FHIRCodeableConcept* method;
    FHIRReference* device;
    struct SpecimenCollectionBodySite* body_site;
    FHIRCodeableConcept* fastingStatus;
} SpecimenCollection;

// Specimen Collection Body Site structure
typedef struct SpecimenCollectionBodySite {
    FHIRElement base;
    FHIRCodeableConcept* site;
    FHIRCodeableConcept** qualifier;
    size_t qualifier_count;
    FHIRString* text;
} SpecimenCollectionBodySite;

// Specimen Processing structure
typedef struct SpecimenProcessing {
    FHIRElement base;
    FHIRString* description;
    FHIRCodeableConcept* method;
    FHIRReference** additive;
    size_t additive_count;
    FHIRDateTime* time_date_time;
    FHIRPeriod* time_period;
} SpecimenProcessing;

// Specimen Container structure
typedef struct SpecimenContainer {
    FHIRElement base;
    FHIRReference* device;
    FHIRReference* location;
    FHIRQuantity* specimen_quantity;
} SpecimenContainer;

// BiologicallyDerivedProduct Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRCodeableConcept* product_category;
    FHIRCodeableConcept* product_code;
    FHIRReference** parent;
    size_t parent_count;
    FHIRReference** request;
    size_t request_count;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRString* biological_source_event;
    struct BiologicallyDerivedProductProcessing** processing;
    size_t processing_count;
    FHIRString* manipulation;
    struct BiologicallyDerivedProductStorage** storage;
    size_t storage_count;
} FHIRBiologicallyDerivedProduct;

// BiologicallyDerivedProduct Processing structure
typedef struct BiologicallyDerivedProductProcessing {
    FHIRElement base;
    FHIRString* description;
    FHIRCodeableConcept* procedure;
    FHIRReference* additive;
    FHIRDateTime* time_date_time;
    FHIRPeriod* time_period;
} BiologicallyDerivedProductProcessing;

// BiologicallyDerivedProduct Storage structure
typedef struct BiologicallyDerivedProductStorage {
    FHIRElement base;
    FHIRString* description;
    FHIRDecimal* temperature;
    FHIRCode* scale;  // farenheit | celsius | kelvin
    FHIRPeriod* duration;
} BiologicallyDerivedProductStorage;

// DeviceMetric Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCodeableConcept* type;
    FHIRCodeableConcept* unit;
    FHIRReference* source;
    FHIRReference* parent;
    FHIRCode* operational_status;  // on | off | standby | entered-in-error
    FHIRCode* color;  // black | red | green | yellow | blue | magenta | cyan | white
    FHIRCode* category;  // measurement | setting | calculation | unspecified
    FHIRTiming* measurement_period;
    struct DeviceMetricCalibration** calibration;
    size_t calibration_count;
} FHIRDeviceMetric;

// DeviceMetric Calibration structure
typedef struct DeviceMetricCalibration {
    FHIRElement base;
    FHIRCode* type;  // unspecified | offset | gain | two-point
    FHIRCode* state;  // not-calibrated | calibration-required | calibrated | unspecified
    FHIRInstant* time;
} DeviceMetricCalibration;

// NutritionProduct Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRCode* status;  // active | inactive | entered-in-error
    FHIRCodeableConcept** category;
    size_t category_count;
    FHIRCodeableConcept* code;
    FHIRString* manufacturer;
    struct NutritionProductNutrient** nutrient;
    size_t nutrient_count;
    struct NutritionProductIngredient** ingredient;
    size_t ingredient_count;
    FHIRReference** known_allergen;
    size_t known_allergen_count;
    struct NutritionProductCharacteristic** characteristic;
    size_t characteristic_count;
    struct NutritionProductInstance** instance;
    size_t instance_count;
    FHIRAnnotation** note;
    size_t note_count;
} FHIRNutritionProduct;

// NutritionProduct Nutrient structure
typedef struct NutritionProductNutrient {
    FHIRElement base;
    FHIRCodeableConcept* item;
    FHIRRatio** amount;
    size_t amount_count;
} NutritionProductNutrient;

// NutritionProduct Ingredient structure
typedef struct NutritionProductIngredient {
    FHIRElement base;
    FHIRCodeableConcept* item;
    FHIRRatio** amount;
    size_t amount_count;
} NutritionProductIngredient;

// NutritionProduct Characteristic structure
typedef struct NutritionProductCharacteristic {
    FHIRElement base;
    FHIRCodeableConcept* type;
    FHIRCodeableConcept* value_codeable_concept;
    FHIRString* value_string;
    FHIRQuantity* value_quantity;
    FHIRBase64Binary* value_base64_binary;
    FHIRAttachment* value_attachment;
    FHIRBoolean* value_boolean;
} NutritionProductCharacteristic;

// NutritionProduct Instance structure
typedef struct NutritionProductInstance {
    FHIRElement base;
    FHIRQuantity* quantity;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRString* lot_number;
    FHIRDateTime* expiry;
    FHIRDateTime* use_by;
    FHIRCodeableConcept* biological_source_event;
} NutritionProductInstance;

// VerificationResult Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRReference** target;
    size_t target_count;
    FHIRString** target_location;
    size_t target_location_count;
    FHIRCodeableConcept* need;
    FHIRCode* status;  // attested | validated | in-process | req-revalid | val-fail | reval-fail
    FHIRDateTime* status_date;
    FHIRCodeableConcept* validation_type;
    FHIRCodeableConcept** validation_process;
    size_t validation_process_count;
    FHIRTiming* frequency;
    FHIRDateTime* last_performed;
    FHIRDate* next_scheduled;
    FHIRCodeableConcept* failure_action;
    struct VerificationResultPrimarySource** primary_source;
    size_t primary_source_count;
    struct VerificationResultAttestation* attestation;
    struct VerificationResultValidator** validator;
    size_t validator_count;
} FHIRVerificationResult;

// VerificationResult Primary Source structure
typedef struct VerificationResultPrimarySource {
    FHIRElement base;
    FHIRReference* who;
    FHIRCodeableConcept** type;
    size_t type_count;
    FHIRCodeableConcept** communication_method;
    size_t communication_method_count;
    FHIRCodeableConcept* validation_status;
    FHIRDateTime* validation_date;
    FHIRCodeableConcept* can_push_updates;
    FHIRCodeableConcept** push_type_available;
    size_t push_type_available_count;
} VerificationResultPrimarySource;

// VerificationResult Attestation structure
typedef struct VerificationResultAttestation {
    FHIRElement base;
    FHIRReference* who;
    FHIRReference* on_behalf_of;
    FHIRCodeableConcept* communication_method;
    FHIRDate* date;
    FHIRString* source_identity_certificate;
    FHIRString* proxy_identity_certificate;
    FHIRSignature* proxy_signature;
    FHIRSignature* source_signature;
} VerificationResultAttestation;

// VerificationResult Validator structure
typedef struct VerificationResultValidator {
    FHIRElement base;
    FHIRReference* organization;
    FHIRString* identity_certificate;
    FHIRSignature* attestation_signature;
} VerificationResultValidator;

// Function declarations for Specialized resources

// Device functions
FHIRDevice* fhir_device_create(const char* id);
void fhir_device_free(FHIRDevice* device);
FHIRDevice* fhir_parse_device(cJSON* json);
cJSON* fhir_device_to_json(const FHIRDevice* device);
bool fhir_validate_device(const FHIRDevice* device);

// DeviceDefinition functions
FHIRDeviceDefinition* fhir_device_definition_create(const char* id);
void fhir_device_definition_free(FHIRDeviceDefinition* device_definition);
FHIRDeviceDefinition* fhir_parse_device_definition(cJSON* json);
cJSON* fhir_device_definition_to_json(const FHIRDeviceDefinition* device_definition);
bool fhir_validate_device_definition(const FHIRDeviceDefinition* device_definition);

// Specimen functions
FHIRSpecimen* fhir_specimen_create(const char* id);
void fhir_specimen_free(FHIRSpecimen* specimen);
FHIRSpecimen* fhir_parse_specimen(cJSON* json);
cJSON* fhir_specimen_to_json(const FHIRSpecimen* specimen);
bool fhir_validate_specimen(const FHIRSpecimen* specimen);

// BiologicallyDerivedProduct functions
FHIRBiologicallyDerivedProduct* fhir_biologically_derived_product_create(const char* id);
void fhir_biologically_derived_product_free(FHIRBiologicallyDerivedProduct* product);
FHIRBiologicallyDerivedProduct* fhir_parse_biologically_derived_product(cJSON* json);
cJSON* fhir_biologically_derived_product_to_json(const FHIRBiologicallyDerivedProduct* product);
bool fhir_validate_biologically_derived_product(const FHIRBiologicallyDerivedProduct* product);

// DeviceMetric functions
FHIRDeviceMetric* fhir_device_metric_create(const char* id);
void fhir_device_metric_free(FHIRDeviceMetric* device_metric);
FHIRDeviceMetric* fhir_parse_device_metric(cJSON* json);
cJSON* fhir_device_metric_to_json(const FHIRDeviceMetric* device_metric);
bool fhir_validate_device_metric(const FHIRDeviceMetric* device_metric);

// NutritionProduct functions
FHIRNutritionProduct* fhir_nutrition_product_create(const char* id);
void fhir_nutrition_product_free(FHIRNutritionProduct* nutrition_product);
FHIRNutritionProduct* fhir_parse_nutrition_product(cJSON* json);
cJSON* fhir_nutrition_product_to_json(const FHIRNutritionProduct* nutrition_product);
bool fhir_validate_nutrition_product(const FHIRNutritionProduct* nutrition_product);

// VerificationResult functions
FHIRVerificationResult* fhir_verification_result_create(const char* id);
void fhir_verification_result_free(FHIRVerificationResult* verification_result);
FHIRVerificationResult* fhir_parse_verification_result(cJSON* json);
cJSON* fhir_verification_result_to_json(const FHIRVerificationResult* verification_result);
bool fhir_validate_verification_result(const FHIRVerificationResult* verification_result);

// Utility functions for Specialized resources
bool fhir_is_specialized_resource(const char* resource_type);
bool fhir_is_active_device(const FHIRDevice* device);
char* fhir_get_device_display_name(const FHIRDevice* device);
bool fhir_is_available_specimen(const FHIRSpecimen* specimen);
bool fhir_is_active_nutrition_product(const FHIRNutritionProduct* product);
bool fhir_is_validated_verification_result(const FHIRVerificationResult* result);

#endif // FHIR_SPECIALIZED_H