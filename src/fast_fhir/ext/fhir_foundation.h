#ifndef FHIR_FOUNDATION_H
#define FHIR_FOUNDATION_H

#include "fhir_datatypes.h"
#include <Python.h>
#include <stdbool.h>
#include <cjson/cJSON.h>

// Forward declarations
struct FHIRResource;
struct FHIRDomainResource;
struct FHIRUsageContext;
struct FHIRSignature;
struct FHIRTask;
struct FHIRCodeSystem;

// Forward declarations for structs
struct FHIRUsageContext;
struct FHIRSignature;
struct FHIRTask;

// Base Resource structure
typedef struct FHIRResource {
    FHIRElement base;
    char* resource_type;
    char* id;
    FHIRMeta* meta;
    FHIRUri* implicit_rules;
    FHIRCode* language;
} FHIRResource;

// Domain Resource structure (extends Resource)
typedef struct FHIRDomainResource {
    FHIRResource resource;
    FHIRNarrative* text;
    struct FHIRResource** contained;
    size_t contained_count;
    FHIRExtension** extension;
    size_t extension_count;
    FHIRExtension** modifier_extension;
    size_t modifier_extension_count;
} FHIRDomainResource;

// Foundation Resource Types

// Patient Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRBoolean* active;
    FHIRHumanName** name;
    size_t name_count;
    FHIRContactPoint** telecom;
    size_t telecom_count;
    FHIRCode* gender;
    FHIRDate* birth_date;
    FHIRBoolean* deceased_boolean;
    FHIRDateTime* deceased_date_time;
    FHIRAddress** address;
    size_t address_count;
    FHIRCodeableConcept* marital_status;
    FHIRBoolean* multiple_birth_boolean;
    FHIRInteger* multiple_birth_integer;
    FHIRAttachment** photo;
    size_t photo_count;
    struct PatientContact** contact;
    size_t contact_count;
    struct PatientCommunication** communication;
    size_t communication_count;
    FHIRReference** general_practitioner;
    size_t general_practitioner_count;
    FHIRReference* managing_organization;
    struct PatientLink** link;
    size_t link_count;
} FHIRPatient;

// Patient Contact structure
typedef struct PatientContact {
    FHIRElement base;
    FHIRCodeableConcept** relationship;
    size_t relationship_count;
    FHIRHumanName* name;
    FHIRContactPoint** telecom;
    size_t telecom_count;
    FHIRAddress* address;
    FHIRCode* gender;
    FHIRReference* organization;
    FHIRPeriod* period;
} PatientContact;

// Patient Communication structure
typedef struct PatientCommunication {
    FHIRElement base;
    FHIRCodeableConcept* language;
    FHIRBoolean* preferred;
} PatientCommunication;

// Patient Link structure
typedef struct PatientLink {
    FHIRElement base;
    FHIRReference* other;
    FHIRCode* type;  // replaced-by | replaces | refer | seealso
} PatientLink;

// Practitioner Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRBoolean* active;
    FHIRHumanName** name;
    size_t name_count;
    FHIRContactPoint** telecom;
    size_t telecom_count;
    FHIRCode* gender;
    FHIRDate* birth_date;
    FHIRAttachment** photo;
    size_t photo_count;
    struct PractitionerQualification** qualification;
    size_t qualification_count;
    FHIRCodeableConcept** communication;
    size_t communication_count;
} FHIRPractitioner;

// Practitioner Qualification structure
typedef struct PractitionerQualification {
    FHIRElement base;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCodeableConcept* code;
    FHIRPeriod* period;
    FHIRReference* issuer;
} PractitionerQualification;

// Organization Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRBoolean* active;
    FHIRCodeableConcept** type;
    size_t type_count;
    FHIRString* name;
    FHIRString** alias;
    size_t alias_count;
    FHIRString* description;
    FHIRContactPoint** telecom;
    size_t telecom_count;
    FHIRAddress** address;
    size_t address_count;
    FHIRReference* part_of;
    struct OrganizationContact** contact;
    size_t contact_count;
    FHIRReference** endpoint;
    size_t endpoint_count;
} FHIROrganization;

