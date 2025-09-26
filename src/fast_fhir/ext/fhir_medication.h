#ifndef FHIR_MEDICATION_H
#define FHIR_MEDICATION_H

#include "fhir_datatypes.h"
#include "fhir_foundation.h"
#include <Python.h>
#include <stdbool.h>
#include <cjson/cJSON.h>

// Medication and Pharmacy Resource Types

// Medication Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCodeableConcept* code;
    FHIRCode* status;  // active | inactive | entered-in-error
    FHIRReference* market_authorization_holder;
    FHIRCodeableConcept* dose_form;
    FHIRRatio* total_volume;
    struct MedicationIngredient** ingredient;
    size_t ingredient_count;
    struct MedicationBatch* batch;
    FHIRReference* definition;
} FHIRMedication;

// Medication Ingredient structure
typedef struct MedicationIngredient {
    FHIRElement base;
    FHIRCodeableConcept* item;
    FHIRBoolean* is_active;
    FHIRRatio* strength_ratio;
    FHIRCodeableConcept* strength_codeable_concept;
    FHIRQuantity* strength_quantity;
} MedicationIngredient;

// Medication Batch structure
typedef struct MedicationBatch {
    FHIRElement base;
    FHIRString* lot_number;
    FHIRDateTime* expiration_date;
} MedicationBatch;

// MedicationRequest Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCanonical** instantiates_canonical;
    size_t instantiates_canonical_count;
    FHIRUri** instantiates_uri;
    size_t instantiates_uri_count;
    FHIRReference** based_on;
    size_t based_on_count;
    FHIRReference* group_identifier;
    FHIRCode* status;  // active | on-hold | cancelled | completed | entered-in-error | stopped | draft | unknown
    FHIRCodeableConcept* status_reason;
    FHIRCode* intent;  // proposal | plan | order | original-order | reflex-order | filler-order | instance-order | option
    FHIRCodeableConcept** category;
    size_t category_count;
    FHIRCode* priority;  // routine | urgent | asap | stat
    FHIRBoolean* do_not_perform;
    FHIRCodeableConcept* medication_codeable_concept;
    FHIRReference* medication_reference;
    FHIRReference* subject;
    FHIRReference* informational_source;
    FHIRReference* encounter;
    FHIRReference** supporting_information;
    size_t supporting_information_count;
    FHIRDateTime* authored_on;
    FHIRReference* requester;
    FHIRBoolean* reported_boolean;
    FHIRReference* reported_reference;
    FHIRCodeableConcept* performer_type;
    FHIRReference* performer;
    FHIRReference* recorder;
    FHIRCodeableConcept** reason_code;
    size_t reason_code_count;
    FHIRReference** reason_reference;
    size_t reason_reference_count;
    FHIRCanonical** instantiates_canonical_course_of_therapy;
    size_t instantiates_canonical_course_of_therapy_count;
    FHIRUri** instantiates_uri_course_of_therapy;
    size_t instantiates_uri_course_of_therapy_count;
    FHIRCodeableConcept* course_of_therapy_type;
    FHIRReference** insurance;
    size_t insurance_count;
    FHIRAnnotation** note;
    size_t note_count;
    FHIRDosage** dosage_instruction;
    size_t dosage_instruction_count;
    struct MedicationRequestDispenseRequest* dispense_request;
    struct MedicationRequestSubstitution* substitution;
    FHIRReference** event_history;
    size_t event_history_count;
} FHIRMedicationRequest;

// MedicationRequest Dispense Request structure
typedef struct MedicationRequestDispenseRequest {
    FHIRElement base;
    struct MedicationRequestDispenseRequestInitialFill* initial_fill;
    FHIRDuration* dispense_interval;
    FHIRPeriod* validity_period;
    FHIRUnsignedInt* number_of_repeats_allowed;
    FHIRQuantity* quantity;
    FHIRDuration* expected_supply_duration;
    FHIRReference* performer;
} MedicationRequestDispenseRequest;

// MedicationRequest Dispense Request Initial Fill structure
typedef struct MedicationRequestDispenseRequestInitialFill {
    FHIRElement base;
    FHIRQuantity* quantity;
    FHIRDuration* duration;
} MedicationRequestDispenseRequestInitialFill;

// MedicationRequest Substitution structure
typedef struct MedicationRequestSubstitution {
    FHIRElement base;
    FHIRBoolean* allowed_boolean;
    FHIRCodeableConcept* allowed_codeable_concept;
    FHIRCodeableConcept* reason;
} MedicationRequestSubstitution;

