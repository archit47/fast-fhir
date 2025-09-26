#ifndef FHIR_CLINICAL_H
#define FHIR_CLINICAL_H

#include "fhir_datatypes.h"
#include "fhir_foundation.h"
#include <Python.h>
#include <stdbool.h>
#include <cjson/cJSON.h>

// Clinical Resource Types - Summary and Care Provision

// AllergyIntolerance Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCodeableConcept* clinical_status;
    FHIRCodeableConcept* verification_status;
    FHIRCode* type;  // allergy | intolerance
    FHIRCode** category;
    size_t category_count;
    FHIRCode* criticality;  // low | high | unable-to-assess
    FHIRCodeableConcept* code;
    FHIRReference* patient;
    FHIRReference* encounter;
    FHIRDateTime* onset_date_time;
    FHIRAge* onset_age;
    FHIRPeriod* onset_period;
    FHIRRange* onset_range;
    FHIRString* onset_string;
    FHIRDateTime* recorded_date;
    FHIRReference* recorder;
    FHIRReference* asserter;
    FHIRDateTime* last_occurrence;
    FHIRAnnotation** note;
    size_t note_count;
    struct AllergyIntoleranceReaction** reaction;
    size_t reaction_count;
} FHIRAllergyIntolerance;

// AllergyIntolerance Reaction structure
typedef struct AllergyIntoleranceReaction {
    FHIRElement base;
    FHIRCodeableConcept* substance;
    FHIRCodeableConcept** manifestation;
    size_t manifestation_count;
    FHIRString* description;
    FHIRCode* severity;  // mild | moderate | severe
    FHIRCodeableConcept* exposure_route;
    FHIRAnnotation** note;
    size_t note_count;
} AllergyIntoleranceReaction;

// Condition Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCodeableConcept* clinical_status;
    FHIRCodeableConcept* verification_status;
    FHIRCodeableConcept** category;
    size_t category_count;
    FHIRCodeableConcept* severity;
    FHIRCodeableConcept* code;
    FHIRCodeableConcept** body_site;
    size_t body_site_count;
    FHIRReference* subject;
    FHIRReference* encounter;
    FHIRDateTime* onset_date_time;
    FHIRAge* onset_age;
    FHIRPeriod* onset_period;
    FHIRRange* onset_range;
    FHIRString* onset_string;
    FHIRDateTime* abatement_date_time;
    FHIRAge* abatement_age;
    FHIRPeriod* abatement_period;
    FHIRRange* abatement_range;
    FHIRString* abatement_string;
    FHIRDateTime* recorded_date;
    FHIRReference* recorder;
    FHIRReference* asserter;
    struct ConditionStage** stage;
    size_t stage_count;
    struct ConditionEvidence** evidence;
    size_t evidence_count;
    FHIRAnnotation** note;
    size_t note_count;
} FHIRCondition;

// Condition Stage structure
typedef struct ConditionStage {
    FHIRElement base;
    FHIRCodeableConcept* summary;
    FHIRReference** assessment;
    size_t assessment_count;
    FHIRCodeableConcept* type;
} ConditionStage;

// Condition Evidence structure
typedef struct ConditionEvidence {
    FHIRElement base;
    FHIRCodeableConcept** code;
    size_t code_count;
    FHIRReference** detail;
    size_t detail_count;
} ConditionEvidence;

// Procedure Resource
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
    FHIRCode* status;  // preparation | in-progress | not-done | on-hold | stopped | completed | entered-in-error | unknown
    FHIRCodeableConcept* status_reason;
    FHIRCodeableConcept** category;
    size_t category_count;
    FHIRCodeableConcept* code;
    FHIRReference* subject;
    FHIRReference* encounter;
    FHIRDateTime* performed_date_time;
    FHIRPeriod* performed_period;
    FHIRString* performed_string;
    FHIRAge* performed_age;
    FHIRRange* performed_range;
    FHIRReference* recorder;
    FHIRReference* asserter;
    struct ProcedurePerformer** performer;
    size_t performer_count;
    FHIRReference* location;
    FHIRCodeableConcept** reason_code;
    size_t reason_code_count;
    FHIRReference** reason_reference;
    size_t reason_reference_count;
    FHIRCodeableConcept** body_site;
    size_t body_site_count;
    FHIRCodeableConcept* outcome;
    FHIRReference** report;
    size_t report_count;
    FHIRCodeableConcept** complication;
    size_t complication_count;
    FHIRReference** complication_detail;
    size_t complication_detail_count;
    FHIRCodeableConcept** follow_up;
    size_t follow_up_count;
    FHIRAnnotation** note;
    size_t note_count;
    struct ProcedureFocalDevice** focal_device;
    size_t focal_device_count;
    FHIRReference** used_reference;
    size_t used_reference_count;
    FHIRCodeableConcept** used_code;
    size_t used_code_count;
} FHIRProcedure;