// Organization Contact structure
typedef struct OrganizationContact {
    FHIRElement base;
    FHIRCodeableConcept* purpose;
    FHIRHumanName* name;
    FHIRContactPoint** telecom;
    size_t telecom_count;
    FHIRAddress* address;
} OrganizationContact;

// Location Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCode* status;  // active | suspended | inactive
    FHIRCoding* operational_status;
    FHIRString* name;
    FHIRString** alias;
    size_t alias_count;
    FHIRString* description;
    FHIRCode* mode;  // instance | kind
    FHIRCodeableConcept** type;
    size_t type_count;
    FHIRContactPoint** telecom;
    size_t telecom_count;
    FHIRAddress* address;
    FHIRCodeableConcept* physical_type;
    struct LocationPosition* position;
    FHIRReference* managing_organization;
    FHIRReference* part_of;
    struct LocationHoursOfOperation** hours_of_operation;
    size_t hours_of_operation_count;
    FHIRString* availability_exceptions;
    FHIRReference** endpoint;
    size_t endpoint_count;
} FHIRLocation;

// Location Position structure
typedef struct LocationPosition {
    FHIRElement base;
    FHIRDecimal* longitude;
    FHIRDecimal* latitude;
    FHIRDecimal* altitude;
} LocationPosition;

// Location Hours of Operation structure
typedef struct LocationHoursOfOperation {
    FHIRElement base;
    FHIRCode** days_of_week;
    size_t days_of_week_count;
    FHIRBoolean* all_day;
    FHIRTime* opening_time;
    FHIRTime* closing_time;
} LocationHoursOfOperation;

// HealthcareService Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRBoolean* active;
    FHIRReference* provided_by;
    FHIRCodeableConcept** category;
    size_t category_count;
    FHIRCodeableConcept** type;
    size_t type_count;
    FHIRCodeableConcept** specialty;
    size_t specialty_count;
    FHIRReference** location;
    size_t location_count;
    FHIRString* name;
    FHIRString* comment;
    FHIRMarkdown* extra_details;
    FHIRAttachment* photo;
    FHIRContactPoint** telecom;
    size_t telecom_count;
    FHIRReference** coverage_area;
    size_t coverage_area_count;
    FHIRCodeableConcept** service_provision_code;
    size_t service_provision_code_count;
    struct HealthcareServiceEligibility** eligibility;
    size_t eligibility_count;
    FHIRCodeableConcept** program;
    size_t program_count;
    FHIRCodeableConcept** characteristic;
    size_t characteristic_count;
    FHIRCodeableConcept** communication;
    size_t communication_count;
    FHIRCodeableConcept** referral_method;
    size_t referral_method_count;
    FHIRBoolean* appointment_required;
    struct HealthcareServiceAvailableTime** available_time;
    size_t available_time_count;
    struct HealthcareServiceNotAvailable** not_available;
    size_t not_available_count;
    FHIRString* availability_exceptions;
    FHIRReference** endpoint;
    size_t endpoint_count;
} FHIRHealthcareService;

// HealthcareService Eligibility structure
typedef struct HealthcareServiceEligibility {
    FHIRElement base;
    FHIRCodeableConcept* code;
    FHIRMarkdown* comment;
} HealthcareServiceEligibility;

// HealthcareService Available Time structure
typedef struct HealthcareServiceAvailableTime {
    FHIRElement base;
    FHIRCode** days_of_week;
    size_t days_of_week_count;
    FHIRBoolean* all_day;
    FHIRTime* available_start_time;
    FHIRTime* available_end_time;
} HealthcareServiceAvailableTime;

// HealthcareService Not Available structure
typedef struct HealthcareServiceNotAvailable {
    FHIRElement base;
    FHIRString* description;
    FHIRPeriod* during;
} HealthcareServiceNotAvailable;

// Endpoint Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCode* status;  // active | suspended | error | off | entered-in-error | test
    FHIRCoding* connection_type;
    FHIRString* name;
    FHIRReference* managing_organization;
    FHIRContactPoint** contact;
    size_t contact_count;
    FHIRPeriod* period;
    FHIRCodeableConcept** payload_type;
    size_t payload_type_count;
    FHIRCode** payload_mime_type;
    size_t payload_mime_type_count;
    FHIRUrl* address;
    FHIRString** header;
    size_t header_count;
} FHIREndpoint;

