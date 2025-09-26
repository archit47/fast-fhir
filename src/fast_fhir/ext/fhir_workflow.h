#ifndef FHIR_WORKFLOW_H
#define FHIR_WORKFLOW_H

#include "fhir_datatypes.h"
#include "fhir_foundation.h"
#include <Python.h>
#include <stdbool.h>
#include <cjson/cJSON.h>

// Workflow Resource Types - Request and Response

// Appointment Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCode* status;  // proposed | pending | booked | arrived | fulfilled | cancelled | noshow | entered-in-error | checked-in | waitlist
    FHIRCodeableConcept* cancellation_reason;
    FHIRCodeableConcept** service_category;
    size_t service_category_count;
    FHIRCodeableConcept** service_type;
    size_t service_type_count;
    FHIRCodeableConcept** specialty;
    size_t specialty_count;
    FHIRCodeableConcept* appointment_type;
    FHIRCodeableConcept** reason_code;
    size_t reason_code_count;
    FHIRReference** reason_reference;
    size_t reason_reference_count;
    FHIRUnsignedInt* priority;
    FHIRString* description;
    FHIRReference** supporting_information;
    size_t supporting_information_count;
    FHIRInstant* start;
    FHIRInstant* end;
    FHIRPositiveInt* minutes_duration;
    FHIRReference** slot;
    size_t slot_count;
    FHIRDateTime* created;
    FHIRString* comment;
    FHIRString* patient_instruction;
    FHIRReference** based_on;
    size_t based_on_count;
    FHIRReference* subject;
    struct AppointmentParticipant** participant;
    size_t participant_count;
    FHIRPeriod** requested_period;
    size_t requested_period_count;
} FHIRAppointment;

// Appointment Participant structure
typedef struct AppointmentParticipant {
    FHIRElement base;
    FHIRCodeableConcept** type;
    size_t type_count;
    FHIRReference* actor;
    FHIRCode* required;  // required | optional | information-only
    FHIRCode* status;  // accepted | declined | tentative | needs-action
    FHIRPeriod* period;
} AppointmentParticipant;

// AppointmentResponse Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRReference* appointment;
    FHIRInstant* start;
    FHIRInstant* end;
    FHIRCodeableConcept** participant_type;
    size_t participant_type_count;
    FHIRReference* actor;
    FHIRCode* participant_status;  // accepted | declined | tentative | needs-action
    FHIRString* comment;
    FHIRBoolean* recurring;
    FHIRDate* occurrence_date;
    FHIRPositiveInt* occurrence_count;
} FHIRAppointmentResponse;

// Schedule Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRBoolean* active;
    FHIRCodeableConcept** service_category;
    size_t service_category_count;
    FHIRCodeableConcept** service_type;
    size_t service_type_count;
    FHIRCodeableConcept** specialty;
    size_t specialty_count;
    FHIRString* name;
    FHIRReference** actor;
    size_t actor_count;
    FHIRPeriod* planning_horizon;
    FHIRString* comment;
} FHIRSchedule;

// Slot Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCodeableConcept** service_category;
    size_t service_category_count;
    FHIRCodeableConcept** service_type;
    size_t service_type_count;
    FHIRCodeableConcept** specialty;
    size_t specialty_count;
    FHIRCodeableConcept* appointment_type;
    FHIRReference* schedule;
    FHIRCode* status;  // busy | free | busy-unavailable | busy-tentative | entered-in-error
    FHIRInstant* start;
    FHIRInstant* end;
    FHIRBoolean* overbooked;
    FHIRString* comment;
} FHIRSlot;