// MedicationDispense Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRReference** part_of;
    size_t part_of_count;
    FHIRCode* status;  // preparation | in-progress | cancelled | on-hold | completed | entered-in-error | stopped | declined | unknown
    FHIRCodeableConcept* status_reason_codeable_concept;
    FHIRReference* status_reason_reference;
    FHIRCodeableConcept** category;
    size_t category_count;
    FHIRCodeableConcept* medication_codeable_concept;
    FHIRReference* medication_reference;
    FHIRReference* subject;
    FHIRReference* encounter;
    FHIRReference** supporting_information;
    size_t supporting_information_count;
    struct MedicationDispensePerformer** performer;
    size_t performer_count;
    FHIRReference* location;
    FHIRReference** authorizingPrescription;
    size_t authorizingPrescription_count;
    FHIRCodeableConcept* type;
    FHIRQuantity* quantity;
    FHIRQuantity* days_supply;
    FHIRDateTime* when_prepared;
    FHIRDateTime* when_handed_over;
    FHIRReference* destination;
    FHIRReference** receiver;
    size_t receiver_count;
    FHIRAnnotation** note;
    size_t note_count;
    FHIRDosage** dosage_instruction;
    size_t dosage_instruction_count;
    struct MedicationDispenseSubstitution* substitution;
    FHIRReference** detected_issue;
    size_t detected_issue_count;
    FHIRReference** event_history;
    size_t event_history_count;
} FHIRMedicationDispense;

// MedicationDispense Performer structure
typedef struct MedicationDispensePerformer {
    FHIRElement base;
    FHIRCodeableConcept* function;
    FHIRReference* actor;
} MedicationDispensePerformer;

// MedicationDispense Substitution structure
typedef struct MedicationDispenseSubstitution {
    FHIRElement base;
    FHIRBoolean* was_substituted;
    FHIRCodeableConcept* type;
    FHIRCodeableConcept** reason;
    size_t reason_count;
    FHIRReference** responsible_party;
    size_t responsible_party_count;
} MedicationDispenseSubstitution;

// MedicationAdministration Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCanonical** instantiates_canonical;
    size_t instantiates_canonical_count;
    FHIRUri** instantiates_uri;
    size_t instantiates_uri_count;
    FHIRReference** based_on;
    size_t based_on_count;
    FHIRReference** part_of;
    size_t part_of_count;
    FHIRCode* status;  // in-progress | not-done | on-hold | completed | entered-in-error | stopped | unknown
    FHIRCodeableConcept** status_reason;
    size_t status_reason_count;
    FHIRCodeableConcept** category;
    size_t category_count;
    FHIRCodeableConcept* medication_codeable_concept;
    FHIRReference* medication_reference;
    FHIRReference* subject;
    FHIRReference* encounter;
    FHIRReference** supporting_information;
    size_t supporting_information_count;
    FHIRDateTime* occurrence_date_time;
    FHIRPeriod* occurrence_period;
    FHIRTiming* occurrence_timing;
    FHIRBoolean* recorded;
    FHIRBoolean* reported_boolean;
    FHIRReference* reported_reference;
    struct MedicationAdministrationPerformer** performer;
    size_t performer_count;
    FHIRCodeableConcept** reason_code;
    size_t reason_code_count;
    FHIRReference** reason_reference;
    size_t reason_reference_count;
    FHIRReference* request;
    FHIRReference** device;
    size_t device_count;
    FHIRAnnotation** note;
    size_t note_count;
    FHIRDosage* dosage;
    FHIRReference** event_history;
    size_t event_history_count;
} FHIRMedicationAdministration;

// MedicationAdministration Performer structure
typedef struct MedicationAdministrationPerformer {
    FHIRElement base;
    FHIRCodeableConcept* function;
    FHIRReference* actor;
} MedicationAdministrationPerformer;

// MedicationStatement Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCanonical** instantiates_canonical;
    size_t instantiates_canonical_count;
    FHIRUri** instantiates_uri;
    size_t instantiates_uri_count;
    FHIRReference** based_on;
    size_t based_on_count;
    FHIRReference** part_of;
    size_t part_of_count;
    FHIRCode* status;  // recorded | entered-in-error | draft
    FHIRCodeableConcept** status_reason;
    size_t status_reason_count;
    FHIRCodeableConcept** category;
    size_t category_count;
    FHIRCodeableConcept* medication_codeable_concept;
    FHIRReference* medication_reference;
    FHIRReference* subject;
    FHIRReference* encounter;
    FHIRDateTime* effective_date_time;
    FHIRPeriod* effective_period;
    FHIRTiming* effective_timing;
    FHIRDateTime* date_asserted;
    FHIRReference* information_source;
    FHIRReference** derived_from;
    size_t derived_from_count;
    FHIRCodeableConcept** reason_code;
    size_t reason_code_count;
    FHIRReference** reason_reference;
    size_t reason_reference_count;
    FHIRAnnotation** note;
    size_t note_count;
    FHIRReference** related_clinical_information;
    size_t related_clinical_information_count;
    FHIRDateTime* rendered_dosage_instruction;
    FHIRDosage** dosage;
    size_t dosage_count;
    FHIRBoolean* adherence_code;
    FHIRCodeableConcept* adherence_reason;
} FHIRMedicationStatement;