// RelatedPerson Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRBoolean* active;
    FHIRReference* patient;
    FHIRCodeableConcept** relationship;
    size_t relationship_count;
    FHIRHumanName** name;
    size_t name_count;
    FHIRContactPoint** telecom;
    size_t telecom_count;
    FHIRCode* gender;
    FHIRDate* birth_date;
    FHIRAddress** address;
    size_t address_count;
    FHIRAttachment** photo;
    size_t photo_count;
    FHIRPeriod* period;
    struct RelatedPersonCommunication** communication;
    size_t communication_count;
} FHIRRelatedPerson;

// RelatedPerson Communication structure
typedef struct RelatedPersonCommunication {
    FHIRElement base;
    FHIRCodeableConcept* language;
    FHIRBoolean* preferred;
} RelatedPersonCommunication;

// Person Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRBoolean* active;
    FHIRHumanName** name;
    size_t name_count;
    FHIRContactPoint** telecom;
    size_t telecom_count;
    FHIRCode* gender;
    FHIRDate* birth_date;
    FHIRBoolean* deceased_boolean;
    FHIRDateTime* deceased_date_time;
    FHIRAddress** address;
    size_t address_count;
    FHIRCodeableConcept* marital_status;
    FHIRAttachment** photo;
    size_t photo_count;
    struct PersonCommunication** communication;
    size_t communication_count;
    FHIRReference* managing_organization;
    struct PersonLink** link;
    size_t link_count;
} FHIRPerson;

// Person Communication structure
typedef struct PersonCommunication {
    FHIRElement base;
    FHIRCodeableConcept* language;
    FHIRBoolean* preferred;
} PersonCommunication;

// Person Link structure
typedef struct PersonLink {
    FHIRElement base;
    FHIRReference* target;
    FHIRCode* assurance;  // level1 | level2 | level3 | level4
} PersonLink;

// Group Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRBoolean* active;
    FHIRCode* type;  // person | animal | practitioner | device | careteam | healthcareservice | location | organization | relatedperson | specimen
    FHIRBoolean* actual;
    FHIRCodeableConcept* code;
    FHIRString* name;
    FHIRString* description;
    FHIRUnsignedInt* quantity;
    FHIRReference* managing_entity;
    struct GroupCharacteristic** characteristic;
    size_t characteristic_count;
    struct GroupMember** member;
    size_t member_count;
} FHIRGroup;

// Group Characteristic structure
typedef struct GroupCharacteristic {
    FHIRElement base;
    FHIRCodeableConcept* code;
    FHIRCodeableConcept* value_codeable_concept;
    FHIRBoolean* value_boolean;
    FHIRQuantity* value_quantity;
    FHIRRange* value_range;
    FHIRReference* value_reference;
    FHIRBoolean* exclude;
    FHIRPeriod* period;
} GroupCharacteristic;

// Group Member structure
typedef struct GroupMember {
    FHIRElement base;
    FHIRReference* entity;
    FHIRPeriod* period;
    FHIRBoolean* inactive;
} GroupMember;

// OrganizationAffiliation Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRBoolean* active;
    FHIRPeriod* period;
    FHIRReference* organization;
    FHIRReference* participating_organization;
    FHIRCodeableConcept** network;
    size_t network_count;
    FHIRCodeableConcept** code;
    size_t code_count;
    FHIRCodeableConcept** specialty;
    size_t specialty_count;
    FHIRReference** location;
    size_t location_count;
    FHIRReference** healthcare_service;
    size_t healthcare_service_count;
    FHIRContactPoint** telecom;
    size_t telecom_count;
    FHIRReference** endpoint;
    size_t endpoint_count;
} FHIROrganizationAffiliation;

// Function declarations for Foundation resources

// Resource creation functions
FHIRResource* fhir_resource_create(const char* resource_type, const char* id);
FHIRDomainResource* fhir_domain_resource_create(const char* resource_type, const char* id);
FHIRPatient* fhir_patient_create(const char* id);
FHIRPractitioner* fhir_practitioner_create(const char* id);
FHIROrganization* fhir_organization_create(const char* id);
FHIRLocation* fhir_location_create(const char* id);
FHIRHealthcareService* fhir_healthcare_service_create(const char* id);
FHIREndpoint* fhir_endpoint_create(const char* id);
FHIRRelatedPerson* fhir_related_person_create(const char* id);
FHIRPerson* fhir_person_create(const char* id);
FHIRGroup* fhir_group_create(const char* id);
FHIROrganizationAffiliation* fhir_organization_affiliation_create(const char* id);