// Encounter Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCode* status;  // planned | in-progress | on-hold | discharged | completed | cancelled | discontinued | entered-in-error | unknown
    FHIRCoding* class;
    FHIRCodeableConcept* priority;
    FHIRCodeableConcept* type;
    FHIRCodeableConcept** service_type;
    size_t service_type_count;
    FHIRReference* subject;
    FHIRReference** episode_of_care;
    size_t episode_of_care_count;
    FHIRReference** based_on;
    size_t based_on_count;
    struct EncounterParticipant** participant;
    size_t participant_count;
    FHIRReference** appointment;
    size_t appointment_count;
    FHIRReference* virtual_service;
    FHIRPeriod* actual_period;
    FHIRPeriod* planned_start_date;
    FHIRPeriod* planned_end_date;
    FHIRDuration* length;
    FHIRCodeableConcept** reason_code;
    size_t reason_code_count;
    FHIRReference** reason_reference;
    size_t reason_reference_count;
    struct EncounterDiagnosis** diagnosis;
    size_t diagnosis_count;
    FHIRReference** account;
    size_t account_count;
    struct EncounterHospitalization* hospitalization;
    struct EncounterLocation** location;
    size_t location_count;
    FHIRReference* service_provider;
    FHIRReference* part_of;
} FHIREncounter;

// Encounter Participant structure
typedef struct EncounterParticipant {
    FHIRElement base;
    FHIRCodeableConcept** type;
    size_t type_count;
    FHIRPeriod* period;
    FHIRReference* individual;
} EncounterParticipant;

// Encounter Diagnosis structure
typedef struct EncounterDiagnosis {
    FHIRElement base;
    FHIRReference* condition;
    FHIRCodeableConcept* use;
    FHIRPositiveInt* rank;
} EncounterDiagnosis;

// Encounter Hospitalization structure
typedef struct EncounterHospitalization {
    FHIRElement base;
    FHIRIdentifier* pre_admission_identifier;
    FHIRReference* origin;
    FHIRCodeableConcept* admit_source;
    FHIRCodeableConcept* re_admission;
    FHIRCodeableConcept** diet_preference;
    size_t diet_preference_count;
    FHIRCodeableConcept** special_courtesy;
    size_t special_courtesy_count;
    FHIRCodeableConcept** special_arrangement;
    size_t special_arrangement_count;
    FHIRReference* destination;
    FHIRCodeableConcept* discharge_disposition;
} EncounterHospitalization;

// Encounter Location structure
typedef struct EncounterLocation {
    FHIRElement base;
    FHIRReference* location;
    FHIRCode* status;  // planned | active | reserved | completed
    FHIRCodeableConcept* form;
    FHIRPeriod* period;
} EncounterLocation;

// Task Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCanonical* instantiates_canonical;
    FHIRUri* instantiates_uri;
    FHIRReference** based_on;
    size_t based_on_count;
    FHIRIdentifier* group_identifier;
    FHIRReference** part_of;
    size_t part_of_count;
    FHIRCode* status;  // draft | requested | received | accepted | rejected | ready | cancelled | in-progress | on-hold | failed | completed | entered-in-error
    FHIRCodeableConcept* status_reason;
    FHIRCode* business_status;
    FHIRCode* intent;  // unknown | proposal | plan | order | original-order | reflex-order | filler-order | instance-order | option
    FHIRCode* priority;  // routine | urgent | asap | stat
    FHIRBoolean* do_not_perform;
    FHIRCodeableConcept* code;
    FHIRString* description;
    FHIRReference* focus;
    FHIRReference* for_reference;
    FHIRReference* encounter;
    FHIRReference* requested_performer;
    FHIRCodeableConcept* performer_type;
    FHIRReference* owner;
    FHIRReference* location;
    FHIRCodeableConcept* reason_code;
    FHIRReference* reason_reference;
    FHIRReference** insurance;
    size_t insurance_count;
    FHIRAnnotation** note;
    size_t note_count;
    FHIRReference** relevant_history;
    size_t relevant_history_count;
    FHIRPeriod* execution_period;
    FHIRDateTime* authored_on;
    FHIRDateTime* last_modified;
    FHIRReference* requester;
    struct TaskRestriction* restriction;
    struct TaskInput** input;
    size_t input_count;
    struct TaskOutput** output;
    size_t output_count;
} FHIRTask;

// Task Restriction structure
typedef struct TaskRestriction {
    FHIRElement base;
    FHIRPositiveInt* repetitions;
    FHIRPeriod* period;
    FHIRReference** recipient;
    size_t recipient_count;
} TaskRestriction;