// Procedure Performer structure
typedef struct ProcedurePerformer {
    FHIRElement base;
    FHIRCodeableConcept* function;
    FHIRReference* actor;
    FHIRReference* on_behalf_of;
} ProcedurePerformer;

// Procedure Focal Device structure
typedef struct ProcedureFocalDevice {
    FHIRElement base;
    FHIRCodeableConcept* action;
    FHIRReference* manipulated;
} ProcedureFocalDevice;

// Observation Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCanonical** instantiates_canonical;
    size_t instantiates_canonical_count;
    FHIRReference** instantiates_reference;
    size_t instantiates_reference_count;
    FHIRReference** based_on;
    size_t based_on_count;
    struct ObservationTriggeredBy** triggered_by;
    size_t triggered_by_count;
    FHIRReference** part_of;
    size_t part_of_count;
    FHIRCode* status;  // registered | preliminary | final | amended | corrected | cancelled | entered-in-error | unknown
    FHIRCodeableConcept** category;
    size_t category_count;
    FHIRCodeableConcept* code;
    FHIRReference* subject;
    FHIRReference** focus;
    size_t focus_count;
    FHIRReference* encounter;
    FHIRDateTime* effective_date_time;
    FHIRPeriod* effective_period;
    FHIRTiming* effective_timing;
    FHIRInstant* effective_instant;
    FHIRInstant* issued;
    FHIRReference** performer;
    size_t performer_count;
    FHIRQuantity* value_quantity;
    FHIRCodeableConcept* value_codeable_concept;
    FHIRString* value_string;
    FHIRBoolean* value_boolean;
    FHIRInteger* value_integer;
    FHIRRange* value_range;
    FHIRRatio* value_ratio;
    FHIRSampledData* value_sampled_data;
    FHIRTime* value_time;
    FHIRDateTime* value_date_time;
    FHIRPeriod* value_period;
    FHIRAttachment* value_attachment;
    FHIRCodeableConcept* data_absent_reason;
    FHIRCodeableConcept** interpretation;
    size_t interpretation_count;
    FHIRAnnotation** note;
    size_t note_count;
    FHIRCodeableConcept* body_site;
    FHIRReference* body_structure;
    FHIRCodeableConcept* method;
    FHIRReference* specimen;
    FHIRReference* device;
    struct ObservationReferenceRange** reference_range;
    size_t reference_range_count;
    FHIRReference** has_member;
    size_t has_member_count;
    FHIRReference** derived_from;
    size_t derived_from_count;
    struct ObservationComponent** component;
    size_t component_count;
} FHIRObservation;

// Observation Triggered By structure
typedef struct ObservationTriggeredBy {
    FHIRElement base;
    FHIRReference* observation;
    FHIRCode* type;  // reflex | repeat | re-run
    FHIRString* reason;
} ObservationTriggeredBy;

// Observation Reference Range structure
typedef struct ObservationReferenceRange {
    FHIRElement base;
    FHIRQuantity* low;
    FHIRQuantity* high;
    FHIRCodeableConcept* type;
    FHIRCodeableConcept** applies_to;
    size_t applies_to_count;
    FHIRRange* age;
    FHIRString* text;
} ObservationReferenceRange;

// Observation Component structure
typedef struct ObservationComponent {
    FHIRElement base;
    FHIRCodeableConcept* code;
    FHIRQuantity* value_quantity;
    FHIRCodeableConcept* value_codeable_concept;
    FHIRString* value_string;
    FHIRBoolean* value_boolean;
    FHIRInteger* value_integer;
    FHIRRange* value_range;
    FHIRRatio* value_ratio;
    FHIRSampledData* value_sampled_data;
    FHIRTime* value_time;
    FHIRDateTime* value_date_time;
    FHIRPeriod* value_period;
    FHIRAttachment* value_attachment;
    FHIRCodeableConcept* data_absent_reason;
    FHIRCodeableConcept** interpretation;
    size_t interpretation_count;
    struct ObservationReferenceRange** reference_range;
    size_t reference_range_count;
} ObservationComponent;

// DiagnosticReport Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRReference** based_on;
    size_t based_on_count;
    FHIRCode* status;  // registered | partial | preliminary | final | amended | corrected | appended | cancelled | entered-in-error | unknown
    FHIRCodeableConcept** category;
    size_t category_count;
    FHIRCodeableConcept* code;
    FHIRReference* subject;
    FHIRReference* encounter;
    FHIRDateTime* effective_date_time;
    FHIRPeriod* effective_period;
    FHIRInstant* issued;
    FHIRReference** performer;
    size_t performer_count;
    FHIRReference** results_interpreter;
    size_t results_interpreter_count;
    FHIRReference** specimen;
    size_t specimen_count;
    FHIRReference** result;
    size_t result_count;
    FHIRReference** imaging_study;
    size_t imaging_study_count;
    struct DiagnosticReportMedia** media;
    size_t media_count;
    FHIRString* conclusion;
    FHIRCodeableConcept** conclusion_code;
    size_t conclusion_code_count;
    FHIRAttachment** presented_form;
    size_t presented_form_count;
} FHIRDiagnosticReport;