// Resource destruction functions
void fhir_resource_free(FHIRResource* resource);
void fhir_domain_resource_free(FHIRDomainResource* domain_resource);
void fhir_patient_free(FHIRPatient* patient);
void fhir_practitioner_free(FHIRPractitioner* practitioner);
void fhir_organization_free(FHIROrganization* organization);
void fhir_location_free(FHIRLocation* location);
void fhir_healthcare_service_free(FHIRHealthcareService* service);
void fhir_endpoint_free(FHIREndpoint* endpoint);
void fhir_related_person_free(FHIRRelatedPerson* related_person);
void fhir_person_free(FHIRPerson* person);
void fhir_group_free(FHIRGroup* group);
void fhir_organization_affiliation_free(FHIROrganizationAffiliation* org_affiliation);

// JSON parsing functions
FHIRResource* fhir_parse_resource(cJSON* json);
FHIRDomainResource* fhir_parse_domain_resource(cJSON* json);
FHIRPatient* fhir_parse_patient(cJSON* json);
FHIRPractitioner* fhir_parse_practitioner(cJSON* json);
FHIROrganization* fhir_parse_organization(cJSON* json);
FHIRLocation* fhir_parse_location(cJSON* json);
FHIRHealthcareService* fhir_parse_healthcare_service(cJSON* json);
FHIREndpoint* fhir_parse_endpoint(cJSON* json);
FHIRRelatedPerson* fhir_parse_related_person(cJSON* json);
FHIRPerson* fhir_parse_person(cJSON* json);
FHIRGroup* fhir_parse_group(cJSON* json);
FHIROrganizationAffiliation* fhir_parse_organization_affiliation(cJSON* json);

// JSON serialization functions
cJSON* fhir_resource_to_json(const FHIRResource* resource);
cJSON* fhir_domain_resource_to_json(const FHIRDomainResource* domain_resource);
cJSON* fhir_patient_to_json(const FHIRPatient* patient);
cJSON* fhir_practitioner_to_json(const FHIRPractitioner* practitioner);
cJSON* fhir_organization_to_json(const FHIROrganization* organization);
cJSON* fhir_location_to_json(const FHIRLocation* location);
cJSON* fhir_healthcare_service_to_json(const FHIRHealthcareService* service);
cJSON* fhir_endpoint_to_json(const FHIREndpoint* endpoint);
cJSON* fhir_related_person_to_json(const FHIRRelatedPerson* related_person);
cJSON* fhir_person_to_json(const FHIRPerson* person);
cJSON* fhir_group_to_json(const FHIRGroup* group);

// Validation functions
bool fhir_validate_patient(const FHIRPatient* patient);
bool fhir_validate_practitioner(const FHIRPractitioner* practitioner);
bool fhir_validate_organization(const FHIROrganization* organization);
bool fhir_validate_location(const FHIRLocation* location);
bool fhir_validate_healthcare_service(const FHIRHealthcareService* service);
bool fhir_validate_endpoint(const FHIREndpoint* endpoint);
bool fhir_validate_related_person(const FHIRRelatedPerson* related_person);
bool fhir_validate_person(const FHIRPerson* person);
bool fhir_validate_group(const FHIRGroup* group);

// Utility functions for Foundation resources
char* fhir_patient_get_full_name(const FHIRPatient* patient);
char* fhir_practitioner_get_full_name(const FHIRPractitioner* practitioner);
char* fhir_organization_get_display_name(const FHIROrganization* organization);
bool fhir_patient_is_active(const FHIRPatient* patient);
bool fhir_practitioner_is_active(const FHIRPractitioner* practitioner);
bool fhir_organization_is_active(const FHIROrganization* organization);

// Resource type detection
const char* fhir_get_resource_type(const FHIRResource* resource);
bool fhir_is_foundation_resource(const char* resource_type);

// Additional Foundation Resource Types