// Task Input structure
typedef struct TaskInput {
    FHIRElement base;
    FHIRCodeableConcept* type;
    FHIRBase64Binary* value_base64_binary;
    FHIRBoolean* value_boolean;
    FHIRCanonical* value_canonical;
    FHIRCode* value_code;
    FHIRDate* value_date;
    FHIRDateTime* value_date_time;
    FHIRDecimal* value_decimal;
    FHIRId* value_id;
    FHIRInstant* value_instant;
    FHIRInteger* value_integer;
    FHIRMarkdown* value_markdown;
    FHIROid* value_oid;
    FHIRPositiveInt* value_positive_int;
    FHIRString* value_string;
    FHIRTime* value_time;
    FHIRUnsignedInt* value_unsigned_int;
    FHIRUri* value_uri;
    FHIRUrl* value_url;
    FHIRUuid* value_uuid;
    FHIRAddress* value_address;
    FHIRAge* value_age;
    FHIRAnnotation* value_annotation;
    FHIRAttachment* value_attachment;
    FHIRCodeableConcept* value_codeable_concept;
    FHIRCoding* value_coding;
    FHIRContactPoint* value_contact_point;
    FHIRCount* value_count;
    FHIRDistance* value_distance;
    FHIRDuration* value_duration;
    FHIRHumanName* value_human_name;
    FHIRIdentifier* value_identifier;
    FHIRMoney* value_money;
    FHIRPeriod* value_period;
    FHIRQuantity* value_quantity;
    FHIRRange* value_range;
    FHIRRatio* value_ratio;
    FHIRReference* value_reference;
    FHIRSampledData* value_sampled_data;
    FHIRSignature* value_signature;
    FHIRTiming* value_timing;
    FHIRContactDetail* value_contact_detail;
    FHIRContributor* value_contributor;
    FHIRDataRequirement* value_data_requirement;
    FHIRExpression* value_expression;
    FHIRParameterDefinition* value_parameter_definition;
    FHIRRelatedArtifact* value_related_artifact;
    FHIRTriggerDefinition* value_trigger_definition;
    FHIRUsageContext* value_usage_context;
    FHIRDosage* value_dosage;
    FHIRMeta* value_meta;
} TaskInput;

// Task Output structure (same as TaskInput)
typedef TaskInput TaskOutput;

// Function declarations for Workflow resources

// Appointment functions
FHIRAppointment* fhir_appointment_create(const char* id);
void fhir_appointment_free(FHIRAppointment* appointment);
FHIRAppointment* fhir_parse_appointment(cJSON* json);
cJSON* fhir_appointment_to_json(const FHIRAppointment* appointment);
bool fhir_validate_appointment(const FHIRAppointment* appointment);

// AppointmentResponse functions
FHIRAppointmentResponse* fhir_appointment_response_create(const char* id);
void fhir_appointment_response_free(FHIRAppointmentResponse* appointment_response);
FHIRAppointmentResponse* fhir_parse_appointment_response(cJSON* json);
cJSON* fhir_appointment_response_to_json(const FHIRAppointmentResponse* appointment_response);
bool fhir_validate_appointment_response(const FHIRAppointmentResponse* appointment_response);

// Schedule functions
FHIRSchedule* fhir_schedule_create(const char* id);
void fhir_schedule_free(FHIRSchedule* schedule);
FHIRSchedule* fhir_parse_schedule(cJSON* json);
cJSON* fhir_schedule_to_json(const FHIRSchedule* schedule);
bool fhir_validate_schedule(const FHIRSchedule* schedule);

// Slot functions
FHIRSlot* fhir_slot_create(const char* id);
void fhir_slot_free(FHIRSlot* slot);
FHIRSlot* fhir_parse_slot(cJSON* json);
cJSON* fhir_slot_to_json(const FHIRSlot* slot);
bool fhir_validate_slot(const FHIRSlot* slot);

// Encounter functions
FHIREncounter* fhir_encounter_create(const char* id);
void fhir_encounter_free(FHIREncounter* encounter);
FHIREncounter* fhir_parse_encounter(cJSON* json);
cJSON* fhir_encounter_to_json(const FHIREncounter* encounter);
bool fhir_validate_encounter(const FHIREncounter* encounter);