// Dosage data type
typedef struct {
    FHIRElement base;
    FHIRInteger* sequence;
    FHIRString* text;
    FHIRCodeableConcept** additional_instruction;
    size_t additional_instruction_count;
    FHIRString* patient_instruction;
    FHIRTiming* timing;
    FHIRBoolean* as_needed_boolean;
    FHIRCodeableConcept* as_needed_codeable_concept;
    FHIRCodeableConcept* site;
    FHIRCodeableConcept* route;
    FHIRCodeableConcept* method;
    struct DosageDoseAndRate** dose_and_rate;
    size_t dose_and_rate_count;
    FHIRRatio* max_dose_per_period;
    FHIRQuantity* max_dose_per_administration;
    FHIRQuantity* max_dose_per_lifetime;
} FHIRDosage;

// Dosage Dose And Rate structure
typedef struct DosageDoseAndRate {
    FHIRElement base;
    FHIRCodeableConcept* type;
    FHIRRange* dose_range;
    FHIRQuantity* dose_quantity;
    FHIRQuantity* rate_ratio;
    FHIRRange* rate_range;
    FHIRQuantity* rate_quantity;
} DosageDoseAndRate;

// Function declarations for Medication resources

// Medication functions
FHIRMedication* fhir_medication_create(const char* id);
void fhir_medication_free(FHIRMedication* medication);
FHIRMedication* fhir_parse_medication(cJSON* json);
cJSON* fhir_medication_to_json(const FHIRMedication* medication);
bool fhir_validate_medication(const FHIRMedication* medication);

// MedicationRequest functions
FHIRMedicationRequest* fhir_medication_request_create(const char* id);
void fhir_medication_request_free(FHIRMedicationRequest* medication_request);
FHIRMedicationRequest* fhir_parse_medication_request(cJSON* json);
cJSON* fhir_medication_request_to_json(const FHIRMedicationRequest* medication_request);
bool fhir_validate_medication_request(const FHIRMedicationRequest* medication_request);

// MedicationDispense functions
FHIRMedicationDispense* fhir_medication_dispense_create(const char* id);
void fhir_medication_dispense_free(FHIRMedicationDispense* medication_dispense);
FHIRMedicationDispense* fhir_parse_medication_dispense(cJSON* json);
cJSON* fhir_medication_dispense_to_json(const FHIRMedicationDispense* medication_dispense);
bool fhir_validate_medication_dispense(const FHIRMedicationDispense* medication_dispense);

// MedicationAdministration functions
FHIRMedicationAdministration* fhir_medication_administration_create(const char* id);
void fhir_medication_administration_free(FHIRMedicationAdministration* medication_administration);
FHIRMedicationAdministration* fhir_parse_medication_administration(cJSON* json);
cJSON* fhir_medication_administration_to_json(const FHIRMedicationAdministration* medication_administration);
bool fhir_validate_medication_administration(const FHIRMedicationAdministration* medication_administration);

// MedicationStatement functions
FHIRMedicationStatement* fhir_medication_statement_create(const char* id);
void fhir_medication_statement_free(FHIRMedicationStatement* medication_statement);
FHIRMedicationStatement* fhir_parse_medication_statement(cJSON* json);
cJSON* fhir_medication_statement_to_json(const FHIRMedicationStatement* medication_statement);
bool fhir_validate_medication_statement(const FHIRMedicationStatement* medication_statement);

// Utility functions for Medication resources
bool fhir_is_medication_resource(const char* resource_type);
char* fhir_get_medication_display_name(const FHIRMedication* medication);
bool fhir_is_active_medication_request(const FHIRMedicationRequest* medication_request);
bool fhir_is_completed_medication_dispense(const FHIRMedicationDispense* medication_dispense);
char* fhir_get_dosage_text(const FHIRDosage* dosage);

#endif // FHIR_MEDICATION_H