// CodeSystem Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRUri* url;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRString* version;
    FHIRString* name;
    FHIRString* title;
    FHIRCode* status;  // draft | active | retired | unknown
    FHIRBoolean* experimental;
    FHIRDateTime* date;
    FHIRString* publisher;
    FHIRContactDetail** contact;
    size_t contact_count;
    FHIRMarkdown* description;
    struct FHIRUsageContext** use_context;
    size_t use_context_count;
    FHIRCodeableConcept** jurisdiction;
    size_t jurisdiction_count;
    FHIRMarkdown* purpose;
    FHIRMarkdown* copyright;
    FHIRBoolean* case_sensitive;
    FHIRCanonical* value_set;
    FHIRCode* hierarchy_meaning;  // grouped-by | is-a | part-of | classified-with
    FHIRBoolean* compositional;
    FHIRBoolean* version_needed;
    FHIRCode* content;  // not-present | example | fragment | complete | supplement
    FHIRCanonical* supplements;
    FHIRUnsignedInt* count;
    struct CodeSystemFilter** filter;
    size_t filter_count;
    struct CodeSystemProperty** property;
    size_t property_count;
    struct CodeSystemConcept** concept;
    size_t concept_count;
} FHIRCodeSystem;

// CodeSystem Filter structure
typedef struct CodeSystemFilter {
    FHIRElement base;
    FHIRCode* code;
    FHIRString* description;
    FHIRCode** operator;
    size_t operator_count;
    FHIRString* value;
} CodeSystemFilter;

// CodeSystem Property structure
typedef struct CodeSystemProperty {
    FHIRElement base;
    FHIRCode* code;
    FHIRUri* uri;
    FHIRString* description;
    FHIRCode* type;  // code | Coding | string | integer | boolean | dateTime | decimal
} CodeSystemProperty;

// CodeSystem Concept structure
typedef struct CodeSystemConcept {
    FHIRElement base;
    FHIRCode* code;
    FHIRString* display;
    FHIRString* definition;
    struct CodeSystemConceptDesignation** designation;
    size_t designation_count;
    struct CodeSystemConceptProperty** property;
    size_t property_count;
    struct CodeSystemConcept** concept;
    size_t concept_count;
} CodeSystemConcept;

// CodeSystem Concept Designation structure
typedef struct CodeSystemConceptDesignation {
    FHIRElement base;
    FHIRCode* language;
    FHIRCoding* use;
    FHIRString* value;
} CodeSystemConceptDesignation;

// CodeSystem Concept Property structure
typedef struct CodeSystemConceptProperty {
    FHIRElement base;
    FHIRCode* code;
    FHIRCode* value_code;
    FHIRCoding* value_coding;
    FHIRString* value_string;
    FHIRInteger* value_integer;
    FHIRBoolean* value_boolean;
    FHIRDateTime* value_date_time;
    FHIRDecimal* value_decimal;
} CodeSystemConceptProperty;

// ValueSet Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRUri* url;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRString* version;
    FHIRString* name;
    FHIRString* title;
    FHIRCode* status;  // draft | active | retired | unknown
    FHIRBoolean* experimental;
    FHIRDateTime* date;
    FHIRString* publisher;
    FHIRContactDetail** contact;
    size_t contact_count;
    FHIRMarkdown* description;
    struct FHIRUsageContext** use_context;
    size_t use_context_count;
    FHIRCodeableConcept** jurisdiction;
    size_t jurisdiction_count;
    FHIRBoolean* immutable;
    FHIRMarkdown* purpose;
    FHIRMarkdown* copyright;
    struct ValueSetCompose* compose;
    struct ValueSetExpansion* expansion;
} FHIRValueSet;

// ValueSet Compose structure
typedef struct ValueSetCompose {
    FHIRElement base;
    FHIRDate* locked_date;
    FHIRBoolean* inactive;
    struct ValueSetComposeInclude** include;
    size_t include_count;
    struct ValueSetComposeInclude** exclude;
    size_t exclude_count;
} ValueSetCompose;

// ValueSet Compose Include structure
typedef struct ValueSetComposeInclude {
    FHIRElement base;
    FHIRUri* system;
    FHIRString* version;
    struct ValueSetComposeIncludeConcept** concept;
    size_t concept_count;
    struct ValueSetComposeIncludeFilter** filter;
    size_t filter_count;
    FHIRCanonical** value_set;
    size_t value_set_count;
} ValueSetComposeInclude;