// Task functions
FHIRTask* fhir_task_create(const char* id);
void fhir_task_free(FHIRTask* task);
FHIRTask* fhir_parse_task(cJSON* json);
cJSON* fhir_task_to_json(const FHIRTask* task);
bool fhir_validate_task(const FHIRTask* task);

// Utility functions for Workflow resources
bool fhir_is_workflow_resource(const char* resource_type);
bool fhir_is_active_appointment(const FHIRAppointment* appointment);
bool fhir_is_completed_encounter(const FHIREncounter* encounter);
char* fhir_get_encounter_class_display(const FHIREncounter* encounter);
bool fhir_is_completed_task(const FHIRTask* task);

// Additional supporting data types for workflow
typedef struct {
    FHIRElement base;
    FHIRString* language;
    FHIRString* expression;
    FHIRString* description;
    FHIRId* name;
    FHIRReference* reference;
} FHIRExpression;

typedef struct {
    FHIRElement base;
    FHIRCode* type;  // named-event | periodic | data-changed | data-added | data-modified | data-removed | data-accessed | data-access-ended
    FHIRString* name;
    FHIRTiming* timing_timing;
    FHIRReference* timing_reference;
    FHIRDate* timing_date;
    FHIRDateTime* timing_date_time;
    FHIRDataRequirement** data;
    size_t data_count;
    FHIRExpression* condition;
} FHIRTriggerDefinition;

typedef struct {
    FHIRElement base;
    FHIRString* type;
    FHIRString* subject_codeable_concept;
    FHIRReference* subject_reference;
    FHIRString** must_support;
    size_t must_support_count;
    struct DataRequirementCodeFilter** code_filter;
    size_t code_filter_count;
    struct DataRequirementDateFilter** date_filter;
    size_t date_filter_count;
    FHIRPositiveInt* limit;
    struct DataRequirementSort** sort;
    size_t sort_count;
} FHIRDataRequirement;

typedef struct DataRequirementCodeFilter {
    FHIRElement base;
    FHIRString* path;
    FHIRString* search_param;
    FHIRCanonical* value_set;
    FHIRCoding** code;
    size_t code_count;
} DataRequirementCodeFilter;

typedef struct DataRequirementDateFilter {
    FHIRElement base;
    FHIRString* path;
    FHIRString* search_param;
    FHIRDateTime* value_date_time;
    FHIRPeriod* value_period;
    FHIRDuration* value_duration;
} DataRequirementDateFilter;

typedef struct DataRequirementSort {
    FHIRElement base;
    FHIRString* path;
    FHIRCode* direction;  // ascending | descending
} DataRequirementSort;

// Transport Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCanonical* instantiates_canonical;
    FHIRUri* instantiates_uri;
    FHIRReference** based_on;
    size_t based_on_count;
    FHIRIdentifier* group_identifier;
    FHIRReference** part_of;
    size_t part_of_count;
    FHIRCode* status;  // draft | requested | received | accepted | rejected | in-progress | completed | cancelled | entered-in-error
    FHIRCodeableConcept* status_reason;
    FHIRCode* intent;  // unknown | proposal | plan | order | original-order | reflex-order | filler-order | instance-order | option
    FHIRCode* priority;  // routine | urgent | asap | stat
    FHIRCodeableConcept* code;
    FHIRString* description;
    FHIRReference* focus;
    FHIRReference* for_reference;
    FHIRReference* encounter;
    FHIRPeriod* completion_time;
    FHIRDateTime* authored_on;
    FHIRDateTime* last_modified;
    FHIRReference* requester;
    FHIRCodeableConcept* performer_type;
    FHIRReference* owner;
    FHIRReference* location;
    FHIRReference** insurance;
    size_t insurance_count;
    FHIRAnnotation** note;
    size_t note_count;
    FHIRReference** relevant_history;
    size_t relevant_history_count;
    struct TransportRestriction* restriction;
    struct TransportInput** input;
    size_t input_count;
    struct TransportOutput** output;
    size_t output_count;
    FHIRReference* requested_location;
    FHIRReference* current_location;
    FHIRCodeableConcept* reason_code;
    FHIRReference* reason_reference;
    FHIRReference* history;
} FHIRTransport;