// DiagnosticReport Media structure
typedef struct DiagnosticReportMedia {
    FHIRElement base;
    FHIRString* comment;
    FHIRReference* link;
} DiagnosticReportMedia;

// Additional supporting data types
typedef struct {
    FHIRElement base;
    FHIRString* text;
    FHIRReference* author_reference;
    FHIRString* author_string;
    FHIRDateTime* time;
} FHIRAnnotation;

typedef struct {
    FHIRElement base;
    FHIRQuantity* origin;
    FHIRDecimal* period;
    FHIRDecimal* factor;
    FHIRDecimal* lower_limit;
    FHIRDecimal* upper_limit;
    FHIRPositiveInt* dimensions;
    FHIRString* data;
} FHIRSampledData;

typedef struct {
    FHIRElement base;
    FHIRDateTime** event;
    size_t event_count;
    struct TimingRepeat* repeat;
    FHIRCodeableConcept* code;
} FHIRTiming;

typedef struct TimingRepeat {
    FHIRElement base;
    FHIRRange* bounds_range;
    FHIRPeriod* bounds_period;
    FHIRDuration* bounds_duration;
    FHIRPositiveInt* count;
    FHIRPositiveInt* count_max;
    FHIRDecimal* duration;
    FHIRDecimal* duration_max;
    FHIRCode* duration_unit;  // s | min | h | d | wk | mo | a
    FHIRPositiveInt* frequency;
    FHIRPositiveInt* frequency_max;
    FHIRDecimal* period;
    FHIRDecimal* period_max;
    FHIRCode* period_unit;  // s | min | h | d | wk | mo | a
    FHIRCode** day_of_week;
    size_t day_of_week_count;
    FHIRTime** time_of_day;
    size_t time_of_day_count;
    FHIRCode** when;
    size_t when_count;
    FHIRUnsignedInt* offset;
} TimingRepeat;

// Function declarations for Clinical resources

// AllergyIntolerance functions
FHIRAllergyIntolerance* fhir_allergy_intolerance_create(const char* id);
void fhir_allergy_intolerance_free(FHIRAllergyIntolerance* allergy_intolerance);
FHIRAllergyIntolerance* fhir_parse_allergy_intolerance(cJSON* json);
cJSON* fhir_allergy_intolerance_to_json(const FHIRAllergyIntolerance* allergy_intolerance);
bool fhir_validate_allergy_intolerance(const FHIRAllergyIntolerance* allergy_intolerance);

// Condition functions
FHIRCondition* fhir_condition_create(const char* id);
void fhir_condition_free(FHIRCondition* condition);
FHIRCondition* fhir_parse_condition(cJSON* json);
cJSON* fhir_condition_to_json(const FHIRCondition* condition);
bool fhir_validate_condition(const FHIRCondition* condition);

// Procedure functions
FHIRProcedure* fhir_procedure_create(const char* id);
void fhir_procedure_free(FHIRProcedure* procedure);
FHIRProcedure* fhir_parse_procedure(cJSON* json);
cJSON* fhir_procedure_to_json(const FHIRProcedure* procedure);
bool fhir_validate_procedure(const FHIRProcedure* procedure);

// Observation functions
FHIRObservation* fhir_observation_create(const char* id);
void fhir_observation_free(FHIRObservation* observation);
FHIRObservation* fhir_parse_observation(cJSON* json);
cJSON* fhir_observation_to_json(const FHIRObservation* observation);
bool fhir_validate_observation(const FHIRObservation* observation);

// DiagnosticReport functions
FHIRDiagnosticReport* fhir_diagnostic_report_create(const char* id);
void fhir_diagnostic_report_free(FHIRDiagnosticReport* diagnostic_report);
FHIRDiagnosticReport* fhir_parse_diagnostic_report(cJSON* json);
cJSON* fhir_diagnostic_report_to_json(const FHIRDiagnosticReport* diagnostic_report);
bool fhir_validate_diagnostic_report(const FHIRDiagnosticReport* diagnostic_report);

// Utility functions for Clinical resources
bool fhir_is_clinical_resource(const char* resource_type);
char* fhir_get_clinical_status_display(const FHIRCodeableConcept* status);
bool fhir_is_active_condition(const FHIRCondition* condition);
bool fhir_is_completed_procedure(const FHIRProcedure* procedure);
char* fhir_get_observation_value_string(const FHIRObservation* observation);

#endif // FHIR_CLINICAL_H