// ValueSet Compose Include Concept structure
typedef struct ValueSetComposeIncludeConcept {
    FHIRElement base;
    FHIRCode* code;
    FHIRString* display;
    struct ValueSetComposeIncludeConceptDesignation** designation;
    size_t designation_count;
} ValueSetComposeIncludeConcept;

// ValueSet Compose Include Concept Designation structure
typedef struct ValueSetComposeIncludeConceptDesignation {
    FHIRElement base;
    FHIRCode* language;
    FHIRCoding* use;
    FHIRString* value;
} ValueSetComposeIncludeConceptDesignation;

// ValueSet Compose Include Filter structure
typedef struct ValueSetComposeIncludeFilter {
    FHIRElement base;
    FHIRCode* property;
    FHIRCode* op;  // = | is-a | descendent-of | is-not-a | regex | in | not-in | generalizes | exists
    FHIRString* value;
} ValueSetComposeIncludeFilter;

// ValueSet Expansion structure
typedef struct ValueSetExpansion {
    FHIRElement base;
    FHIRUri* identifier;
    FHIRDateTime* timestamp;
    FHIRInteger* total;
    FHIRInteger* offset;
    struct ValueSetExpansionParameter** parameter;
    size_t parameter_count;
    struct ValueSetExpansionContains** contains;
    size_t contains_count;
} ValueSetExpansion;

// ValueSet Expansion Parameter structure
typedef struct ValueSetExpansionParameter {
    FHIRElement base;
    FHIRString* name;
    FHIRString* value_string;
    FHIRBoolean* value_boolean;
    FHIRInteger* value_integer;
    FHIRDecimal* value_decimal;
    FHIRUri* value_uri;
    FHIRCode* value_code;
    FHIRDateTime* value_date_time;
} ValueSetExpansionParameter;

// ValueSet Expansion Contains structure
typedef struct ValueSetExpansionContains {
    FHIRElement base;
    FHIRUri* system;
    FHIRBoolean* abstract;
    FHIRBoolean* inactive;
    FHIRString* version;
    FHIRCode* code;
    FHIRString* display;
    struct ValueSetExpansionContainsDesignation** designation;
    size_t designation_count;
    struct ValueSetExpansionContains** contains;
    size_t contains_count;
} ValueSetExpansionContains;

// ValueSet Expansion Contains Designation structure
typedef struct ValueSetExpansionContainsDesignation {
    FHIRElement base;
    FHIRCode* language;
    FHIRCoding* use;
    FHIRString* value;
} ValueSetExpansionContainsDesignation;

// ConceptMap Resource
typedef struct {
    FHIRDomainResource domain_resource;
    FHIRUri* url;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRString* version;
    FHIRString* name;
    FHIRString* title;
    FHIRCode* status;  // draft | active | retired | unknown
    FHIRBoolean* experimental;
    FHIRDateTime* date;
    FHIRString* publisher;
    FHIRContactDetail** contact;
    size_t contact_count;
    FHIRMarkdown* description;
    struct FHIRUsageContext** use_context;
    size_t use_context_count;
    FHIRCodeableConcept** jurisdiction;
    size_t jurisdiction_count;
    FHIRMarkdown* purpose;
    FHIRMarkdown* copyright;
    FHIRUri* source_uri;
    FHIRCanonical* source_canonical;
    FHIRUri* target_uri;
    FHIRCanonical* target_canonical;
    struct ConceptMapGroup** group;
    size_t group_count;
} FHIRConceptMap;

// ConceptMap Group structure
typedef struct ConceptMapGroup {
    FHIRElement base;
    FHIRUri* source;
    FHIRString* source_version;
    FHIRUri* target;
    FHIRString* target_version;
    struct ConceptMapGroupElement** element;
    size_t element_count;
    struct ConceptMapGroupUnmapped* unmapped;
} ConceptMapGroup;

// ConceptMap Group Element structure
typedef struct ConceptMapGroupElement {
    FHIRElement base;
    FHIRCode* code;
    FHIRString* display;
    struct ConceptMapGroupElementTarget** target;
    size_t target_count;
} ConceptMapGroupElement;