// Transport Restriction structure (same as TaskRestriction)
typedef struct TransportRestriction {
    FHIRElement base;
    FHIRPositiveInt* repetitions;
    FHIRPeriod* period;
    FHIRReference** recipient;
    size_t recipient_count;
} TransportRestriction;

// Transport Input structure (same as TaskInput)
typedef TaskInput TransportInput;

// Transport Output structure (same as TaskOutput)
typedef TaskOutput TransportOutput;

// EpisodeOfCare Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCode* status;  // planned | waitlist | active | onhold | finished | cancelled | entered-in-error
    struct EpisodeOfCareStatusHistory** status_history;
    size_t status_history_count;
    FHIRCodeableConcept** type;
    size_t type_count;
    struct EpisodeOfCareDiagnosis** diagnosis;
    size_t diagnosis_count;
    FHIRReference* patient;
    FHIRReference* managing_organization;
    FHIRPeriod* period;
    FHIRReference** referral_request;
    size_t referral_request_count;
    FHIRReference* care_manager;
    FHIRReference** team;
    size_t team_count;
    FHIRReference** account;
    size_t account_count;
} FHIREpisodeOfCare;

// EpisodeOfCare Status History structure
typedef struct EpisodeOfCareStatusHistory {
    FHIRElement base;
    FHIRCode* status;  // planned | waitlist | active | onhold | finished | cancelled | entered-in-error
    FHIRPeriod* period;
} EpisodeOfCareStatusHistory;

// EpisodeOfCare Diagnosis structure
typedef struct EpisodeOfCareDiagnosis {
    FHIRElement base;
    FHIRReference* condition;
    FHIRCodeableConcept* role;
    FHIRPositiveInt* rank;
} EpisodeOfCareDiagnosis;

// EncounterHistory Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCode* status;  // planned | in-progress | on-hold | discharged | completed | cancelled | discontinued | entered-in-error | unknown
    FHIRCoding* class;
    FHIRCodeableConcept* type;
    FHIRCodeableConcept** service_type;
    size_t service_type_count;
    FHIRReference* subject;
    FHIRReference* encounter;
    FHIRPeriod* actual_period;
    FHIRPeriod* planned_start_date;
    FHIRPeriod* planned_end_date;
    FHIRDuration* length;
    struct EncounterHistoryLocation** location;
    size_t location_count;
} FHIREncounterHistory;

// EncounterHistory Location structure
typedef struct EncounterHistoryLocation {
    FHIRElement base;
    FHIRReference* location;
    FHIRCodeableConcept* form;
    FHIRPeriod* period;
} EncounterHistoryLocation;

// Transport functions
FHIRTransport* fhir_transport_create(const char* id);
void fhir_transport_free(FHIRTransport* transport);
FHIRTransport* fhir_parse_transport(cJSON* json);
cJSON* fhir_transport_to_json(const FHIRTransport* transport);
bool fhir_validate_transport(const FHIRTransport* transport);

// EpisodeOfCare functions
FHIREpisodeOfCare* fhir_episode_of_care_create(const char* id);
void fhir_episode_of_care_free(FHIREpisodeOfCare* episode_of_care);
FHIREpisodeOfCare* fhir_parse_episode_of_care(cJSON* json);
cJSON* fhir_episode_of_care_to_json(const FHIREpisodeOfCare* episode_of_care);
bool fhir_validate_episode_of_care(const FHIREpisodeOfCare* episode_of_care);

// EncounterHistory functions
FHIREncounterHistory* fhir_encounter_history_create(const char* id);
void fhir_encounter_history_free(FHIREncounterHistory* encounter_history);
FHIREncounterHistory* fhir_parse_encounter_history(cJSON* json);
cJSON* fhir_encounter_history_to_json(const FHIREncounterHistory* encounter_history);
bool fhir_validate_encounter_history(const FHIREncounterHistory* encounter_history);

#endif // FHIR_WORKFLOW_H