// ConceptMap Group Element Target structure
typedef struct ConceptMapGroupElementTarget {
    FHIRElement base;
    FHIRCode* code;
    FHIRString* display;
    FHIRCode* equivalence;  // relatedto | equivalent | equal | wider | subsumes | narrower | specializes | inexact | unmatched | disjoint
    FHIRString* comment;
    struct ConceptMapGroupElementTargetDependsOn** depends_on;
    size_t depends_on_count;
    struct ConceptMapGroupElementTargetDependsOn** product;
    size_t product_count;
} ConceptMapGroupElementTarget;

// ConceptMap Group Element Target DependsOn structure
typedef struct ConceptMapGroupElementTargetDependsOn {
    FHIRElement base;
    FHIRUri* property;
    FHIRUri* system;
    FHIRString* value;
    FHIRString* display;
} ConceptMapGroupElementTargetDependsOn;

// ConceptMap Group Unmapped structure
typedef struct ConceptMapGroupUnmapped {
    FHIRElement base;
    FHIRCode* mode;  // provided | fixed | other-map
    FHIRCode* code;
    FHIRString* display;
    FHIRCanonical* url;
} ConceptMapGroupUnmapped;

// Binary Resource
typedef struct {
    FHIRResource resource;
    FHIRCode* content_type;
    FHIRReference* security_context;
    FHIRBase64Binary* data;
} FHIRBinary;

// Bundle Resource
typedef struct {
    FHIRResource resource;
    FHIRIdentifier* identifier;
    FHIRCode* type;  // document | message | transaction | transaction-response | batch | batch-response | history | searchset | collection
    FHIRInstant* timestamp;
    FHIRUnsignedInt* total;
    struct BundleLink** link;
    size_t link_count;
    struct BundleEntry** entry;
    size_t entry_count;
    struct FHIRSignature* signature;
} FHIRBundle;

// Bundle Link structure
typedef struct BundleLink {
    FHIRElement base;
    FHIRString* relation;
    FHIRUri* url;
} BundleLink;

// Bundle Entry structure
typedef struct BundleEntry {
    FHIRElement base;
    struct BundleLink** link;
    size_t link_count;
    FHIRUri* full_url;
    FHIRResource* resource;
    struct BundleEntrySearch* search;
    struct BundleEntryRequest* request;
    struct BundleEntryResponse* response;
} BundleEntry;

// Bundle Entry Search structure
typedef struct BundleEntrySearch {
    FHIRElement base;
    FHIRCode* mode;  // match | include | outcome
    FHIRDecimal* score;
} BundleEntrySearch;

// Bundle Entry Request structure
typedef struct BundleEntryRequest {
    FHIRElement base;
    FHIRCode* method;  // GET | HEAD | POST | PUT | DELETE | PATCH
    FHIRUri* url;
    FHIRString* if_none_match;
    FHIRInstant* if_modified_since;
    FHIRString* if_match;
    FHIRString* if_none_exist;
} BundleEntryRequest;

// Bundle Entry Response structure
typedef struct BundleEntryResponse {
    FHIRElement base;
    FHIRString* status;
    FHIRUri* location;
    FHIRString* etag;
    FHIRInstant* last_modified;
    FHIRResource* outcome;
} BundleEntryResponse;

// Additional structures for supporting types
typedef struct {
    FHIRElement base;
    FHIRCodeableConcept* code;
    FHIRCodeableConcept** value_codeable_concept;
    size_t value_codeable_concept_count;
    FHIRQuantity** value_quantity;
    size_t value_quantity_count;
    FHIRRange** value_range;
    size_t value_range_count;
    FHIRReference** value_reference;
    size_t value_reference_count;
} FHIRUsageContext;

typedef struct FHIRSignature {
    FHIRElement base;
    FHIRCode* type;  // xml-signature | json-signature | proof-signature
    FHIRInstant* when;
    FHIRReference* who;
    FHIRReference* on_behalf_of;
    FHIRCode* target_format;
    FHIRCode* sig_format;
    FHIRBase64Binary* data;
} FHIRSignature;

// Function declarations for additional Foundation resources

// CodeSystem functions
FHIRCodeSystem* fhir_code_system_create(const char* id);
void fhir_code_system_free(FHIRCodeSystem* code_system);
FHIRCodeSystem* fhir_parse_code_system(cJSON* json);
cJSON* fhir_code_system_to_json(const FHIRCodeSystem* code_system);
bool fhir_validate_code_system(const FHIRCodeSystem* code_system);

// ValueSet functions
FHIRValueSet* fhir_value_set_create(const char* id);
void fhir_value_set_free(FHIRValueSet* value_set);
FHIRValueSet* fhir_parse_value_set(cJSON* json);
cJSON* fhir_value_set_to_json(const FHIRValueSet* value_set);
bool fhir_validate_value_set(const FHIRValueSet* value_set);

// ConceptMap functions
FHIRConceptMap* fhir_concept_map_create(const char* id);
void fhir_concept_map_free(FHIRConceptMap* concept_map);
FHIRConceptMap* fhir_parse_concept_map(cJSON* json);
cJSON* fhir_concept_map_to_json(const FHIRConceptMap* concept_map);
bool fhir_validate_concept_map(const FHIRConceptMap* concept_map);

// Binary functions
FHIRBinary* fhir_binary_create(const char* id);
void fhir_binary_free(FHIRBinary* binary);
FHIRBinary* fhir_parse_binary(cJSON* json);
cJSON* fhir_binary_to_json(const FHIRBinary* binary);
bool fhir_validate_binary(const FHIRBinary* binary);

// Bundle functions
FHIRBundle* fhir_bundle_create(const char* id);
void fhir_bundle_free(FHIRBundle* bundle);
FHIRBundle* fhir_parse_bundle(cJSON* json);
cJSON* fhir_bundle_to_json(const FHIRBundle* bundle);
bool fhir_validate_bundle(const FHIRBundle* bundle);

// Bundle utility functions
size_t fhir_bundle_get_entry_count(const FHIRBundle* bundle);
FHIRResource* fhir_bundle_get_entry_resource(const FHIRBundle* bundle, size_t index);
bool fhir_bundle_add_entry(FHIRBundle* bundle, FHIRResource* resource, const char* full_url);

// Utility functions for terminology resources
bool fhir_is_terminology_resource(const char* resource_type);
char* fhir_code_system_lookup_display(const FHIRCodeSystem* code_system, const char* code);
bool fhir_value_set_contains_code(const FHIRValueSet* value_set, const char* system, const char* code);
char* fhir_concept_map_translate(const FHIRConceptMap* concept_map, const char* source_system, const char* code);

// Additional Foundation Resource declarations for new resources

// Location functions (already declared above, but ensuring completeness)
FHIRLocation* fhir_location_create(const char* id);
void fhir_location_free(FHIRLocation* location);
FHIRLocation* fhir_parse_location(cJSON* json);
cJSON* fhir_location_to_json(const FHIRLocation* location);
bool fhir_validate_location(const FHIRLocation* location);

// Task functions
struct FHIRTask* fhir_task_create(const char* id);
void fhir_task_free(struct FHIRTask* task);
struct FHIRTask* fhir_parse_task(cJSON* json);
cJSON* fhir_task_to_json(const struct FHIRTask* task);
bool fhir_validate_task(const struct FHIRTask* task);

// HealthcareService functions (already declared above)
FHIRHealthcareService* fhir_healthcare_service_create(const char* id);
void fhir_healthcare_service_free(FHIRHealthcareService* service);
FHIRHealthcareService* fhir_parse_healthcare_service(cJSON* json);
cJSON* fhir_healthcare_service_to_json(const FHIRHealthcareService* service);
bool fhir_validate_healthcare_service(const FHIRHealthcareService* service);

// Endpoint functions (already declared above)
FHIREndpoint* fhir_endpoint_create(const char* id);
void fhir_endpoint_free(FHIREndpoint* endpoint);
FHIREndpoint* fhir_parse_endpoint(cJSON* json);
cJSON* fhir_endpoint_to_json(const FHIREndpoint* endpoint);
bool fhir_validate_endpoint(const FHIREndpoint* endpoint);

// Additional resource type checking
bool fhir_is_workflow_foundation_resource(const char* resource_type);
bool fhir_is_infrastructure_foundation_resource(const char* resource_type);
#endif
 // FHIR_FOUNDATION_H